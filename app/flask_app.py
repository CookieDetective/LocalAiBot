from flask import Flask, request, jsonify, render_template
from app.conversation_agent import ConversationAgent  # Adjust import if needed
from tools.flask.file_upload import bp as file_upload_bp

def create_app():
    app = Flask(__name__, template_folder="templates")
    #Set Re
    app.register_blueprint(file_upload_bp)

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