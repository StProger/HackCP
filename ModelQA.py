"""
Установить!
pip install transformer
pip install annoy
pip install transformers[torch]
pip install -U sentence-transformers
"""
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import pickle as pkl
import torch

# Загрузка SBERT модели
data = pd.read_csv('data.csv')
question = list(data['Вопрос из БЗ'])
answer = list(data['Ответ из БЗ'])
sbert_model_name = 'sentence-transformers/all-MiniLM-L6-v2'
sbert_model = SentenceTransformer(sbert_model_name)
with open('model_man.pkl', 'rb') as f:
    sbert_embeddings = pkl.load(f)
sbert_embeddings = [torch.tensor(embedding) for embedding in sbert_embeddings]


def question_response(sbert_embeddings, inp_question, top_k_hits = 1):
    question_embedding = sbert_model.encode(inp_question)
    # Семантический поиск с SBERT
    correct_hits = util.semantic_search(question_embedding, sbert_embeddings, top_k=top_k_hits)[0]
    correct_hits_ids = [hit['corpus_id'] for hit in correct_hits]
    return answer[correct_hits_ids[0]]

