from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def text_wrap(text, font, max_width):
    lines = []
    # If the width of the text is smaller than image width
    # we don't need to split it, just add it to the lines array
    # and return
    if font.getsize(text)[0] <= max_width:
        lines.append(text)
    else:
        # split the line by spaces to get words
        words = text.split(' ')
        i = 0
        # append every word to a line while its width is shorter than image width
        while i < len(words):
            line = ''
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            # when the line gets longer than the max width do not append the word,
            # add the line to the lines array
            lines.append(line)
    return lines

def print_text_on_image_and_save(text):
    file_name = 'base-picture.jpeg'

    image = Image.open(file_name)

    image_width, image_height = image.size

    font_type = ImageFont.truetype('ariblk.ttf', 16)

    draw = ImageDraw.Draw(image)

    text_width, text_height = draw.textsize(text)

    #draw.rectangle((10, 10, 10, 10), fill='red', width=100)

    lines = text_wrap(text, font_type, image_width-20)
    line_height = font_type.getsize('hg')[1]

    x = 10
    y = 20

    for line in lines:
        # draw the line on the image
        draw.text((x, y), line, fill=(255, 255, 255), font=font_type)

        # update the y position so that we can use it for next line
        y = y + line_height

    image.save('new-picture.jpg', optimize=True)
