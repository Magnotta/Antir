from PyQt6.QtWidgets import QApplication
import sys
from ui.window import Window
from db.database import init_db
from core.engine import Engine


if __name__ == "__main__":
    sys.tracebacklimit = 1
    session = init_db()
    engine = Engine(session)
    app = QApplication(sys.argv)
    win = Window(engine)
    win.show()
    sys.exit(app.exec())
