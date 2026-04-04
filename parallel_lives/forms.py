from django import forms

from parallel_lives.models import ParallelLife


class ParallelLifeForm(forms.ModelForm):
    class Meta:
        model = ParallelLife
        fields = (
            "title",
            "divergence_date",
            "starting_choice",
            "summary",
            "visibility",
            "status",
            "realism_score",
            "domains",
        )
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "type": "Give this parallel life a title",
            }),
            "divergence_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),
            "starting_choice": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "What decision changed this life?",
            }),
            "summary": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Summarize this alternate life path",
            }),
            "visibility": forms.Select(attrs={
                "class": "form-control",
            }),
            "status": forms.Select(attrs={
                "class": "form-control",
            }),
            "realism_score": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
                "max": 10,
            }),
            "domains": forms.CheckboxSelectMultiple(),
        }
        labels= {
            "starting_choice": "Turning-point decision",
            "realism_score": "Realism score (1-10)",
        }

    def clean_summary(self):
        summary = self.cleaned_data["summary"]
        if len(summary.strip()) < 20:
            raise forms.ValidationError("Summary must be at least 20 characters long.")
        return summary
