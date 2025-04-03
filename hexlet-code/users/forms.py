from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=False, label='Имя')
    last_name = forms.CharField(required=False, label='Фамилия')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')


class CustomUserChangeForm(forms.ModelForm):
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(), required=False)
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Пароли не совпадают.")
            if len(password1) < 3:
                raise forms.ValidationError("Пароль должен содержать минимум 3 символа.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user