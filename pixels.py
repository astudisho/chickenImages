from typing import ClassVar, List, Tuple
from PIL import Image
from enum import IntEnum
import math

# im = Image.open('./imag/(2).png', 'r')
# width, height = im.size
# pixel_values = list(im.getdata())

# for i in range(width):    
#     for j in range(height):
#         print(pixel_values[i*j][:-1],end=',')
#     print('\n')

class BorderSide(IntEnum):
    LEFT = 0
    RIGHT = 1
    UPPER = 2
    BOTTOM = 3

class PixelImage:
    def __init__(self, path ) -> None:
        self.image = Image.open(path, 'r')
        self.width, self.height = self.image.size
        self.pixels = self.image.load()
        self.path = path        
        self.fit = [math.inf] * 4    
        self.fitImage = [None] * 4
        
        self.borders = [None] * 4
        self.position = [None, None]

        self.borders[BorderSide.LEFT] = [self.pixels[0,i][:-1] for i in range(self.width)]
        self.borders[BorderSide.RIGHT] = [self.pixels[-1,i][:-1] for i in range(self.width)]
        self.borders[BorderSide.UPPER] = [self.pixels[i,0][:-1] for i in range(self.width)]
        self.borders[BorderSide.BOTTOM] = [self.pixels[i,-1][:-1] for i in range(self.width)]

    # def GetBorder(self, border):
    #     if(border is BorderSide.LEFT):
    #         return [self.pixels[0,i][:-1] for i in range(self.width)]            

    #     if(border is BorderSide.RIGHT):
    #         return [self.pixels[-1,i][:-1] for i in range(self.width)]
        
    #     if(border is BorderSide.UPPER):
    #         return [self.pixels[i,0][:-1] for i in range(self.width)]

    #     if(border is BorderSide.BOTTOM):
    #         return [self.pixels[i,-1][:-1] for i in range(self.width)]

    def IsBorderBlack(self,borderSide):
        border = self.borders[borderSide]
        result = border == [(0,0,0)] * self.width
        return result

    def BorderFit(self, image2, borderSide):
        borderSide2 = None
        if(borderSide is BorderSide.BOTTOM): borderSide2 = BorderSide.UPPER
        if(borderSide is BorderSide.LEFT): borderSide2 = BorderSide.RIGHT
        if(borderSide is BorderSide.RIGHT): borderSide2 = BorderSide.LEFT
        if(borderSide is BorderSide.UPPER): borderSide2 = BorderSide.BOTTOM

        border1 = self.borders[borderSide]
        border2 = image2.borders[borderSide2]

        sum = 0
        for i in range(len(border1)):
            for j in range(len(border1[0])):
                sum = sum + abs(border1[i][j] - border2[i][j])
        
        if(sum < self.fit[borderSide]):
            self.fit[borderSide] = sum
            self.fitImage[borderSide] = image2

    def __str__(self) -> str:
        return self.path


# pixelImage = PixelImage('./imag/(1).png')
# pixelImage2 = PixelImage('./imag/(2).png')

# lborder = pixelImage.GetBorder(BorderSide.LEFT)

# for i in range(1200):
#     i = i + 1
#     pixelImage = PixelImage(f'./imag/({i}).png')
#     rborder = pixelImage.GetBorder(BorderSide.RIGHT)

#     if(lborder == rborder):
#         print(f'Found !!! {i}')

#     print(f'Lado de imagen {i}')

for side in BorderSide:
    list = [] 
    upperCorner = None
    bottomCorner = None
    for i in range(1200):
        i = i + 1
        pixelImage = PixelImage(f'./imag/({i}).png')

        isBlack = pixelImage.IsBorderBlack(side)
        if(isBlack):
            print(f"Is black {i} side {side}")
            if(pixelImage.IsBorderBlack(BorderSide.UPPER)):
                print(f"{i} is Upper-{side} corner")
                upperCorner = pixelImage
            # if(pixelImage.IsBorderBlack(BorderSide.BOTTOM)):
            #     print(f"{i} is Upper-{side} corner")
                bottomCorner = pixelImage
            list.append(pixelImage)

        # print(f'Lado de imagen negro {i} side {side}')
    print(list, side)

    # Intentar acomodar la orilla
    list.remove(upperCorner)

    selected = upperCorner
    sideFit = BorderSide.BOTTOM
    newImage = Image.new('RGB', (selected.width, selected.height * 30))
    offset = 0
    while len(list) > 0:
        for image in list:
            selected.BorderFit(image, sideFit)
            pass

        # Paste images
        newImage.paste(selected.image, (0, offset * 40))
        offset += 1

        selected = selected.fitImage[sideFit]
        list.remove(selected)
    
    newImage.paste(selected.image, (0, offset * 40))
    newImage.save(f"test{side}.jpg")        

print("No match")

img = PixelImage("./white.png")

img.IsBorderBlack(BorderSide.RIGHT)