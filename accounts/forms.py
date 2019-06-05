from django.contrib.auth import get_user_model
from django.db.models import Q

from django import forms
from django.forms import CharField

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    # first_name = forms.CharField(required=True, label='First Name', widget=forms.CharField)
    # last_name = forms.CharField(required=True, label='Last Name', widget=forms.CharField)
    # location = forms.CharField(widget=forms.CharField)
    # link = forms.URLField(required=True, label='Your website link', widget=forms.CharField)
    # description = forms.CharField(required=True, label='About Yourself', widget=forms.Textarea)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    location = forms.CharField(required=False)
    link = forms.URLField(required=True)
    description = forms.CharField(required=True, widget=forms.Textarea)

    password1 = forms.CharField(required=True, label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(required=True, label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'location', 'link', 'description']

    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.location = self.cleaned_data['location']
        user.link = self.cleaned_data['link']
        user.description = self.cleaned_data['description']

        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    query = forms.CharField(label='Username / Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        query = self.cleaned_data.get('query')
        password = self.cleaned_data.get('password')
        user_qs_final = User.objects.filter(
            Q(username__iexact=query) |
            Q(email__iexact=query)
        ).distinct()
        if not user_qs_final.exists() and user_qs_final.count != 1:
            raise forms.ValidationError("Invalid credentials - user does note exist")
        user_obj = user_qs_final.first()
        if not user_obj.check_password(password):
            raise forms.ValidationError("credentials are not correct")
        self.cleaned_data["user_obj"] = user_obj
        return super(UserLoginForm, self).clean(*args, **kwargs)
