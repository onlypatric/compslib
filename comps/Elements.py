from comps.styles import Style
from .styles import *
from typing import Callable, List, Self, Tuple, Union, overload
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction, QKeyEvent
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel, \
    QPushButton, QHBoxLayout, QTextEdit, QLineEdit, QLayout, QTabWidget, \
    QGridLayout, QStackedLayout, QComboBox, QFileDialog, QScrollArea, \
    QDialog, QMessageBox, QErrorMessage, QRadioButton, QSizePolicy, \
    QSlider, QProgressBar, QSpinBox, QDial, QMenuBar, QMenu, QMainWindow, \
    QTableView, QTableWidget, QTableWidgetItem, QTableWidgetSelectionRange, \
    QListWidget, QListWidgetItem, QButtonGroup, QGroupBox,QToolButton


ButtonGroup = QButtonGroup


class Finder:
    elements = {}

    @staticmethod
    def add(element: QWidget):
        """Adds an element to the map

        Args:
            element (QWidget): what element to add
        """
        Finder.elements[element.objectName()] = element

    @staticmethod
    def remove(element: QWidget | str):
        """removes an element from the map

        Args:
            element (QWidget): what element to remove
        """
        if isinstance(element, QWidget):
            Finder.elements.pop(element.objectName(), None)
        else:
            Finder.elements.pop(element, None)


class Identifiable:
    """Identifiable widget, which supports objectName
    """

    def set_id(self, id_: str) -> Self:
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

    def identify(self, name: str = None, objectName: str = None) -> Self:
        """Identifies the element

        Args:
            name (str, optional): name to apply. Defaults to None.
            objectName (str, optional): objectName to apply. Defaults to None.

        Returns:
            Self: _description_
        """
        if name:
            self.set_id(name)
        if objectName:
            self.set_name(objectName)
        return self


class TextValueEditable:
    """
    something which supports the editability of a text value, meaning it can be changed or altered by the user if enabled
    """

    def key_press(self, event: QKeyEvent) -> Self:
        """
        key press event handler
        """
        self.keyPressEvent(event)

    def key_release(self, event: QKeyEvent) -> Self:
        """
        key release event handler
        """
        self.keyReleaseEvent(event)

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
    def add_action(self, text: str, triggered_func=None, shortcut: str | None = None) -> Tuple[Self, QAction]:
        """Addds an action to a menu

        Args:
            text (str): what the label of that action should be
            triggered_func (Callable, optional): Something that can be called to a `triggered.connect` tunnel. Defaults to None.
            shortcut (str | None, optional): shortcut of the action. Defaults to None.

        Returns:
            Tuple[Self, QAction]: returns itself and the action generated
        """
        action = QAction(text, self)
        if triggered_func:
            action.triggered.connect(triggered_func)
        if shortcut:
            action.setShortcut(shortcut)
        self.addAction(action)
        return self, action

    def add_menu(self, menu: "Menu") -> Tuple[Self, QMenu]:
        """Adds a menu to a menu

        Args:
            menu (Menu): what menu to add

        Returns:
            Tuple[Self, QMenu]: returns itself and the menu generated
        """
        return self, self.addMenu(menu)

    def add_separator(self) -> Self:
        """Adds a separator to a menu"""
        self.addSeparator()
        return self


class TextEditable:
    def set_text(self, text: str) -> Self:
        """Sets the text of the widget"""
        self.setText(text)
        return self


class Padded:
    def padding(self, p_: int) -> Self:
        """Sets the padding of the widget"""
        self.setContentsMargins(p_, p_, p_, p_)
        return self
    def gap(self, g_: int) -> Self:
        """Sets the gap of the widget"""
        self.setContentsMargins(g_, g_, g_, g_)
        self.layout_padding(g_)
        self.content_gap(g_)
        return self


class Stylable:
    def set_style(self, style: Union[Style, QSS]) -> Self:
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
            '#'+self.objectName) if self.objectName() != '' else ''}{target}{{{style.to_str()}}}")
        return self


class Attributable:
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


class Checkable:
    def set_checked(self, checked: bool) -> Self:
        """Sets the checked state of the object.

        Args:
            checked (bool): The desired checked state.

        Returns:
            itself: Returns itself after updating the checked state.
        """
        self.setChecked(checked)
        return self


class Clickable:
    def action(self, action: QAction) -> Self:
        """Connects a QAction to the object's clicked signal.

        Args:
            action (QAction): The QAction to connect.

        Returns:
            itself: Returns itself after connecting the QAction.
        """
        self.clicked.connect(action)
        return self


class Iconizable:
    def set_icon(self, icon: QIcon) -> Self:
        """Sets the icon for the object.

        Args:
            icon (QIcon): The QIcon to set as the object's icon.

        Returns:
            itself: Returns itself after setting the icon.
        """
        self.setIcon(icon)
        return self


class Ranged:
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


class BasicElement(Padded, Stylable, Attributable, Identifiable):
    """
    A basic element that combines functionality from multiple classes.

    Inherited Classes:
    - Padded: Adds padding functionality to the element.
    - Stylable: Provides methods for styling the element with CSS-like styles.
    - Attributable: Allows setting and getting attributes for the element.
    - Identifiable: Adds functionality for assigning and retrieving identifiers for the element.

    Note: This class doesn't define any additional methods but inherits functionality from the mentioned classes.
    """
    def set_size(self, wSizePolicy: QSizePolicy,hSizePolicy:QSizePolicy) -> Self:
        """Sets the size policy of the element"""
        self.setSizePolicy(wSizePolicy, hSizePolicy)
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

    def __init__(self, items: Union[List[Union[QWidget, QLayout, Stretch]], Tuple[Union[QWidget, QLayout, Stretch]]] = None,
                 parent=None,
                 layout: QLayout = None,
                 style: Style = None):
        super().__init__(parent=parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        self.setAccessibleName(self.__class__.__name__)
        self.lyt = layout if layout is not None else QVBoxLayout()
        self.setLayout(self.lyt)
        self.setStyleSheet(style.to_str() if style else "")
        self.add(*items)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

    def add(self, *items: Union[QWidget, QLayout, Stretch, Spacer]) -> Self:
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
                self.lyt.addLayout(item)
            else:
                self.lyt.addStretch()
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

    def __init__(self, *items: Union[QWidget, QLayout], parent=None, style: Style = None):
        super().__init__(items=items, parent=parent, layout=QVBoxLayout(), style=style)


class Horizontal(BaseContainer):
    """
    A container with a horizontal layout.

    Args:
    - items: Variable number of items to add to the horizontal container. Can be QWidget, QLayout, Stretch, or Spacer.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the horizontal container.
    """

    def __init__(self, *items: Union[QWidget, QLayout], parent=None, style: Style = None):
        super().__init__(items=items, parent=parent, layout=QHBoxLayout(), style=style)


class Grid(BaseContainer):
    """
    A container with a grid layout.

    Args:
    - items: Variable number of items to add to the grid container. Can be QWidget, QLayout, Stretch, or Spacer.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the grid container.
    """

    def __init__(self, *items: Union[QWidget, QLayout], parent=None, style: Style = None):
        super().__init__(items=items, parent=parent, layout=QGridLayout(), style=style)


class Stacked(BaseContainer):
    """
    A container with a stacked layout.

    Args:
    - items: Variable number of items to add to the stacked container. Can be QWidget, QLayout, Stretch, or Spacer.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the stacked container.
    """

    def __init__(self, *items: Union[QWidget, QLayout], parent=None, style: Style = None):
        super().__init__(items=items, parent=parent, layout=QStackedLayout(), style=style)


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
    - set_pane_movable: Sets whether the panes (tabs) are movable.
    - set_tab_index: Sets the current tab index.
    - set_tab_close_button: Sets the visibility of close buttons on the tabs.
    - add: Overloaded method to add tabs with different parameters.
    """

    def __init__(self, *elements: Tab, parent: QWidget | None = None, style: Style = None) -> None:
        super().__init__(parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        for element in elements:
            self.add(element)

    def set_pane_movable(self, movable: bool) -> Self:
        """
        Sets whether the panes (tabs) are movable.

        Args:
        - movable: Boolean indicating whether the panes are movable.

        Returns:
        - itself: Returns itself after setting the pane movability.
        """
        self.setMovable(movable)
        return self

    def set_tab_index(self, i: int) -> Self:
        """
        Sets the current tab index.

        Args:
        - i: The index of the tab to set as the current tab.

        Returns:
        - itself: Returns itself after setting the current tab index.
        """
        self.setCurrentIndex(i)
        return self

    def set_tab_close_button(self, enabled: bool) -> Self:
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
    def add(self, widget: QWidget, title: str) -> Self:
        ...

    @overload
    def add(self, widget: QWidget, title: str, icon: QIcon) -> Self:
        ...

    def add(self, widget: QWidget | Tab, title: str = "", icon: QIcon = None) -> Self:
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

    def __init__(self, text: str, parent=None, style: Style = None):
        super().__init__(text=text, parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)

    def set_icon(self, icon: QIcon) -> Self:
        """
        Sets the icon for the label.

        Args:
        - icon: The QIcon to set as the label's icon.

        Returns:
        - itself: Returns itself after setting the icon.
        """
        self.setPixmap(icon.pixmap(self.size()))
        return self


class Button(QPushButton, BasicElement, Linked, Clickable, Iconizable):
    """
    Represents a button widget with additional features.

    Args:
    - text: The text content of the button.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the button.
    """

    def __init__(self, text: str, parent=None, style: Style = None):
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

    def __init__(self, text: str, parent=None, style: Style = None):
        super().__init__(text=text, parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)


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

    def __init__(self, text: str, parent=None, style: Style = None):
        super().__init__(text=text, parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)

    def group(self, group: QButtonGroup) -> Self:
        """
        Adds the radio button to a QButtonGroup.

        Args:
        - group: The QButtonGroup to add the radio button to.

        Returns:
        - itself: Returns itself after adding to the group.
        """
        group.addButton(self)
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

    def __init__(self, *items: str, parent=None, style: Style = None):
        super().__init__(parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        self.add(items)

    def get(self) -> str:
        """
        Returns the current selected item in the combo box.

        Returns:
        - The current selected item.
        """
        return self.currentText()

    def add(self, items: Union[List[str], Tuple[str]]) -> Self:
        """
        Adds items to the combo box.

        Args:
        - items: A list or tuple of strings to add to the combo box.

        Returns:
        - itself: Returns itself after adding items.
        """
        if items:
            self.addItems(items)
        return self

    def set(self, items: Union[List[str], Tuple[str]]) -> Self:
        """
        Sets items in the combo box, clearing existing items.

        Args:
        - items: A list or tuple of strings to set in the combo box.

        Returns:
        - itself: Returns itself after setting items.
        """
        self.clear()
        self.add(items)
        return self

    def clear(self) -> Self:
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

    def __init__(self, placeholder: str | None = None, parent: QWidget | None = None, style: Style = None):
        super().__init__(parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        if placeholder:
            self.setPlaceholderText(placeholder)
        self.setAccessibleName(self.__class__.__name__)


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

    def __init__(self, parent=None, style: Style = None):
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

    def __init__(self, parent=None, style: Style = None):
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

    def __init__(self, parent=None, style: Style = None):
        super().__init__(parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        self.setValue


class Dial(QDial, BasicElement, Linked, Ranged):
    """
    Represents a dial widget with additional features.

    Args:
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the dial.
    """

    def __init__(self, parent=None, style: Style = None):
        super().__init__(parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        self.setValue


class Menu(QMenu, AnyMenu):
    """
    Represents a menu with additional features.

    Args:
    - title: The title of the menu.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the menu.
    """

    def __init__(self, title: str, parent=None, style: Style = None):
        super().__init__(title, parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)


class MenuBar(QMenuBar, AnyMenu):
    """Represents a menu bar."""
    pass


class FileDialog(QFileDialog):
    """
    Represents a file dialog with additional features.

    Args:
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the file dialog.
    - mode: Optional. The mode of the file dialog.
    """

    def __init__(self, parent=None, style: Style = None, mode: QFileDialog.AcceptMode = QFileDialog.AcceptMode.AcceptOpen):
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

    def __init__(self, child: QWidget | None = None, parent=None, style: Style = None):
        super().__init__(parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        if child:
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

    def __init__(self, content: QWidget, parent=None):
        super().__init__(parent=parent)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # Set the content widget for the scroll area
        self.scroll_area.setWidget(content)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)
        self.set_id("scroll-container")
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


class GroupBox(QGroupBox, BasicElement, Padded):
    """
    Represents a group box with additional features.

    Args:
    - title: The title of the group box.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the group box.
    """

    def __init__(self, content: BaseContainer, title: str, parent=None, style: Style = None):
        super().__init__(title, parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        self.setLayout(content.layout())

    def layout_padding(self, p0_: int) -> Self:
        self.layout().setContentsMargins(p0_, p0_, p0_, p0_)
        return self

    def content_gap(self, p0_: int) -> Self:
        self.layout().setSpacing(p0_)
        return self


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

    def __init__(self, rows: int = 0, columns: int = 0, parent=None, style: Style = None) -> None:
        super().__init__(rows, columns, parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        self.itemClicked.connect(self.handle_cell_click)
        self.clicked_function = None

    def add_row(self, data: List[str]) -> Self:
        """
        Adds a new row with the specified data to the table.

        Args:
        - data: A list of strings representing the data for the new row.

        Returns:
        - itself: Returns itself after adding the new row.
        """
        row_position = self.rowCount()
        self.insertRow(row_position)

        for col, value in enumerate(data):
            item = QTableWidgetItem(value)
            self.setItem(row_position, col, item)
        return self

    def add_column(self, header_text: str, data: List[str]) -> Self:
        """
        Adds a new column with the specified header text and data to the table.

        Args:
        - header_text: The header text for the new column.
        - data: A list of strings representing the data for the new column.

        Returns:
        - itself: Returns itself after adding the new column.
        """
        col_position = self.columnCount()
        self.insertColumn(col_position)
        self.setHorizontalHeaderItem(
            col_position, QTableWidgetItem(header_text))

        for row, value in enumerate(data):
            item = QTableWidgetItem(value)
            self.setItem(row, col_position, item)
        return self

    def set_cell_data(self, row: int, col: int, data: str) -> Self:
        """
        Sets the data for a specific cell in the table.

        Args:
        - row: The row index of the cell.
        - col: The column index of the cell.
        - data: The data to set in the cell.

        Returns:
        - itself: Returns itself after setting the cell data.
        """
        item = QTableWidgetItem(data)
        self.setItem(row, col, item)
        return self

    def add_button(self, row: int, col: int, text: str, on_click: Callable[[], None]) -> Self:
        """
        Adds a button to a specific cell in the table.

        Args:
        - row: The row index of the cell.
        - col: The column index of the cell.
        - text: The text to display on the button.
        - on_click: The function to be called when the button is clicked.

        Returns:
        - itself: Returns itself after adding the button.
        """
        button = Button(text)
        button.clicked.connect(on_click)
        self.setCellWidget(row, col, button)
        return self

    def add_checkbox(self, row: int, col: int, text: str, on_state_changed: Callable[[bool], None]) -> Self:
        """
        Adds a checkbox to a specific cell in the table.

        Args:
        - row: The row index of the cell.
        - col: The column index of the cell.
        - text: The text to display next to the checkbox.
        - on_state_changed: The function to be called when the checkbox state changes.

        Returns:
        - itself: Returns itself after adding the checkbox.
        """
        checkbox = CheckBox(text)
        checkbox.stateChanged.connect(
            lambda state: on_state_changed(state == Qt.CheckState.Checked))
        self.setCellWidget(row, col, checkbox)
        return self

    def add_combobox(self, row: int, col: int, items: List[str], on_current_index_changed: Callable[[int], None]) -> Self:
        """
        Adds a combobox to a specific cell in the table.

        Args:
        - row: The row index of the cell.
        - col: The column index of the cell.
        - items: A list of strings representing the items in the combobox.
        - on_current_index_changed: The function to be called when the combobox index changes.

        Returns:
        - itself: Returns itself after adding the combobox.
        """
        combobox = ComboBox()
        combobox.add(items)
        combobox.currentIndexChanged.connect(on_current_index_changed)
        self.setCellWidget(row, col, combobox)
        return self

    def handle_cell_click(self, item: QTableWidgetItem) -> Self:
        """
        Handles the click event on a cell and executes corresponding actions.

        Args:
        - item: The QTableWidgetItem representing the clicked cell.

        Returns:
        - itself: Returns itself after handling the cell click.
        """
        row = item.row()
        col = item.column()

        cell_widget = self.cellWidget(row, col)
        if isinstance(cell_widget, Button):
            cell_widget.clicked.emit()
        elif isinstance(cell_widget, CheckBox):
            cell_widget.toggle()
        elif isinstance(cell_widget, ComboBox):
            combobox = cell_widget
            combobox.showPopup()

        if self.clicked_function is not None:
            self.clicked_function(row, col)
        return self

    def set_clicked_function(self, func: Callable[[int, int], None]) -> Self:
        """
        Sets a function to be called when a cell is clicked.

        Args:
        - func: The function to be called with the row and column indices when a cell is clicked.

        Returns:
        - itself: Returns itself after setting the clicked function.
        """
        self.clicked_function = func
        return self


class LoginForm(Vertical):
    """
    Represents a login form with predefined structure.

    Args:
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the login form.
    """

    def __init__(self, parent=None, style: Style = None):
        super().__init__(parent=parent, style=style)
        self.username = Field("Username")
        self.password = Field("Password")

        self.add(
            Label("Login").set_id("login-header").set_style(Style().add(
                "Label#login-header", "font-size:24px;font-weight:bold")),
            self.username,
            self.password,
            Button("Login").set_id("login-button"),
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
    def __init__(self, denom: str, importFromFile: bool, suggestions: List[str], identificator: str, parent=None, style: Style = None):
        super().__init__(parent=parent, style=style)
        self.textField = MultilineField()
        self.suggestions = ComboBox(
            *suggestions).change_listener(self.combobox_listener_call)
        self.set_name("MultilineAssistedField")
        self.set_id(identificator)
        self.add(
            Vertical(
                Label(denom, style=TextStyles.Body),
                self.textField,
                Horizontal(
                    GroupBox(
                        Vertical(
                            Button("Import").action(self.load),
                            Button("Export").action(self.export),
                        ).gap(0), "File options"
                    ).gap(0).layout_padding(5) if importFromFile else None,
                    GroupBox(
                        Vertical(
                            self.suggestions,
                            Button("Add").action(self.combobox_listener_call)
                        ).layout_padding(0).padding(0).content_gap(0), "Suggestions"
                    ).gap(0).layout_padding(5) if suggestions else None,
                ).gap(0)
            ).gap(0),
            Spacer()
        ).gap(0)

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


class ListWidget(QListWidget,BasicElement,Linked,Padded):
    def __init__(self, *items:str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.addItems(items)
    def add(self,*items:str|QListWidgetItem) -> Self:
        if items and isinstance(items[0],QListWidgetItem):
            for item in items:
                self.addItem(item)
        else:
            self.addItems(items)
        return self
    def change(self, *items:str) -> Self:
        self.clear()
        self.addItems(items)
        return self
    def change_at(self, index:int, item:str) -> Self:
        self.takeItem(index)
        self.insertItem(index, item)
        return self
    def pop(self,index:int) -> str:
        return self.takeItem(index).text()
    def remove(self,index:int) -> Self:
        self.takeItem(index)
        return self


class ProxyMultiLineInput(Vertical):
    def __init__(self, parent=None, style: Style = None):
        super().__init__(parent=parent, style=style)
        self.list = ListWidget()
        self.add(
            Label("Proxy list").set_style(TextStyles.Heading),
            self.list,
            Horizontal(
                Spacer(),
                Button("+").padding(0),
                Button("-").padding(0)
            ).gap(0)
        ).content_gap(0)