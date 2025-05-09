import pygame
import os
import csv
from shutil import copyfile
import getopt
import sys
from Card import Card

"""
This script reads a CSV file with card data and generates cards using the Card class.
It initializes pygame, reads the configuration from a config file, and processes each row in the CSV file to create cards.
It also removes any existing output files before generating new ones.
The script is designed to be run from the command line and takes an optional argument for the config file path.
It uses the Card class to create and print cards based on the data in the CSV file.
"""


# Init pygame.
pygame.init()

# Config file path
config_path = os.path.join(os.getcwd(),"config.ini")

# Read the config file
config_file = open(config_path, 'r')
config_lines = config_file.readlines()
config_file.close()
# Parse the lines of the config file
config_data = dict()
for line in config_lines:
    # Split the at the = sign
    split_line = line.split("=")
    # Strip the later value of the escape character.
    split_line[1] = split_line[1].replace('\n', '')
    # Add the data to the dict.
    config_data.update({split_line[0]:split_line[1]})

# The csv file path
input_root_dir = os.path.join(os.getcwd(), config_data["input_dir"])
csv_path = os.path.join(input_root_dir, config_data["csv_file"])

# Define colors.
black = pygame.Color(0,0,0,255)

# Read the CSV file.
card_rows = []
with open(csv_path, 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    count = 0
    for i, row in enumerate(reader):
        # Ignore the first row. (the header row)
        if i == 0:
            continue
        # Ignore empty rows.
        if len(row) == 0:
            continue
        # ignore rows with not filled in all data
        if len(row) < 5 or any(r == "" for r in row):
            continue
        # Ignore comment rows.
        if row[0][0] == "_":
            continue
        card_rows.append(row)
        count += 1
      
# Remove all output files.
output_dir = os.path.join(os.getcwd(), config_data["output_dir"])
filesToRemove = [f for f in os.listdir(output_dir) if f.endswith(".png") or f.endswith("pdf")]
for f in filesToRemove:
    os.remove(os.path.join(output_dir, f))
    
card_data = []

# Read the cards.
for card_row in card_rows:
    # Parse the card data.
    header_text = card_row[0]
    body_text = card_row[1]
    fg_image_file = card_row[2]
    bg_color = card_row[3]
    filename = card_row[4]

    # Create the card.
    card = Card(header_text, body_text, fg_image_file, bg_color, filename, config_data)
    card.print()
    
# Close pygame.
pygame.quit()
