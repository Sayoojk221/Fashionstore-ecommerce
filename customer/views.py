from django.shortcuts import render
from .models import *
import requests
from passlib.hash import pbkdf2_sha256
from django.http import JsonResponse
def home(request):
    return render(request,'customer/homepage/index.html')

def emailpassword(request):
    emailid = request.GET.get('email')
    phone = request.GET.get('phone')
    print(emailid)
    email_details = register.objects.all().filter(email=emailid)
    phone_details = register.objects.all().filter(phoneno=phone)
    if email_details:
        email_data = "Emailid Already exist"
    else:
        email_data=''
    if phone_details:
        phone_data = 'Phone Number already exist'
    else:
        phone_data = ''
    info = {'phone':phone_data,'email':email_data}
    return JsonResponse(info)

def send_sms(phone,message):
    url = "https://www.fast2sms.com/dev/bulk"
    querystring = {
        'authorization':'hv02BN1kYVOqyuftJIzEXC7rlDKF5bcRsowWgjxHiPU398MTASaFKDwsVgUdEZcR4Mk5Yql9mAXuvfjS',
        'sender_id':'FSTSMS',
        'message':message,
        'language':'english',
        'route':'p',
        'number':phone
    }
    headers = {'cache-control':'no-cache'}
    response = requests.request('GET',url,headers=headers, params=querystring)
    return 'SMS send success'

def user_register(request):
    if request.method == 'POST':
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['pass']
        hashpassword = pbkdf2_sha256.encrypt(password,rounds=12000,salt_size=32)
        email_exist = register.objects.all().filter(email=email)
        phone_exist = register.objects.all().filter(phoneno=phone)
        if email_exist:
            return render(request,'customer/homepage/login.html',{'error':email+' already exist'})
        elif phone_exist:
            return render(request,'customer/homepage/login.html',{'error':phone+' already exist'})
        else:
            message = 'This is test message'
            send_sms(phone,message)
            user_details = register(email=email,phoneno=phone,password=hashpassword)
            user_details.save()

            return render(request,'customer/homepage/login.html',{'success':'Successfully Registered'})
    else:
        return render(request,'customer/homepage/login.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST['emailid']
        password = request.POST['password']
        pass_details = register.objects.all().filter(email=email).values_list('password')
        if pass_details:
            encryptkey = [i for j in pass_details for i in j]
            check_password = pbkdf2_sha256.verify(password,encryptkey[0])
            if check_password:
                return render(request,'customer/account/index.html')
            else:
                return render(request,'customer/homepage/login.html',{'error':'Password Incorrect'})

        else:
            return render(request,'customer/homepage/login.html',{'error':email+' Invalid '})
    else:
        return render(request,'customer/homepage/login.html')

def account_user(request):
    return render(request,'customer/account/index.html')
