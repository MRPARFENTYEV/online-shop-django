from django import forms

class StoreTitleForm(forms.Form):

    Shop_title = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите название магазина'}
        )
    )