from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator as token_generator
from  django.urls import reverse

from .forms import UserRegistrationForm, UserLoginForm, ManagerLoginForm, EditProfileForm, EditContactForm, ContactForm
from accounts.models import User, Contact
from django.views import View
from django.core.exceptions import ValidationError
from online_shop.settings import EMAIL_HOST_USER
from django.template.loader import get_template
from django.utils.html import format_html
import time
def create_manager():
    """
    to execute once on startup:
    this function will call in online_shop/urls.py
    """
    if not User.objects.filter(email="manager@example.com").first():
        user = User.objects.create_user(
            "manager@example.com", 'shop manager','123'
        )
        # give this user manager role
        user.is_manager = True
        user.save()


def confirm_email_notice(request,user): # перенаправление для вывода сообщения о необходимости подтвердить email
    context = {'notice': 'Перейдите по ссылке'}
    current_site = get_current_site(request)
    send_mail('Онлайн магазин - Потный айтишник',
              f'http://{current_site.domain}/accounts/verify_email/{urlsafe_base64_encode(force_bytes(user.pk))}/{token_generator.make_token(user)}',
              EMAIL_HOST_USER, [user.email])
    return render(request, 'confirm_email.html',context)


def manager_login(request):
    if request.method == 'POST':
        form = ManagerLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, email=data['email'], password=data['password']
            )
            if user is not None and user.is_manager:
                login(request, user)
                return redirect('dashboard:products')
            else:
                messages.error(
                    request, 'username or password is wrong', 'danger'
                )
                return redirect('accounts:manager_login')
    else:
        form = ManagerLoginForm()
    context = {'form': form}
    return render(request, 'manager_login.html', context)

def verify_email(request, uidb64, token):
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        print(user)
        print(token)
        if user is not None and token_generator.check_token(user,token):
            print('Hurra')
            user.email_verify = True
            login(request,user)
            user.save()

            context = {'massage' : 'Почта подтверждена, ура!'}
        else:
            context = {'massage': 'Ключ неверен'}
        return render(request,'verifying_is_done.html',context)


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                data['email'], data['full_name'], data['password'],
            )

            current_site = get_current_site(request)
            send_mail('Онлайн магазин - Потный айтишник',
                      f'http://{current_site.domain}/accounts/verify_email/{urlsafe_base64_encode(force_bytes(user.pk))}/{token_generator.make_token(user)}',
                      EMAIL_HOST_USER, [user.email])
            # confirm_email_notice(request,user)
            context = {'notice': 'Перейдите по ссылке'}
            return render(request, 'confirm_email.html', context)
            # verify_email(request,user)
            # return redirect('accounts:confirm_email_notice',)
    #         send_mail('Онлайн магазин - Потный айтишник',f'Спасибо за регистрацию {user.full_name}',EMAIL_HOST_USER,
    #                   [user.email])
    else:
        form = UserRegistrationForm()
    context = {'title':'Signup', 'form':form}
    return render(request, 'register.html', context)
    #
    #         # return render(request, 'redirect_confirmation.html')
    #         return redirect('accounts:user_login')
    # else:
    #     form = UserRegistrationForm()
    # context = {'title':'Signup', 'form':form}
    # return render(request, 'register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, email=data['email'], password=data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('shop:home_page')
            else:
                messages.error(
                    request, 'Имя или пароль не верны', 'danger'
                )
                return redirect('accounts:user_login')
    else:
        form = UserLoginForm()
    context = {'title':'Login', 'form': form}
    return render(request, 'login.html', context)
def user_contact(request):

    user_post = request.user
    user_adress = Contact.objects.filter(user_id=user_post.id)
    all_adresses = Contact.objects.all()
    if user_adress:
        print(user_adress)
    else: print('create')

    if request.method == 'POST':
        form = EditContactForm()
        data = request.POST
        if user_adress:


            user_adress.update(user=user_post, city=data['city'], street=data['street'], house=data['house'],
                               structure=data['structure'],
                               building=data['building'], apartment=data['apartment'], phone=data['phone'])
        else:
            user_adress.create(user=user_post, city=data['city'], street=data['street'], house=data['house'],
                               structure=data['structure'],
                               building=data['building'], apartment=data['apartment'], phone=data['phone'])
        return redirect('accounts:contact')
    else:
        form = ContactForm()


    context = { 'form': form,'adress': user_adress,}
    return render(request, 'contact.html',context)






def user_logout(request):
    logout(request)
    return redirect('accounts:user_login')


def edit_profile(request):
    print(request.user)

    form = EditProfileForm(request.POST, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Ваш профиль был изменен', 'success')
        return redirect('accounts:edit_profile')
    else:
        form = EditProfileForm(instance=request.user)
    context = {'title':'Edit Profile', 'form':form}
    return render(request, 'edit_profile.html', context)

