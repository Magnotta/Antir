from collections import defaultdict
from db.models.player_stat import HistoricalStat
from core.game_state import GameState


class Summarizer:
    def __init__(self, state: GameState):
        self.state = state
        self._batch_active = False
        self._start_snapshot: dict[tuple[int, str], int] = (
            {}
        )  # (player_id, stat_name) -> value
        self._last_summary: str = ""

    def start_batch(self):
        """Take a snapshot of all player stats at the beginning of the time skip."""
        self._batch_active = True
        self._start_snapshot.clear()

        for player in self.state.players:
            stats = self.state.player_repo.get_all_stats(
                player.player_rec.id
            )
            for stat_name, value in stats.items():
                self._start_snapshot[
                    (player.player_rec.id, stat_name)
                ] = value

    def end_batch(self, minutes_elapsed: int):
        """
        Evaluate current state against thresholds and generate summary.

        Args:
            minutes_elapsed: Total minutes that passed during this batch.
                           Used to calculate hourly rate of change.
        """
        # 1. Fetch current stats for all players
        current_statvals: dict[tuple[int, str], int] = {}
        historicals: dict[
            tuple[int, str], HistoricalStat
        ] = {}
        for player in self.state.players:
            stats = self.state.player_repo.get_all_stats(
                player.player_rec.id
            )
            for stat_name, value in stats.items():
                current_statvals[
                    (player.player_rec.id, stat_name)
                ] = value
            hist_stats = (
                self.state.player_repo.get_historical_stats(
                    player.player_rec.id
                )
            )
            for stat_name, hist in hist_stats.items():
                historicals[
                    (player.player_rec.id, stat_name)
                ] = hist

        # 2. Fetch thresholds (once)
        thresholds = (
            self.state.player_repo.get_all_thresholds()
        )

        # 3. Evaluate each stat
        lose_controls = defaultdict(list)
        criticals = defaultdict(list)
        cautions = defaultdict(list)

        near_record_peaks = defaultdict(
            list
        )  # player_id -> list of (stat_name, current, record_low)

        fast_deltas = (
            []
        )  # (player_id, stat_name, delta_per_hour, current_value, max_value)

        for (
            player_id,
            stat_name,
        ), current_value in current_statvals.items():
            start_value = self._start_snapshot.get(
                (player_id, stat_name), current_value
            )

            delta = current_value - start_value
            if delta == 0:
                continue

            hours_elapsed = minutes_elapsed / 60.0
            delta_per_hour = (
                delta / hours_elapsed
                if hours_elapsed > 0
                else 0
            )
            pct_change_per_hour = delta_per_hour / 100

            if delta > 0 and pct_change_per_hour > 1.0:
                # Estimate time to zero (in hours)
                if delta_per_hour > 0:
                    hours_to_max = (
                        10000 - current_value
                    ) / delta_per_hour
                    fast_deltas.append(
                        {
                            'player_id': player_id,
                            'stat_name': stat_name,
                            'delta_per_hour': delta_per_hour,
                            'current_value': current_value,
                            'start_value': start_value,
                            'pct_change_per_hour': pct_change_per_hour,
                            'hours_to_max': hours_to_max,
                        }
                    )

            # Check threshold crossings
            threshold = thresholds.get(stat_name)
            if current_value > threshold.lose_control_high:
                lose_controls[player_id].append(
                    f"{stat_name}({current_value})"
                )
            elif current_value > threshold.critical_high:
                criticals[player_id].append(
                    f"{stat_name}({current_value})"
                )
            elif current_value > threshold.caution_high:
                cautions[player_id].append(
                    f"{stat_name}({current_value})"
                )

            # Check if close to record high
            historical_stat = historicals[
                (player_id, stat_name)
            ]
            if (
                historical_stat.all_time_max
                != current_value
            ):  # avoid showing if it's exactly the record itself
                # Check if within 5% of all-time low
                if (
                    historical_stat.all_time_max > 0
                ):  # avoid division by zero
                    pct_below_record = (
                        (
                            historical_stat.all_time_max
                            - current_value
                        )
                        / historical_stat.all_time_max
                        * 100
                    )
                    if (
                        pct_below_record < 5.0
                    ):  # within 5% of record high
                        near_record_peaks[player_id].append(
                            f"{stat_name}({current_value}, {pct_below_record:.1f}% below record {historical_stat.all_time_max}, set at {historical_stat.last_updated})"
                        )

        # --- Update historical stats (after evaluation, for next time) ---
        for player in self.state.players:
            player_stats = {
                name: current_statvals.get(
                    (player.player_rec.id, name), 0
                )
                for name, _ in current_statvals
                if _[0] == player.player_rec.id
            }
            self.state.player_repo.update_historical_stats(
                player.player_rec.id,
                player_stats,
                self.state.time.tick,
            )

        # 4. Build summary text
        lines = []
        lines.append(
            f"=== SUMMARIZER ({minutes_elapsed} min / {hours_elapsed:.1f} hr) ==="
        )

        if lose_controls:
            lines.append(
                "\n [CONTROL LOSS] - GM takes over character control"
            )
            for (
                player_id,
                stats_list,
            ) in lose_controls.items():
                player_name = self._get_player_name(
                    player_id
                )
                lines.append(
                    f"  {player_name}: {', '.join(stats_list)}"
                )

        if criticals:
            lines.append("\n[CRITICAL] - Immediate danger")
            for player_id, stats_list in criticals.items():
                player_name = self._get_player_name(
                    player_id
                )
                lines.append(
                    f"  {player_name}: {', '.join(stats_list)}"
                )

        if cautions:
            lines.append("\n[CAUTION] - Monitor closely")
            for player_id, stats_list in cautions.items():
                player_name = self._get_player_name(
                    player_id
                )
                lines.append(
                    f"  {player_name}: {', '.join(stats_list)}"
                )

        if fast_deltas:
            lines.append(
                "\n--- Rapid Decline (≥1%/hr, death in <4 days) ---"
            )
            # Sort by fastest decline (most negative delta per hour)
            sorted_deltas = sorted(
                fast_deltas,
                key=lambda x: x['delta_per_hour'],
            )
            for item in sorted_deltas[:5]:
                player_name = self._get_player_name(
                    item['player_id']
                )
                hours_to_death = item['hours_to_max']
                days_to_death = hours_to_death // 24
                lines.append(
                    f"  {player_name}: {item['stat_name']} "
                    f"({item['current_value']}, -{item['pct_change_per_hour']:.2f}%/hr, "
                    f"death in {days_to_death} days)"
                )

        if near_record_peaks:
            lines.append(
                "\n[HISTORICAL] - Near all-time maximum (within 5% of record)"
            )
            for (
                player_id,
                stats_list,
            ) in near_record_peaks.items():
                player_name = self._get_player_name(
                    player_id
                )
                lines.append(
                    f"  {player_name}: {', '.join(stats_list)}"
                )

        if not (
            criticals
            or cautions
            or fast_deltas
            or lose_controls
            or near_record_peaks
        ):
            lines.append("\nAll vital signs nominal.")

        summary = "\n".join(lines)
        self._last_summary = summary

    def _get_player_name(self, player_id: int) -> str:
        """Get player name from engine state."""
        for player in self.state.players:
            if player.player_rec.id == player_id:
                return player.player_rec.name
        return f"Player {player_id}"

    def get_last_summary(self) -> str:
        """Retrieve the most recent summary (for GUI display)."""
        return self._last_summary
