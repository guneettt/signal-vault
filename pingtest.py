from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def test():
    data = request.get_json()
    print("✅ Got data:", data)
    return jsonify({"ok": True, "echo": data})

if __name__ == '__main__':
    app.run(debug=True)
