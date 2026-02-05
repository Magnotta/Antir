from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from core.defs import SLOT_RULES, BASE_PLAYER_STATS
from db.schemas import BODY_SCHEMA
from db.models import (
    Base,
    PlayerRecord,
    PlayerStat,
    BodyNode,
    EquipmentSlot,
)

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
    session,
    owner_id: int,
    name: str,
    schema: dict,
    parent: BodyNode | None = None,
):
    node = BodyNode(
        health=1000,
        owner=owner_id,
        name=name,
        parent=parent,
    )
    session.add(node)
    session.flush()
    for slot_type in schema.get("slots", []):
        for idx in range(SLOT_RULES[slot_type]):
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


def init_players(session):
    existing = session.query(PlayerRecord).count()
    if existing >= 5:
        return
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
            session.flush()
        for root_name, root_schema in BODY_SCHEMA.items():
            create_body_node_recursive(
                session=session,
                owner_id=player.id,
                name=root_name,
                schema=root_schema,
            )
    session.commit()


def init_db(session):
    init_players(session)
