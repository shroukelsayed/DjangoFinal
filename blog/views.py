from django.shortcuts import render,render_to_response
from django.http import HttpResponse ,HttpResponseRedirect
from .models import *
from django.conf import settings
import datetime
import os
from django.contrib.auth.models import User
from _mysql import result
from html5lib.treewalkers._base import to_text
from django.contrib.auth import authenticate
from .forms import UserForm
from django.template import RequestContext
from django.db.models import Count
import re
from .forms import *
from random import randint
from django.core.mail import send_mail , BadHeaderError


# Create your views here.
def addArticaleForm(request):
    #adding article is depending on user's rolles --> Sarah
    # user = request.user
    # if user.is_staff or user.is_superuser:
        #Salma
    return render(request, 'blog/addArtical.html')
    # else :
    #     return render(request, 'blog/permissionDenied.html')

def updateArticaleForm(request, articale_id,user_id):
    articale=Articles.objects.get(pk=articale_id)
    #adding article is depending on user's rolles --> Sarah
    # user = request.user
    # if user.is_staff or user.is_superuser:
    return render(request, 'blog/updateArticale.html', {'articale':articale})
    # else :
    #     return render(request, 'blog/permissionDenied.html')

def deleteArticaleForm(request, articale_id):
    #adding article is depending on user's rolles --> Sarah
    # user = request.user
    # if user.is_staff or user.is_superuser:
        #salma
    return render(request, 'blog/deleteArticale.html', {'articale_id':articale_id})
    # else :
    #     return render(request, 'blog/permissionDenied.html')

def addArticale(request):
    content = request.POST['content']
    title = request.POST['title']
    if request.FILES.has_key('img') :
        image = request.FILES['img']
    else:
        image = ''
    c = Articles(article_content=content, article_title=title, article_creationDate=datetime.datetime.now(), article_image=image)
    c.save()
    #adding article is depending on user's rolles --> Sarah
    # user = request.user
    # if user.is_staff or user.is_superuser:
        #Salma
    return render(request, 'blog/addArtical.html')
    # else :
    #     return render(request, 'blog/permissionDenied.html')

#Salma
def updateArticale(request, articale_id):
    articale = Articles.objects.get(pk=articale_id)
    if articale.article_image :
        os.remove(os.path.join(settings.MEDIA_ROOT, articale.article_image.name))
    articale.article_title = request.POST['title']
    articale.article_content = request.POST['content']
    articale.article_image = request.FILES['img']
    articale.save()
    #adding article is depending on user's rolles --> Sarah
    # user = request.user
    # if user.is_staff or user.is_superuser:
        #salma
    articales = Articles.objects.all().order_by('-id')[:5]
    return render(request, 'blog/firstPage.html',{'articales':articales})
    # else :
    #     return render(request, 'blog/permissionDenied.html')

def deleteArticale(request, articale_id):
    articale = Articles.objects.get(pk=articale_id)
    if articale.article_image :
        os.remove(os.path.join(settings.MEDIA_ROOT, articale.article_image.name))
    articale.delete()
    #adding article is depending on user's rolles --> Sarah
    # user = request.user
    # if user.is_staff or user.is_superuser:
        #Salma
    return render(request, 'blog/addArtical.html')
    # else :
    #     return render(request, 'blog/permissionDenied.html')

def selectAllArticales(request):
	articales = Articles.objects.all().order_by('-id')[:5]
	return render(request, 'blog/firstPage.html',{'articales':articales})

def data_singleArticalePage(articale_id,user_id):
    articale = Articles.objects.get(pk=articale_id)
    comments=articale.comments_set.all()
    user=User.objects.get(pk=user_id)
    likes=Comments.objects.filter(article_id__id=articale_id).annotate(num_likes=Count('likes')) # number of users liked each comment in this articale
    isLike=user.likedBy.filter(article_id=articale_id).values_list('id', flat=True)
    return {'articale':articale,'comments':comments,'likes':likes,'isLike':isLike}

def selectAnArticale(request,articale_id,user_id):
    data=data_singleArticalePage(articale_id,user_id)
    return render(request, 'blog/singleArticale.html',data)

def like(request,comment_id,user_id):
    comment=Comments.objects.get(pk=comment_id)
    articale_id=comment.article_id.id
    data=data_singleArticalePage(articale_id,user_id)
    user=User.objects.get(pk=user_id)
    comment.likes.add(user)
    return render(request, "blog/singleArticale.html", data)

def unlike(request,comment_id,user_id):
    comment=Comments.objects.get(pk=comment_id)
    articale_id=comment.article_id.id
    data=data_singleArticalePage(articale_id,user_id)
    user=User.objects.get(pk=user_id)
    comment.likes.remove(user)
    return render(request, "blog/singleArticale.html", data)


def likes2(request,articale_id,user_id):
    articale = Articles.objects.get(pk=articale_id)
    comments=articale.comments_set.all() #all comments on this articale
    user=User.objects.get(pk=user_id)
    isLike=user.likedBy.filter(article_id=articale_id)
    return render(request, "blog/likes.html", {'isLike':isLike})

def baned_words_filteration(massege):
    words=Banwords.objects.all().values('word')
    arr=[]
    for w in words:
        arr.append(' '+w['word']+' ')
    prohibitedWords = ['Some', 'Random', 'Words']
    big_regex = re.compile('|'.join(map(re.escape, arr)),flags=re.IGNORECASE)
    return big_regex.sub("*****", massege)

def addComment(request,articale_id):
    comment = request.POST['comment']
    new_comment = baned_words_filteration(comment)
    articale=Articles.objects.get(pk=articale_id)
    c = Comments(comment_content=new_comment, comment_creationDate=datetime.datetime.now(), article_id=articale)
    c.save()
    data=data_singleArticalePage(articale_id,1)

    return render(request, 'blog/singleArticale.html',data)

def addReply(request,articale_id,comment_id):
    reply = request.POST['reply']
    new_reply=baned_words_filteration(reply)
    articale=Articles.objects.get(pk=articale_id)
    comment=Comments.objects.get(pk=comment_id)
    c = Comments(comment_content=new_reply, comment_creationDate=datetime.datetime.now(), article_id=articale,parent_id=comment)
    c.save()
    data=data_singleArticalePage(articale_id,1)
    return render(request, 'blog/singleArticale.html',data)

# list all users --> Sarah
def listAllUsers(request):
    users = User.objects.all()
    result = "<table border='1'><th>First name</th>"
    result += "<th>Last name</th><th>username</th>"
    result += "<th>email</th><th>Last Login</th>"
    result += "<th>date joined</th><th>is active?</th>"
    result += "<th>is staff?</th><th>is super user?</th>"
    for user in users :
        result += '<tr><td>' + user.first_name + '</td>'
        result += '<td>' + user.last_name + '</td>'
        result += '<td>' + user.username + '</td>'
        result += '<td>' + user.email + '</td>'
        result += '<td>' + to_text(user.last_login) + '</td>'
        result += '<td>' + to_text(user.date_joined) + '</td>'
        result += '<td>' + to_text(user.is_active) + '</td>'
        result += '<td>' + to_text(user.is_staff) + '</td>'
        result += '<td>' + to_text(user.is_superuser) + '</td></tr>'


    result += "<table>"
    return HttpResponse(result)

# Login Part  With Sessions  -->  Shrouk (functions : home,signin)
def signin(request):
    users = User.objects.all()
    try:
        for user in users:
            # check for username and pass in DB ...
            if (user.username == request.POST['u_name'] and user.password == request.POST['pass']):
            # the password verified for the user ...
                if user.is_active:
                    # User is valid, active and authenticated ...
                    #set user session to move around pages ...
                    request.session["user_id"] = user.id
                    #check if the user marked the remember me checkbox to set cookie ...
                    if request.POST.get('remember_me') == "checked":
                        request.session.set_test_cookie()
                        # if request.session.test_cookie_worked():
                        #     print "cookie wokrs"
                        #set user cookie to remember when logged in again ...
                        request.COOKIES['rememberMe'] = request.POST['remember_me']
                    return render(request, 'blog/home.html',{'User':user})
                else:
                    #The password is valid, but the account has been disabled! ...
                    return render(request, 'blog/activeAccount.html')
    except:
        try:
            if "user_id" in request.session :
                return  render(request, 'blog/home.html')
            else:
                return render(request, 'blog/signin.html')
        except:
            return render(request, 'blog/signin.html')
    return render(request, 'blog/register.html')

def home(request):
    #check if the user logged in redirect to home page with a session
    if "user_id" in request.session :
        user_id = request.session["user_id"]
        return  render(request, 'blog/home.html',{'user_id':user_id})
    return render(request,'blog/home.html')

def logout(request):
    #delete user session ...
    del request.session["user_id"]
    #check if there's cookie to delete it  ...
    if request.session.test_cookie_worked():
       request.session.delete_test_cookie()
    return render(request,'blog/signin.html')


#Forget Password Part --> shrouk (functions : randomConfirm ,forgetPass ,confirm )
def randomConfirm(length=3):
    #create random number to send it within an email for user email to set his password ...
    return randint(100**(length-1), (100**(length)-1))

def forgetPass(request):
    form = forgetPassForm(request.POST or None)
   
    if form.is_valid():
        email = form.cleaned_data.get("email")
        userName = form.cleaned_data.get("username")
        global forgetPass_user
        users = User.objects.all()
        try:
            for user in users :
                if user.username == userName :
                    # print user.username
                    # print userName
                    forgetPass_user = userName
                    subject = " Hi ,Somebody recently asked to reset your Facebook password. "
                    global msg
                    msg = str(randomConfirm())
                    fromEmail = settings.EMAIL_HOST_USER
                    toEmail = [email]
                    try:
                        send_mail(subject,msg,fromEmail,toEmail,fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return HttpResponseRedirect('/confirm/',{'User':user})
        except:
            return render(request,'blog/forgetPassword.html',{'form':form })
        return render(request,'blog/forgetPassword.html',{'form':form })
    return render(request,'blog/forgetPassword.html',{'form':form })

def confirm(request):
    form = confirmPassForm(request.POST or None)
    if form.is_valid():
        code = form.cleaned_data.get("code")
        print code
        print msg
        if code == msg :
            return HttpResponseRedirect('/reset/')
    context = {
        "form" : form,
    }
    return render(request,'blog/confirmMail.html',context)

def resetPass(request):
    form = resetPassForm(request.POST or None)
    if form.is_valid():
        password = form.cleaned_data.get("password")
        passwordConf = form.cleaned_data.get("confirmPassword")
        if password == passwordConf :
            user = User.objects.get(username=forgetPass_user)
            user.set_password(password)
            user.save()
            request.session["user_id"] = user.id
            return render(request,'blog/home.html')
       
    context = {
        "form" : form,
    }
    return render(request,'blog/resetPass.html',context) 




def index(request) :
	context = {}
	return render(request,'blog/index.html',context)

def validate(request):

        return render(request,'blog/index.html',context)

def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print user_form.errors
    else:
        user_form=UserForm()

    return render_to_response(
        'blog/register.html',
        {'user_form':user_form,'registered':registered},context
    )



#Sarah
def UserProfile(request, username):
    # get current user
    user = request.user
    newUsername = request.POST['username']
    newEmail = request.POST['email']
    newPassword = request.POST['password']
    u = User(username=newUsername, email=newEmail, password=newPassword)
    u.save()
    return render(request, 'admin/profile.html', {'user':user})