from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.shortcuts import render, HttpResponse, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import Profile
from django.conf import settings
import json
from .tokens import account_activation_token


with open("Home/config.json",'r') as auther:
    params = json.load(auther)["some_importent_data"]

def index(request):
    var = {'f':'fi'}
    return  render(request , 'home/index.html',var)

def sign_up(request):
    var = {'f':'fi'}
    if request.method=='POST':
        # getting use details here
        firstname = request.POST.get('fname',' default')
        lname = request.POST.get('lname','')
        password = request.POST.get('password','')
        city = request.POST.get('city','')
        birthdate = request.POST.get('birthdate','22-06-1990')
        email = request.POST.get('email', '')
        email_validation = Profile.objects.filter(email=email)
        if email_validation.exists():
            error = 'entered email is already exits'
            messages.error(request,error)
        else:
            prof = Profile(fname=firstname, lname=lname, email=email,city =city, password=password,birthdate=birthdate,is_active = False)
            Profile.is_active = False
            user = prof.save()
            current_site = get_current_site(request)
            html_content = render_to_string('home/acc_active_email.html', {
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(prof.profile_id)),
            'token': account_activation_token.make_token(user),
            })
            text_content = strip_tags(html_content)
            alt_email = EmailMultiAlternatives(
                'email verficaton',text_content,settings.EMAIL_HOST_USER,[email]
            )
            alt_email.attach_alternative(html_content,'text/html')
            alt_email.send()
            return render(request,'home/verification.html',{'usernam' : firstname})
    return render(request, 'home/sign_up.html',var)


# this function is about mail sending and user verification 
def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = Profile.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Profile.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active=True
        user.save()
        return render(request,'home/index.html',{'signup':'Congratulation you have create your account successfully' })
    else:
        return HttpResponse('Activation link is invalid!')