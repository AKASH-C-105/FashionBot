from flask import Flask, render_template, request, jsonify
import difflib

app = Flask(__name__)

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
    user_input = data['input'].strip()
    gender = data.get('gender')
    event_type = data.get('eventType')
    color = data.get('color')
    style = data.get('style')
    last_suggestion = data.get('last_suggestion')
    user_input_lower = user_input.lower()

    # Exit condition (including "they exceed")
    if user_input_lower in ["exit", "quit", "exit.", "quit."]:
        return jsonify({
            'response': "👋 Thank you for chatting with FashionBot! Stay stylish and take care! ✨",
            'step': 0,
            'end': True
        })

    elif user_input_lower == "yes" and last_suggestion:
        user_input = last_suggestion
        last_suggestion = None

    user_input_cap = user_input.capitalize()

    if step == 1:
        valid_genders = ["Male", "Female", "Unisex"]
        suggestion = get_suggestion(user_input_cap, valid_genders)
        if user_input_cap in valid_genders:
            step = 2
            return jsonify({'response': "Great! What type of event are you dressing for? (Casual, Formal, Party, Work, Outdoor, Date Night)", 'step': step, 'gender': user_input_cap})
        elif suggestion:
            return jsonify({'response': f"Did you mean '{suggestion}'?", 'step': step, 'last_suggestion': suggestion})
        else:
            return jsonify({'response': "Please type 'Male', 'Female', or 'Unisex'.", 'step': step})

    elif step == 2:
        valid_events = ["Casual", "Formal", "Party", "Work", "Outdoor", "Date Night"]
        suggestion = get_suggestion(user_input_lower, [e.lower() for e in valid_events])
        if user_input_lower in [e.lower() for e in valid_events]:
            event_type = next(e for e in valid_events if e.lower() == user_input_lower)
            step = 3
            return jsonify({'response': "Great choice! What is your preferred color? (e.g., Black, White, Red, Blue, Green, Pink, Yellow, Other)", 'step': step, 'eventType': event_type, 'gender': gender})
        elif suggestion:
            display = next(e for e in valid_events if e.lower() == suggestion)
            return jsonify({'response': f"Did you mean '{display}'?", 'step': step, 'gender': gender, 'last_suggestion': display})
        else:
            return jsonify({'response': "Please choose a valid event.", 'step': step, 'gender': gender})

    elif step == 3:
        step = 4
        return jsonify({'response': "Awesome! What style do you prefer? (Modern, Classic, Sporty, Minimalist, Vintage, Bohemian)", 'step': step, 'color': user_input, 'eventType': event_type, 'gender': gender})

    elif step == 4:
        valid_styles = ["Modern", "Classic", "Sporty", "Minimalist", "Vintage", "Bohemian"]
        suggestion = get_suggestion(user_input_cap, valid_styles)
        if user_input_cap in valid_styles:
            outfit = suggest_outfit(gender, event_type, color, user_input_cap)
            step = 5
            return jsonify({
                'response': (
                    "✨ Thank you! Based on your fabulous choices... ✨\n\n"
                    f"👗 Here's your outfit suggestion:\n💡 {outfit}\n\n"
                    "Would you like to continue and explore more looks? (Yes or No)"
                ),
                'step': step,
                'style': user_input_cap
            })
        elif suggestion:
            return jsonify({'response': f"Did you mean '{suggestion}'?", 'step': step, 'last_suggestion': suggestion})
        else:
            return jsonify({'response': "🚫 Please choose a valid style.", 'step': step})

    elif step == 5:
        if user_input_lower == "yes":
            step = 1
            return jsonify({'response': "💫 Awesome! Let's create another fabulous look.\n\nWho are you shopping for? (Male, Female, Unisex)", 'step': step})
        elif user_input_lower == "no":
            return jsonify({'response': "👗 Thank you for using FashionBot! Stay stylish and have a fabulous day! ✨", 'step': 0, 'end': True})
        else:
            return jsonify({'response': "🧐 Please respond with 'Yes' or 'No'.", 'step': step})

    return jsonify({'response': "❓ I didn't get that. Can you try again?", 'step': step})

if __name__ == '__main__':
    app.run(debug=True)
