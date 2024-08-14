from flask import Flask
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration for file uploads
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Debugging: ensure folder exists and print out directory contents
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

print("UPLOAD_FOLDER contents before upload:", os.listdir(UPLOAD_FOLDER))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    image_urls = [url_for('uploaded_file', filename=image) for image in images]
    return render_template('index.html', images=image_urls)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        print("No file part")
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        print("No selected file")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print(f"File saved to {file_path}")
        return redirect(url_for('index'))
    else:
        print("File not allowed")
        return redirect(request.url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


@app.route('/upload', methods=['POST'])
def upload_image():
    data = request.get_json()
    image_data = data.get('image')

    # You can process the image data here (e.g., save it to a file or database)
    # For example, to save it to a file:
    if image_data:
        # Extract the base64 part of the image data URL
        image_base64 = image_data.split(",")[1]
        with open('received_image.png', 'wb') as f:
            f.write(base64.b64decode(image_base64))
        return jsonify({'message': 'Image received and saved'}), 200
    else:
        return jsonify({'error': 'No image data received'}), 400
