#coding=utf-8
import Image, ImageFont, ImageDraw

IMG_SRC = "/home/ajie/watermark/test7.jpg"
LOGO_SRC = "/opt/aoaola/web/img/page/watermark.png"
USER_NAME = u"@无量山"
PAGE_URL = u"Aoaola.com/topic/156"
FONT = "/usr/share/fonts/zh_CN/msyhbd.ttf"
EN_FONT = "/usr/share/fonts/truetype/freefont/FreeMono.ttf"
FONT_COLOR = "#fff"
FONT_SIZE = 13
PADDING = 10
MARGIN = 15

def waterMark(img_src, user_name, page_url):
    logo = Image.open(LOGO_SRC)    #原始图片
    im = Image.open(img_src)    #原始图片
    (im_width, im_height) = im.size
    if im.format != 'GIF' and im_width > 320:
        (logo_width, logo_height) = logo.size
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        font = ImageFont.truetype(FONT, FONT_SIZE)    #设置字体及文字尺寸
        en_font = ImageFont.truetype(FONT, FONT_SIZE)    #设置字体及文字尺寸

        #链接水印
        (url_width, url_height) = en_font.getsize(page_url)    #获得文字水印的尺寸
        url_mark = Image.new("RGBA", (url_width, url_height))    #创建水印透明背景图
        draw = ImageDraw.ImageDraw(url_mark, "RGBA")    #绘制水印透明背景图
        draw.text((0,0), page_url, font=en_font, fill=FONT_COLOR)
        mark_pos = (im_width-url_width-MARGIN-logo_width, im_height-url_height-PADDING)
        im.paste(url_mark, mark_pos, url_mark)

        #用户名水印
        (name_width, name_height) = font.getsize(user_name)    #获得文字水印的尺寸
        name_mark = Image.new("RGBA", (name_width, name_height))    #创建水印透明背景图
        draw = ImageDraw.ImageDraw(name_mark, "RGBA")    #绘制水印透明背景图
        draw.text((0,0), user_name, font=font, fill=FONT_COLOR)
        name_pos = (im_width-name_width-MARGIN-logo_width, im_height-url_height-name_height-PADDING)
        im.paste(name_mark, name_pos, name_mark)

        #logo水印
        logo_pos = (im_width-logo_width-PADDING+2, im_height-logo_height-PADDING)
        im.paste(logo, logo_pos, logo)

        im.save(img_src)

if __name__ == "__main__":
    waterMark(IMG_SRC, USER_NAME, PAGE_URL)
