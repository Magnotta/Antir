"""
RecordPickerDialog: modal OK/Cancel wrapper around SearchableRecordPicker.
Used wherever picking one Mold or one Item needs to be a blocking step
inside a bigger flow (e.g. "Add Tool" while assigning equipped tools).
"""

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QDialogButtonBox,
)
from ui.widgets.searchable_record_picker import (
    SearchableRecordPicker,
)


class RecordPickerDialog(QDialog):
    def __init__(
        self,
        fetch_fn,
        label_fn,
        title: str = "Select",
        placeholder: str = "Search...",
        parent=None,
    ):
        super().__init__(parent)
        self.setWindowTitle(title)

        layout = QVBoxLayout(self)
        self.picker = SearchableRecordPicker(
            fetch_fn, label_fn, placeholder=placeholder
        )
        layout.addWidget(self.picker)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    @classmethod
    def get_record(
        cls,
        fetch_fn,
        label_fn,
        title="Select",
        placeholder="Search...",
        parent=None,
    ):
        """Convenience: run the dialog modally, return the picked record or
        None if cancelled / nothing selected."""
        dialog = cls(
            fetch_fn, label_fn, title, placeholder, parent
        )
        if (
            dialog.exec()
            and dialog.picker.selected() is not None
        ):
            return dialog.picker.selected()
        return None
