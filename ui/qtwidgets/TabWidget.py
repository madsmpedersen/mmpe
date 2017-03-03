'''
Created on 10/02/2014

@author: mmpe
'''



import sys

from qtpy import QtCore, QtGui
from qtpy.QtWidgets import QTabWidget, QLabel


class TabWidget(QTabWidget):

    def __init__(self, tab_widget):
        QTabWidget.__init__(self)
        self.tab_widget = tab_widget
        self.setTabsClosable(True)
        self.setMovable(True)
        self.insertTab(0, QWidget(), "")
        self.new_label = QLabel("*")
        self.tabBar().setTabButton(0, QTabBar.RightSide, self.new_label)
        self.currentChanged.connect(self.current_tab_changed)
        QObject.connect(self, SIGNAL("tabCloseRequested(int)"), self.close_tab)
        QObject.connect(self.tabBar(), SIGNAL("tabMoved(int,int)"), self.tabMoved)

        self.labels = lambda: [str(self.tabBar().tabText(i)).lower() for i in range(self.count())]
        self.tabBar().setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabBar().customContextMenuRequested.connect(self.openMenu)
        self.add_tab()


    def widget(self, tab=None):
        """tab must be index, text, widget, tab or None(current tab)"""
        if tab is None:
            tab = self.currentWidget()
        if isinstance(tab, int):
            tab = self.tabText(tab)
        tab = str(tab)
        if tab.lower() not in self.labels():
            self.add_tab(tab)
        index = self.labels().index(str(tab).lower())
        return QTabWidget.widget(self, index)


    def current_tab_changed(self, index):
        # Add new tab if "*" tab is clicked
        if index == self.count() - 1:
            self.add_tab()
        else:
            self.widget(index).update()

    def close_tab(self, index):
        self.setCurrentIndex(index - 1)
        try:
            self.widget(index).terminate()
        except:
            pass
        self.removeTab(index)

    def add_tab(self, label=None):
        widget = self.tab_widget()
        if label is None:
            label = widget.name
        index = self.insertTab(self.count() - 1, widget, u"")  # Do not set tab label here in order to avoid duplicate labels

        actual_name = self.setTabText(index, label)
        widget.name = actual_name
        self.setCurrentIndex(index)
        return index

    def setTabText(self, index, tab_text):
        tab_text = self.unique_tab_text(tab_text, index)
        QTabWidget.setTabText(self, index, tab_text)
        return tab_text

    def unique_tab_text(self, tab_text, index=-1):
        labels = self.labels()
        i = 0
        l = tab_text
        while l.lower() in labels and labels.index(l.lower()) != index:
            i += 1
            l = "%s%d" % (tab_text, i)
        return l

    def tabMoved(self, from_index, to_index):
        if from_index == self.count() - 1:
            self.tabBar().moveTab(to_index, from_index)


    def openMenu(self, position):
        def edit():
            menu = QMenu()
            editAction = menu.addAction("Rename")
            return editAction == menu.exec_(self.mapToGlobal(position))
        tabindex = self.tabBar().tabAt(position)
        if tabindex < self.count() - 1:
            self.setCurrentIndex(tabindex)

            if edit():
                tabname, ok = QInputDialog.getText(self, "Enter new name", "New name", text=self.tabText(tabindex))
                if ok:
                    self.widget(tabindex).name = tabname
                    self.setTabText(tabindex, str(tabname))


    def close_all_tabs(self):
        for i in range(self.count() - 1):
            self.close_tab(0)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    def ptt(txt):
        print (txt)
    m = QMainWindow()
    def new_widget():
        return QPushButton("hello")
    t = TabWidget(new_widget)

    m.setCentralWidget(t)
    t.connect
    m.show()
    sys.exit(app.exec_())


