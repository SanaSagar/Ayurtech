from django import forms
from django.utils.safestring import mark_safe  # Import mark_safe to handle safe HTML rendering
from .models import UserProfile, DoshaQuestion

class DoshaForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'age']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control text-primary mb-3',
                'placeholder': 'Your Name',
                'id': 'name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control text-primary mb-3',
                'placeholder': 'Your Email',
                'id': 'email'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control text-primary mb-3',
                'placeholder': 'Your Age',
                'id': 'age'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load questions dynamically
        questions = DoshaQuestion.objects.all()
        for question in questions:
            choices = [(option.dosha_type, option.option_text) for option in question.options.all()]
            # Use mark_safe to allow bold HTML in the label
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=mark_safe(f'<strong style="font-size:20px;color:#003a66">{question.question_text}</strong>'),  # Bold label using mark_safe
                choices=choices,
                widget=forms.RadioSelect
            )

        # Create a separate attribute for questions to pass to the template
        self.question_fields = [f'question_{question.id}' for question in questions]
