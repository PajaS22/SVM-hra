import pygame
import os
import csv
from shutil import copyfile
import getopt
import sys
import scipy
import numpy as np
import re

colors = {
    "red": (255, 0, 0),
    "green": (0, 200, 0),
    "blue": (0, 100, 255),
    "orange": (255, 140, 0),
    "purple": (160, 32, 240),
    "cyan": (0, 200, 200),
    "yellow": (255, 215, 0),
    "magenta": (255, 0, 200),
    "lime": (150, 255, 0),
}

class Card():
    "Class for capturing information about a single card"
    def __init__(self, header, body_text, foreground_fn, bg_color, out_fn, config):
        self.header = header
        self.body_text = body_text
        self.fg_fn = foreground_fn
        self.bg_color = bg_color
        self.out_fn = out_fn
        
        
        # root_dir is the directory of this file.
        root_dir = os.path.dirname(os.path.abspath(__file__))
        input_root_dir = os.path.join(root_dir, config["input_dir"])
        self.output_root_dir = os.path.join(root_dir, config["output_dir"])
        self.fonts_dir = os.path.join(input_root_dir, config["fonts_dir"])
        images_dir = os.path.join(input_root_dir, config["images_dir"])
        self.images_bg_dir = os.path.join(images_dir, config["images_bg_dir"])
        self.images_fg_dir = os.path.join(images_dir, config["images_fg_dir"])
        
        self.config = config

        self.card_width = int(config["card_width"])
        self.card_height = int(config["card_height"])
        self.header_font_size = int(config["header_font_size"])
        self.body_font_size = int(config["body_font_size"])
        self.header_width_percent = float(config["header_width_percent"])
        self.header_pad = int(config["header_pad"])
        self.body_pad = int(config["body_pad"])
        self.header_line_spacing = float(config["header_line_spacing"])
        self.body_line_spacing = float(config["body_line_spacing"])
        self.header_y = int(config["header_y"])
        self.body_y = int(config["body_y"])
        self.body_width_percent = float(config["body_width_percent"])
        self.fg_width_percent = float(config["fg_width_percent"])
        self.text_percent_box = float(config["text_percent_box"])
        
    def try_extensions(self, filename, extensions, dir=None):
        if dir is None:
            dir = self.images_fg_dir
        else:
            dir = self.images_bg_dir

        for ext in extensions:
            if os.path.exists(os.path.join(dir, f"{filename}.{ext}")):
                return os.path.join(dir, f"{filename}.{ext}")
        raise FileNotFoundError(f"File {filename} not found with any of the extensions: {extensions}")
    
    def wrap_text(self, text, font, max_width):
        lines = []

        for raw_line in text.split('\\n'):
            words = raw_line.split()
            current_line = ''

            for word in words:
                test_line = current_line + (' ' if current_line else '') + word
                width, _ = font.size(test_line)
                if width <= max_width*self.text_percent_box:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word

            if current_line:
                lines.append(current_line)

        return lines
    
    def text_labels(self, text, font, max_width, bg, y_start, line_spacing, fill=False, center=False):
        lines = self.wrap_text(text, font, max_width)
        

        # Draw a white rectangle under the text
        rect_x = (self.card_width - max_width)/2
        rect_y = y_start
        rect_width = max_width
        if not fill:
            rect_height = font.get_height() * len(lines) + (len(lines) - 1) * line_spacing
        else:
            rect_height = self.card_height - y_start - self.body_pad - int(self.config["border_width"])

        rect = pygame.Surface((rect_width, rect_height))
        rect.fill((255, 255, 255))  # Fill with white color
        bg.blit(rect, (rect_x, rect_y))

        y = y_start
        if center:
            y = y_start + (rect_height - font.get_height() * len(lines) - (len(lines) - 1) * line_spacing) / 2

        for line in lines:
            label = font.render(line, True, (0, 0, 0))
            x = ((self.card_width - max_width*self.text_percent_box)/2)
            if center:
                x = (self.card_width - font.size(line)[0]) / 2
            bg.blit(label, (x,y))
            y += font.get_height() * line_spacing
        
        height = y - y_start
        return height
        
    
    def print(self):
        fg_fn = self.try_extensions(self.fg_fn, ["png", "jpg", "jpeg"])
        
        # Create a background with a rounded rectangle
        bg = pygame.Surface((self.card_width, self.card_height), pygame.SRCALPHA)
        border_color = colors.get(self.bg_color, (0, 0, 0))  # Default to black if color not found
        border_thickness = int(self.config["border_width"])
        fill_color = (0, 0, 0)  # Black fill

        # Draw the rounded rectangle
        rect = pygame.Rect(0, 0, self.card_width, self.card_height)
        pygame.draw.rect(bg, border_color, rect, border_thickness, border_radius=20)
        pygame.draw.rect(bg, fill_color, rect.inflate(-2 * border_thickness, -2 * border_thickness), border_radius=20)


        fg = pygame.image.load(fg_fn)
        
        # Scale the images to fit the card size.
        bg = pygame.transform.scale(bg, (self.card_width, self.card_height))
        
        # process text
        header_font = pygame.font.Font(
            os.path.join(self.fonts_dir, self.config["header_font"]), self.header_font_size)
        body_font = pygame.font.Font(
            os.path.join(self.fonts_dir, self.config["body_font"]), self.body_font_size)
        
        header_maxwidth = self.header_width_percent * self.card_width
        body_maxwidth = self.body_width_percent * self.card_width
        
        # create header onto background
        header_start_y = self.header_y
        header_height = self.text_labels(self.header, header_font, header_maxwidth, bg, 
                                         header_start_y, self.header_line_spacing)
        
        # resize fg - scale fg image as much as possible until limits specified in config
        fg_h = fg.get_height()
        fg_w = fg.get_width()
        fg_maxheight = int(self.config["fg_maxheight"])
        fg_maxwidth = float(self.config["fg_width_percent"]) * self.card_width
        
        c = -1
        A_ub = np.array([[fg_h],[fg_w]])
        b_ub = np.array([[fg_maxheight], [fg_maxwidth]])
        
        optim_res = scipy.optimize.linprog(c=c, A_ub=A_ub, b_ub=b_ub)
        scale = optim_res.x.item()
        
        fg_h = fg_h * scale
        fg_w = fg_w * scale
        
        fg = pygame.transform.scale(fg, (fg_w, fg_h))
        fg_x = (self.card_width - fg_w)/2
        fg_y = header_start_y + header_height + self.header_pad
        bg.blit(fg, (fg_x, fg_y))
        
        # create body text labels
        body_start_y = fg_y + fg_h + self.body_pad
        body_height = self.text_labels(self.body_text, body_font, body_maxwidth, bg, 
                                         body_start_y, self.body_line_spacing, fill=True, center=True)
        r = self.card_height - body_start_y + body_height
        if r < 0:
            raise Exception(f"Card {self.header} does not fit in card_height (reserve {r})")

        # save card image
        output_fn = self.out_fn
        filepath = os.path.join(self.output_root_dir, f"{output_fn}.png")
        pygame.image.save(bg, filepath)
        print("Wrote: " + filepath)
        