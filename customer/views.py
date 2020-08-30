from django.shortcuts import render

def home(request):
    return render(request,'customer/homepage/index.html')
