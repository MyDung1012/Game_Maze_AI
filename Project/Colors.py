from PIL import ImageColor

def getcolor(hexcode):
    """Chuyển đổi mã hex thành màu RGB."""
    return ImageColor.getcolor(hexcode, "RGB")

class Colors:
    # Các màu sắc được chuyển đổi từ mã hex sang RGB
    BLACK = getcolor("#000000")
    YELLOW = getcolor("#FFFF00")
    YELLOW_BLACK = getcolor("#CCA300")
    BUTTON_COLOR = getcolor("#6464FF")
    BUTTON_HOVER_COLOR = getcolor("#9696FF")
    PURPLE = getcolor("#800080")
    DARK_BLUE = getcolor("#003366")
    WHITE = getcolor("#FFFFFF")
    PINK = getcolor("#FFC0CB")
    RED = getcolor("#FF0000")
    GREEN = getcolor("#00FF00")
    GREY = getcolor("#808080")
    PURPLE_2 = getcolor("#BA55D3")
    LIGHT_YELLOW = getcolor("#FFFA96")

