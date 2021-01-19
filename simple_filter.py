from PIL import Image
import math
def read_input_image():
    image = Image.open('baboon.png').convert('L')
    image.show()
    image_data = [x / 255.0 for x in list(image.getdata())]
    return {'image': image_data}

def image_to_list(image, width, height):
    out = []
    for i in range(height):
        for j in range(width):
            out.append(image[i][j])
    return out
def list_to_image(list, width):
    out = []
    for i in range(0, len(list), width):
        out.append(list[i:i+width])
    return out

def convolution(image, width, height, filter, k):
    image = list_to_image(image, width)
    offset = k//2
    tmp = list_to_image([0] * (width * height), width)
    for i in range(height):
        for j in range(width):
            line_start = i - offset
            column_start = j - offset
            sum = 0
            for idx1 in range(k):
                for idx2 in range(k):
                    if (line_start + idx1 < 0) or (column_start + idx2 < 0) or (line_start + idx1 >= height) or (column_start + idx2 >= width):
                        val = 0
                    else:
                        val = image[line_start + idx1][column_start + idx2]
                    sum = sum + (val * filter[idx1][idx2])
            tmp[i][j] = sum

    return tmp

def rotate(l, n):
    return l[n:] + l[:n]

def convolution1(image, width, filter):
    for i in range(len(filter)):
        for j in range(len(filter[0])):
            rotated = rotate(image, i*width+j)
            #rotated = image << i * width + j
            partial = [x * filter[i][j] for x in rotated]
            if i == 0 and j == 0:
                convolved = [x for x in partial]
            else:
                convolved = [convolved[i] + partial[i] for i in range(4096)]
    return convolved

def generate_mean_filter(k):
    filter = [[0] * k] * k
    for i in range(k):
        for j in range(k):
            filter[i][j] = 1/(k**2)
    return filter

input = read_input_image()

mean_filter = generate_mean_filter(3)

sobel_filter_x = [
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]]

sobel_filter_y = [
    [-1, -2, -1],
    [0, 0, 0],
    [1, 2, 1]]


identity_filter = [
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0]]



#conv = convolution(input['image'], 64, 64, mean_filter, 3)
conv = convolution1(input['image'], 64, mean_filter)
image_out = Image.new('L', (64, 64))
#serialized_image = image_to_list(conv, 64, 64)
image_out.putdata([x*255 for x in conv])
image_out.show()