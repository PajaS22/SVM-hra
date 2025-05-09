# CardCreator Tutorial

## Overview

The `CardCreator` tool allows you to create custom cards from a CSV file and arrange them into printable layouts. Follow this tutorial to quickly set up and use the tool.

---

## Step 1: Prepare Your Input Files

1. **CSV File**: Create a CSV file (`mycards.csv`) with the following columns:
   - `HEADER TEXT`: The title of the card.
   - `BODY TEXT`: The description or details of the card.
   - `FG_IMAGE_FILE`: The name of the foreground image (without extension).
   - `BG_COLOR`: The background color (e.g., `red`, `blue`, `green`).
   - `FILENAME`: The output filename for the card (without extension).

   Example:

   | HEADER TEXT              | BODY TEXT                                          | FG_IMAGE_FILE | BG_COLOR | FILENAME       |
   |--------------------------|---------------------------------------------------|---------------|----------|----------------|
   | Slibový oheň             | +2 VB, +2 VB pokud máš "Rozdělávání ohně"         | slibak        | purple   | slibak         |
   | Dobrý skutek každý den   | +1 VB                                             | 1gooddeed     | purple   | dobry_skutek   |

2. **Images**: Place your foreground images in the `Input/Images/Foregrounds` directory.

3. **Fonts**: Add any custom fonts to the `Input/Fonts` directory.

## Step 2: Configure the Tool

Edit the 'config.ini' file to set up your directories and card settings. Example:

```ini
input_dir=Input
output_dir=Output
csv_file=mycards.csv
fonts_dir=Fonts
images_dir=Images
images_bg_dir=Backgrounds
images_fg_dir=Foregrounds
card_width=800
card_height=600
header_font_size=40
body_font_size=20
header_font=Arial.ttf
body_font=Arial.ttf
border_width=10
```

## Step 3: Generate Cards

Run the `SVM_CardCreator.py` script to create cards:

```python
python [SVM_CardCreator.py](http://_vscodecontentref_/0)
```

The cards will be saved as PNG files in the `Output` directory.

## Step 4: Arrange Cards into Layouts

Run the `layout_images.py` script to arrange the cards into an A4 grid layout:

```shell
python layout_images.py --source Output --out layout --copies 2 --width 60 --height 90 --pad 10 --inner_pad 5
```

This will create:

- PNG layout files in the layout directory.
- A combined PDF file (all_pages.pdf) in the same directory.

## Example Workflow

1. Prepare your mycards.csv file and images.
2. Configure config.ini with your settings.
3. Run SVM_CardCreator.py to generate cards.
4. Run layout_images.py to create printable layouts.

### Output

- Cards: Individual PNG files in the Output directory.
- Layouts: PNG files and a combined PDF in the layout directory.
You're ready to print your custom cards!

---
*This project builds on Esther Alter's [CardCreator](https://github.com/subalterngames/CardCreator)*