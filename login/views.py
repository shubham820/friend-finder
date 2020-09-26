import datetime
from django.shortcuts import render,redirect,HttpResponse
from Home.models import Post,Profile,FriendRequest,PostComment
from django.http import JsonResponse
import json
from django.template.loader import render_to_string
import datetime

with open("Home/config.json",'r') as auther:
    params = json.load(auther)["some_importent_data"]

fname = ""
lname = ""
profiles = None
wish = ""
profile_img = None
post_like_counts=0
#main user newsfeed function 
def login(request):
    following = 0
    if request.method == 'POST':
        entered_email = request.POST['email']
        enterde_pass = request.POST['password']
        username_value = Profile.objects.filter(email = entered_email)
        password_value = Profile.objects.filter(password= enterde_pass)
        if username_value.exists():
            if password_value.exists():
                prfl = Profile.objects.get(email = entered_email)
                if prfl.is_active == True:
                    request.session["user"] = prfl.profile_id
                    request.session["email"] = prfl.email
                    # it can be accessed by all the requsts function           
                    global fname,lname,profile_img,profiles
                    fname = prfl.fname
                    lname = prfl.lname
                    profile_img =prfl.profile_image
                    userid = request.session["user"]
                    profiles = Profile.objects.filter(friends=userid)           
                    if request.session.has_key("user"):
                        scc = "you logged in suucessfully"
                        vars = Profile.objects.get(profile_id=userid)
                        request_notification = FriendRequest.objects.filter(to_user = vars)
                        comments = PostComment.objects.filter(reply_of_comnt = None)
                        replys   = PostComment.objects.filter().exclude(reply_of_comnt = None)
                        var = vars.post_set.all()
                        for i in var:
                            print(i.likes.count())
                        global wish
                        hour = int(datetime.datetime.now().hour)
                        if hour >= 0 and hour <12:
                            wish = 'Good Morning'
                        elif hour >= 12 and hour <= 18 :
                            wish = 'Good Afternoon'
                        else:
                            wish = 'Good evening'
                        some_importent_data ={                                        
                                        'profilefname':vars,
                                        'success':scc,
                                        'logout' : params['logout'],
                                        'welcom' : wish,
                                        'friends':profiles,
                                        'following' : following,
                                        'on_login' : params['on_login'],
                                        'login_menu' : params['login_menu'],
                                        'sesion' : var,
                                        'comment' : comments,
                                        'reply' : replys,
                                        'notification':request_notification,
                                        }
                        response = render(request, 'login/newsfeed.html',some_importent_data)
                        response.set_cookie('fname',prfl.email)
                        response.set_cookie('lname',prfl.lname)
                        response.set_cookie('profile_img',prfl.profile_image)
                        return response
                else:
                    Profile.objects.filter(email = entered_email).delete()
                    err1 = {
                            'error1' :'You are not registered',
                            'forgot' : 'Forgot Password' 
                           }
                    return render(request,'home/index.html',err1)
            else:
                err = {'error' :'err', 'forgot' : 'Forgot Password' }
                return render(request,'home/index.html',err)
        else:
            err = {'error': 'err' }
            return render(request,'home/index.html',err)
    # if login request get and browser has cookies then it will run    
    elif request.COOKIES.get('fname'):
        userid = request.session["user"]
        vars   = Profile.objects.get(profile_id=userid)
        request_notification = FriendRequest.objects.filter(to_user = vars)
        var    = vars.post_set.all()
        profiles = Profile.objects.filter(friends=userid) 
        post = Post.objects.filter(id_profile=vars).first()
        comments = PostComment.objects.filter(reply_of_comnt = None)
        replys   = PostComment.objects.filter().exclude(reply_of_comnt = None)
        if request.session.has_key("user"):
            some_importent_data = {
                                'logout' : params['logout'],
                                'on_login' : params['on_login'],
                                'login_menu' : params['login_menu'],
                                'welcom' : wish,
                                'profilefname': vars,
                                'friends':profiles,
                                'following' : following,
                                'sesion' : var,
                                'comment' : comments,
                                'reply' : replys,
                                'notification':request_notification
                                }
        return render(request,'login/newsfeed.html',some_importent_data)
    else:
        return redirect('home')
def forgot_view(request):
    return render(request,'home/verification.html',{'forgot_password':'forget'}) 

def logout_view(request):
    response = redirect('home')
    # response.delete_cookie('fname')
    # response.delete_cookie('lname')
    if "user" in request.session:
        del request.session["user"]
    return response

def post_view(request):
    if request.method == 'POST':
        if request.session.has_key("user"):
            userid = request.session["user"]
            post_text = request.POST['posttext']
            var = Profile.objects.get(profile_id=userid)
            post = Post(id_profile=var,pub_date = datetime.datetime.today(),post_img = "",post_video = "",status = post_text)
            post.save()
        return redirect('login')
    return redirect(f'/profile/')

def delete_post(request):
    return ('login')


def people_nearby(request):
    if request.session.has_key("user"):
        userid = request.session["user"]
        vars   = Profile.objects.get(profile_id=userid)
        request_notification = FriendRequest.objects.filter(to_user = vars)
        var    = vars.post_set.all()
        some_importent_data = {
            'logout' : params['logout'],
            'on_login' : params['on_login'],
            'login_menu' : params['login_menu'],
            'welcom': wish,
            'profilefname': vars,
           
            'nearby': Profile.objects.filter(city = vars.city).exclude(email = vars.email).exclude(friends=userid),
            'friends':profiles,
            'sesion': var,
            
            'notification':request_notification
        }
        return render(request,'login/newsfeed-people-nearby.html',some_importent_data)
    return redirect('home')

def friends_newsfeed(request):
    if request.session.has_key("user"):
        userid = request.session["user"]
        vars   = Profile.objects.get(profile_id=userid)
        var    = vars.post_set.all()
        comments = PostComment.objects.filter(reply_of_comnt = None)
        request_notification = FriendRequest.objects.filter(to_user = vars)
        replys = PostComment.objects.filter().exclude(reply_of_comnt = None)
        some_importent_data = {
            'logout' : params['logout'],
            'on_login' : params['on_login'],
            'login_menu' : params['login_menu'],
            'welcom': wish,
            'profilefname': vars,
            'friends':profiles,
            'sesion': var,
            'reply' : replys,
            'notification':request_notification
        }
        return render(request,'login/newsfeed-friends.html',some_importent_data)
    return redirect('home')

def contact(request):
    if request.session.has_key("user"):
        userid = request.session["user"]
        vars   = Profile.objects.get(profile_id=userid)
        var    = vars.post_set.all()
        some_importent_data = {
            'logout': params['logout'],
            'welcom': wish,
            'on_login': params['on_login'],
            'login_menu': params['login_menu'],
            'friends':profiles,
            'profilefname': vars,
            'sesion': var,

        }
        return render(request,'login/contact.html',some_importent_data )
    return redirect('home')

def about(request):
    if request.session.has_key("user"):
        userid = request.session["user"]
        vars   = Profile.objects.get(profile_id=userid)
        var    = vars.post_set.all()
        some_importent_data = {
            'logout': params['logout'],
            'welcom': wish,
            'on_login': params['on_login'],
            'login_menu': params['login_menu'],
            'friends':profiles,
            'profilefname': vars,
            'sesion': var,
        }
        return render(request, 'login/timeline-about.html', some_importent_data)
    return redirect('home')

def messages(request):
    if request.session.has_key("user"):
        userid = request.session["user"]
        vars   = Profile.objects.get(profile_id=userid)
        var    = vars.post_set.all()
        some_importent_data = {
            'logout': params['logout'],
            'welcom': wish,
            'on_login': params['on_login'],
            'login_menu': params['login_menu'],
            'friends':profiles,
            'profilefname': vars,
            'sesion': var,
        }
        return render(request,'login/newsfeed-messages.html',some_importent_data)
    return redirect('home')

def images(request):
    if request.session.has_key("user"):
        userid = request.session["user"]
        vars = Profile.objects.get(profile_id=userid)
        var = vars.post_set.all()
        some_importent_data = {
            'logout': params['logout'],
            'welcom': wish,
            'on_login': params['on_login'],
            'login_menu': params['login_menu'],
            'friends':profiles,
            'profilefname': vars,
            'sesion': var,
        }
        return render(request, 'login/newsfeed-images.html',some_importent_data)
    return redirect('home')

def videos(request):
    if request.session.has_key("user"):
        userid = request.session["user"]
        vars = Profile.objects.get(profile_id=userid)
        var = vars.post_set.all()
        some_importent_data = {
            'logout': params['logout'],
            'on_login': params['on_login'],
            'login_menu': params['login_menu'],
            'welcom': wish,
            'friends':profiles,
            'profilefname': vars,
            'sesion': var,
        }
        return render(request, 'login/newsfeed-videos.html',some_importent_data)
    return redirect('home')

#friends timeline .html
def anothers_timeline(request,id_name):
    friend = Profile.objects.get(profile_id = id_name)
    if request.session.has_key("user"):
        userid = request.session["user"]
        vars   = Profile.objects.get(profile_id=userid)
        var    = friend.post_set.all()
        comments = PostComment.objects.all()
        some_importent_data = {
            'logout': params['logout'],
            'welcom': wish,
            'login_menu' : params['login_menu'],
            'on_login': params['on_login'],
            'profilefname': vars.fname,
            'friendname': friend,
            'another_sesion': var,
            'comment' : comments
        }
        return render(request,'login/timeline.html',some_importent_data)
    return redirect('home')

def send_request(request,request_id):
    if request.session.has_key("user"):
        userid    = request.session["user"]
        from_user = Profile.objects.get(profile_id=userid)
        to_user   = Profile.objects.get(profile_id = request_id)
        f_request = FriendRequest.objects.get_or_create(from_user=from_user,to_user=to_user)
        return redirect('/profile/people_nearby')
    return HttpResponse("error")

def accept_request(request,request_id):
    if request.session.has_key("user"):
        userid   = request.session["user"]
        user1    = Profile.objects.get(profile_id=userid)
        user2    = Profile.objects.get(profile_id = request_id)
        user1.friends.add(user2)
        user2.friends.add(user1)
        FriendRequest.objects.filter(from_user = user2,to_user=user1).delete()
        return redirect('login')    

def delete_request(request,request_id):   
    if request.session.has_key('user'):
        userid   = request.session["user"]
        user1    = Profile.objects.get(profile_id = userid)
        user2    = Profile.objects.get(profile_id = request_id)
        FriendRequest.objects.filter(from_user = user2,to_user=user1).delete()
    return redirect('login') 

def notify(request):      
    if request.session.has_key("user"):
        userid = request.session["user"]
        vars   = Profile.objects.get(profile_id=userid)
        request_notification = FriendRequest.objects.filter(to_user = vars )
        print(request_notification)
        return render(request,'login/friendrequest.html',{'notification':request_notification})
    return redirect('login')

def post_comment(request):
    if request.method == 'POST':
        userid      = request.session["user"]
        commenter   = Profile.objects.get(profile_id = userid)
        postsno     = request.POST.get('commentSno')
        post        = Post.objects.get(sno=postsno)
        coment      = request.POST.get("comment")
        reply       = request.POST.get("replySno")
        if reply == "":
            comment = PostComment(comment = coment, comment_id = postsno ,user = commenter , post = post)
            comment.save()
        else:
            parent = PostComment.objects.get(sno = reply)
            comment = PostComment(comment = coment,reply_of_comnt = parent ,comment_id = reply,user = commenter , post = post)
            comment.save()
        return HttpResponse(coment)
    return redirect("/profile/")

def post_like(request,post_id):
    if request.session.has_key("user"):
        userid      = request.session["user"]
        user        = Profile.objects.get(profile_id = userid)
        try:
            post   = Post.objects.get(sno = post_id)
            post.likes.add(user)
            post_like_counts=post.likes.count()
            response = post_like_counts
            return HttpResponse(response)
        except Post.DoesNotExist:
            pass
        try:
            comment = PostComment.objects.get(sno = post_id)
            comment.likes.add(user)
            comment_like_counts = comment.likes.count()
            response = comment_like_counts
            return HttpResponse(response)
        except Exception as e:
            pass

        

          
