import re
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import RegisterForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

# import verification email module
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.
def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            first_name   = form.cleaned_data.get('first_name')
            last_name    = form.cleaned_data.get('last_name')
            email        = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')
            password     = form.cleaned_data.get('password')
            username     = email.split('@')[0]
            
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                username=username,
            )
            user.phone_number = phone_number
            
            user.is_active = True 
            user.save()
            
            messages.success(request, 'Registration successful! You can now login.')
            return redirect('login')
            
        else:
            context = {
                'form': form,
            }
            return render(request, 'accounts/register.html', context)
    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == "POST":
        email    = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user_obj = Account.objects.get(email=email)
        except Account.DoesNotExist:
            messages.error(request, 'Invalid credentials.')
            return redirect('login')
        
        if not user_obj.is_active:
            messages.error(request, 'Please activate your account first. Check your email.')
            return redirect('login')
        
        user = auth.authenticate(request, email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('login')
    
    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account is activated.")
        
        return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def forgotpassword(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            
            # send reset forgot password email
            current_site = get_current_site(request)
            mail_subject = 'Reset your password.'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            messages.success(request, 'Please check your email to reset your password.')
            return redirect('login')
            
        else:
            messages.error(request, 'Account does not exist.')
            return redirect('forgotpassword')
        
    return render(request, 'accounts/forgotpassword.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        
        messages.success(request, "Please reset your password.")
        
        return redirect('resetpassword')
    else:
        messages.error(request, "This link has been expired.")
        
        return redirect('login')

def resetpassword(request):
    if request.method == "POST":
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Password does not match.')
            return redirect('resetpassword')
        else:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Your password has been reset.')
            return redirect('login')         
    else:  
        return render(request, 'accounts/resetpassword.html')

@login_required(login_url='login')
def transactions(request):
    return render(request, 'accounts/transactions.html')

@login_required(login_url='login')
def returns(request):
    return render(request, 'accounts/returns.html')

@login_required(login_url='login')
def settings(request):
    return render(request, 'accounts/settings.html')

@login_required(login_url='login')
def my_selling_items(request):
    return render(request, 'accounts/my_selling_items.html')

@login_required(login_url='login')
def received_orders(request):
    return render(request, 'accounts/received_orders.html')