import shared_state
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return 'LinkBridge Server is Running'

@app.route('/share', methods=['POST'])
def share():
    data = request.get_json()
    content = data.get('content')
    shared_state.update_message(f"HTTP: {content}")
    print(f"Received via HTTP:{content}")
    return {"status":"Success", "message":"Data Received"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)