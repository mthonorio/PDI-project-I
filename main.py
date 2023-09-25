import os

from modules import *


directory = "tests/"
test_image = directory+"image.png"

# Show the original image
original_img = Image.open(test_image)
original_img.show(title="Original Image")

# Show the image converted to rgb to hsb after to rgb
rgb_hsb_rgb = Image.open(test_image)
rgb_hsb_rgb = rgb_to_hsb(rgb_hsb_rgb)
rgb_hsb_rgb = hsb_to_rgb(rgb_hsb_rgb)
rgb_hsb_rgb.show(title="RGB to HSB to RGB")


# Show image modified in HUE
image_hue_modified = change_hue_sat(rgb_hsb_rgb, 100)
image_hue_modified.show(title="Modified Hue")
image_hue_modified.save("Lena Hue only modified.png")


# Show the image converted to negative in B
negative_b = turn_negative_b(rgb_hsb_rgb)
negative_b.show(title="Negative in B")
negative_b.save("Lena in negative V.png")

# Show the image converted to negative
negative_img = Image.open(test_image)
negative_img = turn_negative(negative_img)
negative_img.show(title="Negative RGB")


# Show the image with histogram expansion
expanded = histogram_expansion(rgb_hsb_rgb)
expanded.show()
expanded.save("Lena_hist_expanded.png")

# List all files in the directory
files = os.listdir(directory)

# Loop to verify if the file is a .txt
for file in files:
    # Verify if the file is a .txt
    if file.endswith(".txt"):
        # Execute the function to all files .txt
        read_correlational_filters(directory + file)
