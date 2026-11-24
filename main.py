from flask import Flask, render_template, url_for, request, make_response, redirect
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import uuid
from flask import Flask
from flask_caching import Cache

app = Flask(__name__)
app.config["CACHE_TYPE"] = "FileSystemCache"  # или "SimpleCache", "RedisCache"
app.config["CACHE_DIR"] = "/tmp/img-cache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 60*60*24

cache = Cache(app)

CACHE_FOLDER = "/tmp/img-cache"

os.makedirs(CACHE_FOLDER, exist_ok=True)

menu = [{"name": "Распознавание на картинке", "url": "detection-on-image"},
        {"name": "Распознавание на камере", "url": "detection-on-camera"}]

filepath = ""

@app.route("/")
def index():
    return render_template('index.html', menu=menu, title="Main")

@app.route('/loadImage')
def loadImage():
    global filepath
    print("loadImage(), filepath = " + filepath) 
    img = None
    if filepath == "":
        try:
            with app.open_resource(app.root_path + url_for('static', filename='images/default.png'), "rb") as f:
                img = f.read()
        except FileNotFoundError as e:
            print("Не найдена картинка по умолчанию: " + str(e))
    else:
        try:
            with app.open_resource(filepath, "rb") as f:
                img = f.read()
            filepath = ""
        except FileNotFoundError as e:
            print("Не найдена загруженная картинка: " + str(e))

    if not img:
        return ""
     
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h

@app.route('/upload', methods=["POST", "GET"])
def upload():
    global filepath
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            return "Файл не передан", 400

        # Генерируем уникальное имя на диске
        ext = os.path.splitext(file.filename)[1]
        filepath = os.path.join(CACHE_FOLDER, f"{uuid.uuid4().hex}{ext}")
        file.save(filepath)

        # В кэш пишем только путь к файлу
        cache.set(f"filepath:{file.filename}", filepath, timeout=600)
        print({"cached_path": filepath})
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)