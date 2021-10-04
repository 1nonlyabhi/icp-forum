from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from users.models import User


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('blog-home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            user = request.user
            if request.user.groups.exists():
                group= request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            elif(user in User.objects.all()):
                messages.success(request, f'Your account has been created for {user}. Follow the verifications process.')
                return redirect('logout')
            elif(user == AnonymousUser()):
                return redirect('login')
            else:
                print(type(user))
                print(user)
                return HttpResponse("You're not authorised to enter the platform.")
        return wrapper_func
    return decorator