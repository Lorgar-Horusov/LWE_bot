from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

class AchievementGenerator:
    def __init__(self, width=1000, height=130, bg_color=(30, 30, 30)):
        self.width = width
        self.height = height
        self.bg_color = bg_color

        try:
            self.font_title = ImageFont.truetype("PressStart2P-Regular.ttf", 25)
            self.font_desc = ImageFont.truetype("PressStart2P-Regular.ttf", 12)
        except:
            self.font_title = ImageFont.load_default()
            self.font_desc = ImageFont.load_default()

    def generate(self, title, description):
        img = Image.new("RGBA", (self.width, self.height), self.bg_color)
        draw = ImageDraw.Draw(img)
        border_color = (255, 165, 0)
        draw.rounded_rectangle([(5, 5), (self.width - 5, self.height - 5)], outline=border_color, width=3, radius=15)
        draw.text(((self.width - self.font_title.getlength(title)) // 2, 30), title, font=self.font_title, fill=(255, 140, 0))
        draw.text(((self.width - self.font_desc.getlength(description)) // 2, 80), description, font=self.font_desc, fill=(255, 255, 255))
        img_bytes = BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        return img_bytes
