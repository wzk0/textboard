import random
import os
import time as ttt
from flask import Flask,render_template,request,send_from_directory

##密码
pwd='123'

app=Flask(__name__,template_folder='./templates',static_folder='./templates/css')

##密钥集
str_all='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

##从密钥集中随机抽取指定长度的字符组成字符串
def get_code(length):
	one=1
	ls=[]
	while one<=length:
		ls.append(random.choice(str_all))
		one+=1
	if ''.join(ls) in os.listdir('data/post'):
		get_code(length)
	else:
		return ls

##分析前端textarea传来的内容, 将第一行删去并得到文件名
def analyse(s):
	try:
		name_all=str(''.join(get_code(6)))+'.'+str(s.split('\n')[0])
		with open('data/post/'+name_all[:-1],'w')as f:
			f.write('\n'.join(s.split('\n')[1:]))
		return name_all
	except:
		return render_template('404.html'),404

##以下是视图函数
@app.route('/',methods=['POST', 'GET'])
def index():
	try:
		if request.method=='POST':
			text=request.form.get('text')
			filename=analyse(text)
			return render_template('result.html',look_url='/look/'+filename,raw_url='/raw/'+filename,filename=filename,last_name=filename.split('.')[-1][:-1])
		return render_template('index.html',num=len(os.listdir('data/post'))-1)
	except:
		return render_template('404.html'),404

@app.route('/look/<string:filename>')
def look(filename):
	try:
		file='data/post/'+filename
		time=ttt.strftime("%Y-%m-%d %H:%M:%S",ttt.localtime(os.path.getctime(file)))
		size=str(os.stat(file).st_size/1000)
		print(size)
		with open(file,'r')as f:
			text=f.read()
		return render_template('look.html',last_name=filename.split('.')[-1],time=time,text=text,filename=filename,size=size+' kB')
	except:
		return render_template('404.html'),404

@app.route('/raw/<string:filename>')
def raw(filename):
	if filename not in os.listdir('data/post'):
		return render_template('404.html'),404
	else:
		return send_from_directory('data/post',filename)		

@app.errorhandler(404)
def pnf(e):
    return render_template('404.html'),404

@app.route('/pack/<string:passwd>')
def packup(passwd):
	global pwd
	if passwd==pwd:
		with open('ls','w')as f:
			f.write('\n'.join(os.listdir('data/post')))
		return send_from_directory('.','ls')
	else:
		return render_template('404.html'),404

if __name__ == "__start__":
    app.run(host='0.0.0.0')