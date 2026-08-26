# from PyQt6.QtCore import Qt
# from PyQt6.QtWidgets import (
#     QWidget,
#     QVBoxLayout,
#     QTextEdit,
#     QLineEdit,
#     QLabel,
# )
# from core.engine import Engine


# class HomeTab(QWidget):
#     def __init__(self, engine: Engine):
#         super().__init__()
#         self.engine = engine
#         self.output = QTextEdit()
#         self.output.setReadOnly(True)
#         self.output.setPlaceholderText(
#             "Welcome to the world..."
#         )
#         self.output.setFocusPolicy(Qt.FocusPolicy.NoFocus)
#         self.output.setStyleSheet(
#             "QTextEdit"
#             "{ font-family: Consolas, monospace; }"
#         )
#         self.input = QLineEdit()
#         self.input.setPlaceholderText(
#             "Type a command and press Enter..."
#         )
#         self.input.returnPressed.connect(
#             self.on_command_entered
#         )
#         self.input.setStyleSheet(
#             "QLineEdit"
#             "{ font-family: Consolas, monospace; }"
#         )
#         self.placedatetime = QLabel()
#         self.placedatetime.setAlignment(
#             Qt.AlignmentFlag.AlignRight
#             | Qt.AlignmentFlag.AlignVCenter
#         )
#         self.placedatetime.setObjectName("statusLabel")
#         self.refresh()
#         layout = QVBoxLayout(self)
#         layout.addWidget(self.output, stretch=1)
#         layout.addWidget(self.input)
#         layout.addWidget(self.placedatetime)
#         self._init_style()
#         self.print_line("🗡️ Welcome, adventurer.")
#         self.input.setFocus()

#     def _init_style(self):
#         self.output.setStyleSheet(
#             "QTextEdit"
#             "{ font-family: Consolas, monospace; }"
#         )
#         self.input.setStyleSheet(
#             "QLineEdit"
#             "{ font-family: Consolas, monospace; }"
#         )
#         self.placedatetime.setStyleSheet(
#             """
#             QLabel#statusLabel {
#                 font-family: Consolas, monospace;
#                 font-size: 11px;
#                 color: #666;
#                 padding: 4px;
#             }
#             """
#         )

#     def print_line(self, text: str):
#         self.output.append(text)
#         self.output.verticalScrollBar().setValue(
#             self.output.verticalScrollBar().maximum()
#         )

#     def refresh(self):
#         string = (
#             self.engine.state.get_placedatetime_string()
#         )
#         self.placedatetime.setText(string)

#     def on_command_entered(self):
#         text = self.input.text().strip()
#         if not text:
#             return
#         self.print_line(f"> {text}")
#         responses = self.engine.cmd.execute(text)
#         for line in responses:
#             self.print_line(line)
#         self.input.clear()


import math
import random
from PyQt6.QtCore import Qt, QRect, QRectF, QPointF, QTimer
from PyQt6.QtGui import (
    QPainter,
    QColor,
    QBrush,
    QPen,
    QLinearGradient,
    QRadialGradient,
)
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLineEdit,
    QLabel,
)
from core.engine import Engine


class HomeTab(QWidget):
    def __init__(self, engine: Engine):
        super().__init__()
        self.engine = engine

        # --- Create widgets ---
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlaceholderText(
            "Welcome to the world..."
        )
        self.output.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.output.setStyleSheet(
            "QTextEdit {"
            "  font-family: Consolas, monospace;"
            "  background: rgba(0, 0, 0, 150);"  # semi-transparent dark
            "  color: white;"
            "  border: none;"
            "}"
        )

        self.input = QLineEdit()
        self.input.setPlaceholderText(
            "Type a command and press Enter..."
        )
        self.input.returnPressed.connect(
            self.on_command_entered
        )
        self.input.setStyleSheet(
            "QLineEdit {"
            "  font-family: Consolas, monospace;"
            "  background: rgba(0, 0, 0, 150);"
            "  color: white;"
            "  border: 1px solid gray;"
            "}"
        )

        self.placedatetime = QLabel()
        self.placedatetime.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.placedatetime.setObjectName("statusLabel")
        self.placedatetime.setStyleSheet(
            "QLabel#statusLabel {"
            "  font-family: Consolas, monospace;"
            "  font-size: 11px;"
            "  color: #ddd;"
            "  padding: 4px;"
            "  background: rgba(0,0,0,100);"
            "}"
        )

        # --- Layout ---
        layout = QVBoxLayout(self)
        layout.addWidget(self.output, stretch=1)
        layout.addWidget(self.input)
        layout.addWidget(self.placedatetime)

        # --- Initial state ---
        self.refresh_location()
        self.print_line("🗡️ Welcome, adventurer.")
        QTimer.singleShot(0, self.input.setFocus)

    def paintEvent(self, event):
        """Draw the moody background."""
        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )
        rect = self.rect()

        # 1. Get current time and weather
        state = self.engine.state
        hour = state.time.h
        weather = state.weather
        cloud = weather.cloud_coverage
        precip = weather.precipitation

        # 2. Classify time of day
        if hour < 6 or hour >= 20:
            tod = "night"
        elif 6 <= hour < 8:
            tod = "dawn"
        elif 18 <= hour < 20:
            tod = "dusk"
        else:
            tod = "day"

        # 3. Classify weather condition
        if precip > 0:
            wc = "rain"
        elif cloud > 0:
            wc = "cloudy"
        else:
            wc = "clear"

        # 4. Paint sky gradient
        top_color, bottom_color = self._sky_colors(tod, wc)
        top_left = QPointF(rect.topLeft())
        bottom_left = QPointF(rect.bottomLeft())
        grad = QLinearGradient(top_left, bottom_left)
        grad.setColorAt(0, top_color)
        grad.setColorAt(1, bottom_color)
        painter.fillRect(rect, grad)

        # 5. Draw sun (if visible)
        if (
            tod in ("dawn", "day", "dusk")
            and wc != "rain"
            and wc != "cloudy"
        ):
            self._draw_sun(painter, rect, hour)

        # 6. Draw clouds (if cloudy or rainy)
        if wc in ("cloudy", "rain"):
            self._draw_clouds(painter, rect, wc)

        # 7. Draw rain (if rainy)
        if wc == "rain":
            self._draw_rain(painter, rect)

    def _sky_colors(self, tod, wc):
        """
        Return (top_color, bottom_color) for the sky gradient.
        tod: 'dawn', 'day', 'dusk', 'night'
        wc:  'clear', 'cloudy', 'rain'
        """
        # Dawn
        if tod == "dawn":
            if wc == "clear":
                top = QColor(255, 200, 150)  # warm peach
                bottom = QColor(
                    255, 180, 100
                )  # golden horizon
            elif wc == "cloudy":
                top = QColor(
                    200, 180, 160
                )  # muted orange‑grey
                bottom = QColor(180, 150, 130)
            else:  # rain
                top = QColor(
                    150, 160, 180
                )  # cool grey‑blue
                bottom = QColor(130, 140, 160)

        # Day
        elif tod == "day":
            if wc == "clear":
                top = QColor(70, 150, 230)  # deep sky blue
                bottom = QColor(
                    180, 220, 255
                )  # pale at horizon
            elif wc == "cloudy":
                top = QColor(160, 170, 185)  # greyish blue
                bottom = QColor(190, 200, 210)
            else:  # rain
                top = QColor(100, 110, 130)  # dark slate
                bottom = QColor(130, 140, 160)

        # Dusk
        elif tod == "dusk":
            if wc == "clear":
                top = QColor(220, 100, 50)  # vibrant orange
                bottom = QColor(
                    180, 60, 120
                )  # purple horizon
            elif wc == "cloudy":
                top = QColor(
                    180, 130, 100
                )  # muted orange‑brown
                bottom = QColor(150, 100, 120)
            else:  # rain
                top = QColor(
                    100, 100, 130
                )  # dark purplish‑grey
                bottom = QColor(80, 80, 110)

        # Night (always dark, but we differentiate clear vs overcast)
        else:  # night
            if wc == "clear":
                top = QColor(5, 5, 35)  # very dark navy
                bottom = QColor(15, 15, 50)
            elif wc == "cloudy":
                top = QColor(20, 20, 30)  # dark grey‑blue
                bottom = QColor(30, 30, 40)
            else:  # rain (even darker)
                top = QColor(10, 10, 20)
                bottom = QColor(20, 20, 30)

        return top, bottom

    def _draw_sun(
        self, painter: QPainter, rect: QRect, hour
    ):
        """Draw a glowing sun at the correct position."""
        w, h = rect.width(), rect.height()
        center_x = w / 2
        center_y = h  # bottom of the widget
        radius = h * 0.7  # semi‑circle radius

        # Map hour 6..18 to angle 180°..0° (left to right)
        t = max(0, min(1, (hour - 6) / 12.0))
        angle_deg = 180 - t * 180
        angle_rad = math.radians(angle_deg)

        sun_x = int(center_x + radius * math.cos(angle_rad))
        sun_y = int(center_y - radius * math.sin(angle_rad))

        # Glow (large semi‑transparent aura)
        glow_radius = int(min(w, h) * 0.08)
        glow = QRadialGradient(
            sun_x, sun_y, glow_radius * 3
        )
        glow.setColorAt(0, QColor(255, 255, 200, 180))
        glow.setColorAt(0.5, QColor(255, 200, 50, 100))
        glow.setColorAt(1, QColor(255, 200, 50, 0))
        painter.setBrush(QBrush(glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(
            sun_x - glow_radius * 3,
            sun_y - glow_radius * 3,
            glow_radius * 6,
            glow_radius * 6,
        )

        # Core
        painter.setBrush(QBrush(QColor(255, 255, 100)))
        painter.drawEllipse(
            sun_x - glow_radius,
            sun_y - glow_radius,
            glow_radius * 2,
            glow_radius * 2,
        )

    def _draw_clouds(
        self, painter: QPainter, rect: QRect, wc
    ):
        """Draw a variable number of fluffy cloud blobs based on coverage."""
        state = self.engine.state
        weather = state.weather
        coverage = weather.cloud_coverage if weather else 0

        # Map 0..10000 -> 0..40 clouds
        max_clouds = 40
        n = int((coverage / 10000.0) * max_clouds)
        n = min(max_clouds, max(0, n))

        # Base colour: white for cloudy, greyish for rainy
        if wc == "rain":
            base = QColor(160, 170, 190)
        else:
            base = QColor(255, 255, 255)

        painter.setPen(Qt.PenStyle.NoPen)

        for _ in range(n):
            # Random position (with small margin)
            margin = 0.05
            x = (
                random.uniform(margin, 1 - margin)
                * rect.width()
            )
            y = (
                random.uniform(margin, 1 - margin)
                * rect.height()
            )

            # Random size: width 5–15%, height 2–6% of widget
            w = random.uniform(0.05, 0.15) * rect.width()
            h = random.uniform(0.02, 0.06) * rect.height()

            # Slight opacity variation
            alpha = random.randint(150, 220)
            color = QColor(base)
            color.setAlpha(alpha)

            painter.setBrush(QBrush(color))
            cloud_rect = QRectF(x - w / 2, y - h / 2, w, h)
            painter.drawEllipse(cloud_rect)

    def _draw_rain(self, painter: QPainter, rect: QRect):
        """Draw many diagonal streaks."""
        painter.setPen(QPen(QColor(200, 220, 255, 120), 3))
        for _ in range(
            self.engine.state.weather.precipitation // 12
        ):
            x = random.randint(0, rect.width())
            y = random.randint(0, rect.height())
            length = random.randint(10, 20)
            angle = 30  # degrees
            dx = length * math.cos(math.radians(angle))
            dy = length * math.sin(math.radians(angle))
            painter.drawLine(x, y, int(x + dx), int(y + dy))

    def print_line(self, text: str):
        self.output.append(text)
        self.output.verticalScrollBar().setValue(
            self.output.verticalScrollBar().maximum()
        )

    def refresh_location(self):
        """Update time label and redraw background."""
        string = (
            self.engine.state.get_placedatetime_string()
        )
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
