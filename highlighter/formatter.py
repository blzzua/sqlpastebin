#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image
from PIL import ImageDraw, ImageFont
from pygments.formatters.img import ImageFormatter
import time


class Formatter(ImageFormatter):

    @staticmethod
    def textsize(text, font):
        im = Image.new(mode="P", size=(0, 0))
        draw = ImageDraw.Draw(im)
        _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
        return width, height

    def format(self, tokensource, outfile):
        ttfont = ImageFont.truetype("Consolas-Regular.ttf", 16)
        #ttfont = ImageFont.load_path("/home/oleg/pp/codephoto/DejaVuSansMono.ttf")
        #ttfont = ImageFont.load_default()

        self._create_drawables(tokensource)
        self.maxcharno = 1200
        self.maxlineno = 60
        self._draw_line_numbers()
        self.background_color = '#ffffff'
        im = Image.new(mode='RGB',
            size = self._get_image_size(self.maxcharno, self.maxlineno),
            color = self.background_color
        )
        self._paint_line_number_bg(im)
        draw = ImageDraw.Draw(im)
        
        # Highlight
        if self.hl_lines:
            x = self.image_pad + self.line_number_width - self.line_number_pad + 1
            recth = self._get_line_height()
            rectw = im.size[0] - x
            for linenumber in self.hl_lines:
                y = self._get_line_y(linenumber - 1)
                draw.rectangle([(x, y), (x + rectw, y + recth)],
                               fill=self.hl_color)
        
        for pos, value, font, _color, kw in self.drawables:
            if kw is None:
                kw = {}
            draw.text(pos, value, fill=_color, font=ttfont)
            
##            # Draw a rectangular border around each character
##            for i, char in enumerate(value):
##                char_width, char_height = self.textsize(char, font=ttfont)
##                char_x = pos[0] + i * char_width
##                char_y = pos[1]
##                draw.rectangle([(char_x, char_y), (char_x + char_width, char_y + char_height)], outline="black")

        self.image = im
        
        # debug
        ## timestamp = int(time.time())
        ## filename = f'/tmp/filename-{timestamp}.png'
        ## im.save(filename)
        ## print(f"Image saved to {filename}")

