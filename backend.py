import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
import traceback 

app = Flask(__name__)
CORS(app)

# Set up GPT-3
openai.api_key = "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"

# Set up BERT
tokenizer = AutoTokenizer.from_pretrained("savasy/bert-base-turkish-squad")
model = AutoModelForQuestionAnswering.from_pretrained("savasy/bert-base-turkish-squad")
nlp = pipeline("question-answering", model=model, tokenizer=tokenizer)

with open("passage.txt", "r", encoding="utf-8") as f:
    text = f.read()

@app.route("/api/status", methods=["GET"])
def get_status():
    try:
        response = openai.Completion.create(engine="davinci", prompt="test", max_tokens=5)
        return jsonify({"status": "Online"})
    except Exception as e:
        return jsonify({"status": "Offline"})

@app.route("/generate-response-gpt3", methods=["POST"])
def get_gpt3_response():
    message = request.json["message"]
    print(message)
    try:
        response = openai.Completion.create(
          model="davinci:ft-maryuzun-2023-03-15-00-59-45",
          prompt=message,
          temperature=0,
          max_tokens=120,
          top_p=1,
          best_of=3,
          frequency_penalty=0,
          presence_penalty=0
        )

        return jsonify({"text": response.choices[0].text.strip()})
    except Exception as e:
        print(e)
        return jsonify({"error": "Error generating response"}), 500

@app.route("/generate-response-bert", methods=["POST"])
def get_bert_response():
    message = request.json["message"]
    try:
        print("Message:", message)
        print("Context:", text)
        response = nlp(question=message, context=text)
        return jsonify({"text": response['answer']})
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": "Error generating response"}), 500

if __name__ == "__main__":
    app.run(debug=True)
