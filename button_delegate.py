from PySide6.QtWidgets import (QStyledItemDelegate, QStyle)
from PySide6.QtGui import (QPainter, QFontMetrics, QColor)
from PySide6.QtCore import Qt

class ButtonDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        if index.data() is None:
            return

        if isinstance(index.data(), str) and index.data().endswith("МБ"):
            painter.drawText(option.rect, Qt.AlignCenter, index.data())
            return

        button_rect = option.rect
        button_rect.adjust(5, 5, -5, -5)

        button_color = QColor(211, 211, 211)
        painter.fillRect(button_rect, button_color)

        button_style = option.widget.style()
        button_style.drawControl(QStyle.CE_PushButton, option, painter, option.widget)

        painter.drawText(button_rect, Qt.AlignCenter, "Обновить")

