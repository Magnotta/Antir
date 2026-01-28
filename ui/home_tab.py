from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLineEdit,
    QLabel
)

from PyQt6.QtCore import Qt

# from systems.command_service import CommandService
from engine.event_engine import Engine


class HomeTab(QWidget):
    def __init__(self):
        super().__init__()

        self.engine = Engine()

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlaceholderText("Welcome to the world...")
        self.output.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.output.setStyleSheet(
                    "QTextEdit { font-family: Consolas, monospace; }")

        self.input = QLineEdit()
        self.input.setPlaceholderText("Type a command and press Enter...")
        # self.input.returnPressed.connect(self.execute_command)
        self.input.setStyleSheet(
                    "QLineEdit { font-family: Consolas, monospace; }")
        
        self.placedatetime = QLabel()
        self.placedatetime.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                        Qt.AlignmentFlag.AlignVCenter)
        self.placedatetime.setObjectName("statusLabel")
        self.update_placedatetime()

        layout = QVBoxLayout(self)
        layout.addWidget(self.output, stretch=1)
        layout.addWidget(self.input)
        layout.addWidget(self.placedatetime)

        self._init_style()

        self.print_line("🗡️ Welcome, adventurer.")

        self.input.setFocus()

    def _init_style(self):
        self.output.setStyleSheet(
            "QTextEdit { font-family: Consolas, monospace; }"
        )
        self.input.setStyleSheet(
            "QLineEdit { font-family: Consolas, monospace; }"
        )
        self.placedatetime.setStyleSheet(
            """
            QLabel#statusLabel {
                font-family: Consolas, monospace;
                font-size: 11px;
                color: #888;
                padding: 4px;
            }
            """
        )

    def print_line(self, text: str):
        self.output.append(text)
        self.output.verticalScrollBar().setValue(
            self.output.verticalScrollBar().maximum()
        )

    def update_placedatetime(self):
        string = self.engine.state.get_placedatetime_string()
        self.placedatetime.setText(string)
