import base64
from io import BytesIO
from flask import Flask, request, jsonify
from pdf2image import convert_from_bytes

app = Flask(__name__)

@app.route('/api/convert', methods=['POST'])
def convert_pdf_to_jpg():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    pdf_file = request.files['file']
    if not pdf_file.filename.endswith('.pdf'):
        return jsonify({"error": "File must be a PDF"}), 400

    try:
        # Convert PDF to images
        images = convert_from_bytes(pdf_file.read())
        image_data_list = []

        # Convert each image to Base64
        for i, image in enumerate(images):
            img_io = BytesIO()
            image.save(img_io, 'JPEG', quality=95)
            img_io.seek(0)

            # Convert image bytes to Base64 and add to list
            img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
            image_data_list.append({
                'page': i + 1,
                'image': img_base64
            })

        # Return a JSON response containing the Base64-encoded images
        return jsonify({
            "pages": len(images),
            "images": image_data_list
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# For local testing
if __name__ == '__main__':
    app.run(debug=True)
