import base64
import io
import json

from PIL import Image


def ImageToLCDBytesArray(image, width, height, level, invert):
    im = image
    W = width
    H = height

    im = im.resize((W, H), Image.BILINEAR)
    im = im.convert("L")

    imageString = ""
    for y in range(H):
        for x in range(W):
            pixel = im.getpixel((x, y))
            if im.getpixel((x, y)) > level:
                pixel = True
            else:
                pixel = False
            if invert:
                pixel = not pixel
            if (pixel):
                imageString += '1'
            else:
                imageString += '0'

    # L=len(imageString)
    NumberofROW = 16
    x = 0
    for i in range(NumberofROW):
        x = i*96
        print(imageString[x:x+96])

    halfByteArray = []
    numberOfHalfbyte = int(len(imageString)/8)
    x = 0
    for i in range(numberOfHalfbyte):
        x = i*8
        temp = imageString[x:x+8]
        halfByteArray.append(int(temp[::-1], 2))

    hexHead = "0x"
    hexStringArray = ["0", "1", "2", "3", "4", "5", "6",
                      "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    outputString = "{"

    for b in halfByteArray:
        lowerHalf = b & 15
        upperHalf = (b >> 4)
        byteString = hexHead + \
            hexStringArray[upperHalf]+hexStringArray[lowerHalf]+","
        outputString += byteString
    outputString = outputString[:-1]
    outputString += "};"
    return (outputString)


def lambda_handler(event, context):
    img_data = event['imageData']
    imgdata = base64.b64decode(img_data)

    with open('tempfile.jpg', 'wb') as f:
        f.write(imgdata)
    W = event['width']
    H = event['height']
    im = Image.open("tempfile.jpg")
    data = ImageToLCDBytesArray(im, W, H, 100, 0)
    return {
        'statusCode': 200,
        'data': data
    }

