from django import forms

from milestones.models import Milestone


class MilestoneForm(forms.ModelForm):
    parallel_life_title = forms.CharField(
        required=False,
        disabled=True,
        label="Parallel life",
        widget=forms.TextInput(attrs={
            "class": "form-control",
        })
    )

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

    def __init__(self, *args, **kwargs):
        parallel_life = kwargs.pop("parallel_life", None)
        super().__init__(*args, **kwargs)

        if parallel_life:
            self.fields["parallel_life_title"].initial = parallel_life.title
        elif self.instance and self.instance.pk:
            self.fields["parallel_life_title"].initial = self.instance.parralel_life.title

    def clean_progress(self):
        progress = self.cleaned_data["progress"]
        if progress < 0 or progress > 100:
            raise forms.ValidationError("Progress must be between 0 and 100.")
        return progress