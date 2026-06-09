from PIL import Image

import customtkinter as ctk


class UiAssets:
    """Loads reusable pixel-art images for the CustomTkinter companion windows."""

    def __init__(self):
        self.titleLogo = self.loadImage("./img/title_screen.png", (2, 60, 176, 88), (220, 110), (255, 0, 220))
        self.mario = self.loadImage("./img/characters.gif", (276, 44, 292, 60), (64, 64))
        self.mushroom = self.loadImage("./img/Items.png", (0, 16, 16, 32), (48, 48))
        self.coin = self.loadImage("./img/Items.png", (0, 112, 16, 128), (42, 42))
        self.shopBackdrop = self.loadFullImage("./img/shop_pixel_backdrop.png", (960, 680))
        self.itemIcons = {
            "Mushroom": self.createPixelIcon("mushroom"),
            "Star Shield": self.createPixelIcon("shield"),
            "Super Jump": self.createPixelIcon("jump"),
            "Enemy Cleaner": self.createPixelIcon("cleaner"),
            "Checkpoint": self.createPixelIcon("checkpoint"),
        }

    def loadImage(self, path, cropArea, size, transparentColor=None):
        image = Image.open(path).convert("RGBA")
        image = image.crop(cropArea)

        if transparentColor is not None:
            pixels = []

            for red, green, blue, alpha in image.getdata():
                if (red, green, blue) == transparentColor:
                    pixels.append((red, green, blue, 0))
                else:
                    pixels.append((red, green, blue, alpha))

            image.putdata(pixels)

        image = image.resize(size, Image.Resampling.NEAREST)
        return ctk.CTkImage(light_image=image, dark_image=image, size=size)

    def loadFullImage(self, path, size):
        image = Image.open(path).convert("RGBA")
        image = image.resize(size, Image.Resampling.NEAREST)
        return ctk.CTkImage(light_image=image, dark_image=image, size=size)

    def createPixelIcon(self, iconType, size=(56, 56)):
        image = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        pixels = image.load()

        palettes = {
            "mushroom": {
                "dark": (91, 33, 24, 255),
                "main": (229, 37, 33, 255),
                "light": (255, 241, 216, 255),
            },
            "shield": {
                "dark": (30, 64, 175, 255),
                "main": (37, 99, 235, 255),
                "light": (250, 204, 21, 255),
            },
            "jump": {
                "dark": (21, 128, 61, 255),
                "main": (34, 197, 94, 255),
                "light": (254, 240, 138, 255),
            },
            "cleaner": {
                "dark": (107, 33, 168, 255),
                "main": (147, 51, 234, 255),
                "light": (216, 180, 254, 255),
            },
            "checkpoint": {
                "dark": (22, 101, 52, 255),
                "main": (34, 197, 94, 255),
                "light": (255, 255, 255, 255),
            },
        }
        color = palettes[iconType]

        def rect(x1, y1, x2, y2, fill):
            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1):
                    pixels[x, y] = fill

        if iconType == "mushroom":
            rect(4, 2, 11, 3, color["dark"])
            rect(2, 4, 13, 8, color["main"])
            rect(4, 4, 6, 6, color["light"])
            rect(10, 4, 11, 6, color["light"])
            rect(5, 9, 10, 13, color["light"])
            rect(5, 11, 6, 12, color["dark"])
            rect(9, 11, 10, 12, color["dark"])
        elif iconType == "shield":
            rect(3, 2, 12, 4, color["dark"])
            rect(3, 5, 12, 9, color["main"])
            rect(5, 10, 10, 12, color["main"])
            rect(7, 13, 8, 14, color["dark"])
            rect(7, 4, 8, 10, color["light"])
            rect(5, 6, 10, 7, color["light"])
        elif iconType == "jump":
            rect(6, 2, 9, 10, color["main"])
            rect(3, 5, 12, 8, color["main"])
            rect(5, 3, 10, 9, color["main"])
            rect(7, 2, 8, 7, color["light"])
            rect(4, 11, 11, 13, color["dark"])
            rect(6, 9, 9, 12, color["main"])
        elif iconType == "cleaner":
            rect(6, 2, 9, 8, color["light"])
            rect(5, 7, 10, 10, color["main"])
            rect(3, 10, 12, 13, color["dark"])
            rect(2, 12, 13, 14, color["main"])
            rect(4, 11, 5, 12, color["light"])
            rect(8, 11, 9, 12, color["light"])
        elif iconType == "checkpoint":
            rect(3, 2, 12, 4, color["main"])
            rect(2, 4, 13, 6, color["dark"])
            rect(4, 6, 11, 14, color["main"])
            rect(7, 7, 8, 13, color["light"])

        image = image.resize(size, Image.Resampling.NEAREST)
        return ctk.CTkImage(light_image=image, dark_image=image, size=size)
