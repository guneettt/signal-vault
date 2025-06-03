from flask import Flask, render_template, request, url_for
from index.search_engine import build_tf_idf_index, compute_tfidf_scores, get_snippet
from markupsafe import escape

app = Flask(__name__)

# 🔁 Build TF-IDF index once at startup
tf_index, df_counts, total_docs, file_texts = build_tf_idf_index()

# 🏠 Homepage — handles search
@app.route('/', methods=['GET', 'POST'])
def home():
    results = []
    query = ""

    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        if query:
            scored = compute_tfidf_scores(query, tf_index, df_counts, total_docs)
            for filename, score in scored:
                snippet = get_snippet(file_texts[filename], query)
                results.append({
                    'filename': filename,
                    'score': round(score, 4),
                    'snippet': snippet
                })

    return render_template('index.html', query=query, results=results)

# 📄 File viewer — match query snippets or full content
@app.route('/view/<path:filename>')
def view_file(filename):
    query = request.args.get('query', '')
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

    # 🔄 Fallback — show full content if no query
    return render_template('view.html', filename=filename, content=content)

# 🧪 Optional debug test route
@app.route('/dashboard')
def dashboard():
    return render_template('view.html')

if __name__ == '__main__':
    app.run(debug=True)
