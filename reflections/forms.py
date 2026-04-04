from django import forms

from reflections.models import ReflectionEntry


class ReflectionForm(forms.ModelForm):
    class Meta:
        model = ReflectionEntry
        fields = ("title", "content", "mood_score", "is_private")
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Reflection title",
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Write your reflection",
            }),
            "mood_score": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
                "max": 10,
            }),
            "is_private": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }

    def clean_content(self):
        content = self.cleaned_data["content"]
        if len(content.strip()) < 15:
            raise forms.ValidationError("Reflection content must be at least 15 characters long.")
        return content