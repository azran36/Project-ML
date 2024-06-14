import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Load the CSV data
df = pd.read_csv('Project Bola Dataset.csv')

# Preprocessing and Feature Extraction
df['Fasilitas_Harga'] = df[
    'Fasilitas_Lapangan'] + ' ' + df['Harga'].astype(str)

# TF-IDF Vectorization on Fasilitas_Harga
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['Fasilitas_Harga'].fillna(''))

# Function to recommend fields based on keyword and similarity


def recommend_fields_by_type(keyword, df, tfidf_matrix):
    # Filter fields that match the search keyword
    filtered_fields = df[df.apply(
        lambda row: keyword.lower() in row['Jenis_Lapangan'].lower()
        or keyword.lower() in row['Jenis_Lapangan'].lower()
        or keyword.lower() in row['Jenis_Lapangan'].lower(), axis=1)]

    # Compute similarity score using cosine similarity
    keyword_tfidf = tfidf.transform([keyword])
    cosine_similarities = linear_kernel(keyword_tfidf, tfidf_matrix).flatten()

    # Sort fields by similarity score
    filtered_fields['similarity'] = cosine_similarities
    filtered_fields = filtered_fields.sort_values(
        by='similarity', ascending=False)

    return filtered_fields[['Nama_Lapangan', 'Fasilitas_Lapangan', 'Harga',
                            'Lokasi_Lapangan', 'similarity']]

# Example: Get recommendations for Futsal


keyword = 'Lapangan Basket'
print(f"Rekomendasi untuk {keyword}:")
print("==========================")
recommendations = recommend_fields_by_type(keyword, df, tfidf_matrix)
print(recommendations.head(5))
