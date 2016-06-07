import flask
from werkzeug import secure_filename
import datetime
import os
# import videoClassify as vC
import timeFusion as tF
import json

app = flask.Flask(__name__)

REPO_DIRNAME = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../..')
print ('>>>: ',REPO_DIRNAME)
UPLOAD_FOLDER = './video'
ALLOWED_VIDEO_EXTENSIONS = set(['avi', 'mp4', 'MOV'])

@app.route('/')
def index():
    return flask.render_template('index.html', has_result=False)

@app.route('/classify_upload', methods=['POST'])
def classify_upload():
    try:
        # We will save the file to disk for possible data collection.
        videofile = flask.request.files['videofile']
        filename_ = secure_filename(videofile.filename)
        filename = os.path.join(UPLOAD_FOLDER, filename_)
        videofile.save(filename)
        print ('Saving to %s.', filename)
        result = tF.getFinal(filename)
    except Exception as err:
        print ('Uploaded image open error: %s', err)
        return flask.render_template(
            'index.html', has_result=True,
            result=(False, 'Cannot open uploaded image.')
        )

    print result
    return json.dumps(result) 

if __name__ == "__main__":
    app.run()

