from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from accounts.models import Profile

UserModel = get_user_model()


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email address",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your email",
        }),
    )

    display_name = forms.CharField(
        required=False,
        max_length=40,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "How should others see you?",
        })
    )

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ("username", "email", "display_name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Choose a username",
        })
        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Create a password",
        })
        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Repeat your password",
        })

        self.fields["username"].help_text = "Use letters, digits and @/./+/-/_ only."
        self.fields["password1"].help_text = "Your password must be strong and hard to guess."

    def clean_email(self):
        email = self.cleaned_data["email"]
        if UserModel.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your username",
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your password",
        })
    )


class ProfileEditForm(forms.ModelForm):
    display_name = forms.CharField(
        required=False,
        max_length=40,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Display name",
        })
    )
    current_city = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Current city",
        })
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 4,
            "placeholder": "Tell others a bit about yourself",
        })
    )
    birth_year = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Birth year",
        })
    )

    class Meta:
        model = Profile
        fields = ("occupation", "personal_motto", "website", "is_profile_public")
        widgets = {
            "occupation": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Your occupation",
            }),
            "personal_motto": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "A short personal motto",
            }),
            "website": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "https://example.com",
            }),
            "is_profile_public": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }
        labels = {
            "is_profile_public": "Make my profile visible to other users",
        }

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop("user_instance", None)
        super().__init__(*args, **kwargs)

        if self.user_instance:
            self.fields["display_name"].initial = self.user_instance.display_name
            self.fields["current_city"].initial = self.user_instance.current_city
            self.fields["bio"].initial = self.user_instance.bio
            self.fields["birth_year"].initial = self.user_instance.birth_year

    def clean_birth_year(self):
        birth_year = self.cleaned_data.get("birth_year")
        if birth_year:
            if birth_year < 1900:
                raise forms.ValidationError("Birth year cannot be earlier than 1900.")
            if birth_year > 2100:
                raise forms.ValidationError("Birth year cannot be later than 2100.")
        return birth_year

    def save(self, commit=True):
        profile = super().save(commit=False)

        if self.user_instance:
            self.user_instance.display_name = self.cleaned_data.get("display_name", "")
            self.user_instance.current_city = self.cleaned_data.get("current_city", "")
            self.user_instance.bio = self.cleaned_data.get("bio", "")
            self.user_instance.birth_year = self.cleaned_data.get("birth_year")

            if commit:
                self.user_instance.save()

        if commit:
            profile.save()

        return profile