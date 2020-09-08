from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .models import *
from passlib.hash import pbkdf2_sha256
from django.http import JsonResponse
from .decorator import *
from django.urls import reverse
import urllib
import json

def emailpass_check(request):
    email = request.GET.get('email')
    password = request.GET.get('pass')
    check = Register.objects.filter(email=email).values_list('password')
    if check:
        email_data = ''
        encrypt_code = [i for j in check for i in j]
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

# def custom_redirect(url_name,args):
#     url = reverse(url_name,args=args)
#     return HttpResponseRedirect(url)

@adminauthentication
def product_common(request):
    if request.method == 'POST':
        name = request.POST['name']
        gender = request.POST['gender']
        details = request.POST['details']
        stylenote = request.POST.get('note')
        shipping = request.POST['shipreturn']
        check = ProductCommon.objects.filter(title=name,gender=gender,productdetail=details,stylenote=stylenote)
        if not check:
            last_productid = ProductCommon.objects.all().last()
            if last_productid:
                id2 = last_productid.productid
                value = id2[3:]
            else:
                value = 1000
            id1 = int(value)+1
            newproductid = f'FAS{id1}'
            common = ProductCommon(productid=newproductid,title=name,gender=gender,productdetail=details,stylenote=stylenote,shippingandreturns=shipping)
            common.save()
            message = newproductid
            return render(request,'admin/dashboard/productcommon.html',{'id':message})
        else:
            exist=True
            return render(request,'admin/dashboard/productcommon.html',{'exist':exist})
    else:
        return render(request,'admin/dashboard/productcommon.html')

@adminauthentication
def product_color(request):
    totalproduct = ProductCommon.objects.all()
    if request.method == 'POST':
        mainid = request.POST['id']         #this id created by database.its used for  add foreign key of this product
        propic = request.FILES['propic']
        pic = request.FILES['pic']
        pic2 = request.FILES['pic2']
        pic3 = request.FILES['pic3']
        color = request.POST['color']
        print(pic)
        check = ProductColor.objects.filter(productcommon=mainid,color=color)
        if not check:
            foriegndata = ProductCommon.objects.get(id=mainid)
            colorid = f'{foriegndata.productid}/{color}'
            color_details = ProductColor(productpicture=propic,productcommon=foriegndata,colorid=colorid,picture=pic,picture2=pic2,picture3=pic3,color=color)
            color_details.save()
            context = {'products':totalproduct,'colorid':colorid,'color':color}
            return render(request,'admin/dashboard/productcolor.html',context)
        else:
            exist = True
            context = {'products':totalproduct,'exist':exist}
            return render(request,'admin/dashboard/productcolor.html',context)
    else:
        context = {'products':totalproduct}
        return render(request,'admin/dashboard/productcolor.html',context)

@adminauthentication
def product_size(request):
    totalproduct = ProductColor.objects.all()
    if request.method == 'POST':
        mainid = request.POST['id']             #this id below to productcolor table.
        size = request.POST['size']             #its used determine which product is want to add different size with price,quntity
        quty = request.POST['qunty']
        price = request.POST['price']
        check = ProductSize.objects.filter(productcolor=mainid,size=size)
        if not check:
            value = ProductColor.objects.get(id=mainid)
            sizeid = f'{value.colorid}/{size}'
            size_deatils = ProductSize(productcolor=value,size=size,quantity=quty,price=price,sizeid=sizeid)
            size_deatils.save()
            context = {'products':totalproduct,'sizeid':sizeid}
            productid = value.productcommon.productid
            check_productid = ProductLists.objects.filter(productid=productid)
            if not check_productid:
                value = ProductSize.objects.filter(productcolor=value,size=size,quantity=quty,price=price,sizeid=sizeid).values_list('id')
                sizeid = [i for j in value for i in j]                                                     #In this condition adding product on Productlists table.if the productid already
                fulldetails = ProductSize.objects.get(id=sizeid[0])                                           #exist in that table its not store . so that way we can add different color and also add different size of same product
                list_details = ProductLists(productfulldetails=fulldetails,productid=productid)            #In home page only have one product . but inside that product have necessary colors and size
                list_details.save()
                return render(request,'admin/dashboard/productsize.html',context)
            else:
                return render(request,'admin/dashboard/productsize.html',context)
        else:
            context = {'products':totalproduct,'exist':True}
            return render(request,'admin/dashboard/productsize.html',context)
    else:
        context = {'products':totalproduct}
        return render(request,'admin/dashboard/productsize.html',context)

def logout(request):
    del request.session['admin-id']
    return redirect('/')



