import flask
from werkzeug import secure_filename
import datetime
import os
import videoClassify as vC
import json

app = flask.Flask(__name__)

REPO_DIRNAME = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../..')
print ('>>>: ',REPO_DIRNAME)
UPLOAD_FOLDER = './video'
ALLOWED_VIDEO_EXTENSIONS = set(['avi', 'mp4', 'MOV'])

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_VIDEO_EXTENSIONS

@app.route('/')
def index():
    return flask.render_template('index.html', has_result=False)

# @app.route('/classify_upload', methods=['POST'])
# def classify_upload():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

@app.route('/classify_upload', methods=['POST'])
def classify_upload():
    try:
        # We will save the file to disk for possible data collection.
        videofile = flask.request.files['videofile']
        filename_ = secure_filename(videofile.filename)
        filename = os.path.join(UPLOAD_FOLDER, filename_)
        videofile.save(filename)
        print ('Saving to %s.', filename)
        # result = vC.classifyVideo(filename)
    except Exception as err:
        print ('Uploaded image open error: %s', err)
        return flask.render_template(
            'index.html', has_result=True,
            result=(False, 'Cannot open uploaded image.')
        )

    result = {'name': 'hello'}
    return flask.render_template(
        'index.html', has_result=True, result=json.dumps(result)
    )

if __name__ == "__main__":
    app.run()