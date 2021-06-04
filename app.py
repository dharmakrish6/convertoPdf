import os
import uuid
from PIL import Image
from werkzeug.utils import secure_filename
from flask import Flask,flash,request,redirect,send_file,render_template

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads/')

#app = Flask(__name__)
app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Upload API
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    sessionId = uuid.uuid1()
    imagelist = []
    if request.method == 'POST' and 'file' in request.files:
        for file in request.files.getlist('file'):
            print(file)
            filename = secure_filename(file.filename)
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            filename=filename.replace("_", " ")
            image1 = Image.open(UPLOAD_FOLDER + filename)
            im1 = image1.convert('RGB')
            imagelist.append(im1)

        #send file name as parameter to downlad
        filename=str(sessionId)+".pdf"
        imagelist.remove(im1)
        im1.save(UPLOAD_FOLDER+filename,save_all=True, append_images=imagelist)
        return redirect('/downloadfile/'+ filename)
    return render_template('upload_file.html')
# Download API
@app.route("/downloadfile/<filename>", methods = ['GET'])
def download_file(filename):
    return render_template('download.html',value=filename)
@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = UPLOAD_FOLDER + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')
@app.route("/about", methods = ['GET'])
def about():
    return render_template('about.html')
if __name__ == "__main__":
    app.run(debug=True)