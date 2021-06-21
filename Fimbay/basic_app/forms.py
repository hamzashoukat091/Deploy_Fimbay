from django import forms
from django.core import validators
from django.contrib.auth.models import User
from basic_app.models import UserProfileInfo


class UserForm(forms.ModelForm):
    # vendor = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Email already Exists!')
        return email

    def clean(self):
        clean_data = super(UserForm, self).clean()
        password = clean_data.get('password')
        v_password = clean_data.get('confirm_password')

        SpecialSym =['!','$', '@', '#', '%']
        val = True

        if len(password) < 8:
            raise forms.ValidationError('length should be at least 8')
            val = False

        if not any(char.isdigit() for char in password):
            raise forms.ValidationError('Password should have at least one numeral')
            val = False

        if not any(char.isupper() for char in password):
            raise forms.ValidationError('Password should have at least one uppercase letter')
            val = False

        if not any(char.islower() for char in password):
            raise forms.ValidationError('Password should have at least one lowercase letter')
            val = False

        if not any(char in SpecialSym for char in password):
            raise forms.ValidationError('Password should have at least one of the symbols $,@,#,%')
            val = False
        if val:
            val == True

        if password != v_password:
            raise forms.ValidationError('Make sure your Password Match!')
        elif val == False:
            raise forms.ValidationError('Make sure your password contains 8-digits,1-upper,1-lower and 1-specialcharacter!')

    class Meta():
        model = User
        fields = ('username','email','password','confirm_password')

# from django import forms
# from django.core import validators
# from basic_app.models import UserProfile

# def check_for_z(value):
#     if value[0].lower() != 'z':
#         raise forms.ValidationError('Name need to start with z')

# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())
#     verify_password = forms.CharField(label='Enter password again',widget=forms.PasswordInput())
#
#     def clean(self):
#         clean_data = super().clean()
#         password = clean_data['password']
#         v_password = clean_data['verify_password']
#
#         if password != v_password:
#             raise forms.ValidationError('Make sure your Password Match!')
#     class Meta():
#         model = UserProfile
#         fields = '__all__'

    # botcatcher = forms.CharField(required=False,widget=forms.HiddenInput,validators=[validators.MaxLengthValidator(0)])

    # def clean_botcatcher(self):
    #     botcatcher = self.cleaned_data['botcatcher']
    #     if len(botcatcher) > 0:
    #         raise forms.ValidationError('GOTCHA BOT!')
    #     return botcatcher
