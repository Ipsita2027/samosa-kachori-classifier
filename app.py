import os
import io
from PIL import Image
from flask import Flask,render_template,url_for,request,flash,redirect
from fastai.learner import load_learner
from fastai.vision.all import *
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

# Initialize the Flask application
app = Flask(__name__)

# Configuration for the upload folder
# It's good practice to define a dedicated folder for uploads
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE=1837*1024 #bytes
# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Set a secret key for Flask sessions (needed for flash messages)
app.config['MAX_FILE_SIZE']= MAX_FILE_SIZE# In a real application, use a strong, randomly generated key

# Define allowed extensions for image files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

app=Flask(__name__)

@app.route("/")
def upload_image():
    return render_template("home.html")

# Error handler for when the file size limit is exceeded
@app.errorhandler(RequestEntityTooLarge)
def handle_file_size_exceeded(error):
    # flash('File too large. Maximum size is 1837 KB.')
    # Render the index template with an error message
    return render_template('index.html', error_message='File too large. Maximum size is 1837 KB.'), 413

@app.route("/classify",methods=["POST"])
def classify():
    """
    Handle the image upload and save it to the UPLOAD_FOLDER.
    """
    # Check if the POST request has the file part
    if 'image' not in request.files:
        # flash('No file part')
        return redirect(request.url) # In a real app, you might return JSON or an error page

    file = request.files['image']#FileStorage object

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        # flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        # Securely get the filename to prevent directory traversal attacks
        filename = secure_filename(file.filename)
        # Save the file to the specified upload folder
        pred_image_path=os.path.join("uploads","prediction.png")
        file.save(pred_image_path)
        learn=None
        # In a real application, you would now process the image
        # and return classification results.
        # flash("The file uploaded successfully")

        with open(os.path.join(".","artifacts","fastai_resnet34_model.pkl"),"rb") as file:
            learn=load_learner(file)

        label,_,probs=learn.predict(PILImage.create(pred_image_path))          
    
        return render_template("home.html",label=label[:-1])
    else:
        # flash('Allowed image types are: png, jpg, jpeg')
        return '<h1>Invalid file type.</h1><p>Allowed image types are: png, jpg, jpeg.</p>'

if __name__ == '__main__':
    # Run the Flask application in debug mode
    # In production, debug=False and use a production-ready WSGI server
    app.run(host="127.0.0.1",port=4000,debug=True)