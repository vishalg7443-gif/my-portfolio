import os
from flask import Flask, jsonify, render_template_string, request
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

app = Flask(__name__)

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-05-01-preview",
)
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5-nano")

PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Chat</title>
  <style>
    body{font-family:Inter,system-ui,sans-serif;background:#07111f;color:#eaf2ff;margin:0}
    main{max-width:760px;margin:48px auto;padding:24px}
    .card{background:#0d1b2d;border:1px solid #20344f;border-radius:18px;padding:20px}
    #log{display:grid;gap:12px;min-height:260px;margin-bottom:16px}
    .bubble{padding:12px 14px;border-radius:14px;background:#172943;max-width:78%}
    .me{margin-left:auto;background:#2458a6}
    form{display:flex;gap:10px}input{flex:1;padding:12px;border-radius:10px;border:1px solid #38506f;background:#081521;color:white}
    button{padding:12px 16px;border:0;border-radius:10px;background:#6ee7c7;font-weight:700;cursor:pointer}
  </style>
</head>
<body><main><h1>AI Chat</h1><p>A Flask + Azure OpenAI chat interface.</p><div class="card"><div id="log"></div><form id="chat"><input id="message" autocomplete="off" placeholder="Ask something…"><button>Send</button></form></div></main>
<script>
const form=document.getElementById('chat'), log=document.getElementById('log'), input=document.getElementById('message');
function add(text,me=false){const d=document.createElement('div');d.className='bubble'+(me?' me':'');d.textContent=text;log.appendChild(d)}
form.addEventListener('submit',async e=>{e.preventDefault();const message=input.value.trim();if(!message)return;add(message,true);input.value='';
try{const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message})});const data=await r.json();add(data.reply||data.error||'No response');}catch(err){add('Unable to reach the server.');}});
</script></body></html>
"""

@app.get("/")
def home():
    return render_template_string(PAGE)

@app.post("/api/chat")
def chat():
    message = (request.get_json(silent=True) or {}).get("message", "").strip()
    if not message:
        return jsonify(error="Message is required"), 400
    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT,
            messages=[
                {"role": "system", "content": "You are a concise, helpful assistant."},
                {"role": "user", "content": message},
            ],
        )
        return jsonify(reply=response.choices[0].message.content)
    except Exception as exc:
        return jsonify(error=f"AI request failed: {exc}"), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
