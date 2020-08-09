import random
import string
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO

def get_validCode_img(request):

    def get_random_color():
        return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    img = Image.new("RGB",(270,40),color=get_random_color())
    draw = ImageDraw.Draw(img)
    kumo_font = ImageFont.truetype("static/font/kumo.ttf", size=32)
    str1 = "".join(random.sample(string.ascii_letters+string.digits,4))
    for index,i in enumerate(str1,1):
        draw.text((index*50,5),i,get_random_color(),font=kumo_font)

    f=BytesIO()
    img.save(f,"png")
    data = f.getvalue()
    return data

