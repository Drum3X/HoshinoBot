class BaseColor():
    _CSI = "\033["
    _OSC = "\033]"
    _BEL = "\a"
    
    def __init__(self, colors):
        for color in colors:
            setattr(self, color, self.code_to_chars(colors[color]))           

    def code_to_chars(self, code):
        return self._CSI + str(code) + "m"

    def set_title(self, title):
        return self._OSC + "2;" + title + self._BEL

    def clear_screen(self, mode = 2):
        print(self._CSI + str(mode) + "J")

    def clear_line(self, mode = 2):
        print(self._CSI + str(mode) + "K")
        
class Color(BaseColor):
    black = None
    red = None
    green = None
    yellow = None
    blue = None
    magenta = None
    cyan = None
    white = None
    reset = None
    light_black = None
    light_red = None
    light_green = None
    light_yellow = None
    light_blue = None
    light_magenta = None
    light_cyan = None
    light_white = None
      
    color_codes = {
        "black": 30,
        "red": 31,
        "green": 32,
        "yellow": 33,
        "blue": 34,
        "magenta": 35,
        "cyan": 36,
        "white": 37,
        "reset": 39,
        "light_black": 90,
        "light_red": 91,
        "light_green": 92,
        "light_yellow": 93,
        "light_blue": 94,
        "light_magenta": 95,
        "light_cyan": 96,
        "light_white": 97  
    }
    
    def __init__(self):
        super().__init__(self.color_codes)

class BackColor(BaseColor):
    black = None
    red = None
    green = None
    yellow = None
    blue = None
    magenta = None
    cyan = None
    white = None
    reset = None
    light_black = None
    light_red = None
    light_green = None
    light_yellow = None
    light_blue = None
    light_magenta = None
    light_cyan = None
    light_white = None
    
    backcolor_codes = {
        "black": 40,
        "red": 41,
        "green": 42,
        "yellow": 43,
        "blue": 44,
        "magenta": 45,
        "cyan": 46,
        "white": 47,
        "reset": 49,
        "light_black": 100,
        "light_red": 101,
        "light_green": 102,
        "light_yellow": 103,
        "light_blue": 104,
        "light_magenta": 105,
        "light_cyan": 106,
        "light_white": 107,
    }
    
    def __init__(self):
        super().__init__(self.backcolor_codes)   

class Style(BaseColor):
    bright = None
    dim = None
    normal = None
    reset = None
    
    style_codes = {
        "bright": 1,
        "dim": 2,
        "normal": 22,
        "reset": 0
    }
    
    def __init__(self):
        super().__init__(self.style_codes)   

color = Color()    
bgcolor = BackColor()  
style = Style()                  