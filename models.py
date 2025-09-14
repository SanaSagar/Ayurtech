from django.db import models

# Choices for Dosha types
DOSHA_CHOICES = [
    ('Vata', 'Vata'),
    ('Pitta', 'Pitta'),
    ('Kapha', 'Kapha'),
]

# Model to store user profile and dosha result
class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    predominant_dosha = models.CharField(max_length=50)  # Vata, Pitta, or Kapha

    def __str__(self):
        return self.name

# Model to store questions related to Dosha analysis
class DoshaQuestion(models.Model):
    question_text = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text

# Model to store options for each question
class DoshaOption(models.Model):
    question = models.ForeignKey(DoshaQuestion, related_name='options', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)
    dosha_type = models.CharField(max_length=10, choices=DOSHA_CHOICES)

    def __str__(self):
        return f'{self.option_text} ({self.dosha_type})'

# Model to store user responses to questions
class UserResponse(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    question = models.ForeignKey(DoshaQuestion, on_delete=models.CASCADE)
    option = models.ForeignKey(DoshaOption, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} - {self.question.question_text} - {self.option.option_text}"
