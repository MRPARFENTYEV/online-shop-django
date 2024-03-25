from django import forms

from .models import User, Contact


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'почта'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'пароль'}
        )
    )

# 'phone'
class UserRegistrationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'почта'}
        )
    )
    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите имя целиком'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'пароль'}
        )
    )

class ManagerLoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'почта'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'пароль'}
        )
    )


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'email']

class EditContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields =['city','street','house','structure','building','apartment','phone']


class ContactForm(forms.Form):
    city = forms.CharField(
        widget=forms.TextInput(
            attrs={ 'visiblity': 'hidden ','placeholder': "Город"}
        )
    )
    street = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': "Улица"}
        )
    )
    house = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': "Дом"}
        )
    )
    structure = forms.CharField(required=False,
                               widget=forms.TextInput(
                                   attrs={'placeholder': "Строение"}
                               ))
    building = forms.CharField(required=False,
        widget=forms.TextInput(
            attrs={'placeholder': "Корпус"}
        )
    )
    apartment = forms.CharField(required=False,
        widget=forms.TextInput(
            attrs={'placeholder': "Квартира"}
        )
    )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': "Телефон"}
        )
    )



