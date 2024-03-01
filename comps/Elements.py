import json
import os
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Self, Tuple, Union, overload, override
from PyQt6.QtCore import Qt, QEvent, QMetaObject,pyqtSignal
from PyQt6.QtGui import QIcon,QAction,QKeyEvent
from PyQt6.QtWidgets import QWidget,QVBoxLayout,QCheckBox,QLabel,\
    QPushButton,QHBoxLayout,QTextEdit,QLineEdit,QLayout,QTabWidget,\
    QGridLayout,QStackedLayout,QComboBox,QFileDialog,QScrollArea,\
    QDialog, QMessageBox, QErrorMessage, QRadioButton, QSizePolicy,\
    QSlider, QProgressBar, QSpinBox, QDial, QMenuBar, QMenu

class Finder:
    elements = {}
    @staticmethod
    def add(element:QWidget):
        Finder.elements[element.objectName()] = element
    def remove(element:QWidget):
        Finder.elements.pop(element.objectName(),None)

class Identifiable:
    def set_id(self, id_:str) -> Self:
        Finder.remove(self)
        self.setObjectName(id_)
        Finder.add(self)
        return self
    def set_name(self, name:str) -> Self:
        self.setAccessibleName(name)
        return self

class TextValueEditable:
    def key_press(self, event: QKeyEvent) -> Self:
        self.keyPressEvent(event)
    def key_release(self, event: QKeyEvent) -> Self:
        self.keyReleaseEvent(event)

class AnyMenu:
    def add_action(self, text: str, triggered_func=None, shortcut: str | None = None) -> Tuple[Self, QAction]:
        action = QAction(text, self)
        if triggered_func:
            action.triggered.connect(triggered_func)
        if shortcut:
            action.setShortcut(shortcut)
        self.addAction(action)
        return self, action

    def add_menu(self, menu: "Menu") -> Tuple[Self, QAction]:
        return self, self.addMenu(menu)
    
    def add_separator(self) -> Self:
        self.addSeparator()
        return self

class Style:
    def __init__(self) -> None:
        self._styles = {}
    def add(self,identifier:str,style:str) -> Self:
        self._styles[identifier] = style
        return self
    def merge(self, style:Self) -> Self:
        self._styles.update(style._styles)
        return self
    def addDict(self, styles:Dict[str,str]) -> Self:
        self._styles.update(styles)
        return self
    def pop(self, name:str):
        return self._styles.pop(name)
    def get(self, name:str):
        return self._styles[name]
    def to_str(self):
        content = "\n".join([f"{k}{{{v}}};" for k,v in self._styles.items()])
        return content

class TextEditable:
    def set_text(self,text:str) -> Self:
        self.setText(text)
        return self

class Padded:
    def padding(self,p_:int) -> Self:
        self.setContentMargins(p_,p_,p_,p_)
        return self

class Stylable:
    def set_style(self, style):
        self.setStyleSheet(style.to_str())
        return self

    def add_style(self, style):
        self.setStyleSheet(self.styleSheet() + style.to_str())
        return self
    
    def setIdentifier(self,name:str=None,class_name:str=None)->Self:
        if name:
            self.setAccessibleName(name)
        if class_name:
            self.setObjectName(class_name)
        return self

class Attributable:
    def set_attribute(self,attribute:Qt.WidgetAttribute,value:bool) -> Self:
        self.setAttribute(attribute,value)
        return self

class Linked:
    def link(self,chbox:"CheckBox") -> Self: #link enabled
        self.setEnabled(chbox.isChecked())
        chbox.stateChanged.connect(lambda x:self.setEnabled(x))
        return self

class Checkable:
    def set_checked(self, checked: bool) -> Self:
        self.setChecked(checked)
        return self

class Clickable:
    def action(self, action: QAction) -> Self:
        self.clicked.connect(action)
        return self

class Iconizable:
    def set_icon(self, icon:QIcon) -> Self:
        self.setIcon(icon)
        return self

class Ranged:
    def min(self, m: int) -> Self:
        self.setMinimum(m)
        return self

    def max(self, m: int) -> Self:
        self.setMaximum(m)
        return self

class BasicElement(Padded, Stylable, Attributable, Identifiable):
    pass

class Stretch:
    pass

class BaseContainer(QWidget, BasicElement, Linked):
    def __init__(self, items: Union[List[Union[QWidget, QLayout,Stretch]], Tuple[Union[QWidget, QLayout,Stretch]]] = None,
                 parent=None,
                 layout:QLayout=None,
                 style:Style=None):
        super().__init__(parent=parent)
        self.setAccessibleName(self.__class__.__name__)
        self.lyt = layout if layout is not None else QVBoxLayout()
        self.setLayout(self.lyt)
        self.setStyleSheet(style.to_str() if style else "")
        self.add(items)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
    @overload
    def add(self, widget:QWidget) -> Self:
        ...
    @overload
    def add(self, component_array: Union[List[Union[QWidget, QLayout]], Tuple[Union[QWidget, QLayout]]]) -> Self:
        ...
    @overload
    def add(self, layout:QLayout) -> Self:
        ...

    def add(self, items: Union[List[Union[QWidget, QLayout]], Tuple[Union[QWidget, QLayout]]] = None) -> Self:
        if not items: return self
        elif isinstance(items, list) or isinstance(items,tuple):
            for item in items:
                if isinstance(item, QWidget):self.lyt.addWidget(item)
                elif isinstance(item, QLayout):self.lyt.addLayout(item)
                else:self.lyt.addStretch()
        elif isinstance(items,QWidget):
            self.lyt.addWidget(items)
        elif isinstance(items, QLayout):
            self.lyt.addLayout(items)
        elif isinstance(items, Stretch):
            self.lyt.addStretch()
        return self
    def set_style(self,style:Style) -> Self:
        self.setStyleSheet(style.to_str())
        return self
    def add_style(self, style:Style) -> Self:
        self.setStyleSheet(self.styleSheet()+style.to_str())
        return self
    def layout_padding(self, padding:int) -> Self:
        self.lyt.setContentsMargins(padding, padding, padding, padding)
        return self
    def content_gap(self, gap:int) -> Self:
        self.lyt.setSpacing(gap)
        return self

class Vertical(BaseContainer):
    def __init__(self, *items: Union[QWidget,QLayout], parent=None, style:Style=None):
        super().__init__(items=items, parent=parent, layout=QVBoxLayout(), style=style)

class Horizontal(BaseContainer):
    def __init__(self, *items: Union[QWidget, QLayout], parent=None, style: Style = None):
        super().__init__(items=items, parent=parent, layout=QHBoxLayout(), style=style)

class Grid(BaseContainer):
    def __init__(self, *items: Union[QWidget, QLayout], parent=None, style: Style = None):
        super().__init__(items=items, parent=parent, layout=QGridLayout(), style=style)

class Stacked(BaseContainer):
    def __init__(self, *items: Union[QWidget, QLayout], parent=None, style: Style = None):
        super().__init__(items=items, parent=parent, layout=QStackedLayout(), style=style)

class Tab:
    def __init__(self,tab:QWidget|None=None,title:str|None=None,icon:QIcon|None=None) -> None:
        self.tab=tab
        self.title=title
        self.icon=icon

    def reset(self, tab: QWidget | None = None, title: str | None = None, icon: QIcon | None = None) -> Self:
        self.tab = tab
        self.title = title
        self.icon = icon
        return self

    def setTab(self,tab:QWidget) -> Self:
        self.tab=tab
        return self

    def setTitle(self, title: str) -> Self:
        self.title=title
        return self

    def setIcon(self, icon: QIcon) -> Self:
        self.icon = icon
        return self

class Tabs(QTabWidget,BasicElement, Linked):
    def __init__(self, *elements:Tab, parent:QWidget|None=None, style:Style=None) -> None:
        super().__init__(parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        for element in elements:
            self.add(element)

    @overload
    def add(self, tab:Tab) -> Self:
        ...

    @overload
    def add(self, widget: QWidget,title:str) -> Self:
        ...

    @overload
    def add(self, widget: QWidget, title: str,icon:QIcon) -> Self:
        ...

    def add(self,widget:QWidget|Tab,title:str="",icon:QIcon=None)->Self:
        if isinstance(widget,Tab):
            if widget.icon is not None:
                self.addTab(widget.tab, widget.icon, widget.title)
            else:
                self.addTab(widget.tab, widget.title)
        else:
            if icon is not None:
                self.addTab(widget, icon, title)
            else:
                self.addTab(widget,title)
        return self

class Label(QLabel, BasicElement, Linked, Iconizable):
    def __init__(self, text:str, parent=None, style:Style=None):
        super().__init__(text=text, parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)

    
    def set_icon(self, icon:QIcon) -> Self:
        self.setPixmap(icon.pixmap(self.size()))
        return self

class Button(QPushButton, BasicElement, Linked, Clickable, Iconizable):
    def __init__(self, text:str, parent=None, style:Style=None):
        super().__init__(text=text, parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)

class CheckBox(QCheckBox, BasicElement, Checkable, Linked, Iconizable):
    def __init__(self, text: str, parent=None, style: Style = None):
        super().__init__(text=text, parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)

class RadioButton(QRadioButton, BasicElement,Checkable, TextEditable, Linked,Iconizable):
    def __init__(self, text:str, parent=None, style:Style=None):
        super().__init__(text=text, parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)

class ComboBox(QComboBox, BasicElement, TextEditable, Linked):
    def __init__(self, parent=None, style:Style=None):
        super().__init__(parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)

    def add(self, items: Union[List[str], Tuple[str]]) -> Self:
        self.addItems(items)
        self.add
        return self
    
    def set(self, items:Union[List[str], Tuple[str]]) -> Self:
        self.clear()
        self.add(items)
        return self
    
    def clear(self) -> Self:
        super().clear()
        return self

class Field(QLineEdit, BasicElement, TextEditable, Linked, TextValueEditable):
    def __init__(self, parent=None, style: Style = None):
        super().__init__(parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)

class MultilineField(QTextEdit, BasicElement, TextEditable, Linked,TextValueEditable):
    def __init__(self, parent=None, style=None):
        super().__init__(parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)

class Slider(QSlider, BasicElement, Linked,Ranged):
    def __init__(self, parent=None, style: Style = None):
        super().__init__(parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)

class ProgressBar(QProgressBar, BasicElement, Linked,Ranged):
    def __init__(self, parent=None, style: Style = None):
        super().__init__(parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)

class SpinBox(QSpinBox, BasicElement, Linked, TextEditable,Ranged):
    def __init__(self, parent=None, style: Style = None):
        super().__init__(parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        self.setValue

class Dial(QDial, BasicElement, Linked, Ranged):
    def __init__(self, parent=None, style: Style = None):
        super().__init__(parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        self.setValue

class Menu(QMenu,AnyMenu):
    def __init__(self, title:str, parent=None, style:Style=None):
        super().__init__(title, parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)

class MenuBar(QMenuBar,AnyMenu):
    pass