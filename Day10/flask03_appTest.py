from flask import Flask

app = Flask(__name__)

@app.route('/')	# @는 데코레이터
def home():
	return "Flask Server Test"

@app.route('/user/<state>')
def show_username(state):
	if state == 'on':
		return "User : %s" % state
	elif state == 'off':
		return

@app.route('/post/<int:post_id>')
def show_post(post_id):
	return "post %d" % post_id
	
if __name__ == "__main__":
	app.run(host="0.0.0.0", port="8800")

