# Python script: flask_server.py
import pandas as pd
from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from flask_cors import CORS
from sklearn.metrics.pairwise import linear_kernel

app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)

# Load CSV data
df = pd.read_csv('Project Bola Dataset.csv')

# Preprocessing and Feature Extraction
df['Fasilitas_Harga'] = df[
    'Fasilitas_Lapangan'] + ' ' + df['Harga'].astype(str)

# TF-IDF Vectorization on Fasilitas_Harga
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['Fasilitas_Harga'].fillna(''))

# Function to recommend fields based on keyword and similarity
# Filter fields that match the search keyword


@app.route('/recommend-fields', methods=['GET'])
def recommend_fields_by_type(keyword):
    filtered_fields = df[df.apply(
        lambda row: keyword.lower() in row['Jenis_Lapangan'].lower(),
        axis=1
    )]

    # Compute similarity score using cosine similarity
    keyword_tfidf = tfidf.transform([keyword])
    cosine_similarities = linear_kernel(keyword_tfidf, tfidf_matrix).flatten()

    # Sort fields by similarity score
    filtered_fields['similarity'] = cosine_similarities
    filtered_fields = filtered_fields.sort_values(
        by='similarity', ascending=False
    )

    return filtered_fields[['Nama_Lapangan', 'Fasilitas_Lapangan', 'Harga',
                            'Lokasi_Lapangan', 'similarity']].head(5)


def recommend_fields():
    keyword = request.args.get('keyword')
    recommendations = recommend_fields_by_type(keyword)
    return jsonify(recommendations.to_dict(orient='records'))
