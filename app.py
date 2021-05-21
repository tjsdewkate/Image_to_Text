import cv2
import pytesseract
import numpy as np
from flask import Flask, request, render_template


pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\Tejas\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'

img_path = "img.jpg"

def ocr(img_path):
    img = cv2.imread(img_path)

    #Alternatively: can be skipped if you have a Blackwhite image
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray, img_bin = cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    gray = cv2.bitwise_not(img_bin)

    kernel = np.ones((2, 1), np.uint8)
    img = cv2.erode(gray, kernel, iterations=1)
    img = cv2.dilate(img, kernel, iterations=1)
    output = pytesseract.image_to_string(img)
    print("OUTPUT:", output)
    return output


app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')


@app.route("/predictRoute", methods=['POST'])
def predictRoute():
    filename = request.files['image']
    print(filename)
    filename.save(img_path)
    print("img saved")
    result = ocr(img_path)
    print(result)
    return render_template('index.html', text=result)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)


