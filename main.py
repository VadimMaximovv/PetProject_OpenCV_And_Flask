from flask import Flask, render_template, url_for, request, make_response, redirect
from werkzeug.utils import secure_filename
import os
from pathlib import Path

app = Flask(__name__)
  
menu = [{"name": "Распознавание на картинке", "url": "detection-on-image"},
        {"name": "Распознавание на камере", "url": "detection-on-camera"}]

filepath = ""

@app.route("/")
def index():
    if filepath == "":
        print("File is empty")

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

    # if not Self.__user['avatar']:
    #     try:
    #         with app.open_resource(app.root_path + url_for('static', filename='images/default.png'), "rb") as f:
    #             img = f.read()
    #     except FileNotFoundError as e:
    #         print("Не найден аватар по умолчанию: "+str(e))
    # else:
    #     img = Self.__user['avatar']
 
    # return img
    
    # img = current_user.getAvatar(app)
    # if not img:
    #     return ""
 
    # h = make_response(img)
    # h.headers['Content-Type'] = 'image/png'
    # return h

@app.route('/upload', methods=["POST", "GET"])
def upload():
    global filepath
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.root_path + url_for('static', filename='tempImages'), filename)
        file.save(filepath)
        print("Файл загружен " + str(filepath))
    return redirect(url_for('index'))

# def cleanUpTempFolder():
#     with app.app_context():
#         tempFolder = app.root_path + url_for('static', filename='tempImages')
  
#     # folder = app.root_path + url_for('static', filename='tempImages')
#     for item in tempFolder.iterdir():
#         if item.is_file():
#             item.unlink()

# import atexit

# def on_exit():
#     cleanUpTempFolder()
#     print("Приложение Flask завершает работу...")

# atexit.register(on_exit)

if __name__ == "__main__":
    app.run(debug=True)