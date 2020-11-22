from flask import Flask, flash, request, redirect, url_for, make_response
from flask import render_template, send_from_directory, abort, jsonify, json
from werkzeug.utils import secure_filename
import os
import sys
import fitz
import texthero as hero
from texthero import preprocessing
import pandas as pd
from resumeCleaning import process_resume
from recommender import get_recommendations

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Limit upload size to 8mb
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home (index)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Process uploaded resume and
# make recommendations


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file attached in request')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submits an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        elif not allowed_file(file.filename):
            abort(400, 'Incorrect file extension')
            flash('Incorrect file extension. Must be PDF!')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(
                BASE_DIR, app.config['UPLOAD_FOLDER'], filename))

            resume_cleaned = final_resume_clean(os.path.join(
                app.config['UPLOAD_FOLDER'], filename), filename)
            jobs_df = pd.read_csv('cleaned_data.csv')

            global df
            df = get_recommendations(resume_cleaned, jobs_df)

            # Remove diacritics from original job descriptions
            custom_pipeline = [preprocessing.remove_diacritics]
            df['Description'] = hero.clean(
                df['Description'], pipeline=custom_pipeline)

    return render_template("recommendation.html", column_names=df.columns.values, target_column="Company", hide_column="Job Description",
                           row_data=list(df.values.tolist()), zip=zip)
    # return render_template('upload.html')


def final_resume_clean(path, filename):
    input = path
    doc = fitz.open(input)
    resume_text = process_resume(doc)  # from resume cleaning file
    return resume_text


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True)
