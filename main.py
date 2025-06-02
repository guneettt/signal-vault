from index.search_engine import build_tf_idf_index, compute_tfidf_scores, get_snippet

def run_cli():
    print("=" * 50)
    print("🔍 SignalVault – Offline Emergency Search")
    print("Type a keyword to search. Type 'exit' to quit.")
    print("=" * 50)

    tf_index, df_counts, total_docs, file_texts = build_tf_idf_index()

    while True:
        query = input("\nSearch> ").strip()
        if not query:
            print("⚠️  Please enter a keyword.")
            continue
        if query.lower() == 'exit':
            print("👋 Exiting SignalVault.")
            break

        results = compute_tfidf_scores(query, tf_index, df_counts, total_docs)
        if results:
            print(f"\n📂 Results for '{query}' (ranked):\n")
            for i, (filename, score) in enumerate(results, 1):
                snippet = get_snippet(file_texts[filename], query)
                print(f"{i}. {filename}  —  Score: {round(score, 4)}")
                if snippet:
                    print(f"   ➤ {snippet}\n")
        else:
            print("❌ No matches found.")

if __name__ == '__main__':
    run_cli()
