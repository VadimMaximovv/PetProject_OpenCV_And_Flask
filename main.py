from flask import Flask, render_template, url_for, request

app = Flask(__name__)

menu = [{"name": "Распознавание на картинке", "url": "detection-on-image"},
        {"name": "Распознавание на камере", "url": "detection-on-camera"}]

@app.route("/")
def index():
    return render_template('index.html', menu=menu)

if __name__ == "__main__":
    app.run(debug=True)