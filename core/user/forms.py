from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm

from .models import CustomUser, Profile


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Phone Number'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})

        for _, field in self.fields.items():
            field.label = ''

    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number", "password1", "password2") 

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Phone number or Email'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})

        for _, field in self.fields.items():
            field.label = ''

    class Meta:
        fields = ("username", "password")

class CustomUserEditForm(forms.ModelForm):
    first_name = forms.CharField(label='first name', required=False)
    last_name = forms.CharField(label='last name', required=False)
    description = forms.CharField(required=False, widget=forms.Textarea)
    image = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'email']

    def __init__(self, *args, **kwargs):

        
        super(CustomUserEditForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            try:
                profile = self.instance.profile
                self.initial['first_name'] = profile.first_name
                self.initial['last_name'] = profile.last_name
                self.initial['description'] = profile.description
                self.initial['image'] = profile.image
            except Profile.DoesNotExist:
                pass

    def save(self, commit=True):
        user = super(CustomUserEditForm, self).save(commit=False)
        user.save()
        # print(type(user))
        if commit:
            try:
                profile = Profile.objects.get(user=user)
                profile.first_name = self.cleaned_data['first_name']
                profile.last_name = self.cleaned_data['last_name']
                profile.description = self.cleaned_data['description']
                if 'image' in self.cleaned_data:
                    profile.image = self.cleaned_data['image']
                profile.save()
            except Profile.DoesNotExist:
                Profile.objects.create(user=user, first_name=self.cleaned_data['first_name'], last_name=self.cleaned_data['last_name'], description=self.cleaned_data['description'], image=self.cleaned_data['image'])
        
        return user
    
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Old Password', 'class' : 'form-control'}))
    new_password1 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'New Password', 'class' : 'form-control'}))
    new_password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password', 'class' : 'form-control'}))

    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']
