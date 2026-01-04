import os
import re
import pandas as pd
import numpy as np
import faiss

from flask import Flask, jsonify, request, Response
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# ---------- Load data + build FAISS index once ----------
CSV_PATH = os.environ.get("DATA_CSV", "CustomerInteractionData.csv")

df = pd.read_csv(CSV_PATH)
texts = df["CustomerInteractionRawText"].fillna("").astype(str).tolist()

MODEL = SentenceTransformer("all-MiniLM-L6-v2")
embs = MODEL.encode(texts)
dim = int(embs.shape[1])

INDEX = faiss.IndexFlatL2(dim)
INDEX.add(embs.astype("float32"))


def rag_answer(query: str, k: int = 3):
    q_emb = MODEL.encode([query]).astype("float32")
    _, I = INDEX.search(q_emb, k)

    hits = [texts[i] for i in I[0] if i >= 0]
    answer = "Top similar interactions:\n" + "\n".join([f"- {h[:220].strip()}" for h in hits])

    # Example escalation rules (edit to match your notebook rules)
    escalate = any(re.search(r"\b(port\s*out|cancel|threaten|dissatisfied)\b", h, re.I) for h in hits)
    return answer, escalate


# ---------- Simple UI (HTML served by Flask) ----------
HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>AI Customer Service Chatbot</title>
  <style>
    body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;background:#f6f7fb;margin:0}
    .wrap{max-width:820px;margin:0 auto;padding:24px}
    .card{background:#fff;border:1px solid #e7e7ee;border-radius:14px;box-shadow:0 8px 24px rgba(0,0,0,.06);overflow:hidden}
    header{padding:18px 22px;border-bottom:1px solid #eee;background:#0f172a;color:#fff}
    header h1{font-size:18px;margin:0}
    header p{margin:6px 0 0 0;opacity:.85;font-size:13px}
    #chat{height:520px;overflow:auto;padding:18px;background:#fbfbfd}
    .msg{max-width:78%;padding:12px 14px;margin:10px 0;border-radius:14px;white-space:pre-wrap;line-height:1.35}
    .user{margin-left:auto;background:#2563eb;color:#fff;border-bottom-right-radius:6px}
    .bot{margin-right:auto;background:#fff;border:1px solid #e7e7ee;border-bottom-left-radius:6px}
    .warn{border-color:#ef4444;background:#fff5f5}
    form{display:flex;gap:10px;padding:14px;border-top:1px solid #eee;background:#fff}
    input{flex:1;padding:12px 14px;border:1px solid #d8d8e3;border-radius:999px;font-size:15px;outline:none}
    button{padding:12px 18px;border:0;border-radius:999px;background:#16a34a;color:#fff;font-weight:600;cursor:pointer}
    button:disabled{opacity:.6;cursor:not-allowed}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <header>
        <h1>AI Customer Service Chatbot</h1>
        <p>Flask UI + backend (FAISS + sentence-transformers)</p>
      </header>

      <div id="chat">
        <div class="msg bot">Hi! Ask about port-out, connectivity, high bill, roaming, etc.</div>
      </div>

      <form id="f">
        <input id="q" placeholder="Type a message..." autocomplete="off" />
        <button id="btn" type="submit">Send</button>
      </form>
    </div>
  </div>

<script>
  const chat = document.getElementById('chat');
  const form = document.getElementById('f');
  const q = document.getElementById('q');
  const btn = document.getElementById('btn');

  function add(cls, text){
    const div = document.createElement('div');
    div.className = 'msg ' + cls;
    div.textContent = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = q.value.trim();
    if(!text) return;

    add('user', text);
    q.value = '';
    btn.disabled = true;

    try{
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({query: text})
      });
      const data = await res.json();
      const cls = data.escalation_required ? 'bot warn' : 'bot';
      add(cls, data.answer + (data.escalation_required ? "\n\n[Escalation required]" : ""));
    }catch(err){
      add('bot warn', 'Error contacting server. Check Render logs.');
    }finally{
      btn.disabled = false;
      q.focus();
    }
  });

  q.focus();
</script>
</body>
</html>
"""

@app.get("/")
def ui():
    return Response(HTML, mimetype="text/html")


@app.post("/api/chat")
def api_chat():
    data = request.get_json(silent=True) or {}
    query = (data.get("query") or "").strip()
    if not query:
        return jsonify({"answer": "Please type a message.", "escalation_required": False})

    answer, escalate = rag_answer(query, k=3)
    return jsonify({"answer": answer, "escalation_required": bool(escalate)})


# Local run only; Render will run with gunicorn
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
