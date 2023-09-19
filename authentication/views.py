from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from django_project import settings
from django.core.mail import send_mail
import datetime
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.cache import cache_control
from django.contrib.sessions.backends.db import SessionStore
# from .models import CustomUser



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    if request.user.is_authenticated:
        fname = request.user.first_name
        return render(request, 'index.html',{'fname': fname})
    return render(request, 'index.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try another username.")
            return redirect("signup")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists! Please try another email.")
            return redirect("signup")
        
        
        myuser = User.objects.create_user(username=username,email=email, password=password)
        myuser.is_active = False
        myuser.save()

        messages.success(request, "Your account has been successfully created.")

        # welcoming email

        # subject = "Welcome to Palleta !!"
        # message = " Hello " + myuser.username +" !! \n" + "Welcome to Palleta !! \n Thank you for visiting our website \n We have also sent you  a confirmation email, please confirm your email address in order to activate your account . \n\n Thanking You \n Abin R "
        # from_email = settings.EMAIL_HOST_USER
        # to_list =[myuser.email]
        # send_mail(subject, message, from_email, to_list, fail_silently=True)

        # # Generate verification token
        # token = default_token_generator.make_token(myuser)

        # # Build verification URL
        # current_site = get_current_site(request)
        # uidb64 = urlsafe_base64_encode(force_bytes(myuser.pk))
        # verification_url = reverse('verify_email', kwargs={'uidb64': uidb64, 'token': token})
        # verification_url = f"{request.scheme}://{current_site}{verification_url}"

        # # Send verification email
        # mail_subject = 'Activate your account'
        # message = render_to_string('verification_email.html', {
        #     'user': myuser,
        #     'verification_url': verification_url
        # })
        # send_mail(mail_subject, message, 'palletacompany@gmail.com', [email])


        
        return redirect('email_confirmation')

    return render(request, "signup.html")

# def verify_email(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         return redirect('signin')

#     # Handle invalid token or user not found
#     return render(request, 'verification_failed.html')




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User does not exist!")
            return redirect('signin')

        # Authenticate using the retrieved user object and provided password
        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            username = user.username
            return render(request, 'index.html', {'username': username})
        else:
            messages.error(request, "Bad credentials!")
            return redirect('signin')

    return render(request, 'signin.html')





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('signin')


@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
def admins(request):
    if request.user.is_superuser:
        if request.GET.get('search') is not None:
            search = request.GET.get('search')
            users = User.objects.filter(username__contains=search)
        else:
            users = User.objects.all()  # Corrected line here
        context = {
            'users': users
        }
        return render(request, 'admin.html', context)
    else:
        return redirect('home')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
def edit_user(request,user_id):
    if request.user.is_superuser:

        user=User.objects.get(id=user_id)
        
        if request.method == 'POST':
            username=request.POST['username']
            email=request.POST['email']
            password=request.POST['password']
            
            user.username=username
            user.email=email
            user.set_password=password
            
            user.save()
            messages.success(request,'Updated succesfully')
            
            return redirect('admins')
        
        return render(request,'edit.html',{'user':user  })
        
    else:
        return redirect('home')


        

@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
def delete_user(request,user_id):
    if request.user.is_superuser:
        
        user=User.objects.get(id=user_id)
        
        if request.method == 'POST':

            user.delete()
            messages.success(request,'user has succesfully deleted')
            return redirect('admins')
        
        
    else:
        return redirect('admins')

@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
def add_user(request):
    if request.user.is_superuser:

        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']

            myuser = User.objects.create_user(username,email,password)
            
            myuser.save()
            messages.success(request,'Account has succesfully created')
            return redirect('admins')
        
        return render(request , 'add_user.html')
    else:
        return redirect('home')
        
def forgot_password(request):
    return render(request, 'forgot_password.html')
def reset_password(request):
    return render(request, 'reset_password.html')
def email_confirmation(request):
    return render(request, 'email_confirmation.html')