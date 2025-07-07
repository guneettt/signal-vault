from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from index.search_engine import build_tf_idf_index, compute_tfidf_scores, get_snippet
from urllib.parse import unquote
from markupsafe import escape
from nltk.tokenize import sent_tokenize
import re

app = Flask(__name__)
CORS(app)

# Build TF-IDF index once
tf_index, df_counts, total_docs, file_texts = build_tf_idf_index()

# Emergency guides (unchanged)
EMERGENCY_GUIDES = {
    "stuck in flood": [...],
    "can't find water": [...],
    "unclear breathing": [...],
    "earthquake": [...],
    "fire in building": [...],
    "trapped under rubble": [...],
    "injured with bleeding": [...],
    "lost in forest": [...]
}


@app.route("/", methods=["POST"])
def search():
    try:
        data = request.get_json(force=True)
        query = data.get("query", "").strip()
        if not query:
            return jsonify({"error": "Empty query"}), 400

        lower_query = query.lower()
        if lower_query in EMERGENCY_GUIDES:
            return jsonify({
                "emergency": True,
                "query": query,
                "checklist": EMERGENCY_GUIDES[lower_query]
            })

        results = []
        scored = compute_tfidf_scores(query, tf_index, df_counts, total_docs)

        for filename, score in scored:
            content = file_texts.get(filename, "")
            step_count = 0
            summary = "No relevant instructions found."

            if content:
                sentences = sent_tokenize(content)

                # Smart preview snippet
                preview_lines = [
                    s.strip() for s in sentences
                    if re.search(r"\b(apply|clean|cover|treat|rinse|protect|call|seek|avoid|move|bandage|stop|remove)\b", s, re.IGNORECASE)
                ]
                if preview_lines:
                    summary = preview_lines[0][:160] + "..."
                else:
                    summary = content[:160] + "..."

                # Flowchart steps (used to filter in frontend)
                step_count = len([
                    s for s in sentences
                    if re.search(r"\b(apply|check|clean|cover|treat|protect|rinse|call|remove)\b", s, re.IGNORECASE)
                ])

            results.append({
                "filename": filename,
                "score": round(score, 4),
                "snippet": summary,
                "flowstep_count": step_count
            })

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

    combined_text = " ".join(matched_snippets)
    sentences = sent_tokenize(combined_text)

    important_steps = []
    for s in sentences:
        s_clean = re.sub(r'\s+', ' ', s).strip()
        if len(s_clean) < 30 or len(s_clean) > 220:
            continue
        if re.search(r"\b(apply|check|call|clean|cover|move|remove|perform|place|stay|protect|signal|monitor|keep|treat|rinse|bandage)\b", s_clean, re.IGNORECASE):
            important_steps.append(s_clean)

    # Remove duplicates
    unique_steps = []
    for step in important_steps:
        if step not in unique_steps:
            unique_steps.append(step)

    return jsonify({
        "filename": filename,
        "query": query,
        "steps": unique_steps[:10]
    })


if __name__ == "__main__":
    app.run(debug=True, port=5050)
