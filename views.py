from .forms import DoshaForm
from .utils import determine_dosha
from .models import UserProfile, UserResponse, DoshaOption, DoshaQuestion

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')  # Redirect to your dashboard
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    form = AuthenticationForm()
    return render(request, 'dosha_analysis/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in
            messages.success(request, 'Account created successfully!')
            return redirect('home')  # Redirect to home page


    else:
        form = AuthenticationForm()
    return render(request, 'dosha_analysis/signup.html', {'form': form})


def home(request):
    return render(request, 'dosha_analysis/home.html')


def analyze_dosha(request):
    if request.method == 'POST':
        form = DoshaForm(request.POST)
        if form.is_valid():
            # Check if user is logged in
            if request.user.is_authenticated:
                user_profile, created = UserProfile.objects.get_or_create(
                    email=request.user.email,
                    defaults={'name': request.user.username, 'age': form.cleaned_data.get('age')}
                )
            else:
                name = form.cleaned_data.get('name', 'Guest')
                email = form.cleaned_data.get('email', f'guest_{form.cleaned_data.get("age")}@example.com')
                user_profile = UserProfile.objects.create(
                    name=name,
                    email=email,
                    age=form.cleaned_data.get('age'),
                    predominant_dosha=''
                )

            # Determine dosha based on user responses
            dosha_result, vata_score, pitta_score, kapha_score = determine_dosha(request.POST)

            # Save the predominant dosha in UserProfile
            user_profile.predominant_dosha = dosha_result
            user_profile.save()

            # Debugging: Check cleaned_data for available keys
            print("Form cleaned_data:", form.cleaned_data)

            questions = DoshaQuestion.objects.all()
            for question in questions:
                selected_option_id = form.cleaned_data.get(f'option_{question.id}')
                if selected_option_id:
                    try:
                        option = DoshaOption.objects.get(id=selected_option_id)
                        UserResponse.objects.create(
                            user=user_profile,
                            question=question,
                            option=option
                        )
                    except DoshaOption.DoesNotExist:
                        print(f"Option with ID {selected_option_id} does not exist.")

            # Pass the dosha scores to the result template
            context = {
                'dosha': dosha_result,
                'vata_score': vata_score,
                'pitta_score': pitta_score,
                'kapha_score': kapha_score,
            }
            return render(request, 'dosha_analysis/result.html', context)

    else:
        form = DoshaForm()

    return render(request, 'dosha_analysis/analyze.html', {'form': form})



