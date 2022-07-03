# USAGE
# python localize_text_tesseract.py --image apple_support.png
# python localize_text_tesseract.py --image apple_support.png --min-conf 50

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

		if len(text) == 4 and text.isdigit():
			cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), cv2.FILLED)
			# cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
			# 	1.2, (0, 0, 255), 3)
		data_list.append(data)

		# strip out non-ASCII text so we can draw the text on the image
		# using OpenCV, then draw a bounding box around the text along
		# with the text itself

# def checkAadhar(data_list):
# 	original_str = ''
# 	for i in data_list:
# 		if len(text) == 4 and text.isdigit():
# 			cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), cv2.FILLED)
# 		# cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
# 		# 	1.2, (0, 0, 255), 3)
# 			data_list.append(original_str)
#
#
# 	pass
#checkAadhar(data_list) -> {
    #     "confidence": 96,
    #     "text": "9805",
    #     "coordinates": [
    #         188,
    #         333,
    #         258,
    #         357
    #     ]
    # },
    # {
    #     "confidence": 96,
    #     "text": "8246",
    #     "coordinates": [
    #         270,
    #         332,
    #         340,
    #         356
    #     ]
    # },
    # {
    #     "confidence": 96,
    #     "text": "7998",
    #     "coordinates": [
    #         352,
    #         331,
    #         422,
    #         354
    #     ]
    # }
json_string = json.dumps(data_list)
print(json_string)
cv2.imshow("Image", image)
cv2.imwrite("masked.jpeg", image)
cv2.waitKey(0)

#TODO
# [
#     {
#         "confidence": 95,
#         "text": "",
#         "coordinates": [
#             5,
#             0,
#             626,
#             84
#         ]
#     },
#     {
#         "confidence": 65,
#         "text": "Ig.",
#         "coordinates": [
#             240,
#             89,
#             253,
#             104
#         ]
#     },
#     {
#         "confidence": 35,
#         "text": "Wierveuthds",
#         "coordinates": [
#             266,
#             85,
#             350,
#             104
#         ]
#     },
#     {
#         "confidence": 86,
#         "text": "SD",
#         "coordinates": [
#             192,
#             113,
#             201,
#             126
#         ]
#     },
#     {
#         "confidence": 86,
#         "text": "Yesvanth",
#         "coordinates": [
#             226,
#             112,
#             299,
#             125
#         ]
#     },
#     {
#         "confidence": 96,
#         "text": "Raja",
#         "coordinates": [
#             306,
#             112,
#             340,
#             128
#         ]
#     },
#     {
#         "confidence": 63,
#         "text": "wren",
#         "coordinates": [
#             257,
#             146,
#             295,
#             164
#         ]
#     },
#     {
#         "confidence": 89,
#         "text": "/",
#         "coordinates": [
#             303,
#             147,
#             305,
#             159
#         ]
#     },
#     {
#         "confidence": 91,
#         "text": "DOB",
#         "coordinates": [
#             312,
#             147,
#             348,
#             159
#         ]
#     },
#     {
#         "confidence": 54,
#         "text": ":",
#         "coordinates": [
#             352,
#             141,
#             360,
#             168
#         ]
#     },
#     {
#         "confidence": 96,
#         "text": "07/11/2002",
#         "coordinates": [
#             365,
#             146,
#             452,
#             158
#         ]
#     },
#     {
#         "confidence": 35,
#         "text": "4,",
#         "coordinates": [
#             190,
#             165,
#             209,
#             192
#         ]
#     },
#     {
#         "confidence": 92,
#         "text": "/",
#         "coordinates": [
#             283,
#             172,
#             287,
#             182
#         ]
#     },
#     {
#         "confidence": 96,
#         "text": "Male",
#         "coordinates": [
#             293,
#             171,
#             330,
#             183
#         ]
#     },
#     {
#         "confidence": 96,
#         "text": "2345",
#         "coordinates": [
#             293,
#             171,
#             330,
#             183
#         ]
#     },
#     {
#         "confidence": 95,
#         "text": "",
#         "coordinates": [
#             20,
#             102,
#             626,
#             321
#         ]
#     },
#     {
#         "confidence": 96,
#         "text": "9805",
#         "coordinates": [
#             188,
#             333,
#             258,
#             357
#         ]
#     },
#     {
#         "confidence": 96,
#         "text": "8246",
#         "coordinates": [
#             270,
#             332,
#             340,
#             356
#         ]
#     },
#     {
#         "confidence": 96,
#         "text": "7998",
#         "coordinates": [
#             352,
#             331,
#             422,
#             354
#         ]
#     }
# ]