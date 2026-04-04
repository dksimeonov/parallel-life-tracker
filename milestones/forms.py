from django import forms

from milestones.models import Milestone


class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ("title", "description", "target_date", "status", "progress")
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Milestone title",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Describe this milestone",
            }),
            "target_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),
            "status": forms.Select(attrs={
                "class": "form-control",
            }),
            "progress": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0,
                "max": 100,
            }),
        }

    def clean_progress(self):
        progress = self.cleaned_data["progress"]
        if progress < 0 or progress > 100:
            raise forms.ValidationError("Progress must be between 0 and 100.")
        return progress