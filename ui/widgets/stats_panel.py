from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QGroupBox,
    QVBoxLayout,
    QGridLayout,
)
from PyQt6.QtGui import QPixmap
import os
from player.stats import Stats
from core.defs import CHARACTER_STATS


ICON_COLUMNS = 4


class StatsPanel(QGroupBox):
    def __init__(self, stats: Stats):
        super().__init__()

        self.stat_names = CHARACTER_STATS

        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)
        self.setLayout(grid_layout)

        self.labels: dict[str, QLabel] = {}
        self.icon_labels = {}
        icon_size = 35

        for index, stat_name in enumerate(self.stat_names):
            row = index // ICON_COLUMNS
            col = index % ICON_COLUMNS

            # Container for each stat (icon + value)
            container = QWidget()
            container_layout = QVBoxLayout()
            container_layout.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )
            container_layout.setSpacing(1)
            container.setLayout(container_layout)

            # Icon
            icon_path = f"./ui/icons/{stat_name}.png"
            icon_label = QLabel()
            if os.path.exists(icon_path):
                pixmap = QPixmap(icon_path)
                scaled_pixmap = pixmap.scaled(
                    icon_size,
                    icon_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                icon_label.setPixmap(scaled_pixmap)
            else:
                # Fallback: show stat name
                icon_label.setText(
                    stat_name.replace("_", " ").title()
                )
                icon_label.setStyleSheet(
                    "font-weight: bold; font-size: 8pt;"
                )

            icon_label.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )
            container_layout.addWidget(icon_label)
            self.icon_labels[stat_name] = icon_label

            # Value
            value_label = QLabel(
                str(stats.get_all()[stat_name])
            )
            value_label.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )
            value_label.setStyleSheet(
                "font-size: 11pt; font-weight: bold; color: #2c3e50;"
            )
            container_layout.addWidget(value_label)

            self.labels[stat_name] = value_label

            # Add container to grid
            grid_layout.addWidget(container, row, col)

        # Optional styling
        self.setStyleSheet(
            """
            StatsPanel {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 1px;
            }
        """
        )

        # Set a reasonable size
        self.setMaximumWidth(280)

    def refresh(self, stats: Stats):
        """Update all stat values"""
        for name, label in self.labels.items():
            label.setText(str(stats.get(name)))
