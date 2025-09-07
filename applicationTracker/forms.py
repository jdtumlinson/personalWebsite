from django import forms
from .models import Application
from django.contrib.auth.models import User


class applicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["company", "domain", "title", "applicationStatus", "dateApplied", "link"]
        widgets = {
            "applicationStatus": forms.Select(attrs={"class": "appStatusDrop"}),
            'company': forms.TextInput(attrs={'id': 'companyInput', 'placeholder': 'Enter company'}),
            'title': forms.TextInput(attrs={'id': 'title', 'placeholder': 'Enter position title'}),
            'domain': forms.HiddenInput(attrs={'id': 'domainInput',}),
            "dateApplied": forms.DateInput(attrs={"type": "date"}),
            "link": forms.URLInput(attrs={"type": "url", "placeholder": "Enter link to application"}),
        }
        
        
        
class loginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=150,
        required=True,
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        required=True,
    )
    
    
    
class createAccountForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=150,
        required=True,
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        required=True,
    )
    confirmPassword = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(),
        required=True,
    )

    # Optional: add validation to check if passwords match
    def clean(self):
        cleaned_data = super().clean()
    
    def clean_password(self):
        password = self.cleaned_data.get("password")
        confirmPassword = self.cleaned_data.get("confirmPassword")
        
        if password != confirmPassword:
            raise forms.ValidationError("Passwords do not match")
        
        return password
        
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists:
            raise forms.ValidationError("This username is already taken")
        return username