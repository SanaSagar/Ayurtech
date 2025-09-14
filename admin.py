from django.contrib import admin
from .models import UserProfile, DoshaQuestion, DoshaOption, UserResponse

class DoshaOptionInline(admin.TabularInline):
    model = DoshaOption
    extra = 1

class DoshaQuestionAdmin(admin.ModelAdmin):
    inlines = [DoshaOptionInline]

admin.site.register(UserProfile)
admin.site.register(DoshaQuestion, DoshaQuestionAdmin)
admin.site.register(UserResponse)
