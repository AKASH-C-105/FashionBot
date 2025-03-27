from flask import Flask, render_template, request, jsonify
import difflib

app = Flask(__name__)

# Function to suggest similar words if input is not valid
def get_suggestion(user_input, valid_options):
    suggestion = difflib.get_close_matches(user_input, valid_options, n=1, cutoff=0.6)
    return suggestion[0] if suggestion else None

def suggest_outfit(gender, event_type, color, style):
    if gender == "Male":
        if event_type == "Casual":
            return f"A {color} T-shirt with jeans and sneakers for a {style} look."
        elif event_type == "Formal":
            return f"A {color} tailored suit with dress shoes for a {style} style."
        elif event_type == "Party":
            return f"A {color} button-down shirt with chinos for a {style} vibe."
        elif event_type == "Work":
            return f"A {color} blazer with trousers and formal shoes for a {style} look."
        elif event_type == "Outdoor":
            return f"A {color} jacket, cargo pants, and hiking boots for a {style} feel."
        elif event_type == "Date Night":
            return f"A {color} casual blazer with dark jeans for a {style} style."
    
    elif gender == "Female":
        if event_type == "Casual":
            return f"A {color} top with jeans or a skirt for a {style} look."
        elif event_type == "Formal":
            return f"A {color} dress or tailored suit with heels for a {style} style."
        elif event_type == "Party":
            return f"A {color} cocktail dress or jumpsuit with accessories for a {style} vibe."
        elif event_type == "Work":
            return f"A {color} blouse with a pencil skirt or trousers for a {style} work look."
        elif event_type == "Outdoor":
            return f"A {color} waterproof jacket with leggings and hiking boots for a {style} feel."
        elif event_type == "Date Night":
            return f"A {color} chic dress with statement accessories for a {style} vibe."
    
    elif gender == "Unisex":
        if event_type == "Casual":
            return f"A {color} hoodie or oversized T-shirt with jeans for a {style} look."
        elif event_type == "Formal":
            return f"A {color} unisex suit or blazer with versatile shoes for a {style} style."
        elif event_type == "Party":
            return f"A {color} unisex outfit like a jumpsuit or stylish separates for a {style} vibe."
        elif event_type == "Work":
            return f"A {color} business-casual unisex outfit for a {style} work look."
        elif event_type == "Outdoor":
            return f"A {color} windbreaker or parka with outdoor shoes for a {style} adventure."
        elif event_type == "Date Night":
            return f"A {color} relaxed but stylish unisex outfit for a {style} look."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    step = data['step']
    user_input = data['input'].strip().capitalize()
    gender = data.get('gender')
    event_type = data.get('eventType')
    color = data.get('color')
    style = data.get('style')

    if step == 1:
        valid_genders = ["Male", "Female", "Unisex"]
        suggestion = get_suggestion(user_input, valid_genders)
        if user_input in valid_genders:
            response = f"Great! What type of event are you dressing for? (Casual, Formal, Party, Work, Outdoor, Date Night)"
            step = 2
            return jsonify({'response': response, 'step': step, 'gender': user_input})
        elif suggestion:
            response = f"Did you mean '{suggestion}'?"
            return jsonify({'response': response, 'step': step})
        else:
            response = "Please type 'Male', 'Female', or 'Unisex'."
            return jsonify({'response': response, 'step': step})

    elif step == 2:
        # Convert input and valid options to lowercase for better matching
        valid_events = ["Casual", "Formal", "Party", "Work", "Outdoor", "Date Night"]
        user_input_normalized = user_input.lower()
        valid_events_normalized = [event.lower() for event in valid_events]
        
        suggestion = get_suggestion(user_input_normalized, valid_events_normalized)
        if user_input_normalized in valid_events_normalized:
            # Normalize back to the correct case for display
            event_type = valid_events[valid_events_normalized.index(user_input_normalized)]
            response = f"Great choice! What is your preferred color? (e.g., Black, White, Red, Blue, Green, Pink, Yellow, Other)"
            step = 3
            return jsonify({'response': response, 'step': step, 'eventType': event_type, 'gender': gender})
        elif suggestion:
            suggestion_display = valid_events[valid_events_normalized.index(suggestion)]  # Display suggestion in original case
            response = f"Did you mean '{suggestion_display}'?"
            return jsonify({'response': response, 'step': step, 'gender': gender, 'eventType': event_type})
        else:
            response = "Please choose a valid event."
            return jsonify({'response': response, 'step': step, 'gender': gender})
    elif step == 3:
        response = f"Awesome! What style do you prefer? (Modern, Classic, Sporty, Minimalist, Vintage, Bohemian)"
        step = 4
        return jsonify({'response': response, 'step': step, 'color': user_input, 'eventType': event_type, 'gender': gender})

    elif step == 4:
        valid_styles = ["Modern", "Classic", "Sporty", "Minimalist", "Vintage", "Bohemian"]
        suggestion = get_suggestion(user_input, valid_styles)
        if user_input in valid_styles:
            # Suggest the outfit
            outfit_suggestion = suggest_outfit(gender, event_type, color, user_input)
            response = f"Thank you! Based on your choices, \nhere's a suggestion for your outfit:\n\n{outfit_suggestion}\n\nWould you like to continue? (Yes or No)"
            step = 5
            return jsonify({'response': response, 'step': step, 'style': user_input})
        elif suggestion:
            response = f"Did you mean '{suggestion}'?"
            return jsonify({'response': response, 'step': step, 'gender': gender, 'eventType': event_type, 'color': color})
        else:
            response = "Please choose a valid style."
            return jsonify({'response': response, 'step': step, 'gender': gender})

    elif step == 5:
        if user_input.lower() == 'yes':
            response = "Great! Let's start again. Who are you shopping for? (Male, Female, Unisex)"
            step = 1
        elif user_input.lower() == 'no':
            response = "Thank you for using FashionBot! Have a great day!"
            step = 0
        else:
            response = "Please answer with 'Yes' or 'No'."
        return jsonify({'response': response, 'step': step})

    return jsonify({'response': "Sorry, I didn't understand that.", 'step': step})

if __name__ == '__main__':
    app.run(debug=True)
