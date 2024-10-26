from PIL import ImageColor

def getcolor(hexcode):
    return ImageColor.getcolor(hexcode, "RGB")

class Colors:
   # def __init__(self):
        # Các màu sắc được chuyển đổi từ mã hex sang RGB
        BLACK = getcolor("#000000")
        YELLOW = getcolor("#FFFF00")
        BUTTON_COLOR = getcolor("#6464FF")
        BUTTON_HOVER_COLOR = getcolor("#9696FF")
        PURPLE = getcolor("#800080")
        DARK_BLUE = getcolor("#003366")
        WHITE = getcolor("#FFFFFF")
        PINK = getcolor("#FFC0CB")
        # Thêm bất kỳ màu sắc nào khác bạn cần
