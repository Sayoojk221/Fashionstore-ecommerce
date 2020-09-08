from django.shortcuts import render,redirect

def customerauthentication(data_fun):
    def check(request):
        if request.session.has_key('customer-id'):
            return data_fun(request)
        else:
            return redirect('/')
    return check
