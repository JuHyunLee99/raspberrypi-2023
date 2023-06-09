#Flask 웹서버
from flask import Flask, render_template    # Flask 클래스, rendertemplate 함수

app = Flask(__name__)

@app.route('/hello') # http://localhost:5000/hello
def index():
    return render_template('index.html')    # index.html template페이지를 랜더링함.

if __name__ == '__main__':
    app.run(host='localhost', port='8000', debug=True)  # port 8000으로 바꿈
