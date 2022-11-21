import random
import os
import time as ttt
import requests
from flask import Flask,render_template,request,send_from_directory,redirect,url_for

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
	name=''.join(ls)
	if name in os.listdir('data/post') or name in os.listdir('data/share'):
		get_code(length)
	else:
		return ls

##检查密码
def check_pwd(name,pwd):
	try:
		with open('data/user/'+name+'/pwd','r')as f:
			if pwd==f.read():
				return True
			else:
				return render_template('login.html',word='您可能正在尝试伪造cookies, 请勿这么做并注册或重新登陆')
	except:
		return render_template('404.html'),404

##分析前端textarea传来的内容, 将第一行删去并得到文件名
def analyse(s,name,pwd):
	try:
		global str_all
		mark_list=[str(s.split('\n')[0])[:-1]]
		for sl in str_all:
			mark_list.append(mark_list[-1].replace(sl,''))
		if mark_list[-1]=='':
			pass
		else:
			for m in mark_list[-1]:
				if m not in ['.','-','_']:
					return False
				else:
					pass
		name_all=str(''.join(get_code(6)))+'.'+str(s.split('\n')[0])[:-1]
		if name==None:
			with open('data/post/'+name_all,'w')as f:
				f.write('\n'.join(s.split('\n')[1:]))
		elif check_pwd(name,pwd):
			with open('data/user/'+name+'/'+name_all,'w')as f:
				f.write('\n'.join(s.split('\n')[1:]))
			os.system('cp data/user/'+name+'/'+name_all+' data/share')
		return name_all
	except:
		return False

##以下是视图函数
@app.route('/',methods=['POST', 'GET'])
def index():
	cookie=request.cookies
	name=cookie.get('name')
	pwd=cookie.get('pwd')
	try:
		if request.method=='POST':
			text=request.form.get('text')
			result=analyse(text,name,pwd)
			if result==False:
				return render_template('404.html'),404
			else:
				filename=result
			if name==None:
				ar=False
			else:
				ar=True
			return render_template('result.html',user_name=name,ar=ar,share_url='/share/'+filename,look_url='/look/'+filename,raw_url='/raw/'+filename,filename=filename,last_name=filename.split('.')[-1])
		if name==None:
			return render_template('index.html',user_num=len(os.listdir('data/user'))-1,stat=True,word='- 尚未注册或登陆',num=len(os.listdir('data/post'))-2+len(os.listdir('data/share')))
		elif check_pwd(name,pwd):
			return render_template('index.html',user_num=len(os.listdir('data/user'))-1,stat=False,word='for '+name,num=len(os.listdir('data/post'))-2+len(os.listdir('data/share')))
	except:
		return render_template('404.html'),404

@app.route('/import',methods=['POST', 'GET'])
def get_index():
	try:
		if request.method=='POST':
			url=request.form.get('url')
			return redirect(url_for('get_raw',url=url))
		return render_template('get.html')
	except:
		return render_template('404.html'),404

@app.route('/get/<path:url>')
def get_raw(url):
	cookie=request.cookies
	name=cookie.get('name')
	pwd=cookie.get('pwd')
	if name==None:
		return render_template('login.html',word='请先登陆或注册')
	elif check_pwd(name,pwd):
		global str_all
		mark_list=[url.split('/')[-1]]
		for sl in str_all:
			mark_list.append(mark_list[-1].replace(sl,''))
		if mark_list[-1]=='':
			pass
		else:
			for m in mark_list[-1]:
				if m not in ['.','-','_']:
					return render_template('404.html'),404
				else:
					pass
		filename=str(''.join(get_code(6)))+'_'+url.split('/')[-1]
		raw_s=requests.get(url).text
		with open('data/user/%s/'%name+filename,'w')as f:
			f.write(raw_s)
		if filename!='pwd':
			os.system('cp data/user/'+name+'/'+filename+' data/share')
		else:
			pass
		return redirect(url_for('look',filename=filename))

@app.route('/about')
def about():
	cookie=request.cookies
	name=cookie.get('name')
	stat=(name!=None)
	try:
		return render_template('about.html',stat=stat,name=name)
	except:
		return render_template('404.html'),404

@app.route('/login')
def log():
	cookie=request.cookies
	name=cookie.get('name')
	pwd=cookie.get('pwd')
	try:
		if name==None:
			return render_template('login.html',word='登陆或注册')
		elif check_pwd(name,pwd):
			return render_template('login.html',word='已经登陆过了, 亲爱的'+name)
	except:
		return render_template('404.html'),404

@app.route('/me')
def me():
	cookie=request.cookies
	name=cookie.get('name')
	pwd=cookie.get('pwd')
	try:
		if name==None:
			return render_template('login.html',word='请先登陆或注册')
		elif check_pwd(name,pwd):
			ls=os.listdir('data/user/'+name)
			ls.remove('pwd')
			if ls==None:
				ls=False
			name=name
			return render_template('me.html',data=ls,name=name)
	except:
		return render_template('404.html'),404

@app.route('/setc',methods=['POST','GET'])
def setc():
	try:
		name=request.form['name']
		global str_all
		mark_list=[name]
		for sl in str_all:
			mark_list.append(mark_list[-1].replace(sl,''))
		if mark_list[-1]=='':
			pass
		else:
			for m in mark_list[-1]:
				if m not in ['.','-','_']:
					return render_template('404.html'),404
				else:
					pass
		pwd=request.form['pwd']
		response=redirect(url_for('index'))
		response.set_cookie('name',name,max_age=2419200)
		response.set_cookie('pwd',pwd,max_age=2419200)
		if os.path.exists('data/user/'+name):
			with open('data/user/'+name+'/pwd','r')as f:
				if pwd==f.read():
					return response
				else:
					return render_template('login.html',word='用户名已存在或密码错误, 请重新注册或登陆')
		else:
			os.system('mkdir data/user/'+name)
			with open('data/user/'+name+'/pwd','w')as f:
				f.write(pwd)
			return response
	except:
		return render_template('404.html'),404

@app.route('/look/<string:filename>')
def look(filename):
	try:
		cookie=request.cookies
		name=cookie.get('name')
		pwd=cookie.get('pwd')
		if name==None:
			file='data/post/'+filename
			stat=True
		elif check_pwd(name,pwd):
			file='data/user/'+name+'/'+filename
			stat=False
		time=ttt.strftime("%Y-%m-%d %H:%M:%S",ttt.localtime(os.path.getctime(file)))
		size=str(os.stat(file).st_size/1000)
		with open(file,'r')as f:
			text=f.read()
		return render_template('look.html',stat=stat,user_name=name,last_name=filename.split('.')[-1],time=time,text=text,filename=filename,size=size+' kB')
	except:
		return render_template('404.html'),404

@app.route('/share/<string:filename>&type=<string:typ>&ar=<string:ar>')
def share(filename,typ,ar):
	try:
		if typ=='raw':
			return send_from_directory('data/share/',filename)
		elif typ=='look':
			file='data/share/'+filename
			time=ttt.strftime("%Y-%m-%d %H:%M:%S",ttt.localtime(os.path.getctime(file)))
			size=str(os.stat(file).st_size/1000)
			with open(file,'r')as f:
				text=f.read()
			return render_template('look.html',stat=True,user_name=ar,last_name=filename.split('.')[-1],time=time,text=text,filename=filename,size=size+' kB')
	except:
		return render_template('404.html'),404

@app.route('/raw/<string:filename>')
def raw(filename):
	cookie=request.cookies
	name=cookie.get('name')
	pwd=cookie.get('pwd')
	if name==None:
		file='data/post/'
	elif check_pwd(name,pwd):
		file='data/user/'+name+'/'
	try:
		with open(file+filename,'r')as f:
			return send_from_directory(file,filename)
	except:
		return render_template('404.html'),404

@app.route('/edit/<string:filename>',methods=['POST','GET'])
def gedit(filename):
	cookie=request.cookies
	name=cookie.get('name')
	pwd=cookie.get('pwd')
	try:
		try:
			with open('data/user/'+name+'/'+filename,'r')as ff:
				raw_s=ff.read()
		except:
			if name==None:
				return render_template('login.html',word='请先注册或登陆')
			else:
				return render_template('login.html',word='无法修改他人分享的文本!')
		if request.method=='POST':
			text=request.form.get('text')
			if name==None:
				return render_template('login.html',word='请先注册或登陆')
			elif check_pwd(name,pwd):
				with open('data/user/'+name+'/'+filename,'w')as f:
					f.write(text)
				if filename!='pwd':
					os.system('cp data/user/'+name+'/'+filename+' data/share')
				else:
					pass
				return redirect(url_for('look',filename=filename))
		return render_template('edit.html',filename=filename,raw_s=raw_s)
	except:
		return render_template('404.html'),404

@app.route('/del/<string:filename>')
def dele(filename):
	cookie=request.cookies
	name=cookie.get('name')
	pwd=cookie.get('pwd')
	try:
		if name==None:
			return render_template('login.html',word='请先注册或登陆')
		elif check_pwd(name,pwd):
			path='data/user/'+name+'/'+filename
			try:
				with open('data/user/%s/'%name+filename,'r')as f:
					f=f.read()
			except:
				return render_template('login.html',word='无法删除他人分享的文本!')
			os.system('rm -rf data/user/%s/'%name+filename)
			os.system('rm -rf data/share/%s'%filename)
			return redirect(url_for('me'))
	except:
		return render_template('404.html'),404

@app.errorhandler(404)
def pnf(e):
	return render_template('404.html'),404

@app.route('/pack/<string:passwd>')
def packup(passwd):
	global pwd
	if passwd==pwd:
		os.system('touch ls.txt && rm ls.txt && tree data >> ls.txt')
		return send_from_directory('.','ls.txt')
	else:
		return render_template('404.html'),404

@app.route('/clear/<string:passwd>')
def clr(passwd):
	global pwd
	if passwd==pwd:
		os.system('rm -rf data/post/* && touch data/post/.init.txt')
		return '完成!'
	else:
		return render_template('404.html'),404

if __name__ == "__start__":
	app.run(host='0.0.0.0')