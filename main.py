from modules import *

directory = "tests/"
test_image = directory+"image.png"

# Show the original image
original_img = Image.open(test_image)
original_img.show(title="Original Image")

# Show the image converted to rgb to yiq after to rgb
rgb_yiq_rgb = Image.open(test_image)
rgb_yiq_rgb = rgb_to_yiq(rgb_yiq_rgb)
rgb_yiq_rgb = yiq_to_rgb(rgb_yiq_rgb)
rgb_yiq_rgb.show(title="RGB to YIQ to RGB")

# Show the image converted to negative
negative_img = Image.open(test_image)
negative_img = turn_negative(negative_img)
negative_img.show(title="Negative RGB")

# Show the image converted to negative on Y
negative_y = Image.open(test_image)
negative_y = negative_on_y(negative_y)
negative_y.show(title="Negative on Y")

# Show the image correlation with a 3x3 filter
median_3x3_extension = Image.open(test_image)
begin_time = timeit.default_timer()
median_3x3_extension = median_ixj(3, 3, median_3x3_extension)
end_time = timeit.default_timer()
print("Median 3x3 with extension: ", end_time - begin_time)
median_3x3_extension.show(title="Median 3x3 with extension")

# Show the image correlation with a 7x7 filter
median_7x7_extension = Image.open(test_image)
begin_time = timeit.default_timer()
median_7x7_extension = median_ixj(7, 7, median_7x7_extension)
end_time = timeit.default_timer()
print("Median 7x7 with extension: ", end_time - begin_time)
median_7x7_extension.show(title="Median 7x7 with extension")

# List all files in the directory
files = os.listdir(directory)

# Loop to verify if the file is a .txt
for file in files:
    # Verify if the file is a .txt
    if file.endswith(".txt"):
        # Execute the function to all files .txt
        read_correlational_filters(directory + file)
