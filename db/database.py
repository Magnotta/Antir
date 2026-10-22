from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session,
    Session,
)
from core.defs.player import (
    BASE_PLAYER_STATS,
    BASE_PLAYER_ATTRIBUTES,
    SLOT_MAX_INDEX,
    CHARACTER_STAT_BASE_THRESHOLDS,
)
from core.defs.game_state import StateProperties
from db.models.base import Base
import db.models.global_var as globals
import db.models.player_body as body
import db.models.player_record as player_rec
import db.models.player_stat as player_stat
import db.models.world as world
from db.repository.location import LocationRepository


DATABASE_URL = "sqlite:///db/antir_db.db"


def init_metadata():
    engine = create_engine(
        DATABASE_URL, echo=False, future=True
    )
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(
        bind=engine, autoflush=False, autocommit=False
    )
    session = scoped_session(session_factory)()
    return session


def create_body_node_recursive(
    session: Session,
    owner_id: int,
    name: str,
    schema: dict,
    parent: body.BodyNode | None = None,
):
    node = body.BodyNode(
        health=1000,
        owner_id=owner_id,
        name=name,
        parent=parent,
    )
    session.add(node)
    session.flush()
    for slot_type in schema.get("slots", []):
        for idx in range(SLOT_MAX_INDEX[slot_type]):
            slot = body.EquipmentSlot(
                body_node_id=node.id,
                slot_type=slot_type,
                slot_index=idx,
            )
            session.add(slot)
    for child_name, child_schema in schema.get(
        "children", {}
    ).items():
        create_body_node_recursive(
            session,
            owner_id,
            child_name,
            child_schema,
            parent=node,
        )
    return node


def init_globals(session: Session):
    var = session.query(globals.GlobalVar).first()
    if var is None:
        keys = [
            value
            for name, value in vars(StateProperties).items()
            if not name.startswith('_')
            and isinstance(value, str)
        ]
        session.add_all(
            [
                globals.GlobalVar(key=k, value=0)
                for k in keys
            ]
        )
        session.commit()


def init_player_recs(session: Session):
    existing_players = session.query(
        player_rec.PlayerRecord
    ).count()
    if existing_players >= 5:
        return

    existing_historicals = [
        hist.stat_name
        for hist in session.query(
            player_stat.HistoricalStat
        ).all()
    ]

    for pname, stat_dict in BASE_PLAYER_STATS.items():
        player = player_rec.PlayerRecord(name=pname)
        session.add(player)
        session.flush()
        for stat_name, stat_value in stat_dict.items():
            session.add(
                player_stat.PlayerStat(
                    player_id=player.id,
                    name=stat_name,
                    value=stat_value,
                )
            )
            if stat_name in existing_historicals:
                continue
            session.add(
                player_stat.HistoricalStat(
                    player_id=player.id,
                    stat_name=stat_name,
                    all_time_max=stat_value,
                    last_updated=0,
                )
            )
        for attr_name, attr_value in BASE_PLAYER_ATTRIBUTES[
            pname
        ].items():
            session.add(
                player_stat.PlayerAttr(
                    player_id=player.id,
                    name=attr_name,
                    value=attr_value,
                )
            )

    session.commit()


def init_stat_thresholds(session: Session) -> None:
    """
    Populate the stat_thresholds table with initial values.
    Safe to call multiple times - skips existing entries.
    """
    # Check if thresholds already exist
    existing = session.query(
        player_stat.StatThreshold.stat_name
    ).all()
    existing_names = {row[0] for row in existing}

    # Track how many were inserted
    inserted_count = 0

    for stat_name, (
        caution_high,
        critical_high,
        lose_control_high,
    ) in CHARACTER_STAT_BASE_THRESHOLDS.items():

        # Skip if this stat already has thresholds
        if stat_name in existing_names:
            continue

        threshold = player_stat.StatThreshold(
            stat_name=stat_name,
            caution_high=caution_high,
            critical_high=critical_high,
            lose_control_high=lose_control_high,
        )
        session.add(threshold)
        inserted_count += 1

    if inserted_count > 0:
        session.commit()
        print(f"Inserted {inserted_count} stat thresholds.")
    else:
        print("All thresholds already exist. Skipped.")


def init_world(session: Session) -> None:
    """
    Seed localities/sites/paths/junctions from core/world.py -- the same
    "more permanent" source of truth export_world/import_world already
    round-trip through.

    Safe to call multiple times, same as the other init_* functions in
    this file: skips entirely once any Locality exists. That guard
    matters more here than it does for player records or thresholds,
    though -- LocationRepository.import_world_from_file() always inserts
    fresh rows with new ids and has no "does this already exist" check of
    its own, so calling it a second time against an already-populated DB
    would duplicate the entire world rather than just no-op. The manual
    `import_world` command hits that same repo method directly and has
    no such guard -- worth deciding what you actually want it to do if
    invoked mid-game against a non-empty DB (silently refuse? wipe and
    reimport as a hard reset? something else?) before that command sees
    real use, since right now it will duplicate everything.
    """
    if session.query(world.Locality).count() > 0:
        return

    loc_repo = LocationRepository(session)
    loc_repo.import_world_from_file()
    session.commit()


def init_db() -> Session:
    session = init_metadata()
    init_globals(session)
    init_player_recs(session)
    init_stat_thresholds(session)
    init_world(session)
    return session
