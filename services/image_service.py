from textwrap import wrap
from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image

from shared.database_service import get_font_configurations
from models.quote_model import Quote

import random
import os

FACEBOOK_IMAGE_IDEAL_SIZE = 800
FONT_FAMILIES = ['Pacifico', 'Source Code Pro', 'Dancing Script', 'Courgette']
COLORS = ['white']#['orange', 'white', 'blue', 'green' ]

def draw_rectangle(contxt, roi_width, roi_height, top, left, color):
    contxt.push()
    contxt.fill_color = Color('rgba(153, 153, 153, 0.5)')
    contxt.rectangle(left=left, top=top, width=roi_width, height=roi_height)
    contxt.pop()


def word_wrap(image, ctx, text, roi_width, roi_height):
    """Break long text to multiple lines, and reduce point size
    until all text fits within a bounding box."""
    mutable_message = text
    iteration_attempts = 100

    def eval_metrics(txt):
        """Quick helper function to calculate width/height of text."""
        metrics = ctx.get_font_metrics(image, txt, True)
        return (metrics.text_width, metrics.text_height)

    def shrink_text():
        """Reduce point-size & restore original text"""
        ctx.font_size = ctx.font_size - 0.75
        return text

    while ctx.font_size > 0 and iteration_attempts:
        iteration_attempts -= 1
        width, height = eval_metrics(mutable_message)
        if height > roi_height:
            mutable_message = shrink_text()
        elif width > roi_width:
            columns = len(mutable_message)
            while columns > 0:
                columns -= 1
                mutable_message = '\n'.join(wrap(mutable_message, columns))
                wrapped_width, _ = eval_metrics(mutable_message)
                if wrapped_width <= roi_width:
                    break
            if columns < 1:
                mutable_message = shrink_text()
        else:
            break
    if iteration_attempts < 1:
        raise RuntimeError("Unable to calculate word_wrap for " + text)
    return mutable_message

def write_text(quote, x):
    #font_config = random.choice(get_font_configurations())
    font_config = get_font_configurations()[2]
    with Image(filename='new-picture.png') as img:
        with Drawing() as draw:
            color = Color(random.choice(COLORS))
            text_margin_top = 0
            text_width = int(FACEBOOK_IMAGE_IDEAL_SIZE / 1.25)
            text_heigth = int(FACEBOOK_IMAGE_IDEAL_SIZE / 1.15)

            draw_rectangle(draw, FACEBOOK_IMAGE_IDEAL_SIZE, FACEBOOK_IMAGE_IDEAL_SIZE, 0, 0, color)
            draw.fill_color = color
            draw.font = font_config['fontName']
            draw.font_size = font_config['fontSizeLarge']
            draw.font_style = font_config['fontStyle']
            draw.gravity = 'center'

            text = quote.text.upper() if font_config['isUpper'] else quote.text

            aligned_text = word_wrap(img, draw, text, text_width, text_heigth)
            draw.text(0, text_margin_top, aligned_text)

            mtrcs = draw.get_font_metrics(img, aligned_text, True)

            y_position_author = int(15 + (mtrcs.text_height / 2)) #+ text_margin_top)
            draw.gravity = 'center'
            draw.font_size = font_config['fontSizeSmall']
            #draw.text(0, y_position_author, quote.author + "(" + font_config['fontName'] + ")")
            draw.text(0, y_position_author, quote.author)

            draw.draw(img)
            # img.save(filename='new-picture-' + str(x) + '.png')
            img.save(filename='new-picture.png')

def crop_image():
    with Image(filename='base-picture.png') as img:
        img.transform(resize='800x800^')
        img.crop(width=FACEBOOK_IMAGE_IDEAL_SIZE, height=FACEBOOK_IMAGE_IDEAL_SIZE, gravity='center')
        img.save(filename='new-picture.png')

def print_text_on_image_and_save(quote, x):
    crop_image()
    write_text(quote, x)
