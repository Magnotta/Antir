from PyQt6.QtWidgets import QWidget, QToolTip
from PyQt6.QtGui import (
    QPainter,
    QPainterPath,
    QColor,
    QTransform,
    QRegion,
    QPixmap,
    QPen,
)
from PyQt6.QtCore import QRect, QRectF, Qt
from core.defs import INJURY_TYPES
from db.repository.player import PlayerRepository


class BodyWidget(QWidget):
    def __init__(self, player_id, repo: PlayerRepository):
        super().__init__()
        self.setMouseTracking(True)
        self.setMinimumSize(120, 120)
        self.setMaximumSize(300, 300)

        self.player_id = player_id
        self.repo = repo
        self.part_paths = {}
        self.part_regions = {}

        self._load_icons()
        self._init_part_paths()
        self._update_regions()

    def _load_icons(self):
        self.icons = {}
        names = [
            "broken_bone",
            "torn_ligament",
            "dislocated_joint",
            "severed",
            "venomous_bite",
            "insect_bite",
            "poison_sting",
            "swollen_joint",
            "sliced",
            "pierced",
            "bludgeoned",
        ]
        for name in names:
            pixmap = QPixmap(f"./ui/icons/{name}.png")
            if not pixmap.isNull():
                self.icons[name] = pixmap

    def _init_part_paths(self):
        width = 0.19
        height = 0.16
        first_row_y = 0.01
        center_col_x = 0.5 - width / 2
        gap = 0.004

        # Head (top centre)
        head = QPainterPath()
        head.addRect(
            QRectF(
                center_col_x + gap,
                first_row_y + gap,
                width - gap,
                height - gap,
            )
        )
        self.part_paths["head"] = head

        # Neck (small connector)
        neck = QPainterPath()
        neck.addRect(
            QRectF(
                center_col_x + gap,
                first_row_y + height + gap,
                width - gap,
                height - gap,
            )
        )
        self.part_paths["neck"] = neck

        # Torso (main trunk)
        spine = QPainterPath()
        spine.addRect(
            QRectF(
                center_col_x - width / 2 + gap,
                first_row_y + 2 * height + gap,
                width - gap,
                height - gap,
            )
        )
        self.part_paths["spine"] = spine

        # Spine (thin vertical bar behind torso – from neck to hips)
        torso = QPainterPath()
        torso.addRect(
            QRectF(
                center_col_x + width / 2 + gap,
                first_row_y + 2 * height + gap,
                width - gap,
                height - gap,
            )
        )
        self.part_paths["torso"] = torso

        # Shoulders (left and right, attached to top of torso)
        left_shoulder = QPainterPath()
        left_shoulder.addRect(
            QRectF(
                center_col_x - width + gap,
                first_row_y + height + gap,
                width - gap,
                height - gap,
            )
        )
        self.part_paths["left_shoulder"] = left_shoulder

        right_shoulder = QPainterPath()
        right_shoulder.addRect(
            QRectF(
                center_col_x + width + gap,
                first_row_y + height + gap,
                width - gap,
                height - gap,
            )
        )
        self.part_paths["right_shoulder"] = right_shoulder

        # Upper arms
        left_arm = QPainterPath()
        left_arm.addRect(
            QRectF(
                center_col_x - 2 * width + gap,
                first_row_y + height + gap,
                width - gap,
                height - gap,
            )
        )
        self.part_paths["left_arm"] = left_arm

        right_arm = QPainterPath()
        right_arm.addRect(
            QRectF(
                center_col_x + 2 * width + gap,
                first_row_y + height + gap,
                width - gap,
                height - gap,
            )
        )
        self.part_paths["right_arm"] = right_arm

        # Forearms
        left_forearm = QPainterPath()
        left_forearm.addRect(
            QRectF(
                center_col_x - 2 * width + gap,
                first_row_y + 2 * height + gap,
                width - gap,
                height - gap,
            )
        )
        self.part_paths["left_forearm"] = left_forearm

        right_forearm = QPainterPath()
        right_forearm.addRect(
            QRectF(
                center_col_x + 2 * width + gap,
                first_row_y + 2 * height + gap,
                width - gap,
                height - gap,
            )
        )
        self.part_paths["right_forearm"] = right_forearm

        # Hands
        left_hand = QPainterPath()
        left_hand.addRect(
            QRectF(
                center_col_x - 2 * width + gap,
                first_row_y + 3 * height + gap,
                width - gap,
                height - gap,
            )
        )
        self.part_paths["left_hand"] = left_hand

        right_hand = QPainterPath()
        right_hand.addRect(
            QRectF(
                center_col_x + 2 * width + gap,
                first_row_y + 3 * height + gap,
                width - gap,
                height - gap,
            )
        )
        self.part_paths["right_hand"] = right_hand

        # Hips / Pelvis (below torso, connects to legs)
        hips = QPainterPath()
        hips.addRect(
            QRectF(
                center_col_x + gap,
                first_row_y + 3 * height + gap,
                width - gap,
                height - gap,
            )
        )
        self.part_paths["hips"] = hips

        # Upper legs (thighs)
        left_leg = QPainterPath()
        left_leg.addRect(
            QRectF(
                center_col_x - width + gap,
                first_row_y + 3 * height + gap,
                width - gap,
                height - gap,
            )
        )
        self.part_paths["left_leg"] = left_leg

        right_leg = QPainterPath()
        right_leg.addRect(
            QRectF(
                center_col_x + width + gap,
                first_row_y + 3 * height + gap,
                width - gap,
                height - gap,
            )
        )
        self.part_paths["right_leg"] = right_leg

        # Shanks (lower legs)
        left_shank = QPainterPath()
        left_shank.addRect(
            QRectF(
                center_col_x - width + gap,
                first_row_y + 4 * height + gap,
                width - gap,
                height - gap,
            )
        )
        self.part_paths["left_shank"] = left_shank

        right_shank = QPainterPath()
        right_shank.addRect(
            QRectF(
                center_col_x + width + gap,
                first_row_y + 4 * height + gap,
                width - gap,
                height - gap,
            )
        )
        self.part_paths["right_shank"] = right_shank

        # Feet
        left_foot = QPainterPath()
        left_foot.addRect(
            QRectF(
                center_col_x - width + gap,
                first_row_y + 5 * height + gap,
                width - gap,
                height - gap,
            )
        )
        self.part_paths["left_foot"] = left_foot

        right_foot = QPainterPath()
        right_foot.addRect(
            QRectF(
                center_col_x + width + gap,
                first_row_y + 5 * height + gap,
                width - gap,
                height - gap,
            )
        )
        self.part_paths["right_foot"] = right_foot

    def _update_regions(self):
        self.part_regions.clear()

        w, h = self.width(), self.height()
        transform = QTransform()
        transform.scale(w, h)

        for name, norm_path in self.part_paths.items():
            path = transform.map(norm_path)

            # Convert path → polygon → region
            polygon = path.toFillPolygon().toPolygon()
            region = QRegion(polygon)

            self.part_regions[name] = region

    def _get_db_data(self):
        nodes = self.repo.get_complete_body(self.player_id)
        part_icons = {}
        injury_data = {}
        for node in nodes:
            icons = []
            for inj in INJURY_TYPES:
                val = getattr(node, inj)
                if val:
                    icons.append(inj)
                    if inj in [
                        "sliced",
                        "pierced",
                        "bludgeoned",
                    ]:
                        injury_data[inj] = val
            part_icons[node.name] = icons
        return part_icons, injury_data

    def _format_tooltip(self, part_name, stats):
        lines = [f"<b>{part_name.title()}</b>"]
        for k, v in stats.items():
            if isinstance(v, bool) and v:
                lines.append(f"• {k}")
            elif isinstance(v, int) and v > 0:
                lines.append(f"• {k}: {v}")
        if len(lines) == 1:
            lines.append("No injuries")
        return "<br>".join(lines)

    def _get_icon_slots(self, rect, count):
        half_gap = 1
        width = rect.width() // 3
        height = rect.height() // 2
        slot_1 = QRect(
            rect.x() + half_gap,
            rect.y() + half_gap,
            width - 2 * half_gap,
            height - half_gap,
        )
        slot_2 = QRect(
            rect.x() + half_gap + width,
            rect.y() + half_gap,
            width - 2 * half_gap,
            height - half_gap,
        )
        slot_3 = QRect(
            rect.x() + half_gap + 2 * width,
            rect.y() + half_gap,
            width - 2 * half_gap,
            height - half_gap,
        )
        slot_4 = QRect(
            rect.x() + half_gap,
            rect.y() + half_gap + height,
            width - 2 * half_gap,
            height - half_gap,
        )
        slot_5 = QRect(
            rect.x() + half_gap + width,
            rect.y() + half_gap + height,
            width - 2 * half_gap,
            height - half_gap,
        )
        slot_6 = QRect(
            rect.x() + half_gap + 2 * width,
            rect.y() + half_gap + height,
            width - 2 * half_gap,
            height - half_gap,
        )
        all_quads = [
            slot_1,
            slot_2,
            slot_3,
            slot_4,
            slot_5,
            slot_6,
        ]
        return all_quads[:count]

    def mouseMoveEvent(self, event):
        pos = event.pos()

        for name, region in self.part_regions.items():
            if region.contains(pos):
                stats = self.injury_data.get(name, {})
                text = self._format_tooltip(name, stats)
                QToolTip.showText(
                    event.globalPosition().toPoint(),
                    text,
                    self,
                )
                return

        QToolTip.hideText()
        super().mouseMoveEvent(event)

    def resizeEvent(self, event):
        self._update_regions()
        super().resizeEvent(event)

    def showEvent(self, a0):
        self.part_icons, self.injury_data = (
            self._get_db_data()
        )
        self.update()
        return super().showEvent(a0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )
        w = self.width()
        h = self.height()

        # ----- Draw body parts (scaled to widget) -----
        painter.save()
        painter.scale(w, h)
        for name, path in self.part_paths.items():
            painter.fillPath(
                path, QColor(200, 200, 200, 100)
            )
            painter.strokePath(
                path, QPen(Qt.GlobalColor.black, 0.001)
            )
        painter.restore()  # restores original coordinate system

        # ----- Draw icons (unscaled pixel coordinates) -----
        for part_name, icon_list in self.part_icons.items():
            if not icon_list:
                continue

            path = self.part_paths[part_name]
            norm_rect = path.boundingRect()
            # Convert normalized rect to pixel rect
            pixel_rect = QRectF(
                norm_rect.x() * w,
                norm_rect.y() * h,
                norm_rect.width() * w,
                norm_rect.height() * h,
            ).toRect()

            icon_slots = self._get_icon_slots(
                pixel_rect, len(icon_list)
            )

            for i, icon_key in enumerate(icon_list[:6]):
                slot = icon_slots[i]
                pixmap = self.icons[icon_key]
                scaled_pixmap = pixmap.scaled(
                    slot.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                x = (
                    slot.x()
                    + (slot.width() - scaled_pixmap.width())
                    // 2
                )
                y = (
                    slot.y()
                    + (
                        slot.height()
                        - scaled_pixmap.height()
                    )
                    // 2
                )

                painter.drawPixmap(x, y, scaled_pixmap)
