from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from db.schemas import PLAYERS_SCHEMA, BODY_SCHEMA
from db.models import Base, Player, BodyNode, EquipmentSlot

DATABASE_URL = "sqlite:///db/antir_db.db"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

def init_metadata():
    Base.metadata.create_all(bind=engine)



def create_body_node_recursive(
    session,
    owner_id: int,
    name: str,
    schema: dict,
    parent: BodyNode | None = None
):
    if parent is not None:
        print(f"Creating {name} of {owner_id}, child of {parent.name}")
    else:
        print(f"Creating {name} of {owner_id}")
    node = BodyNode(
        owner=owner_id,
        name=name,
        parent=parent
    )
    session.add(node)
    session.flush()  # ensures node.id exists

    # Create equipment slots
    for idx, slot_type in enumerate(schema.get("slots", [])):
        slot = EquipmentSlot(
            body_node_id=node.id,
            slot_type=slot_type,
            slot_index=idx
        )
        session.add(slot)

    # Recurse into children
    for child_name, child_schema in schema.get("children", {}).items():
        create_body_node_recursive(
            session,
            owner_id,
            child_name,
            child_schema,
            parent=node
        )

    return node



def init_players(session):
    print("Initializing players")
    existing = session.query(Player).count()
    if existing >= 5:
        print(f"{existing} players already exist, skipping creation.")
        return
    
    for p in PLAYERS_SCHEMA.items():
        player = Player(name=p[0])
        session.add(player)
        session.flush()
        for root_name, root_schema in BODY_SCHEMA.items():
            create_body_node_recursive(
                session=session,
                owner_id=player.id,
                name=root_name,
                schema=root_schema
            )
    session.commit()



def init_db(session):
    init_players(session)

SessionFactory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Session = scoped_session(SessionFactory)