# Text Board

> 一个快速记录或分享纯文本, 且无审核的开源工具. 你的文本在此将**无加密**地储存在服务器端. Where you can share your text faster. 

我的第二次前端尝试!

> 这次引用了markdown渲染时用到的css, 但是思路明显比上次清晰了.

## Demo

wait

## 用法

fork此仓库或直接clone在本地, 随后修改`app.py`中第七行的`pwd`变量.

> 这是一个密码, 可以加在链接 /pack/ 后面以获取文件列表.

输入指令:

```sh
pip3 install -r requirements.txt
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

之后就OK啦!

## 开发

`app.py`中有部分注释!