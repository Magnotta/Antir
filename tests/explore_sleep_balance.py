"""
Exploratory / diagnostic script for the sleep_cycle formulas.

This is NOT a pass/fail test. It's meant to be run and read by a human:
it prints sleep_delay + wakeup duration across a grid of SleepContext
values so you can eyeball whether the resulting sleep timings feel
balanced (e.g. "does a very tired, very anxious character take an
absurd amount of time to fall asleep and stay asleep?").

Once you're happy with a set of reference scenarios, promote them into
a real pytest file as golden-value regression tests (see the bottom of
this file for how).

Run from the repo root:
    python explore_sleep_balance.py

Adjust the import paths below if your package layout differs.
"""

from core.formulas.sleep_cycle import (
    sleep_delay,
    wakeup_thresholds,
)
from core.formulas.context_gatherers import SleepContext


def fmt_minutes(total_minutes: int) -> str:
    """Render a minute count as signed Hh MMm, since raw minute counts
    (e.g. -734) are hard to sanity-check by eye."""
    sign = "-" if total_minutes < 0 else ""
    total_minutes = abs(total_minutes)
    h, m = divmod(total_minutes, 60)
    return f"{sign}{h}h{m:02d}m"


def explore(
    label,
    tiredness_values,
    sleepyness_values,
    anxiety_values,
    heat_values,
):
    print(f"\n=== {label} ===")
    header = (
        f"{'tiredness':>10} {'sleepyness':>10} {'anxiety':>8} {'heat':>6} | "
        f"{'delay':>8} {'duration':>9} {'delay+duration':>15}"
    )
    print(header)
    print("-" * len(header))

    for tiredness in tiredness_values:
        for sleepyness in sleepyness_values:
            for anxiety in anxiety_values:
                for heat in heat_values:
                    ctx = SleepContext(
                        tiredness=tiredness,
                        sleepyness=sleepyness,
                        anxiety=anxiety,
                        heat=heat,
                    )
                    delay = sleep_delay(ctx)
                    # wakeup_thresholds also prints its own debug lines;
                    # that's noisy here, redirect if it bothers you.
                    _, _, _, _, duration = (
                        wakeup_thresholds(ctx)
                    )
                    total = delay + duration

                    print(
                        f"{tiredness:>10} {sleepyness:>10} {anxiety:>8} {heat:>6} | "
                        f"{fmt_minutes(delay):>8} {fmt_minutes(duration):>9} "
                        f"{fmt_minutes(total):>15}"
                    )


if __name__ == "__main__":
    # 1. Vary tiredness alone, everything else held at a "normal day" level.
    #    Watch: does delay behave sensibly as tiredness climbs toward its
    #    6300 documented cap, and beyond it (does going past the cap still
    #    behave, or silently do something weird)?
    explore(
        "Vary tiredness (sleepyness/anxiety/heat held at baseline)",
        tiredness_values=[
            0,
            500,
            1500,
            3000,
            4500,
            6300,
            8000,
        ],
        sleepyness_values=[900],
        anxiety_values=[900],
        heat_values=[1000],
    )

    # 2. Sleepyness is documented as uncapped. This is the most likely
    #    place for sleep_delay to go negative or blow up.
    explore(
        "Vary sleepyness (uncapped input - watch for runaway negative delay)",
        tiredness_values=[1500],
        sleepyness_values=[0, 900, 2000, 5000, 10000],
        anxiety_values=[900],
        heat_values=[1000],
    )

    # 3. Anxiety term is quadratic - small changes at high anxiety should
    #    have a much bigger effect than the same change at low anxiety.
    explore(
        "Vary anxiety (quadratic contribution)",
        tiredness_values=[1500],
        sleepyness_values=[900],
        anxiety_values=[0, 500, 1500, 3000, 5000],
        heat_values=[1000],
    )

    # 4. Heat: note the clamp floor is 1, not 0 - heat=0 should still show
    #    a +1 minute contribution. Confirm that's what you intended.
    explore(
        "Vary heat (min contribution is 1 even at heat=0 - intended?)",
        tiredness_values=[1500],
        sleepyness_values=[900],
        anxiety_values=[900],
        heat_values=[0, 500, 1500, 3000, 5000],
    )

    # 5. Worst-case combo: exhausted, anxious, overheated character.
    #    Good scenario to eventually freeze as a golden regression test.
    explore(
        "Extreme combo - exhausted, anxious, overheated",
        tiredness_values=[6300],
        sleepyness_values=[10000],
        anxiety_values=[5000],
        heat_values=[5000],
    )

    # 6. Best-case combo: freshly rested, calm, comfortable temperature.
    explore(
        "Best case - rested, calm, comfortable",
        tiredness_values=[0],
        sleepyness_values=[0],
        anxiety_values=[0],
        heat_values=[0],
    )


# ---------------------------------------------------------------------------
# Once a scenario above looks "right" to you, freeze it as a real test.
# Example of what that looks like in pytest (put this in tests/, not here):
#
# def test_baseline_day_sleep_delay_matches_docstring_example():
#     ctx = SleepContext(tiredness=1250, sleepyness=2400, anxiety=900, heat=0)
#     assert sleep_delay(ctx) == 32  # from the sleep_delay docstring example
#
# def test_exhausted_character_still_has_nonnegative_delay():
#     ctx = SleepContext(tiredness=6300, sleepyness=10000, anxiety=5000, heat=5000)
#     assert sleep_delay(ctx) >= 0  # currently NOT guaranteed - see notes
# ---------------------------------------------------------------------------
