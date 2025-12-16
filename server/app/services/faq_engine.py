from datasets import load_dataset
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class FAQEngine:
    def __init__(self):
        ds = load_dataset("MakTek/Customer_support_faqs_dataset")
        faqs = ds["train"]
        self.df = pd.DataFrame({
            "question": [item["question"] for item in faqs],
            "answer": [item["answer"] for item in faqs],
        })
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["question"])

    def search_faq(self, query: str, threshold: float = 0.3):
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        best_match_index = int(np.argmax(similarities))
        score = float(similarities[best_match_index])

        if score >= threshold:
            row = self.df.iloc[best_match_index]
            return {
                "question": row["question"],
                "answer": row["answer"],
                "score": score,
            }
        return None

faq_engine = FAQEngine()
