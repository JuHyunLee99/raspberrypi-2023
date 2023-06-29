from flask import Flask

app = Flask(__name__)

@app.route('/')	# @는 데코레이터
def hello_World():
	return "Hello World"

@app.route('/name')
def namefunc():
	return "Hong kil-dong"
	
if __name__ == "__main__":
	app.run(host="0.0.0.0", port="9000")

