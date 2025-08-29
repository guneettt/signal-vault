from flask import Flask, render_template, request, url_for
from index.search_engine import build_tf_idf_index, compute_tfidf_scores, get_snippet
from markupsafe import escape

app = Flask(__name__)

# 🔁 Build TF-IDF index once at startup
tf_index, df_counts, total_docs, file_texts = build_tf_idf_index()

# 🆘 Emergency protocols
EMERGENCY_GUIDES = {
    "stuck in flood": [
        "Move to higher ground immediately.",
        "Avoid walking or driving through flood waters.",
        "Listen to local emergency alerts on a battery-powered radio.",
        "Disconnect electrical appliances if safe to do so.",
        "Do not touch electrical equipment if you are wet or standing in water."
    ],
    "can't find water": [
        "Search for bottled or sealed water sources (e.g., in canned foods).",
        "Collect rainwater or dew using clean containers or plastic sheets.",
        "Boil water for at least 1 minute to kill bacteria.",
        "Use purification tablets or household bleach (8 drops per gallon).",
        "Avoid drinking water from rivers, lakes, or puddles without purification."
    ],
    "unclear breathing": [
        "Check the person's airway, breathing, and pulse.",
        "If unresponsive, call for help or alert someone nearby.",
        "Perform CPR: 30 chest compressions followed by 2 rescue breaths (if trained).",
        "Use an automated external defibrillator (AED) if available.",
        "Place in recovery position if breathing resumes and wait for help."
    ],
    "trapped under rubble": [
        "Protect your head and breathing with cloth or clothing.",
        "Tap on a pipe or wall to alert rescuers, do not shout to conserve oxygen.",
        "Stay still to avoid stirring dust or causing further collapse.",
        "Cover your mouth with cloth to filter debris.",
        "Conserve battery if using a phone; only text or call for help when needed."
    ],
    "earthquake": [
        "Drop, Cover, and Hold On under sturdy furniture.",
        "Stay away from windows, mirrors, and heavy objects.",
        "If outside, move to an open area away from buildings and power lines.",
        "Expect aftershocks; stay alert.",
        "Use a flashlight, not matches, to check for damage and gas leaks."
    ],
    "fire in building": [
        "Stay low to avoid smoke inhalation.",
        "Check door handles with the back of your hand before opening.",
        "If trapped, signal from windows using cloth or light.",
        "Stop, Drop, and Roll if clothes catch fire.",
        "Never use elevators during a fire."
    ],
    "injured with bleeding": [
        "Apply firm pressure with a clean cloth or bandage.",
        "Elevate the wound above heart level if possible.",
        "Do not remove embedded objects; stabilize them instead.",
        "Use tourniquets only as a last resort.",
        "Keep the person calm and still to reduce blood flow."
    ],
    "lost in forest": [
        "Stop moving, stay calm, and mark your location.",
        "Build a visible signal (rock arrows, clothing on trees).",
        "Stay put unless absolutely sure of the way out.",
        "Find or build shelter before dark.",
        "Collect and purify water if available; avoid eating unfamiliar plants."
    ]
}


# 🏠 Homepage — handles search and emergencies
@app.route('/', methods=['GET', 'POST'])
def home():
    results = []
    query = ""

    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        if query:
            lower_query = query.lower()

            # 🆘 Emergency Scenario Detected
            if lower_query in EMERGENCY_GUIDES:
                return render_template('emergency.html', query=query, checklist=EMERGENCY_GUIDES[lower_query])

            # 🧠 Normal document search
            scored = compute_tfidf_scores(query, tf_index, df_counts, total_docs)
            for filename, score in scored:
                snippet = get_snippet(file_texts[filename], query)
                results.append({
                    'filename': filename,
                    'score': round(score, 4),
                    'snippet': snippet
                })

    return render_template('index.html', query=query, results=results)

def extract_actionable_steps(content, query):
    """Extract concise, actionable steps from document content."""
    # Split content into sentences
    sentences = content.replace('\n', ' ').split('.')
    
    # Clean and filter sentences
    clean_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 15 and len(sentence) < 200:  # Skip very short or very long sentences
            clean_sentences.append(sentence)
    
    # Find sentences containing query keywords
    keywords = query.lower().split()
    relevant_sentences = []
    
    for sentence in clean_sentences:
        lower_sentence = sentence.lower()
        # Check if sentence contains any keyword and looks like an instruction
        if any(keyword in lower_sentence for keyword in keywords):
            # Prioritize sentences that start with action words
            action_words = ['call', 'apply', 'use', 'place', 'remove', 'check', 'perform', 'give', 'do', 'take', 'put', 'get', 'move', 'keep', 'avoid', 'ensure', 'press', 'hold', 'wrap', 'clean', 'stop', 'start', 'turn', 'push', 'pull']
            first_word = sentence.split()[0].lower() if sentence.split() else ''
            
            if first_word in action_words or any(word in lower_sentence for word in ['should', 'must', 'need to', 'important', 'immediately']):
                relevant_sentences.append(sentence.strip() + '.')
    
    # Remove duplicates while preserving order
    seen = set()
    unique_steps = []
    for sentence in relevant_sentences:
        if sentence not in seen:
            seen.add(sentence)
            unique_steps.append(sentence)
    
    # Limit to 5-8 most relevant steps
    return unique_steps[:6]

# 📄 File viewer — match query snippets or full content
@app.route('/view/<path:filename>')
def view_file(filename):
    query = request.args.get('query', '')
    filename = escape(filename)
    content = file_texts.get(filename)

    if not content:
        return f"<h2>❌ File '{filename}' not found or unreadable.</h2>", 404

    if query:
        # Generate concise, actionable steps instead of raw snippets
        actionable_steps = extract_actionable_steps(content, query)
        
        # If we don't find enough actionable steps, fall back to key sentences
        if len(actionable_steps) < 3:
            sentences = content.replace('\n', ' ').split('.')
            keywords = query.lower().split()
            
            for sentence in sentences:
                sentence = sentence.strip()
                if (len(sentence) > 20 and len(sentence) < 150 and 
                    any(keyword in sentence.lower() for keyword in keywords)):
                    if sentence not in actionable_steps:
                        actionable_steps.append(sentence + '.')
                        if len(actionable_steps) >= 6:
                            break
        
        return render_template(
            'view_snippets.html',
            filename=filename,
            query=query,
            snippets=actionable_steps
        )

    # 🔄 Fallback — show full content if no query
    return render_template('view.html', filename=filename, content=content)

if __name__ == '__main__':
    app.run(debug=True)
