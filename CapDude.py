import pyscreenshot as pss
from flask import Flask, render_template
import qrcode
import socket
import os, time, math
import psutil, shutil
import pyautogui as pgi

app = Flask(__name__)
qrcode.make(socket.gethostbyname(socket.gethostname())+":5000/").show()
app.config['last_path'] = ""

if 'static' in os.listdir():
	shutil.rmtree('static/')
os.mkdir('static')

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/screenshot')
def shot():
	ss_path = os.path.join('static','screenshot'+str(math.floor(time.time()))+'.png')
	pss.grab().save(ss_path)
	# print(ss_path)
	if app.config['last_path'] == "":
		app.config['last_path'] = ss_path
	else:
		os.remove(app.config['last_path'])
		app.config['last_path'] = ss_path
	return render_template('screenshot.html', screenshot=ss_path)

@app.route('/stats')
def stats():
	pct_cpu = psutil.cpu_percent()
	pct_mem = psutil.virtual_memory().percent
	return render_template('stats.html', pct_cpu = pct_cpu, pct_mem = pct_mem)

@app.route('/steer')
def controls():
	return render_template('steer.html')

@app.route('/actions/<act>')
def control(act):
	keys = act.split('_')
	if(keys[0] == 'hotkey'):
		pgi.hotkey(*keys[1:])
	else:
		pgi.press(act)
	return render_template('steer.html')


if __name__ == "__main__":
	app.run(host = '0.0.0.0')

