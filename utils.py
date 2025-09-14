# dosha_analysis/utils.py
from .models import DoshaOption,DoshaQuestion

def determine_dosha(post_data):
    # Initialize scores for each dosha
    vata_score = 0
    pitta_score = 0
    kapha_score = 0

    # Loop through questions to count selected dosha types
    for question_index in range(1, 6):  # Assuming you have 5 questions
        selected_option = post_data.get(f'question_{question_index}')
        
        if selected_option:  # Check if there is a selected option
            if selected_option == 'Vata':
                vata_score += 1
            elif selected_option == 'Pitta':
                pitta_score += 1
            elif selected_option == 'Kapha':
                kapha_score += 1

    # Determine predominant dosha
    if vata_score > pitta_score and vata_score > kapha_score:
        predominant_dosha = "Vata"
    elif pitta_score > vata_score and pitta_score > kapha_score:
        predominant_dosha = "Pitta"
    else:
        predominant_dosha = "Kapha"

    return predominant_dosha, vata_score, pitta_score, kapha_score
