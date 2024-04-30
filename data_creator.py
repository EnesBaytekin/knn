from random import randrange, choice
from math import sin, pi

SHAPES = {
    "T": [
        [1, 1, 1],
        [0, 1, 0],
    ],
    "O": [
        [1, 1],
        [1, 1],
    ],
    "L": [
        [1, 0, 0],
        [1, 1, 1],
    ],
    "I": [
        [1, 1, 1, 1],
    ],
    "S": [
        [1, 1, 0],
        [0, 1, 1],
    ],
}

def draw_shape(shape):
    for line in shape:
        for i in line:
            print("#" if i else ".", end=" ")
        print()
    print()

def rotate_shape(shape):
    w = len(shape)
    h = len(shape[0])
    return [[shape[y][h-1-x] for y in range(w)] for x in range(h)]

def flip_shape(shape):
    w = len(shape)
    h = len(shape[0])
    return [[shape[w-1-x][y] for y in range(h)] for x in range(w)]

def create_data():
    data = [int(sin(randrange(90)*pi/180+pi/4)*255) for _ in range(16)]
    
    blocks = []
    label = choice(list(SHAPES.keys()))
    shape = SHAPES[label]
    rotation = randrange(4)
    for _ in range(rotation):
        shape = rotate_shape(shape)
    flip = randrange(2)
    if flip:
        shape = flip_shape(shape)
    w = len(shape)
    h = len(shape[0])
    x = randrange(4-w+1)
    y = randrange(4-h+1)
    for dx in range(w):
        for dy in range(h):
            if shape[dx][dy] == 1:
                blocks.append((x+dx, y+dy))
    
    for x, y in blocks:
        data[x+4*y] = max(data[x+4*y]-128, 0)

    filter_value = randrange(128)-64
    for x in range(4):
        for y in range(4):
            data[x+4*y] = min(max(data[x+4*y]+filter_value, 0), 255)
    return data, label

if __name__ == "__main__":
    file_name = "data.csv"
    try:
        open(file_name, "r").close()
        print("Data file already exist.")
    except:
        data_file = open(file_name, "w")
        from PIL import Image
        for i in range(8192):
            pixels, label = create_data()
            print(label, *pixels, sep=", ", file=data_file)
            
            # # CREATE IMAGES
            # image = Image.new("L", (4, 4))
            # image.putdata(pixels)
            
            # scaled_image = image.resize((128, 128), resample=Image.NEAREST)
            # scaled_image.save(f"images/image_{i}.png")
        data_file.close()
        print("Data file created.")
            
