"""django_project URL Configuration

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
from django.conf.urls import url,include
from django.contrib import admin
from blog.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls')),
    url(r'^addArticale/$', addArticale),
    url(r'^addArticaleForm/$', addArticaleForm),

    url(r'^updateArticale/(?P<articale_id>[0-9]+)$', updateArticale),
    url(r'^updateArticaleForm/(?P<articale_id>[0-9]+)/(?P<user_id>[0-9]+)$', updateArticaleForm),
    url(r'^firstPage/$', selectAllArticales),


    url(r'^deleteArticale/(?P<articale_id>[0-9]+)$', deleteArticale),
    url(r'^deleteArticaleForm/(?P<articale_id>[0-9]+)$', deleteArticaleForm),

    url(r'^selectAllArticales/$', selectAllArticales),
    url(r'^selectAnArticale/(?P<articale_id>[0-9]+)/(?P<user_id>[0-9]+)$', selectAnArticale),

    url(r'^addComment/(?P<articale_id>[0-9]+)$', addComment),
    url(r'^addReply/(?P<articale_id>[0-9]+)/(?P<comment_id>[0-9]+)$', addReply),

    url(r'^images/(?P<path>.*)$', 'django.views.static.serve' , {'document_root': settings.MEDIA_ROOT}),
    
    url(r'^likes/(?P<articale_id>[0-9]+)/(?P<user_id>[0-9]+)$', likes2),
    url(r'^like/(?P<comment_id>[0-9]+)/(?P<user_id>[0-9]+)$', like),
    url(r'^unlike/(?P<comment_id>[0-9]+)/(?P<user_id>[0-9]+)$', unlike),

    #start home page from server index #Sarah
    url(r'^$',home),
    url(r'^profile/(?P<username>[a-zA-Z0-9]+)$', UserProfile),


    # urls of login part  --> shrouk
    url(r'^signin/$',signin),
    url(r'home/$',home),
    url(r'logout/$',logout),
    url(r'forgetPassword/$',forgetPass),
    url(r'confirm/$',confirm),
    url(r'reset/$',resetPass),    
    #api
    url(r'^accounts/', include('allauth.urls')),

]
