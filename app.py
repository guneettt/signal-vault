from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from index.search_engine import build_tf_idf_index, compute_tfidf_scores, get_snippet
from urllib.parse import unquote
from markupsafe import escape
from nltk.tokenize import sent_tokenize
import re
from urllib.parse import unquote

app = Flask(__name__)
CORS(app)

# ✅ Build search index once
tf_index, df_counts, total_docs, file_texts = build_tf_idf_index()

# ✅ Emergency guide dictionary
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
    "earthquake": [
        "Drop, Cover, and Hold On under sturdy furniture.",
        "Stay away from windows, mirrors, and heavy objects.",
        "If outside, move to an open area away from buildings and power lines.",
        "Expect aftershocks; stay alert.",
        "Use a flashlight, not matches, to check for damage and gas leaks."
    ],
    "fire in building": [
        "Stay low to avoid smoke inhalation.",
        "Check door handles before opening.",
        "If trapped, signal from windows using cloth or light.",
        "Stop, Drop, and Roll if clothes catch fire.",
        "Never use elevators during a fire."
    ],
    "trapped under rubble": [
        "Protect your head and breathing with cloth or clothing.",
        "Tap on a pipe or wall to alert rescuers, do not shout to conserve oxygen.",
        "Stay still to avoid stirring dust or causing further collapse.",
        "Cover your mouth with cloth to filter debris.",
        "Conserve battery if using a phone; only text or call for help when needed."
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

@app.route("/", methods=["POST"])
def search():
    try:
        data = request.get_json(force=True)
        print("✅ Received:", data)

        query = data.get("query", "").strip()
        if not query:
            return jsonify({"error": "Empty query"}), 400

        lower_query = query.lower()

        # ✅ EMERGENCY CHECK
        if lower_query in EMERGENCY_GUIDES:
            print("🚨 Emergency match")
            return jsonify({
                "emergency": True,
                "query": query,
                "checklist": EMERGENCY_GUIDES[lower_query]
            })

        # ✅ DOCUMENT SEARCH
        print("🔎 Performing TF-IDF search...")
        results = []
        scored = compute_tfidf_scores(query, tf_index, df_counts, total_docs)

        for filename, score in scored:
            snippet = get_snippet(file_texts[filename], query)
            results.append({
                "filename": filename,
                "score": round(score, 4),
                "snippet": snippet
            })

        print(f"✅ Found {len(results)} results")
        return jsonify({
            "emergency": False,
            "query": query,
            "results": results
        })

    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/view/<path:filename>")
def view_file(filename):
    query = request.args.get('query', '')
    filename = unquote(filename)
    filename = escape(filename)
    content = file_texts.get(filename)

    if not content:
        return f"<h2>❌ File '{filename}' not found or unreadable.</h2>", 404

    if query:
        keywords = query.lower().split()
        words = content.split()
        lower_words = [w.lower() for w in words]
        matched_snippets = []

        for keyword in keywords:
            idx = 0
            while keyword in lower_words[idx:]:
                i = lower_words.index(keyword, idx)
                start = max(0, i - 20)
                end = min(len(words), i + 21)
                snippet = ' '.join(words[start:end])
                matched_snippets.append(snippet)
                idx = i + 1

        return render_template(
            'view_snippets.html',
            filename=filename,
            query=query,
            snippets=matched_snippets
        )

    return render_template('view_snippets.html', filename=filename, query=query, snippets=[])

@app.route("/api/flow/<path:filename>")
def flow_json(filename):
    query = request.args.get("query", "")
    filename = unquote(filename)

    content = file_texts.get(filename)
    if not content:
        return jsonify({"error": "File not found"}), 404

    keywords = query.lower().split()
    words = content.split()
    lower_words = [w.lower() for w in words]
    matched_snippets = []

    for keyword in keywords:
        idx = 0
        while keyword in lower_words[idx:]:
            i = lower_words.index(keyword, idx)
            start = max(0, i - 20)
            end = min(len(words), i + 21)
            snippet = ' '.join(words[start:end])
            matched_snippets.append(snippet)
            idx = i + 1

    # 🔍 Combine + tokenize
    combined_text = " ".join(matched_snippets)
    sentences = sent_tokenize(combined_text)

    # 🎯 Extract relevant flow steps (e.g., commands, procedures)
    important_steps = []
    for s in sentences:
        s_clean = re.sub(r'\s+', ' ', s).strip()
        if len(s_clean) < 30 or len(s_clean) > 220:
            continue  # remove too short or too long
        if re.search(r"\b(apply|check|call|clean|cover|move|remove|perform|place|stay|protect|signal|monitor|keep|treat)\b", s_clean, re.IGNORECASE):
            important_steps.append(s_clean)

    # ✅ Return JSON
    return jsonify({
        "filename": filename,
        "query": query,
        "steps": important_steps[:10]  # limit for now
    })


if __name__ == "__main__":
    app.run(debug=True, port=5050)
