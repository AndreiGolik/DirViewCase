import os
from PySide6.QtWidgets import QFileSystemModel
from PySide6.QtCore import Qt, QModelIndex


class MyFileSystemModel(QFileSystemModel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.name = "Размер папки"
        self.updated_indexes = set()

    def columnCount(self, parent=QModelIndex()):
        return super().columnCount(parent) + 2

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return super().data(index, role)

        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 4:
                if index in self.updated_indexes:
                    size = self.calc_size(index)
                    return f'{size:.2f} МБ'

                if self.isDir(index):
                    return "Обновить"
        return super().data(index, role)

    def update_index(self, index):
        self.updated_indexes.add(index)

    def calc_size(self, index):
        path = self.filePath(index)
        sum_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for file in filenames:
                    file_path = os.path.join(dirpath, file)
                    sum_size += os.path.getsize(file_path)
        except Exception as e:
            print(f"Ошибка: {e}")

        return sum_size / (1024 * 1024)

    def headerData(self, section: int, orientation: Qt.Orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if section == 4:
                return self.name
        return super().headerData(section,orientation, role)
