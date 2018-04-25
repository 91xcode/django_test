```

Django项目：

参考：https://code.ziqiangxuetang.com/django/django-views-urls.html

1.安装软件

	pip install django

	pip install uwsgi

	安装nginx

2.创建一个项目firebase_platform

	django-admin.py startproject firebase_platform

3.新建一个应用（app）

	cd  firebase_platform

	python manage.py startapp crash

4.把我们新定义的app加到settings.py中的INSTALL_APPS中

###################vim firebase_platform/firebase_platform/settings.py###################

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
'crash'
]


###################vim  firebase_platform/crash/urls.py###################

# -*- coding: utf-8 -*-
"""manual_xpath URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import views

urlpatterns = [
    url(r'^list/$', views.list),
    ]

###################vim  firebase_platform/crash/views.py###################

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse


def list(request):
    return HttpResponse(u"欢迎光临 自强学堂!")

###################vim  firebase_platform/firebase_platform/urls.py ################### 
 
 """firebase_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^crash/', include('crash.urls')),
]
###################查看效果###################
 终端执行： python manage.py runserver 0.0.0.0:8000
 浏览器执行：http://127.0.0.1:8000/crash/list/
###################over!!###################






###################确定统一的静态页面和静态资源###################

cd firebase_platform
mkdir templates
mkdir static

在templates目录下 新建app_name的目录放置属于它的静态页面
然后添加vim  firebase_platform/firebase_platform/settings.py
# 模板路径
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

STATICFILES_DIRS = (
os.path.join(BASE_DIR, 'static'),
)


TEMPLATES = [
{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [TEMPLATES_DIR],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
},
]


###################修改 vim  firebase_platform/crash/views.py###################

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,render_to_response

# Create your views here.


from django.http import HttpResponse


def lists(request):
    return HttpResponse(u"欢迎光临 自强学堂!")



def list(request):

    host = request.GET.get('host', '')
    return render_to_response("crash/home.html", locals())


###################tree templates###################

新建目录如下：
templates/
├── base.html
└── crash
    └── home.html



###################uWSGI+Django+Nginx搭建###################

参考：
https://www.cnblogs.com/sumoning/p/7147755.html
https://www.centos.bz/2017/07/centos7-uwsgi-nginx-django-app/

项目流程

首先客户端请求服务资源，
nginx作为直接对外的服务接口,接收到客户端发送过来的http请求,会解包、分析，
如果是静态文件请求就根据nginx配置的静态文件目录，返回请求的资源，
如果是动态的请求,nginx就通过配置文件,将请求传递给uWSGI；uWSGI 将接收到的包进行处理，并转发给wsgi，
wsgi根据请求调用django工程的某个文件或函数，处理完后django将返回值交给wsgi，
wsgi将返回值进行打包，转发给uWSGI，
uWSGI接收后转发给nginx,nginx最终将返回值返回给客户端(如浏览器)。
*注:不同的组件之间传递信息涉及到数据格式和协议的转换

然后 安装uWSGI，Django，Nginx，supervisor


pip install uwsgi
yum install nginx
pip install django
pip install supervisor

###################安装uwsgi出错###################
解决办法：
yum install python-devel


###################测试uwsgi是否安装正常###################
创建test.py文件，添加如下代码
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return "Hello World"
#执行如下代码
uwsgi --http :8001 --wsgi-file test.py

打开浏览器，输入(你的IP):8000看到Hello World代表web client到uWSGI到Python的连接正常。


###################yum 安装supervisor之后###################
echo_supervisord_conf > /etc/supervisord.conf
supervisord -c /etc/supervisord.conf

###################编辑supervisor_conf###################

[program:firebase]
command=uwsgi --ini /home/nahao/firebase_platform/uwsgi_conf.ini
directory=/home/nahao/firebase_platform
startsecs=0


###################vim uwsgi_conf.ini###################

#uwsgi.ini file
[uwsgi]

# Django-related settings
# the base directory (full path)
chdir           = /home/nahao/firebase_platform
# Django's wsgi file
module          = firebase_platform.wsgi
# the virtualenv (full path)
#home            = /path/to/virtualenv
 
# process-related settings
# master
master          = true
# maximum number of worker processes
processes       = 3
# the socket (use the full path to be safe)
#socket          = /home/myself/myself.sock
socket = 127.0.0.1:8001
# ... with appropriate permissions - may be needed
chmod-socket    = 666
chown-socket = root:root
# clear environment on exit
vacuum          = true
enable-threads = true


###################firebase.platform.com.conf###################
server {
    listen      80;
    server_name firebase.platform.com;
    charset     utf-8;
    client_max_body_size 75M;
 
    location /media  {
        alias /home/nahao/firebase_platform/media;
    }
 
    location /static {
        alias /home/nahao/firebase_platform/static;
    }
 
    location / {

        uwsgi_pass  django;
        #uwsgi_pass  unix:///home/nahao/firebase_platform.sock;
        include     /etc/nginx/uwsgi_params;
    }


}


###################访问静态资源 加载图片出错###################
nginx error.log 提示没有权限打开某个文件

解决办法：
是nginx启动的用户不统一 可以修改nginx.conf里面的use nobody nobody











```
