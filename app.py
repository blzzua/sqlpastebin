#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
from threading import Thread

from flask import Flask, render_template, redirect, send_from_directory, request, jsonify
from flask_wtf import FlaskForm, CSRFProtect
from telegram import Update
from wtforms import StringField as TextField
from wtforms import StringField
from wtforms.validators import DataRequired

from highlighter import make_image, get_languages, make_doczip
from logic import get_random_bg
from uploader import gen_name_uniq, UPLOAD_DIR

app = Flask(__name__ , static_folder = 'static')
#app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET")
app.config['SECRET_KEY'] = "FLASK_SECRET"
TG_TOKEN = os.environ.get("TG_TOKEN")
csrf = CSRFProtect(app)



class MyForm(FlaskForm):
    language = StringField('language')
    code = TextField("code", validators=[DataRequired()])

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file('favicon.ico')

@app.route('/')
def index_html(): 
    return render_template('index.html')

@app.route('/upload/<path:filename>')
def image(filename):
    return send_from_directory("upload", filename, as_attachment=('download' in request.args))

@app.route("/code", methods=["POST"])
def render_code2():
    app.logger.info('debug print from CODE')
    name = gen_name_uniq(5)
    path = os.path.join(UPLOAD_DIR, name + ".jpg")
    #def make_image(content, output, lang, background, dark=False, matrix=None):
    make_image(content = request.data.decode('utf-8'), output = path, lang = 'Transact-SQL', background=get_random_bg())
    app.logger.info(f"{name=}, {path=}")
    make_doczip(path)
    return jsonify({"key": f"i/{name}"})


@app.route('/i/<path:filename>')
def custom_static(filename):
    if filename.count('.') >=1:
        filename = filename.partition('.')[0]
    path = os.path.join(UPLOAD_DIR, filename + ".jpg")
    if os.path.exists(path):
        return render_template("image.html", image=filename)
    else:
        return render_template("not_found.html"), 404


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run()
