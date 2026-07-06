from sqlalchemy.orm import Session
from db.models.global_var import GlobalVar


class GlobalVarRepository:
    def __init__(self, session: Session):
        self.session = session

    def update_time(self, new_time):
        time = (
            self.session.query(GlobalVar)
            .filter(GlobalVar.key == "simulation_ticks")
            .one()
        )
        time.value = new_time
