from django import forms
from django.contrib.auth import get_user_model


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))
    check_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))


    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'avatar',
            'role'
        )
        widgets = {
            'first_name' : forms.widgets.TextInput(attrs={'class': 'form-control mb-3'}),
            'last_name' : forms.widgets.TextInput(attrs={'class': 'form-control mb-3'}),
            'username' : forms.widgets.TextInput(attrs={'class': 'form-control mb-3'}),
            'email' : forms.widgets.EmailInput(attrs={'class': 'form-control mb-3'}),
            'avatar' : forms.widgets.FileInput(attrs={'class': 'form-control mb-3'}),
            'role' : forms.widgets.Select(attrs={'class': 'form-select mb-3'})
        }
    def clean_check_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['check_password']:
            raise forms.ValidationError('Passwords do not match')
        return self.cleaned_data['check_password']

    def save(self, commit=True):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user
