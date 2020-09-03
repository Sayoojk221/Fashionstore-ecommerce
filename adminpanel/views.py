from django.shortcuts import render,redirect
from .models import *
from passlib.hash import pbkdf2_sha256
from django.http import JsonResponse
from .decorator import *

def emailpass_check(request):
    email = request.GET.get('email')
    password = request.GET.get('pass')
    check = Register.objects.filter(email=email).values_list('password')
    if check:
        email_data = ''
        encrypt_code = [i for j in check for i in j]
        print(encrypt_code[0])
        verify_key = pbkdf2_sha256.verify(password,encrypt_code[0])
        if verify_key:
            password_data = ''
        else:
            password_data = 'Password Incorrect'
    else:
        email_data = f'{email} Invalid'
        password_data = ''

    context = {'email':email_data,'pass':password_data}

    return JsonResponse(context)

@unauthencation
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass']
        admin_details = Register.objects.filter(email=email)
        for item in admin_details:
            request.session['admin-id'] = item.id
        return redirect('/admin/dashboard/')
    else:
        already_Registed = Register.objects.all()
        return render(request,'admin/login/login.html',{'registed':already_Registed})

def registeradmin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass']
        check = Register.objects.all()
        if not check:
            secret_code = pbkdf2_sha256.encrypt(password,rounds=12000,salt_size=32)
            admin_details = Register(email=email,password=secret_code)
            admin_details.save()
            return redirect('/admin/')
        else:
            return redirect('/admin/')
    else:
        return render(request,'admin/login/register.html')

@adminauthentication
def dashboard_admin(request):
    return render(request,'admin/dashboard/index.html')
@adminauthentication
def product_common(request):
    return render(request,'admin/dashboard/productcommon.html')
