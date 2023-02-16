from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

def register(request):
    uf=Userform()
    pf=Profileform()
    d={'uf':uf,'pf':pf}
    if request.method=='POST' and request.FILES:
        ufd=Userform(request.POST)
        pfd=Profileform(request.POST,request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            ufo=ufd.save(commit=False)
            password=ufd.cleaned_data['password']
            ufo.set_password(password)
            ufo.save()

            pfo=pfd.save(commit=False)
            pfo.profile_user=ufo
            pfo.save()

            send_mail('Registration',
            'Registration is successfully.Thanks for register',
            'muniraji775@gmail.com',
            [ufo.email],
            fail_silently=False)

            return HttpResponse('Registration is successfully')
    return render(request,'register.html',d)

def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        user=authenticate(username=username,password=password)

        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('You are not authendicated user')

    return render(request,'user_login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def display(request):
    un=request.session.get('username')
    uo=User.objects.get(username=un)
    po=Profile.objects.get(profile_user=uo)
    d={'uo':uo,'po':po}
    
    return render(request,'display.html',d)

@login_required
def changepw(request):
    if request.method=='POST':
        pw=request.POST['pw']
        un=request.session.get('username')
        uo=User.objects.get(username=un)
        uo.set_password(pw)
        uo.save()
        return HttpResponse('Password is changed successfully')
    return render(request,'changepw.html')

def forgotpw(request):
    if request.method=='POST':
        un=request.POST['un']
        pw=request.POST['pw']
        luo=User.objects.filter(username=un)
        if luo:
            uo=luo[0]
            uo.set_password(pw)
            uo.save()
            return HttpResponse('Password reset is done successfully')
        else:
            return HttpResponse('User is not present')
    return render(request,'forgotpw.html')