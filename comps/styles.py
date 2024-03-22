from enum import Enum
from typing import Any, Dict, Self


class PropertyOwner:
    properties: Dict[str, Any]


class Displayable(PropertyOwner):
    def display(self, display: "Style.DisplayPolicy") -> Self:
        self.properties["display"] = display.value
        return self


class Outlined(PropertyOwner):
    def outline(self, outline: str) -> Self:
        self.properties["outline"] = outline
        return self


class AlignableStyle(PropertyOwner):
    def alignment(self, alignment: "Style.TextAlignmentPolicy") -> Self:
        self.properties["qproperty-alignment"] = alignment.value
        return self


class FontEditable(PropertyOwner):
    def fontSize(self, size: str) -> Self:
        self.properties["font-size"] = size
        return self

    def fontFamily(self, family: str) -> Self:
        self.properties["font-family"] = family
        return self

    def fontWeight(self, style: "Style.FontWeightPolicy") -> Self:
        self.properties["font-weight"] = style.value
        return self


class FontColorizable(PropertyOwner):
    def textColor(self, color: str) -> Self:
        self.properties["color"] = color
        return self


class Bordered(PropertyOwner):
    def border(self, border: str) -> Self:
        self.properties["border"] = border
        return self

    def borderRadius(self, radius: str) -> Self:
        self.properties["border-radius"] = radius
        return self


class PaddedStyle(PropertyOwner):
    def padding(self, padding: str) -> Self:
        self.properties["padding"] = padding
        return self


class Margined(PropertyOwner):
    def margin(self, margin: str) -> Self:
        self.properties["margin"] = margin
        return self


class TextEditable(PropertyOwner):
    def textShadow(self, shadow: str) -> Self:
        self.properties["text-shadow"] = shadow
        return self

    def wordWrap(self, wrap: "Style.WordWrapPolicy") -> Self:
        self.properties["word-wrap"] = wrap.value
        return self

    def letterSpacing(self, spacing: str) -> Self:
        self.properties["letter-spacing"] = spacing
        return self

    def wordSpacing(self, spacing: str) -> Self:
        self.properties["word-spacing"] = spacing
        return self

    def textDecoration(self, decoration: str) -> Self:
        self.properties["text-decoration"] = decoration
        return self

    def textAlignment(self, alignment: "Style.TextAlignmentPolicy") -> Self:
        self.properties["text-align"] = alignment.value
        return self


class OpacityEditable(PropertyOwner):
    def opacity(self, opacity: str) -> Self:
        self.properties["opacity"] = opacity
        return self


class CursorEditable(PropertyOwner):
    def cursor(self, cursor: "Style.CursorStylePolicy") -> Self:
        self.properties["cursor"] = cursor.value
        return self


class BackgroundChangeable(PropertyOwner):
    def backgroundColor(self, color: str):
        self.properties["background"] = color
        return self


class QSS:
    def __init__(self) -> None:
        self._styles = {}

    def set(self, identifier: str, style: "Style") -> Self:
        self._styles[identifier] = style.to_str()
        return self

    def remove(self, identifier: str) -> Self:
        self._styles.pop(identifier)
        return self

    def to_str(self) -> str:
        return "; ".join([f"{identifier} {{ {style} }}" for identifier, style in self._styles.items()])


class Style(AlignableStyle, Bordered, PaddedStyle, Margined, OpacityEditable, CursorEditable, BackgroundChangeable, FontEditable, FontColorizable, TextEditable, Displayable, Outlined):

    class FontWeightPolicy(Enum):
        Normal = "normal"
        Italic = "italic"
        Bold = "bold"
        BoldItalic = "bold italic"
        Underline = "underline"
        Overline = "overline"
        StrikeOut = "strikeout"

    class TextAlignmentPolicy(Enum):
        Left = "AlignLeft"
        Right = "AlignRight"
        Center = "AlignCenter"
        Justify = "AlignJustify"
        Top = "AlignTop"
        Bottom = "AlignBottom"
        TopLeft = "AlignVCenter"
        TopRight = "AlignHCenter"
        BottomLeft = "AlignBaseline"

    class CursorStylePolicy(Enum):
        ArrowCursor = 'arrow'
        UpArrowCursor = 'uparrow'
        CrossCursor = 'cross'
        WaitCursor = 'wait'
        IBeamCursor = 'ibeam'
        SizeVerCursor = 'sizever'
        SizeHorCursor = 'sizehor'
        SizeBDiagCursor = 'sizebdiag'
        SizeFDiagCursor = 'sizefdiag'
        SizeAllCursor = 'sizeall'
        BlankCursor = 'blank'
        SplitVCursor = 'splitv'
        SplitHCursor = 'splith'
        PointingHandCursor = 'pointinghand'
        ForbiddenCursor = 'forbidden'
        OpenHandCursor = 'openhand'
        ClosedHandCursor = 'closedhand'
        WhatsThisCursor = 'whatsthis'
        BusyCursor = 'busy'
        DragMoveCursor = 'dragmove'
        DragCopyCursor = 'dragcopy'
        DragLinkCursor = 'draglink'
        BitmapCursor = 'bitmap'

    class DisplayPolicy(Enum):
        None_ = "none"
        Inline = "inline"
        Block = "block"
        InlineBlock = "inline-block"
        Flex = "flex"
        InlineFlex = "inline-flex"
        Grid = "grid"
        InlineGrid = "inline-grid"
        Table = "table"
        TableRow = "table-row"
        TableCell = "table-cell"
        TableColumn = "table-column"
        TableRowGroup = "table-row-group"
        TableColumnGroup = "table-column-group"
        TableCaption = "table-caption"
        Hidden = "hidden"
        InlineHidden = "inline-hidden"
        Visible = "visible"
        InlineVisible = "inline-visible"
        Inherit = "inherit"
        Initial = "initial"
        Unset = "unset"
        Revert = "revert"
        RevertLayer = "revert-layer"
        RevertInline = "revert-inline"
        RevertGroup = "revert-group"
        RevertItem = "revert-item"

    class WordWrapPolicy(Enum):
        Enabled = "true"
        Disabled = "false"

    def __init__(self, properties: Dict[str, str] | None = None) -> None:
        if properties is not None:
            self.properties = properties
        else:
            self.properties = {}

    def add(self, qssIdentifier: str, value: str):
        self.properties[qssIdentifier] = value
        return self

    def to_str(self):
        content = "\n".join(
            [f"{k}:{v};" for k, v in self.properties.items()])
        return content

    def merge(self, other: "Style") -> "Style":
        copy = self.properties.copy()
        copy.update(other.properties)
        return Style(copy)

    def update(self, other: "Style") -> "Style":
        self.properties.update(other.properties)
        return self


class TextStyles:
    Title = Style().fontSize("40px")\
        .fontWeight(Style.FontWeightPolicy.Bold)
    SubTitle = Style().fontSize("28px")\
        .fontWeight(Style.FontWeightPolicy.Bold)
    TopHeading = Style().fontSize("28px")
    Heading = Style().fontSize("24px")
    SmallHeading = Style().fontSize("20px")
    RedHeading = Style().fontSize("20px").textColor("#e74c3c")
    Body = Style().fontSize("16px")
    Caption = Style().fontSize("14px")
    EndOfPage = StartOfPage = Style().fontSize("13px")
    Label = Style().fontSize("16px").fontWeight(Style.FontWeightPolicy.Bold)
    DarkenedLabel = Style().fontSize("16px").fontWeight(
        Style.FontWeightPolicy.Bold).opacity("0.5")


class PaddingStyles:
    NoPadding = Style().padding("0px")
    Small = Style().padding("5px")
    Medium = Style().padding("10px")
    Large = Style().padding("15px")
    ExtraLarge = Style().padding("20px")


class MarginStyles:
    NoMargin = Style().margin("0px")
    Small = Style().margin("5px")
    Medium = Style().margin("10px")
    Large = Style().margin("15px")
    ExtraLarge = Style().margin("20px")


class OpacityStyles:
    NoOpacity = Style().opacity("0")
    LowOpacity = Style().opacity("0.5")
    MediumOpacity = Style().opacity("0.75")
    HighOpacity = Style().opacity("0.9")
    FullOpacity = Style().opacity("1.0")


class BorderRadiusStyles:
    NoBorderRadius = Style().borderRadius("0px")
    Small = Style().borderRadius("5px")
    Medium = Style().borderRadius("10px")
    Large = Style().borderRadius("15px")
    ExtraLarge = Style().borderRadius("20px")
    Circle = Style().borderRadius("50%")


class TabWidgetStyles:
    clearTab = Style().backgroundColor("transparent").border("0")


class ButtonStyles:
    Primary = QSS().set("Button", Style({
        "background-color": "#4CAF50",
        "border": "none",
        "color": "white",
        "padding": "10px 24px",
        "text-align": "center",
        "text-decoration": "none",
        "font-size": "16px",
        "margin": "2px",
        "border-radius": "10px",
    })).set("Button:hover", Style({
        "background-color": "#45a049",
    })).set("Button:focus",
        Style({
            "border": "2px solid #4CAF50",
            "outline": "none",
        }))
    Secondary = QSS().set("Button", Style({
        "background-color": "#337ab7",
        "border": "none",
        "color": "white",
        "padding": "10px 24px",
        "text-align": "center",
        "text-decoration": "none",
        "font-size": "16px",
        "margin": "2px",
        "border-radius": "10px",
    })).set("Button:hover", Style({
        "background-color": "#286090",
    })).set("Button:focus", Style({
        "border": "2px solid #337ab7",
        "outline": "none",
    }))

    Tertiary = QSS().set("Button", Style({
        "background-color": "#f0ad4e",
        "color": "white",
        "padding": "10px 24px",
        "text-align": "center",
        "text-decoration": "none",
        "font-size": "16px",
        "margin": "2px",
        "border-radius": "10px",
    })).set("Button:hover", Style({
        "background-color": "#ec971f",
    })).set("Button:focus", Style({
        "border": "2px solid #f0ad4e",
        "outline": "none",
    }))

    NavPrimary = QSS().set("Button", Style({
        "margin":"2px",
        "padding":"5px",
        "border-radius":"2px",
        "font-size":"16px",
        "color":"white",
        "background-color":"gray",
        "border":"1px solid gray",
    }))


button_style = '''
QPushButton {
    background-color: #4CAF50; /* Green */
    border: none,
    color: white,
    padding: 10px 24px,
    text-align: center,
    text-decoration: none,
    display: inline-block,
    font-size: 16px,
    margin: 4px 2px,
    cursor: pointer,
    border-radius: 10px,
}

/* Hover effect */
QPushButton:hover {
    background-color: #45a049; /* Darker Green */
}

/* Focus effect */
QPushButton:focus {
    border: 2px solid #4CAF50; /* Green */
    outline: none,
}
'''
