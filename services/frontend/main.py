from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Frontend Service")


@app.get("/", response_class=HTMLResponse)
def home():
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Microservices App</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', sans-serif;
      background: #0f172a;
      color: #e2e8f0;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      gap: 2rem;
    }
    h1 { font-size: 2.5rem; color: #38bdf8; }
    p  { color: #94a3b8; }
    input {
      padding: .6rem 1rem;
      border-radius: 6px;
      border: 1px solid #334155;
      background: #1e293b;
      color: #e2e8f0;
      font-size: 1rem;
      width: 220px;
    }
    button {
      padding: .6rem 1.4rem;
      background: #38bdf8;
      color: #0f172a;
      border: none;
      border-radius: 6px;
      font-weight: 700;
      cursor: pointer;
      font-size: 1rem;
    }
    button:hover { background: #7dd3fc; }
    #result {
      margin-top: 1rem;
      padding: 1rem 2rem;
      background: #1e293b;
      border-radius: 8px;
      font-size: 1.1rem;
      min-width: 280px;
      text-align: center;
      border: 1px solid #334155;
    }
    .row { display: flex; gap: 1rem; align-items: center; }
  </style>
</head>
<body>
  <h1>🚀 Microservices App</h1>
  <p>Frontend → API Gateway → Hello Service</p>
  <div class="row">
    <input id="name" placeholder="Enter your name" />
    <button onclick="greet()">Say Hello</button>
  </div>
  <div id="result">Response will appear here</div>
  <script>
    async function greet() {
      const name = document.getElementById('name').value || 'World';
      const res  = await fetch(`/api/hello?name=${encodeURIComponent(name)}`);
      const data = await res.json();
      document.getElementById('result').textContent = data.message;
    }
  </script>
</body>
</html>"""


@app.get("/health")
def health():
    return {"service": "frontend", "status": "ok"}
