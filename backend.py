import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
import traceback 
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


app = Flask(__name__)
CORS(app)

# Set up GPT-3
openai.api_key = "SECRET" 

# Set up BERT
tokenizer = AutoTokenizer.from_pretrained("savasy/bert-base-turkish-squad")
model = AutoModelForQuestionAnswering.from_pretrained("savasy/bert-base-turkish-squad")
nlp = pipeline("question-answering", model=model, tokenizer=tokenizer)

# Connect to Elasticsearch
es = Elasticsearch(
    hosts=['https://localhost:9200'],
    http_auth=('elastic', 'fIs*jD*3To+IpzLP3D+B'),
    verify_certs=False
)

# Create index mapping
index_name = 'passages'
index_mapping = {
    "mappings": {
        "properties": {
            "passage_id": {"type": "integer"},
            "passage": {"type": "text", "analyzer": "turkish"},
        }
    }
}

# Create the index with the custom mapping if it doesn't exist
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=index_mapping)


# Index the passages
def index_passages():
    with open("passage.txt", "r", encoding="utf-8") as f:
        passages = f.readlines()

    bulk_data = []
    for i, passage in enumerate(passages):
        doc = {
            'passage_id': i,
            'passage': passage.strip()
        }
        bulk_data.append({
            "_index": index_name,
            "_id": i,
            "_source": doc
        })

    bulk(es, bulk_data)

# Call the function to index the passages
index_passages()


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
          model="SECRET", 
          prompt=message,
          temperature=0.0,
          max_tokens=150,
          top_p=1.0,
          best_of=3,
          frequency_penalty=0.0,
          presence_penalty=0.0,
          stop=['.']
        )

        return jsonify({"text": response.choices[0].text.strip()})
    except Exception as e:
        print(e)
        return jsonify({"error": "Error generating response"}), 500

@app.route("/generate-response-bert", methods=["POST"])
def get_bert_response():
    question = request.json["message"]
    # Search for relevant passages using Elasticsearch
    search_results = es.search(index=index_name, body={
        'query': {
            'match': {
                'passage': {
                    'query': question,
                    'analyzer': 'turkish'
                }
            }
        },
        'size': 5  # Return top 5 passages
    })

    try:
        passages = '\n'.join([hit['_source']['passage'] for hit in search_results['hits']['hits']])
    
        if not passages:
            return jsonify({'text': 'Üzgünüm ne dediğinizi anlayamadım. Tekrar sorunuzu sorabilir misiniz?'}), 200

        results = nlp(question=question, context=passages, top_k=5)
        result = max(results, key=lambda x: len(x['answer']))

        if result is None:
            return jsonify({'text': 'Üzgünüm ne dediğinizi anlayamadım. Tekrar sorunuzu sorabilir misiniz?'}), 200
        else:
            return jsonify({'text': result['answer']}), 200

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": "Error generating response"}), 500

if __name__ == "__main__":
    app.run(debug=True)
