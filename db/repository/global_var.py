from sqlalchemy.orm import Session
from db.models.global_var import GlobalVar


class GlobalVarRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> dict[str:int]:
        var_dict = {}
        for var in self.session.query(GlobalVar).all():
            var_dict[var.key] = var.value
        return var_dict

    def get(self, key: str):
        var = (
            self.session.query(GlobalVar)
            .filter(GlobalVar.key == key)
            .one()
        )
        return var.value

    def set(self, key: str, value: int):
        var = (
            self.session.query(GlobalVar)
            .filter(GlobalVar.key == key)
            .one()
        )
        var.value = value

    def update_time(self, new_time):
        time = (
            self.session.query(GlobalVar)
            .filter(GlobalVar.key == "simulation_tick")
            .one()
        )
        time.value = new_time
