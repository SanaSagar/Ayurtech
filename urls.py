from django.urls import path
from .views import analyze_dosha, home  # Import home view
from . import views

urlpatterns = [
    path('', home, name='home'),  # Home page URL
    path('analyze/', analyze_dosha, name='analyze_dosha'),  # Dosha test URL
    path('login/', views.login_view, name='login'),
    path("signup/", views.signup_view, name='signup'),
]


