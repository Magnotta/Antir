"""
FloatSlider: wraps QSlider (which only takes ints) to expose a float value
on a fixed step size, with a live numeric label next to it.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QSlider,
    QLabel,
)
from PyQt6.QtCore import Qt, pyqtSignal


class FloatSlider(QWidget):
    value_changed = pyqtSignal(float)

    def __init__(
        self,
        minimum: float,
        maximum: float,
        step: float = 0.05,
        value: float = 1.0,
        decimals: int = 2,
        parent=None,
    ):
        super().__init__(parent)
        self._min = minimum
        self._max = maximum
        self._step = step
        self._decimals = decimals

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(self._to_ticks(maximum))
        self.slider.setValue(self._to_ticks(value))
        self.slider.valueChanged.connect(
            self._on_slider_changed
        )

        self.value_label = QLabel(self._format(value))
        self.value_label.setMinimumWidth(48)
        self.value_label.setAlignment(
            Qt.AlignmentFlag.AlignRight
        )

        layout.addWidget(self.slider, stretch=1)
        layout.addWidget(self.value_label)

    def _to_ticks(self, value: float) -> int:
        return round((value - self._min) / self._step)

    def _from_ticks(self, ticks: int) -> float:
        return self._min + ticks * self._step

    def _format(self, value: float) -> str:
        return f"{value:.{self._decimals}f}"

    def _on_slider_changed(self, ticks: int):
        value = self._from_ticks(ticks)
        self.value_label.setText(self._format(value))
        self.value_changed.emit(value)

    def value(self) -> float:
        return self._from_ticks(self.slider.value())

    def set_value(self, value: float):
        self.slider.setValue(self._to_ticks(value))
