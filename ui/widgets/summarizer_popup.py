import os
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent, QMouseEvent


class SummarizerPopup(QDialog):
    """
    Modal popup displaying the summarizer text.
    - Closes on Enter / Escape keys.
    - Closes when clicking outside the text area.
    - Saves summary to ./logs/summaries/{tick}.txt
    """

    def __init__(
        self, summary_text: str, tick: int, parent=None
    ):
        super().__init__(parent)

        self.setWindowTitle(f"Game Summary – Tick {tick}")
        self.setModal(True)
        self.setMinimumSize(650, 450)

        # Stay on top of other windows (optional but useful)
        self.setWindowFlags(
            self.windowFlags()
            | Qt.WindowType.WindowStaysOnTopHint
        )

        # --- Main layout ---
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)

        # --- Scrolled text area ---
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlainText(summary_text)
        self.text_edit.setFontFamily(
            "monospace"
        )  # Easier to read tabular data
        self.text_edit.setStyleSheet(
            """
            QTextEdit {
                background-color: #1e1e2e;
                color: #cdd6f4;
                border: 1px solid #45475a;
                border-radius: 4px;
                padding: 6px;
            }
        """
        )
        layout.addWidget(self.text_edit)

        # --- Close button (optional, but good UX) ---
        btn_close = QPushButton("Close (Esc / Enter)")
        btn_close.clicked.connect(self.accept)
        btn_close.setFixedWidth(150)
        btn_close.setStyleSheet(
            """
            QPushButton {
                padding: 6px 12px;
                background-color: #313244;
                color: #cdd6f4;
                border: 1px solid #45475a;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45475a;
            }
        """
        )

        # Put the button in a horizontal layout to right-align it
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(btn_close)
        layout.addLayout(button_layout)

        # --- Save the summary to disk ---
        self._save_summary(summary_text, tick)

        # --- Give focus to the text area so keys work immediately ---
        self.text_edit.setFocus()

    def _save_summary(self, text: str, tick: int) -> None:
        """Write summary to ./logs/summaries/{tick}.txt"""
        log_dir = "./logs/summaries/"
        os.makedirs(log_dir, exist_ok=True)
        filepath = os.path.join(log_dir, f"{tick}.txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)

    # ---- Key handling (Enter / Esc) ----
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() in (
            Qt.Key.Key_Return,
            Qt.Key.Key_Enter,
            Qt.Key.Key_Escape,
        ):
            self.accept()
        else:
            super().keyPressEvent(event)

    # ---- Click outside the text area to close ----
    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        If the user clicks on the dialog background (not on the QTextEdit
        or any of its children), close the popup.
        """
        clicked_widget = self.childAt(event.pos())

        # Check if the clicked widget is the text edit itself or a child of it
        if clicked_widget is not None:
            if (
                clicked_widget is self.text_edit
                or self.text_edit.isAncestorOf(
                    clicked_widget
                )
            ):
                # Normal text selection / interaction – let it pass
                super().mousePressEvent(event)
                return

        # Click outside the text area → close the dialog
        self.accept()
