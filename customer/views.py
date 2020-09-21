from django.shortcuts import render
from .models import *
import requests
from passlib.hash import pbkdf2_sha256
from django.http import JsonResponse
from .decorator import *
from adminpanel.models import *
import uuid
from django.core.serializers import serialize
import json


def customersmacid(request):
    macid = hex(uuid.getnode())
    value = CustomersUniqueId.objects.all().values_list('encryptedid')
    idencrypt = [i for j in value for i in j]
    if idencrypt:
        for item in idencrypt:
            verify = pbkdf2_sha256.verify(macid,item)
            if verify:
                idexist = True
            else:
                idexist = False
        if idexist:
            return JsonResponse({'status':'Failed'})
        else:
            encryt_code = pbkdf2_sha256.encrypt(macid,rounds=12000,salt_size=32)
            CustomersUniqueId.objects.create(encryptedid=encryt_code)
            request.session['unique-id']=encryt_code
            return JsonResponse({'status':'Success'})

    else:
        encryt_code = pbkdf2_sha256.encrypt(macid,rounds=12000,salt_size=32)
        request.session['unique-id']=encryt_code
        CustomersUniqueId.objects.create(encryptedid=encryt_code)
        return JsonResponse({'status':'Success'})



def outofstock():
    value = ProductSize.objects.filter(quantity='0').values_list('productcolor__productcommon__productid')
    if value:
        totalid = [i for j in value for i in j]             #first1 filtering zero coloumn in size table.if have any zero
        out_of_stock = []                                   #row exist , get productid of that row. then check total count of each productid
        for id in totalid:                                  #contain in totalid variable and again check count size created by that productid
            if id not in out_of_stock:                      #if any productid have equel count in both count and totalsize variable.that productid will add to outofstock list
                count = totalid.count(id)
                totalsize = ProductSize.objects.filter(productcolor__productcommon__productid=id).count()
                if count == totalsize:
                    out_of_stock.append(id)
                else:
                    pass
        return out_of_stock
    else:
        out_of_stock = []
        return out_of_stock


def home(request):
    allcloths = ProductLists.objects.all()
    productcolor = ProductColor.objects.all()
    stock = outofstock()
    value = ProductSize.objects.all().values_list('productcolor')
    colorsize = [i for j in value for i in j]
    context = {'cloths':allcloths,'stock':stock,'color':productcolor,'colorsize':colorsize}
    return render(request,'customer/homepage/index.html',context)

def emailpasswordlogin(request):
    emailid = request.GET.get('email')
    password = request.GET.get('password')
    email_details = register.objects.filter(email=emailid)
    if password:
        password_deatils = register.objects.filter(email=emailid).values_list('password')
    else:
        password_deatils=''

    if email_details:
        email_data = False
    else:
        if emailid:
            email_data=f'{emailid} email Invalid'
        else:
            email_data = ''

    if password_deatils:
        encrypt_code = [i for j in password_deatils for i in j]         #here converting database value to list format
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
    email_details = register.objects.filter(email=emailid)
    phone_details = register.objects.filter(phoneno=phone)
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
        'message':message,          #fast2sms api used
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
            register.objects.create(email=email,phoneno=phone,password=hashpassword)
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
        if customer:
            for item in customer:
                request.session['customer-id'] = item.id
            return redirect('/account/')
        else:
            return render(request,'customer/homepage/index.html')
    else:
        return render(request,'customer/homepage/index.html')

@customerauthentication
def account_user(request):
    allcloths = ProductLists.objects.all()
    productcolor = ProductColor.objects.all()
    stock = outofstock()
    value = ProductSize.objects.all().values_list('productcolor')
    colorsize = [i for j in value for i in j]
    context = {'cloths':allcloths,'stock':stock,'color':productcolor,'colorsize':colorsize}
    return render(request,'customer/account/index.html',context)

def product_single(request):
    productid = request.GET.get('id')
    colorid = request.GET.get('id2')
    totalcolors = ProductColor.objects.all()
    totalsize = ProductSize.objects.all().order_by('-size')
    value = ProductSize.objects.all().values_list('productcolor')
    colorsize = [i for j in value for i in j]
    if productid:
        value = ProductLists.objects.filter(productid=productid).values_list('id')
        id = [i for j in value for i in j]
        productdetails = ProductLists.objects.get(id=id[0])
        product_details = ProductSize.objects.filter(productcolor__productcommon__productid=productid,size=productdetails.productfulldetails.size)

    elif colorid:
        product_details = ProductSize.objects.filter(productcolor__colorid=colorid)

    context = {'pro_Details':product_details,'size':totalsize,'color':totalcolors,'colorsize':colorsize}
    return render(request,'customer/homepage/productsingle.html',context)

def product_single_useraccount(request):
    productid = request.GET.get('id')
    colorid = request.GET.get('id2')
    totalcolors = ProductColor.objects.all()
    totalsize = ProductSize.objects.all().order_by('-size')
    value = ProductSize.objects.all().values_list('productcolor')
    colorsize = [i for j in value for i in j]
    if productid:
        value = ProductLists.objects.filter(productid=productid).values_list('id')
        id = [i for j in value for i in j]
        productdetails = ProductLists.objects.get(id=id[0])
        product_details = ProductSize.objects.filter(productcolor__productcommon__productid=productid,size=productdetails.productfulldetails.size)

    elif colorid:
        product_details = ProductSize.objects.filter(productcolor__colorid=colorid)

    context = {'pro_Details':product_details,'size':totalsize,'color':totalcolors,'colorsize':colorsize}
    return render(request,'customer/account/productsingle.html',context)

# def ipencryptedvalue(ip):





def addtocart(request):
    macid = hex(uuid.getnode())
    sizeid = request.GET.get('id')
    value = CustomersUniqueId.objects.all().values_list('encryptedid')
    idencrypt = [i for j in value for i in j]
    for item in idencrypt:
        verify = pbkdf2_sha256.verify(macid,item)
        if verify:
            checkproduct = CartList.objects.filter(productid=sizeid,encryptedid=item)
            if checkproduct:
                return JsonResponse({'status':'item already in cart'})
            else:
                size_details = ProductSize.objects.get(id=sizeid)
                CartList.objects.create(productid=size_details,encryptedid=item)
                return JsonResponse({'status':'item added'})


def uniquecode(macid):
    value = CustomersUniqueId.objects.all().values_list('encryptedid')
    encryptedids = [i for j in value for i in j]
    if encryptedids:
        for item in encryptedids:
            verify = pbkdf2_sha256.verify(str(macid),item)
            if verify:
                code = item
                return code
    else:
        return False


def sidecart(request):
    macid = hex(uuid.getnode())
    code = uniquecode(macid)
    if code:
        cartlists = CartList.objects.filter(encryptedid=code)
        if cartlists:
            productcount = CartList.objects.filter(encryptedid=code).count()
            value = CartList.objects.filter(encryptedid=code).values_list('productid__price')
            pricelist = [i for j in value for i in j]
            totalprice = 0
            for price in pricelist:
                totalprice += int(price)

            value2 = CartList.objects.filter(encryptedid=code).values_list('productid')
            idlist = [i for j in value2 for i in j]
            totallists = []
            for item in idlist:
                productdetails = ProductSize.objects.get(id=item)
                productlist = {}
                productlist['name'] = productdetails.productcolor.productcommon.title
                productlist['link'] = productdetails.productcolor.picture.url
                productlist['price'] = productdetails.price
                productlist['productid'] = productdetails.productcolor.colorid
                productlist['size'] = productdetails.size
                totallists.append(productlist)
            print(totallists)
            info = {'lists':totallists,'count':productcount,'price':totalprice}
            return JsonResponse(info)
        else:
            return JsonResponse({'info':'Cart Empty'})
    else:
        return JsonResponse({'info':'Cart Empty'})
