import os

from argparse import ArgumentParser, RawTextHelpFormatter

from PySide6.QtWidgets import (QMainWindow, QFileIconProvider, QScroller, QTreeView, QLineEdit)
from PySide6.QtCore import QRect, QModelIndex
from PySide6.QtCore import QDir, Qt

from button_delegate import ButtonDelegate
from file_system_model import MyFileSystemModel
from filter_proxy_model import MyFilterProxyModel


class MainWindow(QMainWindow):
    def __init__(self, name):
        super(MainWindow, self).__init__()

        self.name = name
        self.home_path = os.path.expanduser("~")
        self.flag_expand = False

        self.argument_parser = ArgumentParser(description=self.name,
        formatter_class=RawTextHelpFormatter)
        self.argument_parser.add_argument("--no-custom", "-c", action="store_true",
                                     help="Set QFileSystemModel.DontUseCustomDirectoryIcons")
        self.argument_parser.add_argument("--no-watch", "-w", action="store_true",
                                     help="Set QFileSystemModel.DontWatch")
        self.argument_parser.add_argument("directory",
                                     help="The directory to start in.",
                                     nargs='?', type=str)


        self.model = MyFileSystemModel()
        self.model.setFilter(QDir.AllEntries | QDir.Hidden)

        self.proxy_model = MyFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)

        self.tree = QTreeView()
        self.tree.setModel(self.proxy_model)
        self.filter = QLineEdit(self.tree)

        self.delegate = ButtonDelegate()
        self.tree.setItemDelegateForColumn(4, self.delegate)
        self.tree.clicked.connect(self.button_clicked)

        self.__init()

        self.filter.textChanged.connect(self.__update_tree)


    def __init(self):
        options = self.argument_parser.parse_args()
        root_path = options.directory
        icon_provider = QFileIconProvider()
        availableSize = self.tree.screen().availableGeometry().size()

        self.model.setIconProvider(icon_provider)
        self.model.setRootPath(self.home_path)

        if options.no_custom:
            self.proxy_model.setOption(QFileSystemModel.DontUseCustomDirectoryIcons)
        if options.no_watch:
            self.proxy_model.setOption(QFileSystemModel.DontWatchForChanges)

        self.tree.setRootIndex(self.proxy_model.mapFromSource(self.model.index(self.home_path)))

        # Demonstrating look and feel features
        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        self.tree.setColumnWidth(0, self.tree.width() / 4)
        self.tree.setColumnWidth(self.proxy_model.columnCount() - 2, 200)

        self.filter.setGeometry(QRect(658, 0, 310, 22))
        self.filter.setPlaceholderText("Поиск")

        self.resize(availableSize / 2)

        # Make it flickable on touchscreens
        QScroller.grabGesture(self.tree, QScroller.ScrollerGestureType.TouchGesture)

        self.setWindowTitle(self.name)
        self.setCentralWidget(self.tree)
        self.setFixedSize(950, 500)

        self.expand_folder()


    def __update_tree(self):
        text = self.filter.text()
        if text.strip() == "" or text.strip() == "\\" or text.strip() == "/":
            self.proxy_model.setFilterRegex(None)
            self.tree.setRootIndex(self.proxy_model.mapFromSource(self.model.index(self.home_path)))
        else:
            if not self.flag_expand:
                self.flag_expand = True
                self.expand_folder()
            self.proxy_model.setFilterRegex(text)



    def button_clicked(self, index: QModelIndex):
        source_index = self.proxy_model.mapToSource(index)

        if source_index.isValid() and self.model.isDir(source_index) and self.model.data(source_index) == "Обновить":
            self.model.update_index(source_index)
            self.tree.viewport().update()

    def expand_folder(self):
        home_index = self.proxy_model.mapFromSource(self.model.index(self.home_path))
        self.expand_level(home_index)

    def expand_level(self, index):
        if not index.isValid():
            return

        proxy_index = self.proxy_model.mapToSource(index)

        if self.model.isDir(proxy_index):
            if self.proxy_model.canFetchMore(proxy_index):
                self.proxy_model.fetchMore(proxy_index)

            self.tree.expand(index)

            for row in range(self.proxy_model.rowCount(index)):
                child_index = self.proxy_model.index(row, 0, index)
                self.expand_level(child_index)










