import argparse
import os
from PIL import Image, ImageDraw
from math import floor, ceil

"""
This script arranges images in a grid layout on A4 pages for printing.
It takes images from a source directory, resizes them, and arranges them in a specified grid format.
It also allows for multiple copies of each image and custom padding between images.
The output is saved as PNG files and a single PDF file.
"""

# A4 dimensions in mm
A4_HEIGHT_MM = 210
A4_WIDTH_MM = 297
DPI = 300  # For printing, high-quality

def mm_to_px(mm):
    return int(mm * DPI / 25.4)

def load_images_from_directory(source_dir):
    image_files = [f for f in os.listdir(source_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    return [Image.open(os.path.join(source_dir, f)).convert("RGB") for f in sorted(image_files)]

def create_pages(images, copies, w_mm, h_mm, pad_mm, inner_pad_mm):
    img_w_px = mm_to_px(w_mm)
    img_h_px = mm_to_px(h_mm)
    pad_px = mm_to_px(pad_mm)
    inner_pad_px = mm_to_px(inner_pad_mm)

    page_w_px = mm_to_px(A4_WIDTH_MM)
    page_h_px = mm_to_px(A4_HEIGHT_MM)

    cols = (page_w_px - 2 * pad_px + inner_pad_px) // (img_w_px + inner_pad_px)
    rows = (page_h_px - 2 * pad_px + inner_pad_px) // (img_h_px + inner_pad_px)
    images_per_page = rows * cols

    print(f"Page grid: {cols} columns x {rows} rows = {images_per_page} images per page")

    all_images = [img for img in images for _ in range(copies)]
    total_pages = ceil(len(all_images) / images_per_page)
    pages = []

    for p in range(total_pages):
        page = Image.new('RGB', (page_w_px, page_h_px), color='white')
        draw = ImageDraw.Draw(page)

        for i in range(images_per_page):
            idx = p * images_per_page + i
            if idx >= len(all_images):
                break

            row = i // cols
            col = i % cols

            x = pad_px + col * (img_w_px + inner_pad_px)
            y = pad_px + row * (img_h_px + inner_pad_px)

            resized = all_images[idx].resize((img_w_px, img_h_px), Image.LANCZOS)
            page.paste(resized, (x, y))

        pages.append(page)

    return pages

def main():
    parser = argparse.ArgumentParser(description="Arrange images in an A4 grid layout")
    parser.add_argument("--source", type=str, default="Output", help="Directory of source images")
    parser.add_argument("--out", type=str, default="layout", help="Output directory for pages")
    parser.add_argument("--copies", type=int, default=2, help="Number of copies of each image")
    parser.add_argument("--width", type=float, default=60, help="Width of each image in mm")
    parser.add_argument("--height", type=float, default=90, help="Height of each image in mm")
    parser.add_argument("--pad", type=float, default=10, help="Padding around the grid in mm")
    parser.add_argument("--inner_pad", type=float, default=5, help="Padding between images in mm")  # New argument

    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)
    
    # Delete all files in the output directory
    for file in os.listdir(args.out):
        file_path = os.path.join(args.out, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    images = load_images_from_directory(args.source)
    if not images:
        print("No images found in the source directory.")
        return

    pages = create_pages(images, args.copies, args.width, args.height, args.pad, args.inner_pad)
    for i, page in enumerate(pages):
        page.save(os.path.join(args.out, f"page_{i+1}.png"))
    
    pdf_path = os.path.join(args.out, "all_pages.pdf")
    pages[0].save(pdf_path, save_all=True, append_images=pages[1:], format="PDF", resolution=DPI)

    print(f"Saved {len(pages)} pages to '{args.out}'.")

if __name__ == "__main__":
    main()