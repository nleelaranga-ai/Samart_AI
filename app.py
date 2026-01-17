from flask import Flask, render_template_string, request, jsonify
from brain import find_scholarship

app = Flask(__name__)

# --- EMBEDDED HTML TEMPLATE (Single File for Easy Run) ---
HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SamartAI | AP Scholarship Assistant</title>
    <style>
    body { font-family: 'Inter', sans-serif; background: #f0f4f8; padding: 20px; }
    .container { max-width: 700px; margin: 0 auto; background: white; padding: 40px; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); }
    h1 { color: #1a202c; text-align: center; margin-bottom: 5px; }
    .subtitle { text-align: center; color: #718096; margin-bottom: 30px; }
    
    .input-group { display: flex; gap: 10px; margin-bottom: 30px; }
    input { flex: 1; padding: 15px; border: 2px solid #e2e8f0; border-radius: 8px; font-size: 16px; outline: none; transition: 0.2s; }
    input:focus { border-color: #3182ce; }
    button { padding: 15px 30px; background: #3182ce; color: white; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; transition: 0.2s; }
    button:hover { background: #2b6cb0; transform: translateY(-1px); }

    .card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; margin-bottom: 15px; transition: 0.2s; border-left: 5px solid #3182ce; }
    .card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .card h3 { margin: 0 0 10px 0; color: #2d3748; display: flex; justify-content: space-between; align-items: center; }
    .tag { background: #ebf8ff; color: #3182ce; padding: 4px 10px; border-radius: 20px; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; }
    .desc { color: #4a5568; line-height: 1.5; margin-bottom: 15px; }
    .meta { display: flex; gap: 15px; font-size: 14px; color: #718096; margin-bottom: 15px; }
    .btn-apply { display: inline-block; text-decoration: none; color: #3182ce; font-weight: bold; }
    
    .translation-box { margin-top: 30px; background: #fffaf0; border: 1px solid #fbd38d; padding: 15px; border-radius: 8px; color: #744210; }
</style>}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎓 SamartAI</h1>
        <p class="subtitle">AI Assistant for AP Scholarships (English & Telugu)</p>
        
        <div class="input-group">
            <input type="text" id="userInput" placeholder="Ex: 'I am an SC student' or 'నాకు స్కాలర్‌షిప్ కావాలి'">
            <button onclick="search()">Ask AI</button>
        </div>

        <div id="loading" style="display:none; text-align:center; margin-top:20px;">Thinking... 🧠</div>
        
        <div id="output" class="results-area"></div>
    </div>

    <script>
        async function search() {
            const input = document.getElementById('userInput').value;
            if(!input) return;

            document.getElementById('loading').style.display = 'block';
            document.getElementById('output').innerHTML = '';

            const response = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query: input})
            });
            const data = await response.json();

            document.getElementById('loading').style.display = 'none';
            
            // Render Cards
            let html = '';
            if (data.matches.length > 0) {
                data.matches.forEach(item => {
                    html += `
                    <div class="card">
                        <h3>${item.name} <span class="tag">${item.category}</span></h3>
                        <p>${item.description}</p>
                        <p><strong>Limit:</strong> ₹${item.income_limit}</p>
                        <a href="${item.link}" target="_blank" style="color:#27ae60; text-decoration:none;">Apply Now &rarr;</a>
                    </div>`;
                });
            } else {
                html = '<p>No specific schemes found.</p>';
            }

            // Add Telugu Translation at the bottom
            html += `<div class="translation-box"><strong>🇮🇳 Telugu Summary:</strong><br>${data.telugu}</div>`;

            document.getElementById('output').innerHTML = html;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.json.get('query', '')
    result = find_scholarship(user_query)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)