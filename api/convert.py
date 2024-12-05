@app.route('/api/convert', methods=['POST'])
def convert_pdf_to_jpg():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    pdf_file = request.files['file']
    if not pdf_file.filename.endswith('.pdf'):
        return jsonify({"error": "File must be a PDF"}), 400

    try:
        # Open the PDF file using PyMuPDF
        pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
        image_data_list = []

        # High-quality rendering: Increase scaling
        zoom_x, zoom_y = 4.0, 4.0  # Increase scaling for higher resolution
        matrix = fitz.Matrix(zoom_x, zoom_y)

        # Convert each page to an image
        for i in range(len(pdf_document)):
            page = pdf_document[i]  # Load the page
            pix = page.get_pixmap(matrix=matrix, alpha=False)  # Render page as RGB
            img_io = BytesIO(pix.tobytes("png"))  # Save image as PNG in memory
            img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
            image_data_list.append({
                'page': i + 1,
                'image': img_base64
            })

        pdf_document.close()  # Close the PDF document

        # Return the JSON response with the Base64-encoded images
        return jsonify({
            "pages": len(image_data_list),
            "images": image_data_list
        }), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
