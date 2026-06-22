from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session,
    Session,
)
from core.defs import (
    BASE_PLAYER_STATS,
    SLOT_MAX_INDEX,
    CHARACTER_STAT_BASE_THRESHOLDS,
)

from db.models.base import Base
from db.models.player_record import PlayerRecord
from db.models.player_stat import (
    PlayerStat,
    StatThreshold,
    HistoricalStat,
)
from db.models.body_node import BodyNode
from db.models.equipment_slot import EquipmentSlot
from db.models.global_var import GlobalVar


DATABASE_URL = "sqlite:///db/antir_db.db"


def init_metadata():
    engine = create_engine(
        DATABASE_URL, echo=False, future=True
    )
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(
        bind=engine, autoflush=False, autocommit=False
    )
    session = scoped_session(session_factory)
    return (engine, session)


def create_body_node_recursive(
    session: Session,
    owner_id: int,
    name: str,
    schema: dict,
    parent: BodyNode | None = None,
):
    node = BodyNode(
        health=1000,
        owner_id=owner_id,
        name=name,
        parent=parent,
    )
    session.add(node)
    session.flush()
    for slot_type in schema.get("slots", []):
        for idx in range(SLOT_MAX_INDEX[slot_type]):
            slot = EquipmentSlot(
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


def init_time(session: Session):
    var = (
        session.query(GlobalVar)
        .filter(GlobalVar.key == "simulation_ticks")
        .first()
    )
    if var is None:
        var = GlobalVar(key="simulation_ticks", value=0)
        session.add(var)
        session.commit()
    return var.value


def init_players(session: Session):
    existing_players = session.query(PlayerRecord).count()
    if existing_players >= 5:
        return

    existing_historicals = [
        hist.stat_name
        for hist in session.query(HistoricalStat).all()
    ]

    for pname, stat_dict in BASE_PLAYER_STATS.items():
        player = PlayerRecord(name=pname)
        session.add(player)
        session.flush()
        for stat_name, stat_value in stat_dict.items():
            session.add(
                PlayerStat(
                    player_id=player.id,
                    name=stat_name,
                    value=stat_value,
                )
            )
            if stat_name in existing_historicals:
                continue
            session.add(
                HistoricalStat(
                    player_id=player.id,
                    stat_name=stat_name,
                    all_time_max=stat_value,
                    last_updated=0,
                )
            )
    session.commit()


def init_stat_thresholds(session: Session) -> None:
    """
    Populate the stat_thresholds table with initial values.
    Safe to call multiple times - skips existing entries.
    """
    # Check if thresholds already exist
    existing = session.query(StatThreshold.stat_name).all()
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

        threshold = StatThreshold(
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


def init_db(session: Session):
    init_players(session)
    init_stat_thresholds(session)
