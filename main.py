import re
from comps import *
from PyQt6.QtWidgets import QApplication, QMainWindow
from pandas import DataFrame, read_excel, read_csv, read_json
from csv import reader
import sys
import json


class MainWindow(Window):
    def __init__(self):
        super().__init__()

        buttonGp = ButtonGroup()

        # Creating components using your library
        main_layout = Vertical(
            Vertical(
                Tabs(
                    Tab(ScrollableContainer(
                        Vertical(
                            Label("Configure a task", style=TextStyles.Heading.fontWeight(
                                Style.FontWeightPolicy.Bold)),
                            Horizontal(
                                MultilineAssistedField("Message config",True,["{username}","{fullname}","{followers}","{followings}","{mediacount}","{lastpostlike}","{lastpostcomment}","{msgsep}"],
                                                    "message"),
                                MultilineAssistedField("Comment config", True, ["{username}", "{fullname}", "{followers}", "{followings}", "{mediacount}", "{postlike}", "{postcomment}", "{msgsep}"],
                                                    "comment"),
                            ),
                            ProxyMultiLineInput()
                        ).gap(2).padding(0).set_id("configure-tab").set_style(Style().backgroundColor("transparent"))
                    ), "Configure"),
                    Tab(Vertical(), "Read logs"),
                    Tab(Vertical(), "Run script"),
                    Tab(Vertical(), "Help"),
                )
            ).gap(0).padding(15).set_size(QSizePolicy.Policy.Expanding,
                                          QSizePolicy.Policy.Expanding),
        ).gap(0)

        # Setting the central widget
        self.setCentralWidget(main_layout)

        self.setMenuBar(MenuBar()
                        .add_menu(
                            Menu("File")
                            .add_action("Save", lambda *a: None, "ctrl+s")[0]
                            .add_action("Save as", lambda *a: None, "ctrl+shift+s")[0]
                            .add_separator()
                            .add_action("Open", lambda *a: None, "ctrl+o")[0])[0]
                        )

        # Setting up the main window properties
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("QInsta")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
