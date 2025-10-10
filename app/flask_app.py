from flask import Flask, request, jsonify, render_template
from app.conversation_agent import ConversationAgent  # Adjust import if needed

def create_app():
    app = Flask(__name__, template_folder="templates")

    agent = ConversationAgent()

    @app.route('/')
    def index():
        return render_template('chat.html')

    @app.route('/chat', methods=['POST'])
    def chat():
        data = request.get_json()
        user_input = data.get('input', '')
        output = agent.run(user_input)
        return jsonify({'output': output})

    return app