from typing import List, Tuple
from PIL import Image
import numpy as np
from numpy import ndarray
import os
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


def rgb_to_yiq(image: Image) -> List[List[List[float]]]:
    """
    Receives an RGB image and makes the necessary adjusts to convert each pixel to its YIQ counter-part utilizing the
    correct formula for it.
    :param image: Original image in RGB
    :return: List containing every component of every pixel in YIQ format
    """
    y_pixels = [[_ for _ in range(image.size[1] - 1)]
                for _ in range(image.size[0] - 1)]
    i_pixels = [[_ for _ in range(image.size[1] - 1)]
                for _ in range(image.size[0] - 1)]
    q_pixels = [[_ for _ in range(image.size[1] - 1)]
                for _ in range(image.size[0] - 1)]
    for r in range(image.size[0] - 1):
        for c in range(image.size[1] - 1):
            colors = image.getpixel((r, c))
            y = 0.299 * colors[0] + 0.587 * colors[1] + 0.114 * colors[2]
            i = 0.596 * colors[0] - 0.274 * colors[1] - 0.322 * colors[2]
            q = 0.211 * colors[0] - 0.523 * colors[1] + 0.312 * colors[2]
            y_pixels[r][c] = y
            i_pixels[r][c] = i
            q_pixels[r][c] = q
    return [y_pixels, i_pixels, q_pixels]


def get_rgb_pixels_from_yiq(pixels: List[List[List[float]]]) -> ndarray:
    """
    Similar to the RGB-YIQ function, but this time it does the opposite. It receives a list containing every pixel in
    YIQ format, and returns them in RGB format after conversion.
    :param pixels: List containing the pixels in YIQ format
    :return: np array containing every pixel in RGB format
    """
    new_pixels = np.empty(
        [len(pixels[0]), len(pixels[0][0]), 3], dtype=np.uint8)
    for i in range(len(pixels[0])):
        for c in range(len(pixels[0][0])):
            r = pixels[0][i][c] + 0.956 * \
                pixels[1][i][c] + 0.621 * pixels[2][i][c]
            g = pixels[0][i][c] - 0.272 * \
                pixels[1][i][c] - 0.647 * pixels[2][i][c]
            b = pixels[0][i][c] - 1.106 * \
                pixels[1][i][c] + 1.703 * pixels[2][i][c]

            r = round(r)
            g = round(g)
            b = round(b)

            r = r if r > 0 else 0
            g = g if g > 0 else 0
            b = b if b > 0 else 0

            r = r if r < 256 else 255
            g = g if g < 256 else 255
            b = b if b < 256 else 255

            new_pixels[i][c] = np.array([r, g, b], dtype=np.uint8)

    return new_pixels


def yiq_to_rgb(pixels: List[List[List[float]]]) -> Image:
    """
    Transforms an image (in this case, it is a list of values that characterize a pixel) in YIQ into RGB calling an
    auxiliary function to make the calculations. It rotates the pixels as well to adjust the image correctly after the
    conversion.
    :param pixels: YIQ pixels list
    :return: RGB image from the YIQ pixels
    """
    pixels = get_rgb_pixels_from_yiq(pixels)
    rotated_pixels = np.rot90(pixels, axes=(1, 0))
    rotated_pixels = np.flip(rotated_pixels, axis=1)
    new_image = Image.fromarray(rotated_pixels)
    return new_image


def negative_on_y(image: Image) -> Image:
    """
    Turns the Y from the YIQ color scheme into negative and returns an image of the result.
    :param image: Original image in RGB format
    :return: RGB image with the Y coordinate of YIQ negative.
    """
    yiq_pixels = rgb_to_yiq(image)
    for i in range(len(yiq_pixels[0])):
        for r in range(len(yiq_pixels[0][0])):
            yiq_pixels[0][i][r] = 255 - yiq_pixels[0][i][r]
    return yiq_to_rgb(yiq_pixels)


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


def call_correlation_mxn(image: Image, correlational_filter: ndarray, offset: Tuple[int, int]) -> Image:
    """
    This function checks if the size of the filter is valid and then calls the correlational filter
    :param image: image witch the filter will be applied
    :param correlational_filter: array containing the filter and its values
    :param offset: offset to be considered by the function
    :return: image with the filter applied
    """

    size = correlational_filter.shape[0], correlational_filter.shape[1]

    m, n = size
    if m < 0 or n < 0 or type(m) != int or type(n) != int:
        raise ValueError("m and n must be a positive integer!")
    return correlational(image, size, correlational_filter, offset)


def correlational(image: Image, size: Tuple[int, int], correlational_filter: ndarray, offset: Tuple[int, int]) -> Image:
    """
    This function will apply a correlational filter
    :param image: image witch the filter will be applied
    :param size: size of the window of the filter (mxn)
    :param correlational_filter: array containing the filter and its values
    :param offset: offset to be considered by the function
    :return:
    """
    im = np.array(image)
    m, n = size
    window = correlational_filter

    # how many rows and columns will be expanded by 0
    mxn_extended = (m // 2, n // 2)

    # final image will be the 'result'
    result = np.zeros_like(im)

    for i in range(im.shape[2]):
        # getting all the values of R, then G, then B
        channel = im[:, :, i]
        # expanding the array with 0s according to the needs of the filter
        padded_channel = np.pad(channel, mxn_extended, mode='constant')
        for x in range(im.shape[0]):
            for y in range(im.shape[1]):
                # getting a sub_image that starts at position x and finishes at position x+m
                # and starts at position y and finishes at position y+n
                sub_image = padded_channel[x: x + m, y: y + n]

                # if the sub_image has not the same size of the window, it means that the filter is already applied
                # to the image
                if sub_image.shape == window.shape:
                    # the new value will be the absolute value because some filters can return negative numbers
                    new_value = abs(np.sum(sub_image * window))
                    """
                    if the image is ixj, and x+offset[0] is larger than i or y+offset[1] is larger than j, it means
                    that the filter is already applied to all the image, because the offset will be after the end of the
                    image
                    """
                    if x + offset[0] <= im.shape[0] - 1 and y + offset[1] <= im.shape[1] - 1:
                        result[x + offset[0], y + offset[1], i] = new_value

    result = np.uint8(result)
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
        for i in range(len(filters[j])):
            filters[j][i] = filters[j][i].split(' ')
            for h in range(len(filters[j][i])):
                treated_float = filters[j][i][h] if '/' in filters[j][i][h] else None
                if treated_float:
                    split_float = filters[j][i][h].split('/')
                    split_float = int(split_float[0]) / int(split_float[1])
                    filters[j][i][h] = split_float
            filters[j][i] = [float(_) for _ in filters[j][i]]

        finished_arrays[j] = np.array(np.array(filters[j]))

    im = Image.open("tests/image.png")
    if file_name == "tests/box_11x1(box_1x11(image)).txt":
        begin_time = timeit.default_timer()
        for i in range(len(finished_arrays)):
            im = call_correlation_mxn(im, finished_arrays[i], offsets[i])

        end_time = timeit.default_timer()
        print("Time of box_11x1(box_1x11(image)): ", end_time - begin_time)

    elif file_name == "tests/box_11x11.txt":
        begin_time = timeit.default_timer()
        im = call_correlation_mxn(im, finished_arrays[0], offsets[0])
        end_time = timeit.default_timer()
        print("Time of box_11x11: ", end_time - begin_time)
    else:
        for i in range(len(finished_arrays)):
            im = call_correlation_mxn(im, finished_arrays[i], offsets[i])

    if file_name in ["tests/sobel_horizontal.txt", "tests/sobel_vertical.txt"]:
        im = histogram_expansion(im)

    im.show()
