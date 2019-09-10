from textwrap import wrap
from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image

from shared.database_service import get_font_configurations
from models.quote_model import Quote

import random

FACEBOOK_IMAGE_IDEAL_SIZE = 800


def draw_rectangle(context, roi_width, roi_height, top, left):
    print("Drawing Background...")
    context.push()
    context.fill_color = Color('rgba(153, 153, 153, 0.5)')
    context.rectangle(left=left, top=top, width=roi_width, height=roi_height)
    context.pop()


def word_wrap(image, ctx, text, max_width, max_height):
    print("Wrapping Text...")
    """Break long text to multiple lines, and reduce point size
    until all text fits within a bounding box."""
    mutable_message = text
    iteration_attempts = 100

    def eval_metrics(txt):
        """Quick helper function to calculate width/height of text."""
        metrics = ctx.get_font_metrics(image, txt, True)
        return metrics.text_width, metrics.text_height

    def shrink_text():
        """Reduce point-size & restore original text"""
        ctx.font_size = ctx.font_size - 0.75
        return text

    while ctx.font_size > 0 and iteration_attempts:
        iteration_attempts -= 1
        width, height = eval_metrics(mutable_message)
        if height > max_height:
            mutable_message = shrink_text()
        elif width > max_width:
            columns = len(mutable_message)
            while columns > 0:
                columns -= 1
                mutable_message = '\n'.join(wrap(mutable_message, columns))
                wrapped_width, _ = eval_metrics(mutable_message)
                if wrapped_width <= max_width:
                    break
            if columns < 1:
                mutable_message = shrink_text()
        else:
            break
    if iteration_attempts < 1:
        raise RuntimeError("Unable to calculate word_wrap for " + text)
    return mutable_message


def create_image_quote(quote):
    print("Processing Image...")
    crop_image()
    font_config = random.choice(get_font_configurations())
    # font_config = get_font_configurations()[2]

    with Image(filename='new-picture.png') as img:
        with Drawing() as draw:
            basic_font_configuration(draw, font_config)

            formatted_text = format_quote(draw, font_config, img, quote.text)
            metrics = draw.get_font_metrics(img, formatted_text, True)

            draw_rectangle(draw, FACEBOOK_IMAGE_IDEAL_SIZE, FACEBOOK_IMAGE_IDEAL_SIZE, 0, 0)
            draw_quote(draw, formatted_text)
            draw_author(draw, font_config, quote.author, metrics)
            draw_logo(draw)
            draw_page_info(draw)

            draw.draw(img)
            img.save(filename='new-picture.png')
    print("Image Edited!")


def draw_logo(draw):
    print("Drawing Logo...")
    draw.gravity = 'north'
    icon = Image(filename='assets/icon.png')
    draw.composite(operator='over', left=0, top=50, width=60, height=60, image=icon)


def draw_author(draw, font_config, author, metrics):
    print("Drawing Author...")
    vertical_position = int((metrics.text_height / 1.82))
    draw.font_size = font_config['fontSizeSmall']
    draw.text(0, vertical_position, author)


def draw_page_info(draw):
    print("Drawing Footer...")
    draw.font = 'Fjalla-One'
    draw.font_style = 'normal'
    draw.font_size = 21
    vertical_position = 350
    draw.gravity = 'center'
    draw.text(0, vertical_position, 'Siga\n@NessasFrasesDaVida')


def format_quote(draw, font_config, img, quote):
    print("Formatting Text...")
    text = quote.upper() if font_config['isUpper'] else quote
    text_width = int(FACEBOOK_IMAGE_IDEAL_SIZE / 1.25)
    text_height = int(FACEBOOK_IMAGE_IDEAL_SIZE / 1.15)
    wrapped_text = word_wrap(img, draw, text, text_width, text_height)
    return wrapped_text


def draw_quote(draw, quote):
    print("Drawing Text...")
    draw.gravity = 'center'
    draw.text(0, 0, quote)


def basic_font_configuration(draw, font_config):
    print("Setting Fonts...")
    draw.fill_color = Color('white')
    draw.font = font_config['fontName']
    draw.font_style = font_config['fontStyle']
    draw.font_size = font_config['fontSizeLarge']


def crop_image():
    print("Cutting Image...")
    with Image(filename='base-picture.png') as img:
        img.transform(resize='800x800^')
        img.crop(width=FACEBOOK_IMAGE_IDEAL_SIZE, height=FACEBOOK_IMAGE_IDEAL_SIZE, gravity='center')
        img.save(filename='new-picture.png')

