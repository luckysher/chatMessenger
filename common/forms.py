from django import forms
from security.models import ChatUser

class LoginForm(forms.Form):
    username = forms.CharField(label="Username",
                               widget=forms.TextInput(attrs={'placeholder': 'enter username here',
                                                             'class': 'keep-right'}))
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(attrs={'placeholder': 'password',
                                                                 'class': 'keep-right'}))

    class Meta:
        fields = ('username', 'password')


class SignupForm(forms.ModelForm):
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(attrs={'placeholder': 'Enter username for login',
                                                             'class': 'keep-right'}))
    first_name = forms.CharField(label='First name',
                               widget=forms.TextInput(attrs={'placeholder': 'First name',
                                                             'class': 'keep-right'}))
    last_name = forms.CharField(label='Last name',
                               widget=forms.TextInput(attrs={'placeholder': 'Last name',
                                                             'class': 'keep-right'}))
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'keep-right'}))
    password2 = forms.CharField(label='Confirm password',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter password',
                                                                  'class': 'keep-right'}))

    class Meta:
        model = ChatUser
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Password don't match")

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        if commit:
            user.save()
        return user