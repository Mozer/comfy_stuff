from PIL import Image, ImageDraw, ImageFont, ImageOps
import random
import os

# Load the dictionary file
with open("rus_5000.txt", "r", encoding="utf-8") as file:
    words = file.readlines()

# Ensure fonts are available in the same directory or provide the full path to the font files
times_new_roman_font = "times.ttf"  # Replace with the path to Times New Roman font
tahoma_font = "tahoma.ttf"          # Replace with the path to Tahoma font
comic_sans_font = "comic.ttf"       # Replace with the path to Comic Sans font

# Ensure fonts exist
if not all(os.path.exists(font) for font in [times_new_roman_font, tahoma_font, comic_sans_font]):
    raise FileNotFoundError("One or more required font files are missing. Please provide the correct paths.")

# Create output directory if it doesn't exist
output_dir = "img5000"
os.makedirs(output_dir, exist_ok=True)

# Image size
img_width, img_height = 768, 768

# Function to calculate text size using textbbox
def calculate_text_size(text, font):
    dummy_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    return width, height

replacements = {
    "А": "A", "Б": "ß", "В": "B", "Г": "Î", "Д": "ă", "Е": "E", "Ё": "É", "Ж": "ş",
    "З": "3", "И": "ù", "Й": "ü", "К": "K", "Л": "â", "М": "M", "Н": "H", "О": "O",
    "П": "á", "Р": "P", "С": "C", "Т": "T", "У": "Y", "Ф": "ö", "Х": "X", "Ц": "Ü",
    "Ч": "4", "Ш": "##", "Щ": "!!!", "Ъ": "ț", "Ы": "ä", "Ь": "ţ", "Э": "ó",
    "Ю": "ô", "Я": "®"
}

def transliterate(text):
    """Replace Cyrillic letters in text with their transliterated Latin equivalents."""
    for cyrillic, latin in replacements.items():
        text = text.replace(cyrillic, latin)
    return text
    

# Iterate through the words and create images
for i, word in enumerate(words):
    word = word.strip()  # Remove any extra whitespace or newline characters

    # Determine font and colors based on the line number
    if (i + 1) % 100 == 0:  # Every 100th image
        font = ImageFont.truetype(comic_sans_font, 100)
        text_color = "red"
        background_color = "grey"
    elif (i + 1) % 2 == 0:  # Even images
        font = ImageFont.truetype(tahoma_font, 100)
        text_color = "white"
        background_color = "black"
    else:  # Odd images
        font = ImageFont.truetype(times_new_roman_font, 100)
        text_color = "black"
        background_color = "white"

    # Create base image with background color
    img = Image.new("RGB", (img_width, img_height), background_color)
    draw = ImageDraw.Draw(img)

    # Calculate text size and position
    text_width, text_height = calculate_text_size(word, font)
    text_x = (img_width - text_width) // 2
    text_y = (img_height - text_height) // 2

    # Create a separate image for text and apply random rotation
    text_img = Image.new("L", (img_width, img_height), 0)  # 'L' mode for grayscale
    text_draw = ImageDraw.Draw(text_img)
   
    # bold
    if (i + 1) % 2 == 0:  # Even images
        text_draw.text((text_x, text_y), word, font=font, fill=255, stroke_width=2, stroke_fill="white")  # White text on black background with bold
    else:
        text_draw.text((text_x, text_y), word, font=font, fill=255)  # White text on black background

    # Apply anti-aliasing during rotation
    rotated_text = text_img.rotate(
        random.uniform(-10, 10),
        resample=Image.Resampling.BICUBIC,  # Anti-aliasing for smooth edges
        expand=True
    )

    # Colorize the rotated text and paste it onto the base image
    colored_text = ImageOps.colorize(rotated_text, black=background_color, white=text_color)
    img.paste(colored_text, (0, 0), rotated_text)

    # Save the image
    image_filename = f"rus_{i + 1}.png"
    img.save(os.path.join(output_dir, image_filename))

    # Create and save the .txt file with the specified content
    text_filename = f"rus_{i + 1}.txt"
    with open(os.path.join(output_dir, text_filename), "w", encoding="utf-8") as text_file:
        word_encoded = transliterate(word)
        text_file.write(f"{text_color} text \"{word_encoded}\" on {background_color} background")

    print(f"Created: {image_filename} and {text_filename}")

print("Images and text files created successfully!")
