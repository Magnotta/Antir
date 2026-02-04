from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLineEdit,
    QLabel
)

from PyQt6.QtCore import Qt


class HomeTab(QWidget):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlaceholderText("Welcome to the world...")
        self.output.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.output.setStyleSheet(
                    "QTextEdit { font-family: Consolas, monospace; }")
        self.input = QLineEdit()
        self.input.setPlaceholderText("Type a command and press Enter...")
        self.input.returnPressed.connect(self.on_command_entered)
        self.input.setStyleSheet(
                    "QLineEdit { font-family: Consolas, monospace; }")
        self.placedatetime = QLabel()
        self.placedatetime.setAlignment(Qt.AlignmentFlag.AlignRight |
                                        Qt.AlignmentFlag.AlignVCenter)
        self.placedatetime.setObjectName("statusLabel")
        self.refresh()
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
                color: #666;
                padding: 4px;
            }
            """
        )

    def print_line(self, text: str):
        self.output.append(text)
        self.output.verticalScrollBar().setValue(
            self.output.verticalScrollBar().maximum()
        )

    def refresh(self):
        string = self.engine.state.get_placedatetime_string()
        self.placedatetime.setText(string)

    def on_command_entered(self):
        text = self.input.text().strip()
        if not text:
            return
        self.print_line(f"> {text}")
        responses = self.engine.cmd.execute(text)
        for line in responses:
            self.print_line(line)
        self.input.clear()
