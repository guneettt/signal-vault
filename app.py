from flask import Flask, request, jsonify
from flask_cors import CORS
from index.search_engine import build_tf_idf_index, compute_tfidf_scores, get_snippet

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


if __name__ == "__main__":
    app.run(debug=True, port=5050)
