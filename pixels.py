from typing import ClassVar, List, Tuple
from PIL import Image
from enum import IntEnum
import math
from datetime import datetime

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
        self.position = (None, None)

        self.borders[BorderSide.LEFT] = [self.pixels[0,i][:-1] for i in range(self.width)]
        self.borders[BorderSide.RIGHT] = [self.pixels[-1,i][:-1] for i in range(self.width)]
        self.borders[BorderSide.UPPER] = [self.pixels[i,0][:-1] for i in range(self.width)]
        self.borders[BorderSide.BOTTOM] = [self.pixels[i,-1][:-1] for i in range(self.width)]

        self.scores1 = []
        self.scores2 = []
 
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

    def BorderFit(self, image2, borderSide, mustBeBorder, mustBeBorderSide,image3, borderSide3):

        borderSide2 = getOppositeSide(borderSide)
        

        border1 = self.borders[borderSide]
        border2 = image2.borders[borderSide2]

        if(mustBeBorder):
            isBlack = image2.IsBorderBlack(mustBeBorderSide)
            if not isBlack: return

        sum = 0
        for i in range(len(border1)):
            for j in range(len(border1[0])):
                sum += abs(border1[i][j] - border2[i][j])                

        if image3 is not None:
            borderSide3 = getOppositeSide(borderSide3)
            border3 = image3.borders[borderSide3]

            for i in range(len(border1)):
                for j in range(len(border1[0])):
                    sum += abs(border1[i][j] - border3[i][j])

        if(sum < self.fit[borderSide]):
            self.fit[borderSide] = sum
            self.fitImage[borderSide] = image2

    def BorderFit2(self, image2, borderSide, mustBeBorder, mustBeBorderSide,image3, borderSide3):

        borderSide2 = getOppositeSide(borderSide)
        

        border1 = self.borders[borderSide]
        border2 = image2.borders[borderSide2]

        if(mustBeBorder):
            isBlack = image2.IsBorderBlack(mustBeBorderSide)
            if not isBlack: return

        sum1 = 0
        for i in range(len(border1)):
            for j in range(len(border1[0])):
                sum1 += abs(border1[i][j] - border2[i][j])

        self.scores1.append((sum1, image2))

        if image3 is not None:
            sum2 = 0
            borderSide3 = getOppositeSide(borderSide3)
            border3 = image3.borders[borderSide3]

            for i in range(len(border1)):
                for j in range(len(border1[0])):
                    sum2 += abs(border1[i][j] - border3[i][j])

            self.scores2.append((sum2, image3))

        # if(sum < self.fit[borderSide]):
        #     self.fit[borderSide] = sum
        #     self.fitImage[borderSide] = image2


    def __str__(self) -> str:
        return self.path

def getOppositeSide(borderSide):
    if(borderSide is BorderSide.BOTTOM): return BorderSide.UPPER
    if(borderSide is BorderSide.LEFT): return BorderSide.RIGHT
    if(borderSide is BorderSide.RIGHT): return BorderSide.LEFT
    if(borderSide is BorderSide.UPPER): return BorderSide.BOTTOM

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

def Main():
    def getUpperLeftBorder() -> PixelImage:
        imageList = []
        borderImage = None
        for i in range(1200):
            i = i + 1
            pixelImage = PixelImage(f'./imag/({i}).png')

            if(pixelImage.IsBorderBlack(BorderSide.UPPER) and pixelImage.IsBorderBlack(BorderSide.LEFT)):
                borderimage = pixelImage
            
            imageList.append(pixelImage)
        return imageList, borderimage

    # Initialize variables.
    imageList = []
    assignedList = []
    imageList, borderImage = getUpperLeftBorder()

    selectedImage = borderImage
    # selectedImage.position = (0,0)
    # imageList.remove(selectedImage)
    # assignedList.append(selectedImage)

    # assignedList.append(selectedImage)

    side = BorderSide.BOTTOM
    sideFit = BorderSide.UPPER

    # Initialize
    imageMatrix = [[None] * 30] * 40
    imageList, borderImage = getUpperLeftBorder()

    borderImage.position = (0,0)
    imageList.remove(borderImage)
    imageMatrix[0][0] = borderImage
    side = BorderSide.BOTTOM
    selected = borderImage
    mustBeBorder = False
    assignedList.append(selected)
    selected2 = None
    borderSide2 = BorderSide.LEFT

    # Principal loop.
    for i in range(40):
        for j in range(30):
            if i == 0 and j == 0: continue

            if i == 0:
                mustBeBorder = True
                borderSide = BorderSide.LEFT
                selected2 = None
            elif j == 0:
                mustBeBorder = True
                borderSide = BorderSide.UPPER 
                side = BorderSide.RIGHT
                selected = imageMatrix[i - 1][j]
                selected2 = imageMatrix[i-1][j]
                borderSide2 = BorderSide.LEFT
            elif j == 29:
                mustBeBorder = True
                borderSide = BorderSide.BOTTOM
                selected2 = imageMatrix[i-1][j]
                borderSide2 = BorderSide.LEFT
            elif i == 39:
                mustBeBorder = True
                borderSide = BorderSide.RIGHT
                selected2 = imageMatrix[i-1][j]
                borderSide2 = BorderSide.LEFT
            else:
                side = BorderSide.BOTTOM
                mustBeBorder = False
                selected2 = imageMatrix[i-1][j]
                borderSide2 = BorderSide.LEFT
                
            for image in imageList:
                # selected.BorderFit(image, side, mustBeBorder, borderSide, selected2, borderSide2)
                selected.BorderFit2(image, side, mustBeBorder, borderSide, selected2, borderSide2)                
                pass            
            # image = selected.fitImage[side]
            image = selectFitImage(selected, imageList)

            imageMatrix[i][j] = image
            imageList.remove(image)
            image.position = (i,j)
            assignedList.append(image)
            selected = image            
            
            
    printImage(assignedList)
    # newImage = Image.new('RGB', (40 * 40, 40 * 30))

    # for image in assignedList:
    #     newImage.paste(image.image, (image.position[0] * 40, image.position[1] * 40 ))

    # newImage.save(f"ferberNude-{datetime.timestamp(datetime.now())}.jpg")

def selectFitImage(image, pendingList):
    image.scores1.sort(key= lambda x: x[0])

    if len(image.scores2) == 0: return image.scores1[0][1]

    image.scores2.sort(key = lambda x: x[0])

    lowIndex = math.inf
    selected = None

    for pendingImage in pendingList:
        index1 = math.inf
        for index, im in enumerate(image.scores1):
            if im[1] == pendingImage: 
                index1 = index
                break
        
        index2 = math.inf
        if len(image.scores2) > 0:
            for index, im in enumerate(image.scores1):
                if im[1] == pendingImage: 
                    index2 = index
                    break
            pass
        else: index2 = 0

        avgIndex = (index1 + index2) / 2

        if avgIndex < lowIndex:
            selected = pendingImage

    return selected    
    

def printImage(imgList):
    newImage = Image.new('RGB', (40 * 40, 40 * 30))

    for image in imgList:
        newImage.paste(image.image, (image.position[0] * 40, image.position[1] * 40 ))

    newImage.save(f"ferberNude-{datetime.timestamp(datetime.now())}.jpg")

def printMatrix(matrix):
    newImage = Image.new('RGB', (40 * 40, 40 * 30))

    for list in matrix:
        for image in list:
            if(image is None) : continue
            newImage.paste(image.image, (image.position[0] * 40, image.position[1] * 40 ))

    newImage.save(f"ferberNude-{datetime.timestamp(datetime.now())}.jpg")

def findInList(list, property):
    for obj in list:
        if(obj.position == property): 
            return obj
    

Main()

# for side in BorderSide:
#     list = [] 
#     upperCorner = None
#     bottomCorner = None
#     for i in range(1200):
#         i = i + 1
#         pixelImage = PixelImage(f'./imag/({i}).png')

#         isBlack = pixelImage.IsBorderBlack(side)
#         if(isBlack):
#             print(f"Is black {i} side {side}")
#             if(pixelImage.IsBorderBlack(BorderSide.UPPER)):
#                 print(f"{i} is Upper-{side} corner")
#                 upperCorner = pixelImage
#             # if(pixelImage.IsBorderBlack(BorderSide.BOTTOM)):
#             #     print(f"{i} is Upper-{side} corner")
#                 bottomCorner = pixelImage
#             list.append(pixelImage)

#         # print(f'Lado de imagen negro {i} side {side}')
#     print(list, side)

#     # Intentar acomodar la orilla
#     list.remove(upperCorner)

#     selected = upperCorner
#     sideFit = BorderSide.BOTTOM
#     newImage = Image.new('RGB', (selected.width, selected.height * 30))
#     offset = 0
#     while len(list) > 0:
#         for image in list:
#             selected.BorderFit(image, sideFit)
#             pass

#         # Paste images
#         newImage.paste(selected.image, (0, offset * 40))
#         offset += 1

#         selected = selected.fitImage[sideFit]
#         list.remove(selected)
    
#     newImage.paste(selected.image, (0, offset * 40))
#     newImage.save(f"test{side}.jpg")



# Upper border
side = BorderSide.UPPER
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
sideFit = BorderSide.RIGHT
newImage = Image.new('RGB', (selected.width * 40, selected.height))
offset = 0
while len(list) > 0:
    for image in list:
        selected.BorderFit(image, sideFit)
        pass
    # Paste images
    newImage.paste(selected.image, (offset * 40, 0))
    offset += 1
    selected = selected.fitImage[sideFit]
    list.remove(selected)

newImage.paste(selected.image, (offset * 40, offset * 0))
newImage.save(f"test{side}.jpg")