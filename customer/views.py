from django.shortcuts import render
from .models import *
import requests
from passlib.hash import pbkdf2_sha256
from django.http import JsonResponse
def home(request):
    return render(request,'customer/homepage/index.html')

def emailpasswordlogin(request):
    emailid = request.GET.get('email')
    password = request.GET.get('password')
    email_details = register.objects.all().filter(email=emailid)
    if password:
        password_deatils = register.objects.all().filter(email=emailid).values_list('password')
    else:
        password_deatils=''
    if not email_details:
        email_data = f'{emailid} Invalid'
    else:
        email_data=False

    if password_deatils:
        encrypt_code = [i for j in password_deatils for i in j]
        verify_code = pbkdf2_sha256.verify(password,encrypt_code[0])
        if verify_code:
            value=False
        else:
            value = ' Password Incorrect '
    else:
        value=False

    info = {'email':email_data,'password':value}
    return JsonResponse(info)
def emailpassword(request):
    emailid = request.GET.get('email')
    phone = request.GET.get('phone')
    email_details = register.objects.all().filter(email=emailid)
    phone_details = register.objects.all().filter(phoneno=phone)
    if email_details:
        email_data = "Email Already exist"
    else:
        email_data=False
    if phone_details:
        phone_data = 'Phone Number already exist'
    else:
        phone_data = False
    info = {'phoneno':phone_data,'emailid':email_data}
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
        check = register.objects.filter(email=email)
        if not check:
            message = 'This is test message'
            send_sms(phone,message)
            customer_details = register(email=email,phoneno=phone,password=hashpassword)
            customer_details.save()
            return render(request,'customer/homepage/index.html')
        else:
            return render(request,'customer/homepage/index.html')
    else:
        return render(request,'customer/homepage/index.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST['emailid']
        password = request.POST['password']
        customer = register.objects.filter(email=email)
        for item in customer:
            request.session['customer-id'] = item.id
        return render(request,'customer/account/index.html')
    else:
        return render(request,'customer/homepage/index.html')

def account_user(request):
    return render(request,'customer/account/index.html')

