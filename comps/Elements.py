from enum import Enum

from comps.styles import Style
from .styles import QSS, Style, ButtonStyles
from typing import Callable, List, Self, Tuple, Union, overload, Any
from PyQt6.QtCore import (Qt, QSize, QPoint, QPointF, QRectF,QMargins,QThread)
from PyQt6.QtGui import (QIcon, QAction, QKeyEvent, QColor, QBrush, QPaintEvent, QPen, QPainter)
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QCheckBox, QLabel,
    QPushButton, QHBoxLayout, QTextEdit, QLineEdit, QLayout, QTabWidget,
    QGridLayout, QStackedLayout, QComboBox, QFileDialog, QScrollArea,
    QDialog, QRadioButton, QSizePolicy, QSlider, QProgressBar,
    QSpinBox, QDial, QMenuBar, QMenu, QMainWindow, QTableWidget,
    QTableWidgetItem, QListWidget, QListWidgetItem, QButtonGroup,
    QGroupBox, QFrame)


from PyQt6.QtCore import pyqtSlot as Slot


ButtonGroup = QButtonGroup


class Finder:
    elements = {}

    @staticmethod
    def add(element: 'Identifiable|QWidget'):
        """Adds an element to the map

        Args:
            element (QWidget): what element to add
        """
        Finder.elements[element.objectName()] = element

    @staticmethod
    def remove(element: QWidget | Any | str):
        """removes an element from the map

        Args:
            element (QWidget): what element to remove
        """
        if isinstance(element, QWidget):
            Finder.elements.pop(element.objectName(), None)
        else:
            Finder.elements.pop(element, None)

    @staticmethod
    def get(id_: str) -> QWidget:
        """Gets an element from the map

        Args:
            id_ (str): what element to get

        Returns:
            QWidget: the element
        """
        return Finder.elements[id_]


class Alignable:
    setAlignment: Callable

    def align(self, alignment: Qt.AlignmentFlag) -> Self:
        """Aligns the widget

        Args:
            alignment (Qt.AlignmentFlag): what alignment to apply

        Returns:
            Self: the widget
        """
        self.setAlignment(alignment)
        return self


class Identifiable:
    objectName: Callable
    setObjectName: Callable
    setAccessibleName: Callable
    """Identifiable widget, which supports objectName
    """

    def id(self, id_: str) -> Self:
        """Sets the objectName of the widget, replacing the old one if it exists

        Args:
            id_ (str): what to set the objectName to

        Returns:
            Self: the widget
        """
        Finder.remove(self)
        self.setObjectName(id_)
        Finder.add(self)
        return self

    def set_name(self, name: str) -> Self:
        """Sets the accessibleName of the widget, replacing the old one if it exists

        Args:
            name (str): what to set the accessibleName to

        Returns:
            Self: the widget
        """
        self.setAccessibleName(name)
        return self

    def identify(self, name: str | None = None, objectName: str | None = None) -> Self:
        """Identifies the element

        Args:
            name (str, optional): name to apply. Defaults to None.
            objectName (str, optional): objectName to apply. Defaults to None.

        Returns:
            Self: _description_
        """
        if name:
            self.id(name)
        if objectName:
            self.set_name(objectName)
        return self


class TextValueEditable:
    keyPressEvent: Callable
    keyReleaseEvent: Callable
    textChanged: Any
    setPlaceholderText: Callable
    """
    something which supports the editability of a text value, meaning it can be changed or altered by the user if enabled
    """

    def key_press(self, event: QKeyEvent) -> Self:
        """
        key press event handler
        """
        self.keyPressEvent(event)
        return self

    def key_release(self, event: QKeyEvent) -> Self:
        """
        key release event handler
        """
        self.keyReleaseEvent(event)
        return self

    def text_changed(self, text: str) -> Self:
        """
        text changed event handler
        """
        self.textChanged.emit(text)
        return self

    def set_placeholder(self, text: str) -> Self:
        """
        sets the placeholder text of the widget
        """
        self.setPlaceholderText(text)
        return self


class AnyMenu:
    addSeparator: Callable
    addAction: Callable
    addMenu: Callable

    def add_action(self, text: str, triggered_func=None, shortcut: str | None = None) -> Self:
        """Addds an action to a menu

        Args:
            text (str): what the label of that action should be
            triggered_func (Callable, optional): Something that can be called to a `triggered.connect` tunnel. Defaults to None.
            shortcut (str | None, optional): shortcut of the action. Defaults to None.

        Returns:
            Tuple[Self, QAction]: returns itself and the action generated
        """
        action = QAction(text, self)  # type: ignore
        if triggered_func:
            action.triggered.connect(triggered_func)
        if shortcut:
            action.setShortcut(shortcut)
        self.addAction(action)
        return self

    def add_menu(self, menu: "Menu") -> Self:
        """Adds a menu to a menu

        Args:
            menu (Menu): what menu to add

        Returns:
            Tuple[Self, QMenu]: returns itself and the menu generated
        """
        self.addMenu(menu)
        return self

    def add_separator(self) -> Self:
        """Adds a separator to a menu"""
        self.addSeparator()
        return self


class TextEditable:
    setText: Callable

    def set_text(self, text: str) -> Self:
        """Sets the text of the widget"""
        self.setText(text)
        return self


class Padded:
    setContentsMargins: Callable
    layout_padding: Callable
    content_gap: Callable
    contentsMargins: Callable[[],QMargins]

    def padding(self, p_: int) -> Self:
        """Sets the padding of the widget"""
        self.setContentsMargins(p_, p_, p_, p_)
        return self

    def paddingLeft(self, p_:int) -> Self:
        top = self.contentsMargins().top()
        right = self.contentsMargins().right()
        bottom = self.contentsMargins().bottom()
        self.setContentsMargins(p_, top, right, bottom)
        return self
    pl = paddingLeft
    def paddingRight(self, p_:int) -> Self:
        top = self.contentsMargins().top()
        left = self.contentsMargins().left()
        bottom = self.contentsMargins().bottom()
        self.setContentsMargins(left, top, p_, bottom)
        return self
    pr = paddingRight
    def paddingTop(self, p_:int) -> Self:
        left = self.contentsMargins().left()
        right = self.contentsMargins().right()
        bottom = self.contentsMargins().bottom()
        self.setContentsMargins(left, p_, right, bottom)
        return self
    pt = paddingTop
    def paddingBottom(self, p_:int) -> Self:
        left = self.contentsMargins().left()
        right = self.contentsMargins().right()
        top = self.contentsMargins().top()
        self.setContentsMargins(left, top, right, p_)
        return self
    pb = paddingBottom

    def gap(self, g_: int) -> Self:
        """Sets the gap of the widget"""
        try:
            self.setContentsMargins(g_, g_, g_, g_)
            self.layout_padding(g_)
            self.content_gap(g_)
        except:
            pass
        return self


class Stylable:
    setStyleSheet: Callable
    accessibleName: Callable
    objectName: Callable
    styleSheet: Callable
    setAttribute: Callable

    def set_style(self, style: Union[Style, QSS]) -> Self:
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        """Sets the style or QSS of the widget"""
        if isinstance(style, QSS):
            self.setStyleSheet(style.to_str())
        else:
            self.setStyleSheet(f"{self.accessibleName()}{(
                '#'+self.objectName()) if self.objectName() != '' else ''}{{{style.to_str()}}}")
        return self

    def add_style(self, style: Union[Style, QSS]) -> Self:
        """Adds a style or QSS to the widget, it will keep the old one"""
        self.setStyleSheet(self.styleSheet() + style.to_str())
        return self

    def add_qss(self, style_sheet: str) -> Self:
        """adds a raw qss description to the stylesheet

        Args:
            style_sheet (str): the stylesheet to apply

        Returns:
            itself: returns itself
        """
        self.setStyleSheet(self.styleSheet() + style_sheet)
        return self

    def addTo(self, target: str, style: Style) -> Self:
        """Adds a style to a target inside of the element itself, it could be for example the pane of a tabwidget
        """
        self.setStyleSheet(f"{self.accessibleName()}{(
            '#'+self.objectName()) if self.objectName() != '' else ''}{target}{{{style.to_str()}}}")
        return self


class Attributable:
    setAttribute: Callable

    def set_attribute(self, attribute: Qt.WidgetAttribute, value: bool) -> Self:
        """sets an attribute to an element

        Args:
            attribute (Qt.WidgetAttribute)
            value (bool)

        Returns:
            Self: itself
        """
        self.setAttribute(attribute, value)
        return self


class Linked:
    setEnabled: Callable
    setVisible: Callable

    def link(self, chbox: "CheckBox") -> Self:
        """Links the enable state of the object to a CheckBox.

        Args:
            chbox (CheckBox): The CheckBox to link to.

        Returns:
            itself: Returns itself after setting up the linkage.
        """
        self.setEnabled(chbox.isChecked())
        chbox.stateChanged.connect(lambda x: self.setEnabled(x))
        return self

    def visible(self, chbox: "CheckBox"):
        """Sets the visibility of the widget to the state of the checkbox"""
        self.setVisible(chbox.isChecked())
        chbox.stateChanged.connect(lambda x: self.setVisible(x))
        return self
    def notVisible(self, chbox: "CheckBox"):
        """Sets the visibility of the widget to the state of the checkbox"""
        self.setVisible(not chbox.isChecked())
        chbox.stateChanged.connect(lambda x: self.setVisible(not x))
        return self


class Checkable:
    setChecked: Callable

    def check(self, checked: bool) -> Self:
        """Sets the checked state of the object.

        Args:
            checked (bool): The desired checked state.

        Returns:
            itself: Returns itself after updating the checked state.
        """
        self.setChecked(checked)
        return self


class Clickable:
    clicked: Any

    def action(self, action: Callable) -> Self:
        """Connects a QAction to the object's clicked signal.

        Args:
            action (QAction): The QAction to connect.

        Returns:
            itself: Returns itself after connecting the QAction.
        """
        self.clicked.connect(action)
        return self


class Iconizable:
    setIcon: Callable

    def icon(self, icon: QIcon) -> Self:
        """Sets the icon for the object.

        Args:
            icon (QIcon): The QIcon to set as the object's icon.

        Returns:
            itself: Returns itself after setting the icon.
        """
        self.setIcon(icon)
        return self


class Ranged:
    setMaximum: Callable
    setMinimum: Callable

    def min(self, m: int) -> Self:
        """Sets the minimum value for the object.

        Args:
            m (int): The minimum value.

        Returns:
            itself: Returns itself after setting the minimum value.
        """
        self.setMinimum(m)
        return self

    def max(self, m: int) -> Self:
        """Sets the maximum value for the object.

        Args:
            m (int): The maximum value.

        Returns:
            itself: Returns itself after setting the maximum value.
        """
        self.setMaximum(m)
        return self


class Sizable:
    setFixedWidth: Callable[[int], None]
    setFixedHeight: Callable[[int], None]

    def width(self, w: int) -> Self:
        """Sets the width of the widget"""
        self.setFixedWidth(w)
        return self

    def height(self, h: int) -> Self:
        """Sets the height of the widget"""
        self.setFixedHeight(h)
        return self

    def getWidth(self) -> int:
        """Gets the width of the widget"""
        return super().width()  #  type:ignore

    def getHeight(self) -> int:
        """Gets the height of the widget"""
        return super().height()  #  type:ignore


class BasicElement(Padded, Stylable, Attributable, Identifiable, Alignable, Sizable):
    setSizePolicy: Callable
    setMinimumSize: Callable
    setMaximumSize: Callable
    setFixedWidth: Callable
    setFixedHeight: Callable
    """
    A basic element that combines functionality from multiple classes.

    Inherited Classes:
    - Padded: Adds padding functionality to the element.
    - Stylable: Provides methods for styling the element with CSS-like styles.
    - Attributable: Allows setting and getting attributes for the element.
    - Identifiable: Adds functionality for assigning and retrieving identifiers for the element.

    Note: This class doesn't define any additional methods but inherits functionality from the mentioned classes.
    """

    def expand(self, wSizePolicy: QSizePolicy.Policy, hSizePolicy: QSizePolicy.Policy) -> Self:
        """Sets the size policy of the element"""
        self.setSizePolicy(wSizePolicy, hSizePolicy)
        return self

    def minSize(self, w: int, h: int) -> Self:
        """Sets the minimum size of the element"""
        self.setMinimumSize(w, h)
        return self

    def maxSize(self, w: int, h: int) -> Self:
        """Sets the maximum size of the element"""
        self.setMaximumSize(w, h)
        return self

    def setW(self, w: int) -> Self:
        """Sets the width of the element"""
        self.setFixedWidth(w)
        return self

    def setH(self, h: int) -> Self:
        """Sets the width of the element"""
        self.setFixedHeight(h)
        return self


class Stretch:
    pass


Spacer = Stretch


class BaseContainer(QWidget, BasicElement, Linked):
    """
    A base container widget that combines features from QWidget, BasicElement, and Linked.

    Args:
    - items: Optional. Initial items to add to the container. Can be a single widget, a list, or a tuple of widgets, layouts, or stretches.
    - parent: Optional. The parent widget.
    - layout: Optional. The layout to use for the container.
    - style: Optional. The style to apply to the container.

    Methods:
    - __init__: Initializes the BaseContainer with the provided items, parent, layout, and style.
    - add: Overloaded method to add widgets, layouts, or stretches to the container.
    - layout_padding: Sets the padding around the container's layout.
    - content_gap: Sets the gap between items within the container's layout.
    """

    def __init__(self, *items: Union[QWidget, QLayout, Stretch, "GroupBox", Tuple, List, Any],
                 parent=None,
                 layout: QLayout | None = None,
                 style: Style | None = None):
        super().__init__(parent=parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        self.setAccessibleName(self.__class__.__name__)
        self.lyt = layout if layout is not None else QVBoxLayout()
        self.setLayout(self.lyt)
        self.gap(0)
        if style is not None:
            self.set_style(style)
        if items:
            self.add(*items)

    def align(self, alignment: Qt.AlignmentFlag) -> Self:
        """
        Sets the alignment of the container.

        Args:
        - alignment: The alignment to set.

        Returns:
        - itself: Returns itself after setting the alignment.
        """
        self.lyt.setAlignment(alignment)
        return self

    def add(self, *items: Union[QWidget, Tuple, List, str, QLayout, Stretch, Spacer]) -> Self:
        """
        Adds widgets, layouts, or stretches to the container.

        Args:
        - items: Variable number of items to add. Can be QWidget, QLayout, Stretch, or Spacer.

        Returns:
        - itself: Returns the container itself after adding the items.
        """
        for item in items:
            if item is None:
                continue
            elif isinstance(item, QWidget):
                self.lyt.addWidget(item)
            elif isinstance(item, QLayout):
                if isinstance(self.lyt, QHBoxLayout) or isinstance(self.lyt, QVBoxLayout):
                    self.lyt.addLayout(item)
            elif isinstance(item, list):
                self.lyt.addWidget(Horizontal(*item))
            elif isinstance(item, tuple):
                self.lyt.addWidget(Vertical(*item))
            elif isinstance(item, str):
                self.lyt.addWidget(Text(item, Text.Type.P1))
            else:
                if isinstance(self.lyt, QHBoxLayout) or isinstance(self.lyt, QVBoxLayout):
                    self.lyt.addStretch()
        return self

    def remove(self, item: QWidget) -> Self:
        """
        Removes a widget from the container.

        Args:
        - item: The widget to remove.

        Returns:
        - itself: Returns the container itself after removing the widget.
        """
        self.lyt.removeWidget(item)
        return self

    def layout_padding(self, padding: int) -> Self:
        """
        Sets the padding around the container's layout.

        Args:
        - padding: The padding value.

        Returns:
        - itself: Returns the container itself after setting the layout padding.
        """
        self.lyt.setContentsMargins(padding, padding, padding, padding)
        return self

    def content_gap(self, gap: int) -> Self:
        """
        Sets the gap between items within the container's layout.

        Args:
        - gap: The gap value.

        Returns:
        - itself: Returns the container itself after setting the content gap.
        """
        self.lyt.setSpacing(gap)
        return self


class Vertical(BaseContainer):
    """
    A container with a vertical layout.

    Args:
    - items: Variable number of items to add to the vertical container. Can be QWidget, QLayout, Stretch, or Spacer.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the vertical container.
    """

    def __init__(self, *items: Union[QWidget, QLayout, Stretch, Spacer, Tuple, List, "GroupBox", None], parent=None, style: Style | None = None):
        super().__init__(*items, parent=parent, layout=QVBoxLayout(), style=style)


class Horizontal(BaseContainer):
    """
    A container with a horizontal layout.

    Args:
    - items: Variable number of items to add to the horizontal container. Can be QWidget, QLayout, Stretch, or Spacer.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the horizontal container.
    """

    def __init__(self, *items: Union[QWidget, QLayout, Stretch, Spacer, "GroupBox", Tuple, List, None], parent=None, style: Style | None = None):
        super().__init__(*items, parent=parent, layout=QHBoxLayout(), style=style)


class Grid(BaseContainer):
    """
    A container with a grid layout.

    Args:
    - items: Variable number of items to add to the grid container. Can be QWidget, QLayout, Stretch, or Spacer.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the grid container.
    """

    def __init__(self, *items: Union[QWidget, QLayout, Tuple, List], parent=None, style: Style | None = None):
        super().__init__(*items, parent=parent, layout=QGridLayout(), style=style)


class Stacked(BaseContainer):
    """
    A container with a stacked layout.

    Args:
    - items: Variable number of items to add to the stacked container. Can be QWidget, QLayout, Stretch, or Spacer.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the stacked container.
    """
    lyt: QStackedLayout

    def __init__(self, *items: Union[QWidget, QLayout, Tuple, List], parent=None, style: Style | None = None):
        super().__init__(*items, parent=parent, layout=QStackedLayout(), style=style)

    def currentIndex(self, index: int) -> Self:
        """
        Sets the current index of the stacked container.

        Args:
        - index: The index to set.

        Returns:
        - itself: Returns itself after setting the current index.
        """
        self.lyt.setCurrentIndex(index)
        return self

    def currentWidget(self, widget: QWidget) -> Self:
        """
        Sets the current widget of the stacked container.

        Args:
        - widget: The widget to set.

        Returns:
        - itself: Returns itself after setting the current widget.
        """
        self.lyt.setCurrentWidget(widget)
        return self


class Tab:
    """
    Represents a tab within a tab widget.

    Args:
    - tab: The content widget associated with the tab.
    - title: The title of the tab.
    - icon: Optional. The icon associated with the tab.

    Methods:
    - reset: Resets the tab properties to new values.
    - setTab: Sets the content widget for the tab.
    - setTitle: Sets the title of the tab.
    - setIcon: Sets the icon for the tab.
    """

    def __init__(self, tab: QWidget | None = None, title: str | None = None, icon: QIcon | None = None) -> None:
        self.tab = tab
        self.title = title
        self.icon = icon

    def reset(self, tab: QWidget | None = None, title: str | None = None, icon: QIcon | None = None) -> Self:
        """
        Resets the tab properties to new values.

        Args:
        - tab: The content widget associated with the tab.
        - title: The title of the tab.
        - icon: Optional. The icon associated with the tab.

        Returns:
        - itself: Returns itself after resetting the tab properties.
        """
        self.tab = tab
        self.title = title
        self.icon = icon
        return self

    def setTab(self, tab: QWidget) -> Self:
        """
        Sets the content widget for the tab.

        Args:
        - tab: The content widget associated with the tab.

        Returns:
        - itself: Returns itself after setting the tab content widget.
        """
        self.tab = tab
        return self

    def setTitle(self, title: str) -> Self:
        """
        Sets the title of the tab.

        Args:
        - title: The title of the tab.

        Returns:
        - itself: Returns itself after setting the tab title.
        """
        self.title = title
        return self

    def setIcon(self, icon: QIcon) -> Self:
        """
        Sets the icon for the tab.

        Args:
        - icon: The icon associated with the tab.

        Returns:
        - itself: Returns itself after setting the tab icon.
        """
        self.icon = icon
        return self


class Tabs(QTabWidget, BasicElement, Linked, Padded):
    """
    Represents a tab widget with additional features.

    Args:
    - elements: Variable number of Tab instances to add to the tab widget.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the tab widget.

    Methods:
    - paneMovable: Sets whether the panes (tabs) are movable.
    - tabIndex: Sets the current tab index.
    - set_tab_close_button: Sets the visibility of close buttons on the tabs.
    - add: Overloaded method to add tabs with different parameters.
    """

    def __init__(self, *elements: Tab, parent: QWidget | None = None, style: Style | None = None) -> None:
        super().__init__(parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        for element in elements:
            self.add(element)

    def paneMovable(self, movable: bool) -> Self:
        """
        Sets whether the panes (tabs) are movable.

        Args:
        - movable: Boolean indicating whether the panes are movable.

        Returns:
        - itself: Returns itself after setting the pane movability.
        """
        self.setMovable(movable)
        return self

    def tabIndex(self, i: int) -> Self:
        """
        Sets the current tab index.

        Args:
        - i: The index of the tab to set as the current tab.

        Returns:
        - itself: Returns itself after setting the current tab index.
        """
        self.setCurrentIndex(i)
        return self

    def tabClosable(self, enabled: bool) -> Self:
        """
        Sets the visibility of close buttons on the tabs.

        Args:
        - enabled: Boolean indicating whether close buttons should be visible.

        Returns:
        - itself: Returns itself after setting the visibility of close buttons.
        """
        self.setTabsClosable(enabled)
        return self

    @overload
    def add(self, tab: Tab) -> Self:
        ...

    @overload
    def add(self, widget: QWidget, title: str = "") -> Self:
        ...

    @overload
    def add(self, widget: QWidget, title: str = "", icon: QIcon | None = None) -> Self:
        ...

    def add(self, widget: QWidget | Tab, title: str = "", icon: QIcon | None = None) -> Self:  #  type:ignore
        """
        Adds tabs to the tab widget.

        Args:
        - widget: The content widget or Tab instance to add.
        - title: The title of the tab.
        - icon: Optional. The icon associated with the tab.

        Returns:
        - itself: Returns the tab widget itself after adding the tab.
        """
        if isinstance(widget, Tab):
            if widget.icon is not None:
                self.addTab(widget.tab, widget.icon, widget.title)
            else:
                self.addTab(widget.tab, widget.title)
        else:
            if icon is not None:
                self.addTab(widget, icon, title)
            else:
                self.addTab(widget, title)
        return self


class Label(QLabel, BasicElement, Linked, Iconizable):
    """
    Represents a label widget with additional features.

    Args:
    - text: The text content of the label.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the label.

    Methods:
    - set_icon: Sets the icon for the label.
    """

    def __init__(self, text: str, parent=None, style: Style | None = None):
        super().__init__(text=text, parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        self.setOpenExternalLinks(True)
        self.setWordWrap(True)

    def wrap(self, b: bool) -> Self:
        self.setWordWrap(b)
        return self

    def interactiveLinks(self, b: bool) -> Self:
        self.setOpenExternalLinks(b)
        return self

    def icon(self, icon: QIcon) -> Self:
        """
        Sets the icon for the label.

        Args:
        - icon: The QIcon to set as the label's icon.

        Returns:
        - itself: Returns itself after setting the icon.
        """
        self.setPixmap(icon.pixmap(self.size()))
        return self


class Heading(Label):
    class Type(Enum):
        H1 = Style().fontSize("30px").fontWeight(Style.FontWeightPolicy.Bold)
        H2 = Style().fontSize("26px").fontWeight(Style.FontWeightPolicy.Bold)
        H3 = Style().fontSize("22px").fontWeight(Style.FontWeightPolicy.Bold)
        H4 = Style().fontSize("20px").fontWeight(Style.FontWeightPolicy.Normal)
        H5 = Style().fontSize("18px").fontWeight(Style.FontWeightPolicy.Normal)
        H6 = Style().fontSize("16px").fontWeight(Style.FontWeightPolicy.Normal)

    def __init__(self, text: str = "", hp: "Heading.Type" = Type.H1, parent: QWidget | None = None, style: Style | None = None):
        super().__init__(text=text, parent=parent, style=style)
        self.add_style(hp.value)


class Text(Label):
    class Type(Enum):
        P1 = Style().fontSize("16px")
        P2 = Style().fontSize("14px")
        P3 = Style().fontSize("12px")

    def __init__(self, text: str = "", hp: "Text.Type" = Type.P1, parent: QWidget | None = None, style: Style | None = None):
        super().__init__(text=text, parent=parent, style=style)
        self.add_style(hp.value)


class Button(QPushButton, BasicElement, Linked, Clickable, Iconizable):
    """
    Represents a button widget with additional features.

    Args:
    - text: The text content of the button.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the button.
    """

    def __init__(self, text: str, parent=None, style: Style | None = None):
        super().__init__(text=text, parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)


class CheckBox(QCheckBox, BasicElement, Checkable, Linked, Iconizable):
    """
    Represents a check box widget with additional features.

    Args:
    - text: The text content of the check box.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the check box.
    """

    def __init__(self, text: str, parent=None, style: Style | None = None):
        super().__init__(text=text, parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
    def enableCondition(self, other:"CheckBox"):
        self.setEnabled(other.isChecked())
        # add listener for then other value changes and set the same
        other.stateChanged.connect(lambda x: (self.setChecked(other.isChecked()),self.setCheckable(other.isChecked())))
        return self


class RadioButton(QRadioButton, BasicElement, Checkable, TextEditable, Linked, Iconizable):
    """
    Represents a radio button widget with additional features.

    Args:
    - text: The text content of the radio button.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the radio button.

    Methods:
    - group: Adds the radio button to a QButtonGroup.

    """

    def __init__(self, text: str, parent=None, style: Style | None = None):
        super().__init__(text=text, parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)

    def assign(self, group: QButtonGroup) -> Self:
        """
        Adds the radio button to a QButtonGroup.

        Args:
        - group: The QButtonGroup to add the radio button to.

        Returns:
        - itself: Returns itself after adding to the group.
        """
        group.addButton(self)
        return self

    def check(self, b: bool) -> Self:
        self.setChecked(b)
        return self


class ComboBox(QComboBox, BasicElement, TextEditable, Linked):
    """
    Represents a combo box widget with additional features.

    Args:
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the combo box.

    Methods:
    - add: Adds items to the combo box.
    - set: Sets items in the combo box, clearing existing items.
    - clear: Clears all items from the combo box.
    """

    def __init__(self, items: List[str]|Tuple[str], style: Style | None = None):
        super().__init__()
        self.setStyleSheet(style.to_str() if style else "")
        self.add(*items)

    def get(self) -> str:
        """
        Returns the current selected item in the combo box.

        Returns:
        - The current selected item.
        """
        return self.currentText()

    def add(self, *items: str) -> Self:
        """
        Adds items to the combo box.

        Args:
        - items: A list or tuple of strings to add to the combo box.

        Returns:
        - itself: Returns itself after adding items.
        """
        if items:
            for item in items:
                self.addItem(item)
        return self

    def set(self, *items: str) -> Self:
        """
        Sets items in the combo box, clearing existing items.

        Args:
        - items: A list or tuple of strings to set in the combo box.

        Returns:
        - itself: Returns itself after setting items.
        """
        self.clear()
        self.add(*items)
        return self

    def clear(self) -> Self:  # type:ignore
        """
        Clears all items from the combo box.

        Returns:
        - itself: Returns itself after clearing items.
        """
        super().clear()
        return self

    def change_listener(self, callback: Callable[[str], None]) -> Self:
        """
        Adds a change listener to the combo box.

        Args:
        - callback: A function to call when the combo box changes.

        Returns:
        - itself: Returns itself after adding the listener.
        """
        self.currentIndexChanged.connect(callback)
        return self


class Field(QLineEdit, BasicElement, TextEditable, Linked, TextValueEditable):
    """
    Represents a single-line text input field with additional features.

    Args:
    - placeholder: Optional. The placeholder text for the field.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the field.
    """

    def __init__(self, placeholder: str | None = None, parent: QWidget | None = None, style: Style | None = None):
        super().__init__(parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        if placeholder:
            self.setPlaceholderText(placeholder)
        self.setAccessibleName(self.__class__.__name__)

    def get(self) -> str:
        """
        Returns the current text in the field.

        Returns:
        - The current text in the field.
        """
        return self.text()


class MultilineField(QTextEdit, BasicElement, TextEditable, Linked, TextValueEditable):
    """
    Represents a multi-line text input field with additional features.

    Args:
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the field.
    """

    def __init__(self, parent=None, style=None):
        super().__init__(parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)


class Slider(QSlider, BasicElement, Linked, Ranged):
    """
    Represents a slider widget with additional features.

    Args:
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the slider.
    """

    def __init__(self, parent=None, style: Style | None = None):
        super().__init__(parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)


class ProgressBar(QProgressBar, BasicElement, Linked, Ranged):
    """
    Represents a progress bar widget with additional features.

    Args:
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the progress bar.
    """

    def __init__(self, parent=None, style: Style | None = None):
        super().__init__(parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)


class SpinBox(QSpinBox, BasicElement, Linked, TextEditable, Ranged):
    """
    Represents a spin box widget with additional features.

    Args:
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the spin box.
    """

    def __init__(self, parent=None, style: Style | None = None):
        super().__init__(parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        self.setValue

    def valueChange(self, fn: Callable) -> Self:
        self.valueChanged.connect(fn)
        return self

    def set_value(self, value: int) -> Self:
        self.setValue(value)
        return self


class Dial(QDial, BasicElement, Linked, Ranged):
    """
    Represents a dial widget with additional features.

    Args:
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the dial.
    """

    def __init__(self, parent=None, style: Style | None = None):
        super().__init__(parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        self.setValue


class Action(QAction, BasicElement):
    """
    Represents an action with additional features.

    Args:
    - text: The text content of the action.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the action.
    """

    def __init__(self, text: str, f: Callable, key: str | None = None, icon: QIcon | None = None, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.triggered.connect(f)
        self.setShortcut(key)
        if icon:
            self.setIcon(icon)


class Separator:
    pass


class Menu(QMenu, AnyMenu):
    """
    Represents a menu with additional features.

    Args:
    - title: The title of the menu.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the menu.
    """

    def __init__(self, title: str, *items: Action | Separator, parent=None, style: Style | None = None):
        super().__init__(title, parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        for item in items:
            if isinstance(item, Separator):
                self.addSeparator()
                continue
            if isinstance(item, Action):
                self.addAction(item)
                continue
            raise TypeError(f"Invalid item type {type(item)}")


class MenuBar(QMenuBar, AnyMenu):
    """Represents a menu bar."""

    def __init__(self, *items: Menu, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        for item in items:
            self.add_menu(item)


class FileDialog(QFileDialog):
    """
    Represents a file dialog with additional features.

    Args:
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the file dialog.
    - mode: Optional. The mode of the file dialog.
    """

    def __init__(self, parent=None, style: Style | None = None, mode: QFileDialog.AcceptMode = QFileDialog.AcceptMode.AcceptOpen):
        super().__init__(parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        self.setAcceptMode(mode)


class Window(QMainWindow, BasicElement):
    """
    Represents a main window with additional features.

    Args:
    - child: Optional. The central widget of the window.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the window.
    """

    def __init__(self, child: QWidget | Tuple | List | None = None, parent=None, style: Style | None = None):
        super().__init__(parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        if child:
            if isinstance(child, list):
                child = Horizontal(*child)
            elif isinstance(child, tuple):
                child = Vertical(*child)
            if child is not None:
                self.setCentralWidget(child)

    def set_title(self, title: str) -> Self:
        """
        Sets the title of the window.

        Args:
        - title: The title of the window.

        Returns:
        - itself: Returns itself after setting the title.
        """
        self.setWindowTitle(title)
        return self

    def set_widget(self, widget: QWidget) -> Self:
        """
        Sets the central widget of the window.

        Args:
        - widget: The central widget to set.

        Returns:
        - itself: Returns itself after setting the central widget.
        """
        self.setCentralWidget(widget)
        return self


class ScrollableContainer(Vertical, BasicElement):
    """
    Represents a scrollable container for content.

    Args:
    - content: The content widget to display in the scrollable container.
    - parent: Optional. The parent widget.
    """

    def __init__(self, content: QWidget | Tuple | List, parent=None):
        super().__init__(parent=parent)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # Set the content widget for the scroll area
        if isinstance(content, list):
            content = Horizontal(*content)
        elif isinstance(content, tuple):
            content = Vertical(*content)
        self.scroll_area.setWidget(content)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)
        self.id("scroll-container")
        self.set_style(Style().backgroundColor("transparent"))

        # Set up the main layout
        self.scroll_area.setObjectName("scroll-area")
        self.scroll_area.setStyleSheet(
            "QScrollArea#scroll-area{background-color:transparent}")
        self.add(self.scroll_area)

        # Ensure the content expands to fill the available space
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)

        self.gap(0)

    def set_content(self, content: QWidget):
        """
        Sets the content widget for the scrollable container.

        Args:
        - content: The content widget to display in the scrollable container.

        Returns:
        - itself: Returns itself after setting the content.
        """
        self.scroll_area.setWidget(content)
        return self

    def horizontal(self, horizontalBehavior: Qt.ScrollBarPolicy = Qt.ScrollBarPolicy.ScrollBarAlwaysOn) -> Self:
        self.scroll_area.setHorizontalScrollBarPolicy(horizontalBehavior)
        return self

    def vertical(self, verticalBehavior: Qt.ScrollBarPolicy = Qt.ScrollBarPolicy.ScrollBarAlwaysOn) -> Self:
        self.scroll_area.setVerticalScrollBarPolicy(verticalBehavior)
        return self


class GroupBox(QGroupBox, BasicElement, Padded, Linked):
    layout: Callable[..., QLayout]
    """
    Represents a group box with additional features.

    Args:
    - title: The title of the group box.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the group box.
    """

    def __init__(self, content: BaseContainer | Tuple | List, title: str, parent=None, style: Style | None = None):
        super().__init__(title, parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        if isinstance(content, BaseContainer):
            self.setLayout(content.layout())
        elif isinstance(content, tuple):
            l = Vertical(*content)
            self.setLayout(l.layout())
        elif isinstance(content, list):
            l = Horizontal(*content)
            self.setLayout(l.layout())

    def layout_padding(self, p0_: int) -> Self:
        self.layout().setContentsMargins(p0_, p0_, p0_, p0_)
        return self

    def content_gap(self, p0_: int) -> Self:
        self.layout().setSpacing(p0_)
        return self


class Column:
    def __init__(self, head: QTableWidgetItem | str | None = None, *items: QTableWidgetItem | str | QWidget) -> None:
        self.head = head
        self.items = items


class ItemCheckable(QTableWidgetItem):
    def __init__(self, text: str = "") -> None:
        super().__init__()
        self.setFlags(Qt.ItemFlag.ItemIsUserCheckable |
                      Qt.ItemFlag.ItemIsEnabled)
        self.setCheckState(Qt.CheckState.Unchecked)
        self.setText(None)

    def get(self) -> bool:
        return self.checkState() == Qt.CheckState.Checked


class Toggle(CheckBox):

    _transparent_pen = QPen(Qt.GlobalColor.transparent)
    _light_grey_pen = QPen(Qt.GlobalColor.lightGray)

    def __init__(self,
                 parent=None,
                 bar_color=Qt.GlobalColor.gray,
                 checked_color="#00B0FF",
                 handle_color=Qt.GlobalColor.white,
                 ):
        super().__init__("")

        self.setMaximumWidth(50)

        # Save our properties on the object via self, so we can access them later
        # in the paintEvent.
        self._bar_brush = QBrush(bar_color)
        self._bar_checked_brush = QBrush(QColor(checked_color).lighter())

        self._handle_brush = QBrush(handle_color)
        self._handle_checked_brush = QBrush(QColor(checked_color))

        # Setup the rest of the widget.

        self.setContentsMargins(8, 0, 8, 0)
        self._handle_position = 0

        self.stateChanged.connect(self._handle_state_change)

    def sizeHint(self):
        return QSize(48, 35)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self, e: QPaintEvent):

        contRect = self.contentsRect()
        handleRadius = round(0.24 * contRect.height())

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        p.setPen(self._transparent_pen)
        barRect = QRectF(
            0, 0,
            contRect.width() - handleRadius, 0.40 * contRect.height()
        )
        barRect.moveCenter(contRect.center().toPointF())
        rounding = barRect.height() / 2

        # the handle will move along this line
        trailLength = contRect.width() - 2 * handleRadius
        xPos = contRect.x() + handleRadius + trailLength * self._handle_position

        if self.isChecked():
            p.setBrush(self._bar_checked_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setBrush(self._handle_checked_brush)

        else:
            p.setBrush(self._bar_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setPen(self._light_grey_pen)
            p.setBrush(self._handle_brush)

        p.drawEllipse(
            QPointF(xPos, barRect.center().y()),
            handleRadius, handleRadius)

        p.end()

    def pressed(self, func: Callable[[bool], None]) -> Self:
        self.stateChanged.connect(lambda *x: func(self._handle_position == 1))
        return self

    @Slot(int)
    def _handle_state_change(self, value):
        self._handle_position = 1 if value else 0

    def _get_handle_position(self):
        return self._handle_position

    def handle_position(self, pos):
        """change the property
        we need to trigger QWidget.update() method, either by:
            1- calling it here [ what we're doing ].
            2- connecting the QPropertyAnimation.valueChanged() signal to it.
        """
        self._handle_position = pos
        self.update()

    def _get_pulse_radius(self):
        return self._pulse_radius

    def _pulse_radius(self, pos):
        self._pulse_radius = pos
        self.update()

class Table(QTableWidget, BasicElement, Linked):
    """
    Represents a table widget with additional features.

    Args:
    - rows: The initial number of rows in the table.
    - columns: The initial number of columns in the table.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the table.

    Methods:
    - add_row: Adds a new row with the specified data to the table.
    - add_column: Adds a new column with the specified header text and data to the table.
    - set_cell_data: Sets the data for a specific cell in the table.
    - add_button: Adds a button to a specific cell in the table.
    - add_checkbox: Adds a checkbox to a specific cell in the table.
    - add_combobox: Adds a combobox to a specific cell in the table.
    - handle_cell_click: Handles the click event on a cell and executes corresponding actions.
    - set_clicked_function: Sets a function to be called when a cell is clicked.
    """

    def __init__(self, *columns, parent=None, style: Style | None = None) -> None:
        super().__init__(parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        self.clicked_function = None
        for column in columns:
            self.add_column(column)

    def add_column(self, column: Column) -> None:
        """
        Adds a new column to the table with the specified header text and data.

        Args:
        - header: The header text for the new column.
        - data: The data for the new column.

        Returns:
        - None: Returns nothing.
        """
        self.setColumnCount(self.columnCount()+1)
        if column.head is not None:
            self.setHorizontalHeaderItem(
                self.columnCount()-1, QTableWidgetItem(column.head))
        for i, data in enumerate(column.items):
            if isinstance(data, str):
                self.setItem(i, self.columnCount()-1, QTableWidgetItem(data))
            elif isinstance(data, QTableWidgetItem):
                self.setItem(i, self.columnCount()-1, data)
            else:
                self.setCellWidget(i, self.columnCount()-1, data)


class LoginForm(Vertical):
    """
    Represents a login form with predefined structure.

    Args:
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the login form.
    """

    def __init__(self, parent=None, style: Style | None = None):
        super().__init__(parent=parent, style=style)
        self.username = Field("Username")
        self.password = Field("Password")

        self.add(
            Label("Login").id("login-header").set_style(Style().add(
                "Label#login-header", "font-size:24px;font-weight:bold")),
            self.username,
            self.password,
            Button("Login").id("login-button"),
            Spacer()
        )

    def get(self) -> Tuple[str, str]:
        """
        Gets the values entered in the login form.

        Returns:
        - Tuple[str, str]: The username and password entered in the form.
        """
        return self.username.get(), self.password.get()


class MultilineAssistedField(Vertical):
    def __init__(self, denom: str, importFromFile: bool, suggestions: List[str], identificator: str, parent=None, style: Style | None = None):
        super().__init__(parent=parent, style=style)
        self.textField = MultilineField()
        self.suggestions = ComboBox(
            suggestions).change_listener(self.combobox_listener_call)
        self.set_name("MultilineAssistedField")
        self.id(identificator)
        self.add(
            (
                denom if denom else None,
                self.textField,
                [
                    GroupBox(
                        Vertical(
                            Button("Import "+denom).action(self.load),
                            Button("Export "+denom).action(self.export),
                        ), "File options"
                    ) if importFromFile else None,
                    GroupBox(
                        Vertical(
                            self.suggestions,
                            Button("Add suggestion").action(
                                self.combobox_listener_call)
                        ), "Suggestions"
                    ) if suggestions else None,
                ]
            ),
            Spacer()
        )

    def combobox_listener_call(self, *args, **kwargs):
        self.textField.insertPlainText(self.suggestions.get())

    def get(self) -> str:
        return self.textField.toPlainText()

    def load(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open file", "", "Text files (*.txt)")
        if path:
            with open(path, "r") as f:
                self.textField.insertPlainText(f.read())

    def export(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save file", "", "Text files (*.txt)")
        if path:
            with open(path, "w") as f:
                f.write(self.textField.toPlainText())


class ListWidget(QListWidget, BasicElement, Linked, Padded):
    def __init__(self, *items: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.addItems(items)

    def add(self, *items: str | QListWidgetItem | None) -> Self:
        self.addItems(items)  #  type:ignore
        return self

    def change(self, *items: str) -> Self:
        self.clear()
        self.addItems(items)
        return self

    def change_at(self, index: int, item: str) -> Self:
        self.takeItem(index)
        self.insertItem(index, item)
        return self

    def pop(self, index: int) -> str | None:
        item = self.takeItem(index)
        if item:
            return item.text()
        return None

    def remove(self, index: int) -> Self:
        self.takeItem(index)
        return self


class NavigationLink(Button):
    def __init__(self, text: str, icon: QIcon | None = None, dest: QWidget | None = None):
        super().__init__(text, icon)
        self.dest = dest
        self.id("nav-link")
        self.set_style(Style().add("Button#nav-link", "padding:0px;"))
        self.set_style(ButtonStyles.NavPrimary)

    def target(self, target: QWidget | List | Tuple) -> Self:
        if isinstance(target, List):
            target = Horizontal(*target)
        elif isinstance(target, Tuple):
            target = Vertical(*target)
        self.dest = target
        return self


class NavigationBar(Horizontal, BasicElement):
    def __init__(self, *items: NavigationLink | QWidget, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.items = items
        self.set_name("NavigationContainer")
        self.sidebar = Vertical(*items).setW(200)
        self.sidebar.set_name("NavigationSidebar")
        self.sidebar.expand(QSizePolicy.Policy.Expanding,
                            QSizePolicy.Policy.Expanding)
        self.sidebar.align(Qt.AlignmentFlag.AlignTop)
        self.content_bar = Stacked()
        for i, item in enumerate(items):
            if isinstance(item, NavigationLink) and item.dest:
                self.content_bar.add(item.dest)
                item.action(lambda *a, item=item: self.change(item))
            self.sidebar.add(item)
        self.add(self.sidebar, self.content_bar)

    def change(self, item: NavigationLink) -> None:
        if item.dest:
            self.content_bar.currentWidget(item.dest)

    def new(self, *items: NavigationLink | QWidget) -> Self:
        # get the last index in the dictionary self.orders
        for i, item in enumerate(items):
            if isinstance(item, NavigationLink) and item.dest:
                self.content_bar.add(item.dest)
                item.action(lambda *a, item=item: self.change(item))
            self.sidebar.add(item)
        return self

    def shiftAt(self, index: int) -> Self:
        self.change(self.items[index])  # type: ignore
        return self


class Divider(QFrame, BasicElement):
    def __init__(self, orientation: Qt.Orientation = Qt.Orientation.Vertical, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.set_name("Divider")
        self.setFrameShape(QFrame.Shape.VLine if orientation ==
                           Qt.Orientation.Vertical else QFrame.Shape.HLine)


class HDivider(Divider):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(Qt.Orientation.Horizontal, parent)


class VDivider(Divider):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(Qt.Orientation.Vertical, parent)

