# USAGE
# python __init__.py --image test1.jpeg --min-conf 50

# import the necessary packages
from pytesseract import Output
import pytesseract
import argparse
import cv2
import re
import json


def is_valid_aadhar_number(aadhar_string):
    # Regex to check valid
    # Aadhaar number.
    regex = ("^[2-9]{1}[0-9]{3}\\" +
             "s[0-9]{4}\\s[0-9]{4}$")

    # Compile the ReGex
    p = re.compile(regex)

    # If the string is empty
    # return false
    if aadhar_string is None:
        return False

    # Return if the string
    # matched the ReGex
    if re.search(p, aadhar_string):
        return True
    else:
        return False


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\tesseract.exe'

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image to be OCR'd")
ap.add_argument("-c", "--min-conf", type=int, default=0,
                help="mininum confidence value to filter weak text detection")
args = vars(ap.parse_args())


def mask_coordinates():
    return 0


# load the input image, convert it from BGR to RGB channel ordering,
# and use Tesseract to localize each area of text in the input image
image = cv2.imread(args["image"])
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

results = pytesseract.image_to_data(rgb, output_type=Output.DICT)
aadhar_str = ''
aadhar_data = []
# loop over each of the individual text localizations
for i in range(0, len(results["text"])):
    # extract the bounding box coordinates of the text region from
    # the current result
    x = results["left"][i]
    y = results["top"][i]
    w = results["width"][i]
    h = results["height"][i]

    # extract the OCR text itself along with the confidence of the
    # text localization
    text = results["text"][i]
    conf = int(float(results["conf"][i]))
    # filter out weak confidence text localizations
    data = {}
    if conf > args["min_conf"]:
        text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
        if len(text) == 4 and text.isdigit():
            data['confidence'] = conf
            data['text'] = text
            data['x'] = x
            data['y'] = y
            data['w'] = w
            data['h'] = h
            aadhar_data.append(data)
        else:
            if len(aadhar_data) == 1:
                aadhar_data.pop()

for i in range(len(aadhar_data)):
    aadhar_str = aadhar_str + ' ' + aadhar_data[i]['text']
print(is_valid_aadhar_number(aadhar_str.strip()))
if is_valid_aadhar_number(aadhar_str.strip()):
    for i in range(len(aadhar_data)):
        x = aadhar_data[i]['x']
        y = aadhar_data[i]['y']
        w = aadhar_data[i]['w']
        h = aadhar_data[i]['h']
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), cv2.FILLED)

json_string = json.dumps(aadhar_data)
print(json_string)
cv2.imshow("Image", image)
cv2.imwrite("masked.jpeg", image)
cv2.waitKey(0)
