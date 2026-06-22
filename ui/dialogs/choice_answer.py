from PyQt6.QtWidgets import (
    QDialog,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
)


class ChoiceDialog(QDialog):
    def __init__(
        self,
        all_options,
        selected_options=[],
        title="Make a selection",
        validation_func=None,
        parent=None,
    ):
        super().__init__(parent)
        self.setModal(True)
        self.setWindowTitle(title)

        # Convert all options to strings for display; keep original values internally
        self.all_options = all_options
        self.validation_func = validation_func

        # Create the two list widgets
        self.available_list = QListWidget()
        self.selected_list = QListWidget()

        # Populate available list (all options)
        for opt in self.all_options:
            self.available_list.addItem(str(opt))

        # Populate selected list with pre‑selected options, and do not duplicate
        # them in the available list (they remain in available but are not shown there.
        # However, for clarity we leave them in available – the user can still see them,
        # but trying to add them again is prevented by duplicate checking.)
        for opt in selected_options:
            self.selected_list.addItem(str(opt))

        # Buttons
        add_btn = QPushButton("→")
        remove_btn = QPushButton("←")
        add_btn.clicked.connect(self._add_selected)
        remove_btn.clicked.connect(self._remove_selected)

        # Layout for arrow buttons
        arrows_layout = QVBoxLayout()
        arrows_layout.addStretch()
        arrows_layout.addWidget(add_btn)
        arrows_layout.addWidget(remove_btn)
        arrows_layout.addStretch()

        # Layout for the two lists
        lists_layout = QHBoxLayout()
        lists_layout.addWidget(self.available_list)
        lists_layout.addLayout(arrows_layout)
        lists_layout.addWidget(self.selected_list)

        # Accept / Cancel buttons
        accept_btn = QPushButton("Accept")
        cancel_btn = QPushButton("Cancel")
        accept_btn.clicked.connect(self._on_accept)
        cancel_btn.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(accept_btn)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(lists_layout)
        main_layout.addLayout(button_layout)

    def _add_selected(self):
        """Move the currently selected item from available to selected."""
        current = self.available_list.currentItem()
        if not current:
            return
        text = current.text()
        if not self._exists(self.selected_list, text):
            self.selected_list.addItem(text)

    def _remove_selected(self):
        """Remove the currently selected item from the selected list."""
        row = self.selected_list.currentRow()
        if row >= 0:
            self.selected_list.takeItem(row)

    @staticmethod
    def _exists(list_widget, text):
        """Check if an item with the given text already exists in the list widget."""
        for i in range(list_widget.count()):
            if list_widget.item(i).text() == text:
                return True
        return False

    def selected_options(self):
        return [
            self.selected_list.item(i).text()
            for i in range(self.selected_list.count())
        ]

    def _on_accept(self):
        selected = self.selected_options()
        if self.validation_func:
            ok, error_msg = self.validation_func(selected)
            if not ok:
                QMessageBox.critical(
                    self, "Validation Error", error_msg
                )
                return
        self.accept()
