from db.database import engine
from db.models import Base

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()

    from PyQt6.QtWidgets import QApplication
    from ui.window import Window
    import sys

    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())