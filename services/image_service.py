from textwrap import wrap
from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image

FACEBOOK_IMAGE_IDEAL_SIZE = 800

def draw_rectangle(contxt, roi_width, roi_height, top, left, color):
    contxt.push()
    contxt.stroke_color = color
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
        mutable_message = text

    while ctx.font_size > 0 and iteration_attempts:
        iteration_attempts -= 1
        width, height = eval_metrics(mutable_message)
        if height > roi_height:
            shrink_text()
        elif width > roi_width:
            columns = len(mutable_message)
            while columns > 0:
                columns -= 1
                mutable_message = '\n'.join(wrap(mutable_message, columns))
                wrapped_width, _ = eval_metrics(mutable_message)
                if wrapped_width <= roi_width:
                    break
            if columns < 1:
                shrink_text()
        else:
            break
    if iteration_attempts < 1:
        raise RuntimeError("Unable to calculate word_wrap for " + text)
    return mutable_message

def write_text(text):
    with Image(filename='new-picture.png') as img:
        with Drawing() as draw:
            color = Color('WHITE')

            draw_rectangle(draw, FACEBOOK_IMAGE_IDEAL_SIZE, FACEBOOK_IMAGE_IDEAL_SIZE, 0, 0, color)
            draw.fill_color = color
            draw.font_family = 'Arial'
            draw.font_size = 80

            text_margin_top = 200
            text_margin_left = 150
            text_width = FACEBOOK_IMAGE_IDEAL_SIZE - text_margin_left
            text_heigth = FACEBOOK_IMAGE_IDEAL_SIZE - text_margin_top
            aligned_text = word_wrap(img, draw, text, text_width, text_heigth)

            draw.text(int(text_margin_left/2), text_margin_top, aligned_text)
            draw.draw(img)
            img.save(filename='new-picture.png')

def crop_image():
    with Image(filename='base-picture.png') as img:
        img.transform(resize='800x800^')
        img.crop(width=FACEBOOK_IMAGE_IDEAL_SIZE, height=FACEBOOK_IMAGE_IDEAL_SIZE, gravity='center')
        img.save(filename='new-picture.png')

def print_text_on_image_and_save(text):
    crop_image()
    write_text(text)
