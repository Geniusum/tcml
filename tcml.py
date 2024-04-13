import xml.etree.ElementTree as ET
import tkinter as tk
import os

class TCML():
    def __init__(self) -> None:
        self.variables = {}
        self.styles = []
        self.window_properties = {
            "title": "",
            "icon": None,
            "width": 840,
            "height": 680
        }
        self.properties = {
            "background",
            "foreground",
            "font",
            "font-size",
            "bold",
            "margin-x",
            "margin-y",
            "x",
            "y",
            "width",
            "height"
        }
        self.start_tag = "tcml"
        self.measures = {
            "px": self._px,
            "%": self._percent,
        }
        self.primary_tags = {
            "info",
            "style",
            "data",
            "page"
        }
        self.info_tags = {
            "title",
            "icon",
            "width",
            "height"
        }
        self.style_tags = {
            "set"
        }
        self.data_tags = {
            "var"
        }

    def set_to_dict(self, subjet:set):
        d = {}
        for item in subjet:
            d[item] = item
        return d

    def _px(self): ...
    
    def _percent(self): ...

    def valueTextOrNone(self, dictionnary:dict, key:str, value:any):
        if value != None:
            text = str(value.text)
            if len(text) >= 3 and text[:3].lower() == "#py":
                text = eval(text[3:].strip())
            try:
                text = float(text)
            except:
                pass
            try:
                text = int(text)
            except:
                pass
            dictionnary[key] = text

    def getValueTextOrNone(self, value:any):
        if value != None:
            text = str(value)
            if len(text) >= 3 and text[:3].lower() == "#py":
                text = eval(text[3:].strip())
            try:
                text = float(text)
            except:
                pass
            try:
                text = int(text)
            except:
                pass
            return text
        return None

    def parse(self, code:str):
        tcml_tag = ET.fromstring(code)
        info_tag = tcml_tag.find("info")
        style_tag = tcml_tag.find("style")
        data_tag = tcml_tag.find("data")
        page_tag = tcml_tag.find("page")

        if info_tag:
            title = info_tag.find("title")
            width = info_tag.find("width")
            height = info_tag.find("height")
            icon = info_tag.find("icon")

            self.valueTextOrNone(self.window_properties, "title", title)
            self.valueTextOrNone(self.window_properties, "width", width)
            self.valueTextOrNone(self.window_properties, "height", height)
            self.valueTextOrNone(self.window_properties, "icon", icon)
        
        if style_tag:
            set_tags = style_tag.findall("set")
            for set_tag in set_tags:
                r = {}
                for attrib, value in set_tag.attrib.items():
                    if attrib.lower() in self.properties or attrib.lower() in ["tag", "id"]:
                        r[attrib] = self.getValueTextOrNone(value)
                self.styles.append(r)

        if data_tag:
            var_tags = data_tag.findall("var")

    def init_window(self):
        self.window = tk.Tk()

    def init_canvas(self):
        self.canvas = tk.Canvas(self.window, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
    def update_window_properties(self):
        title = self.window_properties["title"]
        width = self.window_properties["width"]
        height = self.window_properties["height"]
        scr_width = self.window.winfo_screenwidth()
        scr_height = self.window.winfo_screenheight()
        icon = self.window_properties["icon"]
        self.window.title(title)
        self.window.geometry(f"{width}x{height}+{int(scr_width / 2 - width / 2)}+{int(scr_height / 2 - height / 2)}")
        if icon and os.path.exists(icon):
            self.window.iconbitmap(icon)

        self.window.update()
    
    def mainloop(self):
        self.window.mainloop()

    def show(self, code:str):
        self.init_window()
        self.init_canvas()
        self.parse(code)
        self.update_window_properties()
        self.mainloop()

code = open("one.xml").read()

TCML().show(code)