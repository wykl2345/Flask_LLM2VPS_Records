from flask import Flask, render_template, request, stream_with_context
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.form['user_input']
        if user_input:
            # 发送请求到OpenAI的本地服务器
            response = send_to_openai(user_input)
            
            content = response['choices'][0]['message']['content'].replace('\n', '')
            content = content.encode('utf-8').decode('utf-8')  # 先编码再解码
            print(content)
            return content
    return render_template('chat.html')

def send_to_openai(content):
    url = "http://localhost:1234/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer lm-studio"
    }
    data = {
        "model": "QuantFactory/Meta-Llama-3-8B-Instruct-GGUF",
        "messages": [
            {"role": "system", "content": "回答都使用中文回答"},
            {"role": "user", "content": content}
        ],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to get response from OpenAI"}

if __name__ == '__main__':
    app.run(debug=True)
