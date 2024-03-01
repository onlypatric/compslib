import re
from comps import *
from PyQt6.QtWidgets import QApplication, QMainWindow
from pandas import DataFrame,read_excel,read_csv,read_json
from csv import reader
import sys
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Creating components using your library
        main_layout = Vertical(
            Horizontal(
                Button("Hello world"),
                Button("Hello world"),
                Button("Hello world"),
            ),
            Horizontal(
                ComboBox(),
                RadioButton("Hello world"),
                Label("Hello world"),
                Stretch
            ),
            Horizontal(
                Tabs(
                    Tab(Button("Tab 1"), "Tab 1"),
                    Tab(Button("Tab 2"), "Tab 2"),
                    Tab(Vertical(
                        Button("Tab 3"),
                        Field().set_text("Tab 3"),
                    ), "Tab 3"),
                )
            ),
            Horizontal(
                Button("Another Horizontal Button"),
                Button("Another Horizontal Button"),
            ),
            Label("Ciao!"),
            Stretch
        ).set_style(Style().add("Vertical", ""))

        # Setting the central widget
        self.setCentralWidget(main_layout)

        self.setMenuBar(MenuBar()
                        .add_menu(Menu("File").add_action("Save", lambda *a: None, "ctrl+s")[0].add_action("Save as", lambda *a: None, "ctrl+shift+s")[0].add_action("Open", lambda *a: None, "ctrl+o")[0])[0])

        # Setting up the main window properties
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Enhanced Sample Application")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
