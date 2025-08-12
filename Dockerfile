FROM python:3.13

# Install system dependencies
RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY langchain_ollama_example.py .
COPY wikipedia_ollama.py .
COPY WikiManager.py .
COPY db.sqlite .
COPY tools/ /app/tools/
COPY deepseek_wikiTool.py .

#Persona testing
COPY chatbot.py .
COPY persona.py .

#CMD ["python", "deepseek_wikiTool.py"]
CMD ["python", "chatbot.py"]