from django import forms
from shop.models import Product


class StoreTitleForm(forms.Form):

    Shop_title = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите название магазина'}
        )
    )

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # fields = '__all__'
        fields = ['avaliable']

# class EditProfileForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['full_name', 'email']