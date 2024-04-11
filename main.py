import os
import re
from typing import Dict, List, Tuple
from comps import *
from PyQt6.QtWidgets import QApplication, QLayout, QMainWindow,QStyleFactory, QWidget,QAbstractItemView
from pandas import DataFrame, read_excel, read_csv, read_json
from csv import reader
import sys
import json

from comps.Elements import GroupBox, Spacer, Stretch
from comps.styles import Style
import socket
import re

def matchTo(selection:int, values:List|Tuple) -> str:
    if selection >= len(values):
        return ""
    return values[selection]
class FormField(Vertical):
    def __init__(self, label:str):
        super().__init__()
        self.field = Field()
        self.add(Text(label,Text.Type.P3),self.field)
    def get(self) -> str:
        return self.field.text()
class ListBox(Vertical):
    def __init__(self,title:str="",on_add:Callable[[ListWidget],None]|None=None):
        super().__init__()
        self.set_name("ListBox")
        self.list = ListWidget()
        self.list.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)
        self.add(GroupBox(
            (
                self.list,
                [Button("Open").action(self.open),Button("Export").action(self.export),Spacer(),Button("+").action(lambda:on_add(self.list) if on_add is not None else None),Button("-")]
            ),
            title
        ).expand(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    def open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select file", "", "All Files (*)")
        if path and os.path.isfile(path) or os.path.islink(path):
            with open(path, "r") as file:
                for line in file:
                    self.list.add(line.strip())
    def export(self):
        path, _ = QFileDialog.getSaveFileName(self, "Select destination", "", "Plain text file (*.txt);;All files (*.*)")
        if path:
            with open(path, "w") as file:
                for index in range(self.list.count()):
                    item = self.list.item(index)
                    if item is not None:
                        file.write(item.text()+"\n")

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
        self.sendingParams=ButtonGroup()

        welcome_section = (
            Heading("Welcome!"),
            HDivider(),
            Heading("Experience the force of a <u>fully automated software</u>.", hp=Heading.Type.H3),
            Text("Introduction to QInsta"),
            GroupBox(
                (
                    "This software can:",
                    Text("""<ol><li>Send messages to millions of users</li><li>Send comments to millions of users</li><li>Send likes to millions of users</li><li>Send follows to millions of users</li><li>Send medias to millions of users</li><li>Increment your business relevance and revenue</li><li>Download user data for later use</li><li>Export users emails for cold mailing</li><li>Use proxies to avoid blocking and banning</li><li>Use multiple accounts at the same time (not avaiable*)</li><li>Load multiple configurations to spend less time configuring and more time sending</li><li>Blacklist with possibility to clear all, or clear by regex or by name</li><li>Add sending exceptions to avoid sending to people that are not targeted</li><li>Export a full overview of the sending campaign for ease of view</li><li>Usable as service (you can sell messages to other people)</li><li>Ask for 2FA code, to make use of more secure accounts and access methods</li><li>Save cookies for faster logins</li><li>Save network data for quicker responses and less bandwidth usage</li></ol>""", Text.Type.P3),
                    "And so much more..."
                ),
                ""
            ),
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
                        GroupBox(
                            ([Text("Current:"), Text("None").id("currentUserList").wrap(True)],
                            [Button("Open").action(self.load_user_list), Spacer(), Button("Export to"), ComboBox(["CSV", "JSON", "EXCEL", "PLAIN TEXT"]).id("exportType")]
                            ),"Users list"),
                        GroupBox(
                            ([Text("Current:"), Text("None").id("currentAccsList").wrap(True)],
                            [Button("Open").action(self.load_accounts_list), Spacer(), Button("Export to"), ComboBox(["CSV", "JSON", "EXCEL", "PLAIN TEXT"]).id("exportType")]
                            ),"Accounts list"),

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
                                MultilineAssistedField("",True,["{username}","{name}","{followers}","{following}","{separator}"],"message").visible("enablemsg"),
                                Spacer()
                            ),
                            #endregion
                            #region COMMENTS
                            (
                                Horizontal(Text("Send comments"),Toggle().id("enablecomment").check(True).pl(5).pr(5).setW(35).setH(28),Spacer()).align(Qt.AlignmentFlag.AlignTop),
                                MultilineAssistedField("", True, ["{username}", "{name}", "{followers}", "{following}", "{separator}", "{likes}", "{comments}"], "comment").visible("enablecomment"),
                                Spacer()
                            )
                            # endregion
                        ],
                        Text("How many users for each account",Text.Type.P3),
                        Field(),
                        GroupBox(
                            (
                                [
                                    #region LIKE PARAMS
                                    Vertical(
                                        CheckBox("Send Likes").id("enablelike"),
                                        SendingValidator("Likes").link("enablelike"),
                                    ).align(Qt.AlignmentFlag.AlignTop),
                                    #endregion
                                    # region FOLLOW PARAMS
                                    Vertical(
                                        CheckBox("Send Follows").id("enablefollow"),
                                        SendingValidator("Follows").link("enablefollow"),
                                    ).align(Qt.AlignmentFlag.AlignTop)
                                    #endregion
                                ],
                                [
                                    # region COMMENT PARAMS
                                    Vertical(
                                        CheckBox("enable comment filters").id("enablecommentfilters").enableCondition("enablecomment"),
                                        SendingValidator("Comments").visible("enablecomment").link("enablecommentfilters"),
                                    ).align(Qt.AlignmentFlag.AlignTop),
                                    # endregion
                                    # region MESSAGE PARAMS
                                    Vertical(
                                        CheckBox("enable message filters").id("enablemessagefilters").enableCondition(
                                            "enablemsg"),
                                        SendingValidator("Messages").visible(
                                            "enablemsg").link("enablemessagefilters"),
                                    ).align(Qt.AlignmentFlag.AlignTop)
                                    # endregion
                                ],
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
                        ),
                        [Text("Device agent picking order",Text.Type.P3),ComboBox(["Default device agent","Random device agent"])]
                    ),
                    "Device configuration"
                ),
                GroupBox(
                    [
                        (
                            FormField("Time before login"),
                            FormField("Time after login"),
                            FormField("Time before message").link("enablemsg"),
                            FormField("Time after message").link("enablemsg"),
                            FormField("Time before comment").link("enablecomment"),
                            FormField("Time after comment").link("enablecomment"),
                            FormField("Time before loading user"),
                            FormField("Time after loading user"),
                            FormField("Time before ending account task"),
                            FormField("Time after ending account task"),
                            Spacer(),
                        ),
                        HDivider(),
                        (
                            FormField("Time before like").link("enablelike"),
                            FormField("Time after like").link("enablelike"),
                            FormField("Time before follow").link("enablefollow"),
                            FormField("Time after follow").link("enablefollow"),
                            FormField("Time between message media and text").link("enablemsg"),
                            FormField("Time after being blocked"),
                            FormField("Time after being banned"),
                            FormField("Time before logout"),
                            FormField("Time after logout"),
                            Spacer(),
                        )
                    ],
                    "Timings (in seconds)"
                ),
                GroupBox(
                    (
                        [Toggle().id("userDataToJSON"), Text("Save user data to JSON",Text.Type.P3),Toggle().id("userDataToCSV"),Text("Save user data to CSV",Text.Type.P3)],
                        [Toggle().id("saveBlocksRecord"), Text("Save blocks record", Text.Type.P3), Toggle(
                        ).id("saveBansRecord"), Text("Save bans record", Text.Type.P3)],
                        [Toggle().id("twiceAttempt"), Text("Attempt twice to login", Text.Type.P3), Toggle().id("askForCode"), Text("Ask for manual code input", Text.Type.P3)],
                        [Toggle().id("saveCookies").check(True), Text("Save cookies", Text.Type.P3), Toggle().id("saveSession").check(True), Text("Save session ID", Text.Type.P3)],
                        [RadioButton("Send only to verified").assign(self.sendingParams),
                         RadioButton("Send only to non verified").assign(self.sendingParams), RadioButton("Send to both").assign(self.sendingParams).check(True)],
                    ),
                    "Extra configurations"
                ),
                Spacer(),
            ).align(Qt.AlignmentFlag.AlignTop)
        ).h(Qt.ScrollBarPolicy.ScrollBarAlwaysOff).v(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        run_section = (
            Heading("Select a script"),
            HDivider(),
            GroupBox([Button("Select").set_icon(QIcon("folder.png")), Label("Current: None"),Spacer()], "Load script"),
            Spacer()
        )
        # Creating components using your library
        main_layout = Vertical(
            NavigationBar(
                Heading("QINSTA"),
                NavigationLink("HOME")   .target(welcome_section),
                NavigationLink("SCRIPTS").target(configure_section),
                NavigationLink("RUN")    .target(run_section)
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
    def add_proxy(self,lst:ListWidget):
        self.win = Vertical()
        self.win.setWindowTitle("Add Proxy")
        connection_type = ComboBox(["HTTP", "HTTPS"])
        field = Field("Proxy IP")
        port = Field("Proxy port")
        username = Field("Proxy username")
        password = Field("Proxy password")
        checkbox = Toggle()
        def voidWin():
            self.win.close()
            self.win.deleteLater()
            self.win = None
            # Check if authentication toggle is enabled
            if checkbox.isChecked():
                auth_part = f"{username.get()}:{password.get()}@"
            else:
                auth_part = ""

            lst.add(f"{connection_type.currentText().lower()}://{auth_part}{field.get()}:{port.get()}")
        self.win.add(
            Heading("Add a new proxy"),
            [connection_type,field,port],
            [checkbox,username.link(checkbox),password.link(checkbox)],
            [Button("OK").action(voidWin), Button("Cancel")]
        ).padding(5)
        self.win.show()
    def load_user_list(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open file", "", "Plain text (*.txt);;Comma separated values (*.csv);;JSON dictionary (*.json);;Excel XML (>2016) (*.xlsx)")
        if path:
            Finder.get("currentUserList").setText(path)

    def load_accounts_list(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open file", "", "Plain text (*.txt);;Comma separated values (*.csv);;JSON dictionary (*.json);;Excel XML (>2016) (*.xlsx)")
        if path:
            Finder.get("currentAccsList").setText(path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("macOS"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
