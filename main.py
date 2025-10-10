from app.flask_app import create_app

if __name__ == "__main__":
    app = create_app()
    # You can add any agent startup logic here, similar to conversation_agent.py
    # For example, loading models, initializing Langfuse, etc.
    app.run(host="0.0.0.0", port=5000, debug=True)