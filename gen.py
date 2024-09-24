## usage: gen.py <filename.csv>

# some dimensions:
# card      = 62x87mm -> rendered in 310x435px
# A4 page   = 210x297mm -> 595x842pt (at 72dpi/28dpc)
# 1px = 1pt so a card is 174x244px (56%) when added to the PDF
# 0,0 -> 16,22mm 18,22mm

import csv

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from qrcode import make as makeqrcode

from PIL import Image, ImageDraw, ImageFont

CARD_DIMENSIONS = (310,435)
TITLE_HEIGHT = 135
QRCODE_DIMENSIONS = (280,280)
QRCODE_ANCHOR = (15,135)
SONG_HEIGHT = 175
SONG_Y_ANCHOR = 260
ARTIST_HEIGHT = 175

SCALE = 0.56
X_OFFSET = 37
Y_OFFSET = 55

def make_pdf(data, filename):
    c = canvas.Canvas("%s.pdf" % (filename), pagesize=A4)

    w = CARD_DIMENSIONS[0]*SCALE
    h = CARD_DIMENSIONS[1]*SCALE
    for g in range(len(data.keys())-1):
        for y in range(3):
            for x in range(3):
                i = (y*3)+x
                try:
                    front = make_card_image_front(data['title'], data[g][i][3])
                    c.drawInlineImage(front,
                                    X_OFFSET + (x* w), Y_OFFSET + (y* h),
                                    width=w, height=h)
                except IndexError:
                    pass
                except KeyError:
                    pass
        c.showPage()

        for y in range(3):
            for x, _x in zip(range(2, -1, -1), range(3)):
                i = (y*3)+x
                try:
                    back, clipped = make_card_image_back(data[g][i][2], data[g][i][0], data[g][i][1])
                    if clipped:
                        print(data[g][i][1], "has clipped text")                    
                    c.drawInlineImage(back,
                                    X_OFFSET + (_x* w), Y_OFFSET + (y* h),
                                    width=w, height=h)
                except IndexError:
                    pass
                except KeyError:
                    pass
        c.showPage()
    c.save()

def draw_border(draw):
    draw.rectangle((1, 1, CARD_DIMENSIONS[0]-2, CARD_DIMENSIONS[1]-2), outline='black', fill='white')

def make_card_image_front(title, spotify_url):
    image = Image.new('L', CARD_DIMENSIONS, 'white')    
    draw = ImageDraw.Draw(image)
    draw_border(draw)

    # draw the title centered in the top
    small_font = ImageFont.truetype("freesansbold.ttf", 32)
    left, top, right, bottom = draw.multiline_textbbox((0, 0), title, font=small_font)
    width, height = right - left, bottom - top
    draw.text(((CARD_DIMENSIONS[0] - width)/2, (TITLE_HEIGHT - height)/2),
              title, fill='black', font=small_font,
              align='center')

    # draw the QR code centered in the bottom
    qrcode_image = makeqrcode(spotify_url).resize(QRCODE_DIMENSIONS)
    image.paste(qrcode_image, QRCODE_ANCHOR)
    
    # save as PNG
    #image.save('front.png')

    return image

def make_card_image_back(artist, year, song):
    image = Image.new('L', CARD_DIMENSIONS, 'white')    
    draw = ImageDraw.Draw(image)
    draw_border(draw)

    # draw the year centered on the card
    large_font = ImageFont.truetype("freesansbold.ttf", 64)
    left, top, right, bottom = draw.multiline_textbbox((0, 0), year, font=large_font)
    width, height = right - left, bottom - top
    draw.text(((CARD_DIMENSIONS[0] - width)/2, (CARD_DIMENSIONS[1] - height)/2),
              year, fill='black', font=large_font)

    clipped = False
    # draw artist centered in the top
    small_font = ImageFont.truetype("freesansbold.ttf", 32)
    left, top, right, bottom = draw.multiline_textbbox((0, 0), artist, font=small_font)
    width, height = right - left, bottom - top
    draw.text(((CARD_DIMENSIONS[0] - width)/2, (ARTIST_HEIGHT - height)/2),
              artist, fill='black', font=small_font,
              align='center')
    if (CARD_DIMENSIONS[0] - width)/2 < 0:
        clipped = True

    # draw song centered in the bottom
    small_font = ImageFont.truetype("freesansbold.ttf", 24)
    left, top, right, bottom = draw.multiline_textbbox((0, 0), song, font=small_font)
    width, height = right - left, bottom - top
    draw.text(((CARD_DIMENSIONS[0] - width)/2, SONG_Y_ANCHOR + (SONG_HEIGHT - height)/2),
              song, fill='black', font=small_font,
              align='center')
    if (CARD_DIMENSIONS[0] - width)/2 < 0:
        clipped = True

    #image.save('back.png')

    return image, clipped

def parse_csv(filename):
    result = {}
    with open(filename) as csvfile:
        _headers = None
        csv_reader = csv.reader(csvfile, delimiter=';')
        i,g=0,-1
        for row in csv_reader:
            if (i-1) % 9 == 0:
                g+=1
                result[g] = []

            if i==0:
                result['title'] = ''.join([x.replace('%', '\n') for x in row])

            else:
                result[g].append([x.replace('%', '\n') for x in row])

            i+=1

    return result, i

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
                    prog = 'gen.py',
                    description = 'Make a PDF file containing Hitster cards based on content in CSV file',
                    epilog = 'Made with love in Gothenburg, Sweden')
    parser.add_argument('filename')
    args = parser.parse_args()

    data,i = parse_csv(args.filename)
    print("%d cards from %s" % (i-1, args.filename))
    make_pdf(data, args.filename.split('.')[0])