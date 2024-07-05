from flask import Flask, send_file, after_this_request

from flask_restx import Api, Resource
from flask_cors import CORS
import os

# create basic app with a signle endpoint that sends a pdf file as image to the client
app = Flask(__name__)
CORS(app)
api = Api(app)

from pdf2image import convert_from_path
from PIL import Image

# gets the first page of a pdf file and converts it to an image
def pdf_to_image(pdf_path, output_image_path, dpi=300):
    # Convert the first page of the PDF to an image
    images = convert_from_path(pdf_path, dpi=dpi, first_page=1, last_page=1)
    # Save the image
    images[0].save(output_image_path, 'PNG')
    return output_image_path

@api.route('/cv')
class CV(Resource):
    def get(self):
        img = pdf_to_image("test2.pdf", "cv.png")

        @after_this_request
        def cleanup(response):
            os.remove(img)
            return response

        return send_file(img, mimetype='image/png')

@api.route('/cv_download')
class CV_download(Resource):
    def get(self):
        return send_file("test2.pdf", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')