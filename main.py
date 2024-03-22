import re
from typing import Dict, List, Tuple
from comps import *
from PyQt6.QtWidgets import QApplication, QLayout, QMainWindow,QStyleFactory, QWidget,QAbstractItemView
from pandas import DataFrame, read_excel, read_csv, read_json
from csv import reader
from PyObjCTools import AppHelper
import sys
import json

from comps.Elements import GroupBox, Spacer, Stretch
from comps.styles import Style

def matchTo(selection:int, values:List|Tuple) -> str:
    if selection >= len(values):
        return ""
    return values[selection]

class ListBox(Vertical):
    def __init__(self,title:str="",on_add:Callable[[],str]|None=None):
        super().__init__()
        self.set_name("ListBox")
        self.list = ListWidget()
        self.list.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)
        self.add(GroupBox(
            (
                self.list,
                [Spacer(),Button("+").action(lambda *x:self.list.add(on_add()) if on_add is not None else None),Button("-")]
            ),
            title
        ).expand(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

class SendingValidator(Vertical):
    def __init__(self,text:str) -> None:
        super().__init__()
        self.set_name("SendingValidator")
        self.frequency  = SpinBox().min(0).max(1000000)
        self.min1       = SpinBox().min(0).max(1000000)
        self.max1       = SpinBox().min(0).max(1000000)
        self.min2       = SpinBox().min(0).max(1000000)
        self.max2       = SpinBox().min(0).max(1000000)
        self.add(GroupBox(
            Horizontal(
                (
                    Text("Frequency ",Text.Type.P3),
                    self.frequency,
                    Text("min followers at", Text.Type.P3),
                    self.min1,
                    Text("max followers at", Text.Type.P3),
                    self.max1,
                    Spacer()
                ),
                (
                    Text("min media likes ", Text.Type.P3),
                    self.min2,
                    Text("max media likes ", Text.Type.P3),
                    self.max2,
                    Spacer()
                )
            ),
            text
        ))
    def get(self) -> Dict[str,int]:
        return {
            "frequency": self.frequency.value(),
            "min1": self.min1.value(),
            "max1": self.max1.value(),
            "min2": self.min2.value(),
            "max2": self.max2.value()
        }

class MainWindow(Window):
    def __init__(self):
        super().__init__()

        self.deviceType = ButtonGroup()

        welcome_section = (
            Heading("Welcome!"),
            HDivider(),
            Heading("Experience the force of a <u>fully automated software</u>.", hp=Heading.Type.H3),
            Text("Introduction to QInsta"),
            Spacer()
        )
        configure_section = ScrollableContainer(
            Vertical(
                #region TITLE PART
                [Heading("Configure"),Spacer(),Button("Open"),Button("Save as"),Button("New")],
                # endregion
                #region userlist and accounts list
                GroupBox(
                    (
                        [Text("Users list"),Spacer(),Text("Current: None")],
                        ListBox("Proxy list",on_add=self.add_proxy),
                    ),
                    "Users Accounts and Proxy configuration"
                ),
                #endregion
                GroupBox(
                    (
                        [ # MESSAGES & COMMENTS
                            #region MESSAGES
                            (
                                Horizontal(
                                    Text("Send messages"),
                                    Toggle().id("enablemsg").check(True).pl(5).pr(5).setW(35).setH(28),
                                    Spacer()
                                ).align(Qt.AlignmentFlag.AlignTop),
                                MultilineAssistedField("",True,["{username}","{name}","{followers}","{following}","{separator}"],"message").visible(Finder.get("enablemsg")), # type: ignore
                                Spacer()
                            ),
                            #endregion
                            #region COMMENTS
                            (
                                Horizontal(Text("Send comments"),Toggle().id("enablecomment").check(True).pl(5).pr(5).setW(35).setH(28),Spacer()).align(Qt.AlignmentFlag.AlignTop),
                                MultilineAssistedField("", True, ["{username}", "{name}", "{followers}", "{following}", "{separator}", "{likes}", "{comments}"], "comment").visible(
                                    Finder.get("enablecomment")), # type: ignore
                                Spacer()
                            ) 
                            # endregion
                        ],
                        GroupBox(
                            (
                                [
                                    #region LIKE PARAMS
                                    Vertical(
                                        CheckBox("Send Likes").id("enablelike").check(True),
                                        SendingValidator("Likes").link(
                                            Finder.get("enablelike")),  # type: ignore
                                    ).align(Qt.AlignmentFlag.AlignTop),
                                    #endregion
                                    # region FOLLOW PARAMS
                                    Vertical(
                                        CheckBox("Send Follows").id("enablefollow").check(True),
                                        SendingValidator("Follows").link(
                                            Finder.get("enablefollow")),  # type: ignore
                                    ).align(Qt.AlignmentFlag.AlignTop)
                                    #endregion
                                ],
                                [
                                    # region COMMENT PARAMS
                                    Vertical(
                                        CheckBox("enable comment filters").id("enablecommentfilters").check(
                                            True).enableCondition(Finder.get("enablecomment")), # type: ignore
                                        SendingValidator("Comments").visible(
                                            Finder.get("enablecomment")).link(Finder.get("enablecommentfilters")), # type: ignore
                                    ).align(Qt.AlignmentFlag.AlignTop),
                                    # endregion
                                    # region MESSAGE PARAMS
                                    Vertical(
                                        CheckBox("enable message filters").id("enablemessagefilters").check(True).enableCondition(
                                            Finder.get("enablemsg")),  # type: ignore
                                        SendingValidator("Messages").visible(
                                            Finder.get("enablemsg")).link(Finder.get("enablemessagefilters")), # type: ignore
                                    ).align(Qt.AlignmentFlag.AlignTop)
                                    # endregion
                                ]
                            ),
                            "Single-tap interactions"
                        )
                    ),
                    "Direct user interactions"
                ),
                GroupBox(
                    (
                        GroupBox(
                            [
                                RadioButton("iPhone").assign(self.deviceType),
                                RadioButton("Android").assign(self.deviceType).check(True)
                            ],
                            "Device Type"
                        ),  # type: ignore
                        [Text("Device agent picking order",Text.Type.P3),ComboBox(["Default device agent","Random device agent"])]
                    ),
                    "Device configuration"
                ),
                Spacer(),
            ).align(Qt.AlignmentFlag.AlignTop)
        ).horizontal(Qt.ScrollBarPolicy.ScrollBarAlwaysOff).vertical(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        # Creating components using your library
        main_layout = Vertical(
            NavigationBar(
                Heading("QINSTA"),
                NavigationLink("HOME").target(welcome_section),
                NavigationLink("SCRIPTS").target(configure_section),
                NavigationLink("RUN", dest=Vertical(
                    Heading("Select a script"), HDivider(), Spacer()))
            ).id("navbar"),
        ).pl(5).pr(5)

        self.setCentralWidget(main_layout)

        # Setting up the main window properties
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("QInsta")
    def delete_selected_parameter(self, widget_id):
        idx = Finder.get(widget_id).currentIndex() # type: ignore
        if idx:
            Finder.get(widget_id).remove(idx.row()) # type: ignore
    def add_proxy(self)->str:
        self.win = Vertical()
        self.win.setWindowTitle("Add Proxy")
        connection_type = ComboBox(["HTTP", "HTTPS"])
        field = Field("Proxy IP")
        port = Field("Proxy port")
        username = Field("Proxy username")
        password = Field("Proxy password")
        checkbox = Toggle()
        self.win.add(
            Heading("Add a new proxy"),
            [connection_type,field,port],
            [checkbox,username.link(checkbox),password.link(checkbox)],
            [Button("OK"),Button("Cancel")]
        ).padding(5)
        self.win.show()
        return f"{connection_type.currentText()}://{field.get()}:{port.get()}"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("macOS"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
