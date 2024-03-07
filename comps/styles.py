from enum import Enum
from typing import Dict, Self

class Alignable:
    def alignment(self, alignment: "Style.TextAlignmentPolicy") -> Self:
        self.properties["qproperty-alignment"] = alignment.value
        return self
class FontEditable:
    def fontSize(self, size: str) -> Self:
        self.properties["font-size"] = size
        return self

    def fontFamily(self, family: str) -> Self:
        self.properties["font-family"] = family
        return self

    def fontWeight(self, style: "Style.FontWeightPolicy") -> Self:
        self.properties["font-weight"] = style.value
        return self
class FontColorizable:
    def textColor(self, color: str) -> Self:
        self.properties["color"] = color
        return self
class Bordered:
    def border(self, border: str) -> Self:
        self.properties["border"] = border
        return self
    def borderRadius(self, radius: str) -> Self:
        self.properties["border-radius"] = radius
        return self
class Padded:
    def padding(self, padding: str) -> Self:
        self.properties["padding"] = padding
        return self
class Margined:
    def margin(self, margin: str) -> Self:
        self.properties["margin"] = margin
        return self
class TextEditable:
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
class OpacityEditable:
    def opacity(self, opacity: str) -> Self:
        self.properties["opacity"] = opacity
        return self
class CursorEditable:
    def cursor(self, cursor: "Style.CursorStylePolicy") -> Self:
        self.properties["cursor"] = cursor.value
        return self
class BackgroundChangeable:
    def backgroundColor(self, color: str):
        self.properties["background"] = color
        return self

class QSS:
    def __init__(self) -> None:
        self._styles = {}
    def set(self, identifier:str, style: "Style") -> Self:
        self._styles[identifier] = style.to_str()
        return self
    def remove(self, identifier:str) -> Self:
        self._styles.pop(identifier)
        return self
    def to_str(self) -> str:
        return "; ".join([f"{identifier} {{ {style} }}" for identifier, style in self._styles.items()])

class Style(Alignable, Bordered, Padded, Margined, OpacityEditable, CursorEditable, BackgroundChangeable, FontEditable, FontColorizable, TextEditable):

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

    class WordWrapPolicy(Enum):
        Enabled = "true"
        Disabled = "false"

    def __init__(self,properties:Dict[str,str]=None) -> None:
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
    DarkenedLabel = Style().fontSize("16px").fontWeight(Style.FontWeightPolicy.Bold).opacity("0.5")
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
    PrimaryButton = Style().backgroundColor("indigo").textColor("white").border("2px solid indigo").padding("8px 16px").borderRadius("4px")
    SecondaryButton = Style().backgroundColor("orange").textColor("white").border("2px solid orange").padding("8px 16px").borderRadius("4px")
    ThirdButton = Style().backgroundColor("#4285F4").textColor("white").border("2px solid #4285F4").padding("8px 16px").borderRadius("4px").merge(BorderRadiusStyles.Circle)