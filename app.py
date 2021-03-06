import os
import uuid
from PIL import Image
from werkzeug.utils import secure_filename
from flask import Flask,flash,request,redirect,send_file,render_template
from pytube import YouTube
import pikepdf

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads/')

#app = Flask(__name__)
app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#error handling
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error.html'), 404
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

@app.route('/password', methods=['GET', 'POST'])
def pdf_password():
    sessionId = uuid.uuid1()
    if request.method == 'POST' and 'file' in request.files:
        usr_password=request.form["password"]
        for file in request.files.getlist('file'):
            filename = secure_filename(file.filename)
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            filename=filename.replace("_", " ")
            
        pdf = pikepdf.open(UPLOAD_FOLDER + filename,password=usr_password)
    
        #send file name as parameter to downlad
        filename=str(sessionId)+".pdf"
        pdf.save(UPLOAD_FOLDER+filename)
        return redirect('/downloadfile/'+ filename)
    return render_template('password.html')

# Download API
@app.route("/downloadfile/<filename>", methods = ['GET'])
def download_file(filename):

    return render_template('download.html',value=filename)
@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = UPLOAD_FOLDER + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')
    # return render_template('/')
@app.route("/youtube", methods=['GET', 'POST'])
def youtube():
    filename = str(uuid.uuid1())
    if request.method == 'POST':
        yurl=request.form["search"]
        yt = YouTube(yurl)
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(UPLOAD_FOLDER,filename)
        return redirect('/downloadfile/'+ filename+".mp4")
    return render_template('about.html')
@app.route("/contact", methods=['GET', 'POST'])
def newtool():
    
    return render_template('contact.html')
if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0')