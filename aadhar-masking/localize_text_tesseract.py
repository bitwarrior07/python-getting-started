# USAGE
# python __init__.py --image test1.jpeg --min-conf 50

# import the necessary packages
from pytesseract import Output
import pytesseract
import argparse
import cv2
import json

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

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


data_list = []
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
	aadhar_data = []
	if conf > args["min_conf"]:
		text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
		print(text)
		# data['confidence'] = conf
		# data['text'] = text
		# data['coordinates'] = [x, y, x + w, y + h]
		data['confidence'] = conf
		data['text'] = text
		data['coordinates'] = [x, y, x + w, y + h]

		# strip out non-ASCII text so we can draw the text on the image
		# using OpenCV, then draw a bounding box around the text along
		# with the text itself
		if len(text) == 4 and text.isdigit():
			cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0),cv2.FILLED)
			# cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
			# 	1.2, (0, 0, 255), 3)
		data_list.append(data)
json_string = json.dumps(data_list)
print(json_string)
cv2.imshow("Image", image)
cv2.imwrite("masked.jpeg", image)
cv2.waitKey(0)
