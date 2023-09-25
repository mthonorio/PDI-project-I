import math
from copy import deepcopy
from typing import List, Tuple
from PIL import Image
import numpy as np
from numpy import ndarray
import timeit


def get_negative_pixels(image: Image) -> List:
    """
    This function returns every pixel in its negative counter-part.
    :param image: Original Image in RGB
    :return: List with the negative RGB pixels
    """
    red_pixels = [[] for _ in range(image.size[0] - 1)]
    green_pixels = [[] for _ in range(image.size[0] - 1)]
    blue_pixels = [[] for _ in range(image.size[0] - 1)]
    for r in range(image.size[0] - 1):
        for c in range(image.size[1] - 1):
            colors = image.getpixel((r, c))
            red_pixels[r].append(255 - colors[0])
            green_pixels[r].append(255 - colors[1])
            blue_pixels[r].append(255 - colors[2])

    return [red_pixels, green_pixels, blue_pixels]


def turn_negative(image: Image) -> Image:
    """
    Transforms the image in its negative RGB counter-part
    :param image: Original image in RGB
    :return: New negative RGB image
    """
    pixels = get_negative_pixels(image)
    for r in range(image.size[0] - 1):
        for c in range(image.size[1] - 1):
            image.putpixel(
                (r, c), (pixels[0][r][c], pixels[1][r][c], pixels[2][r][c]))
    return image


def rgb_to_hsb(image: Image) -> List[List[List[float]]]:
    h_pixels = [[_ for _ in range(image.size[1] - 1)]
                for _ in range(image.size[0] - 1)]
    s_pixels = [[_ for _ in range(image.size[1] - 1)]
                for _ in range(image.size[0] - 1)]
    b_pixels = [[_ for _ in range(image.size[1] - 1)]
                for _ in range(image.size[0] - 1)]
    for r in range(image.size[0] - 1):
        for c in range(image.size[1] - 1):
            colors = image.getpixel((r, c))

            # normalize red, green and blue values
            red = colors[0] / 255.0
            green = colors[1] / 255.0
            blue = colors[2] / 255.0

            # conversion start
            maximum = max(red, max(green, blue))
            minimum = min(red, min(green, blue))

            # if max == min, h is undefined = 0
            if maximum == minimum:
                h = 0.0  # undefined
            elif maximum == red and green >= blue:
                h = 60 * (green - blue) / (maximum - minimum)
            elif maximum == red and green < blue:
                h = 60 * (green - blue) / (maximum - minimum) + 360
            elif maximum == green:
                h = 60 * (blue - red) / (maximum - minimum) + 120
            elif maximum == blue:
                h = 60 * (red - green) / (maximum - minimum) + 240
            h_pixels[r][c] = h
            s = 0.0 if (maximum == 0) else (1.0 - (minimum / maximum))
            s_pixels[r][c] = s
            b_pixels[r][c] = maximum
    return [h_pixels, s_pixels, b_pixels]


def get_rgb_pixels_from_hsb(pixels: List[List[List[float]]]) -> ndarray:
    new_pixels = np.empty(
        [len(pixels[0]), len(pixels[0][0]), 3], dtype=np.uint8)
    for i in range(len(pixels[0])):
        for c in range(len(pixels[0][0])):
            if pixels[1][i][c] == 0:
                red = green = blue = pixels[2][i][c]
            else:
                sector_pos = pixels[0][i][c] / 60.0
                sector_number = int(math.floor(sector_pos))
                fractional_sector = sector_pos - sector_number

                p = pixels[2][i][c] * (1.0 - pixels[1][i][c])
                q = pixels[2][i][c] * (1.0 - (pixels[1][i][c] * fractional_sector))
                t = pixels[2][i][c] * (1.0 - (pixels[1][i][c] * (1 - fractional_sector)))

                if sector_number == 0:
                    red = pixels[2][i][c]
                    green = t
                    blue = p
                elif sector_number == 1:
                    red = q
                    green = pixels[2][i][c]
                    blue = p
                elif sector_number == 2:
                    red = p
                    green = pixels[2][i][c]
                    blue = t
                elif sector_number == 3:
                    red = p
                    green = q
                    blue = pixels[2][i][c]
                elif sector_number == 4:
                    red = t
                    green = p
                    blue = pixels[2][i][c]
                elif sector_number == 5:
                    red = pixels[2][i][c]
                    green = p
                    blue = q

            red = round(red * 255.0)
            green = round(green * 255.0)
            blue = round(blue * 255.0)

            red = red if red > 0 else 0
            green = green if green > 0 else 0
            blue = blue if blue > 0 else 0

            red = red if red < 256 else 255
            green = green if green < 256 else 255
            blue = blue if blue < 256 else 255

            new_pixels[i][c] = np.array([red, green, blue], dtype=np.uint8)

    return new_pixels


def hsb_to_rgb(pixels: List[List[List[float]]]) -> Image:
    """
    Transforms an image (in this case, it is a list of values that characterize a pixel) in HSV into RGB calling an
    auxiliary function to make the calculations. It rotates the pixels as well to adjust the image correctly after the
    conversion.
    :param pixels: HSV pixels list
    :return: RGB image from the HSV pixels
    """
    pixels = get_rgb_pixels_from_hsb(pixels)
    rotated_pixels = np.rot90(pixels, axes=(1, 0))
    rotated_pixels = np.flip(rotated_pixels, axis=1)
    new_image = Image.fromarray(rotated_pixels)
    return new_image


def change_hue_sat(image: Image, add_to_hue=0, add_to_sat=0) -> Image:
    hsb_pixels = rgb_to_hsb(image)

    for r in range(len(hsb_pixels[0])):
        for c in range(len(hsb_pixels[0][0])):
            added_sat = add_to_sat + hsb_pixels[1][r][c]
            if added_sat > 1:
                added_sat = 1
            elif added_sat < 0:
                added_sat = 0

            hsb_pixels[0][r][c] = (add_to_hue + hsb_pixels[0][r][c]) % 360
            hsb_pixels[1][r][c] = added_sat
    return hsb_to_rgb(hsb_pixels)


def turn_negative_b(image: Image) -> Image:
    """
    Transforms an image (in this case, it is a list of values that characterize a pixel) in RGB into HSB calling and
    turning the B channel negative.
    :param image: RGB image that is going to be converted to HSB
    :return: RGB image from the HSB pixels

    """
    hsb_pixels = rgb_to_hsb(image)
    for r in range(len(hsb_pixels[0])):
        for c in range(len(hsb_pixels[0][0])):
            hsb_pixels[2][r][c] = 1 - hsb_pixels[2][r][c]
    return hsb_to_rgb(hsb_pixels)


def median_ixj(i: int, j: int, image: Image) -> Image:
    """
    Verifies if i and j are odd, and calls the function to apply the median filter. If i or j are odd, the function will
    raise an error.
    :param i: quantity of lines in the image
    :param j: quantity of columns in the image
    :param image: Original image in RGB format
    :return: new image with the filter applied.
    """
    if i % 2 == 0 or j % 2 == 0:
        raise ValueError(" 'i' and 'j' must be odd")
    median_image = median_filter(image, (i, j))

    return median_image


def median_filter(image: Image, size: Tuple[int, int]) -> Image:
    """
    Applies the median filter to an image.
    :param image: original image in RGB format
    :param size: size of the median filter (ixj or mxn)
    :return: new image with the filter applied.
    """
    im = np.array(image)
    m, n = size

    # window will be our kernel or 'mask', containing all values equals to 'one' and being m x n
    # because it has only 'ones', it can serve as a mask for the function np.median, used later when applying the filter
    window = np.ones((m, n))

    # the result variable will be initialized with zeros in the size of the original image
    result = np.zeros_like(im)
    # this tuple will contain how many rows and columns must be extended to apply the filter
    mxn_extended = (m // 2, n // 2)
    for i in range(im.shape[2]):
        # channel will have all the values of RGB in the image
        channel = im[:, :, i]
        # padded_im will be the extended image with the necessary number of zeros. If it is not given a value to the
        # param 'constant_values', it will be zero, so the image will be extended by zeros
        padded_channel = np.pad(channel, mxn_extended, mode='constant')
        for x in range(im.shape[0]):
            for y in range(im.shape[1]):
                """
                the sub_image will be the used to determine witch part of the image will be the one used to
                calculate the median with the np.median function. The sub_image will be multiplied by the 'mask', in
                this case, 'window', and passed as a parameter.
                """
                sub_image = padded_channel[x: x + m, y: y + n]
                if sub_image.shape == window.shape:
                    result[x, y, i] = np.median(sub_image * window)
    # the final array will be converted to uint8 in order to use less memory
    result = np.uint8(result)

    return Image.fromarray(result)


def call_correlation_mxn(image: Image, correlational_filter: ndarray, offset: Tuple[int, int], stride: int) -> Image:
    """
    This function checks if the size of the filter is valid and then calls the correlational filter
    :param stride: Regarding the step that the filter is going to take
    :param image: image witch the filter will be applied
    :param correlational_filter: array containing the filter and its values
    :param offset: offset to be considered by the function
    :return: image with the filter applied
    """

    size = correlational_filter.shape[0], correlational_filter.shape[1]

    m, n = size
    if m < 0 or n < 0 or type(m) != int or type(n) != int:
        raise ValueError("m and n must be a positive integer!")
    return correlational(image, size, correlational_filter, offset, stride)


def correlational(image: Image, size: Tuple[int, int], correlational_filter: ndarray, offset: Tuple[int, int], stride) -> Image:
    """
    This function will apply a correlational filter
    :param stride: Regarding the step that the filter is going to take
    :param image: image witch the filter will be applied
    :param size: size of the window of the filter (mxn)
    :param correlational_filter: array containing the filter and its values
    :param offset: offset to be considered by the function
    :return:
    """
    im = np.array(image)
    m, n = size
    window = correlational_filter

    output_height = (im.shape[0] - m) // (stride + 1)
    output_width = (im.shape[1] - n) // (stride + 1)

    # final image will be the 'result', initializes output with array of zeros
    #result = deepcopy(im)
    output = np.zeros((output_height, output_width, 3))
    for i in range(im.shape[2]):
        # getting all the values of R, then G, then B
        channel = im[:, :, i]

        for x in range(0, im.shape[0] - m + 1, stride if stride > 0 else 1):
            for y in range(0, im.shape[1] - n + 1, stride if stride > 0 else 1):
                # getting a sub_image that starts at position x and finishes at position x+m
                # and starts at position y and finishes at position y+n
                sub_image = channel[x: x + m, y: y + n]

                # if the sub_image has not the same size of the window, it means that the filter is already applied
                # to the image
                if sub_image.shape == window.shape:
                    # the new value will be the absolute value because some filters can return negative numbers
                    new_value = abs(np.sum(sub_image * window))

                    output[(x//(stride + 1)) - 1, (y//(stride + 1)) - 1, i] = new_value
                    """
                    if the image is ixj, and x+offset[0] is larger than i or y+offset[1] is larger than j, it means
                    that the filter is already applied to all the image, because the offset will be after the end of the
                    image
                    """
                    #if x + offset[0] <= im.shape[0] - 1 and y + offset[1] <= im.shape[1] - 1:
                    #    result[x + offset[0], y + offset[1], i] = new_value

    result = np.uint8(output)
    return Image.fromarray(result)


def histogram_expansion(image: Image) -> Image:
    """
    the histogram expansion will be from [0, 255]. It will apply the formula to every pixel in the image.
    :param image: image that will receive the expansion
    :return: output image with the expansion applied
    """
    im = np.array(image)
    min_intensity = np.min(image)
    max_intensity = np.max(image)
    im_expanded = (im - min_intensity) * \
                  (255 / (max_intensity - min_intensity))
    output = Image.fromarray(np.uint8(im_expanded))
    return output


def read_correlational_filters(file_name: str) -> None:
    with open(file_name) as f:
        lines = f.readlines()

    correlational_filters = [line.strip() for line in lines]

    offsets = [offset for offset in correlational_filters if ',' in offset]
    offsets = [(int(offset.split(', ')[0]), int(offset.split(', ')[1]))
               for offset in offsets]

    strides = [int(correlational_filters[0])-1]
    if len(offsets) > 1:
        for i in range(len(correlational_filters)):
            if correlational_filters[i] == '':
                strides.append(int(correlational_filters[i+1])-1)
    filters = [[] for _ in correlational_filters if ',' in _]

    j = 0
    for i in range(len(correlational_filters)):
        if correlational_filters[i] != '':
            filters[j].append(correlational_filters[i])
        if correlational_filters[i] == '':
            j += 1

    finished_arrays = [np.array(_) for _ in range(len(filters))]
    for j in range(len(filters)):
        filters[j].pop(0)
        filters[j].pop(0)
        for i in range(len(filters[j])):
            filters[j][i] = filters[j][i].split(' ')
            for h in range(len(filters[j][i])):
                treated_float = filters[j][i][h] if '/' in filters[j][i][h] else None
                if treated_float is not None:
                    split_float = filters[j][i][h].split('/')
                    split_float = int(split_float[0]) / int(split_float[1])
                    filters[j][i][h] = split_float
            filters[j][i] = [float(_) for _ in filters[j][i]]

        finished_arrays[j] = np.array(np.array(filters[j]))

    im = Image.open("tests/image.png")
    if file_name == "tests/box_15x1(box_1x15(image)).txt":
        begin_time = timeit.default_timer()
        for i in range(len(finished_arrays)):
            im = call_correlation_mxn(im, finished_arrays[i], offsets[i], strides[i])

        end_time = timeit.default_timer()
        print("Time of box_15x1(box_1x15(image)): ", end_time - begin_time)

    elif file_name == "tests/box_15x15.txt":
        begin_time = timeit.default_timer()
        im = call_correlation_mxn(im, finished_arrays[0], offsets[0], strides[0])
        end_time = timeit.default_timer()
        print("Time of box_15x15: ", end_time - begin_time)
    else:
        for i in range(len(finished_arrays)):
            im = call_correlation_mxn(im, finished_arrays[i], offsets[i], strides[0])

    if file_name in ["tests/sobel_horizontal.txt", "tests/sobel_vertical.txt"]:
        print("sobel_horizontal")
        im = histogram_expansion(im)

    im.show()
    im.save(file_name + ".png")