import re
from PySide6.QtCore import QSortFilterProxyModel

class MyFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.regex = None


    def setFilterRegex(self, pattern):
       self.regex = re.compile(f'^{pattern}', re.IGNORECASE) if pattern else None
       self.invalidateFilter()

    def filterAcceptsRow(self, sourceRow, sourceParent):
       sourceModel = self.sourceModel()
       index = sourceModel.index(sourceRow, 0, sourceParent)
       fileName = sourceModel.fileName(index)

       if not self.regex or self.regex.match(fileName):
           return True

       if sourceModel.isDir(index):
           return self.checkChild(index)

       return False

    def checkChild(self, index):
        sourceModel = self.sourceModel()

        for i in range(sourceModel.rowCount(index)):
            child_index = sourceModel.index(i, 0, index)

            if self.filterAcceptsRow(i, index):
                return True

            if sourceModel.isDir(child_index):
                if self.checkChild(child_index):
                    return True

        return False


