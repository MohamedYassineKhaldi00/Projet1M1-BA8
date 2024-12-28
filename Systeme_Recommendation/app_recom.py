import streamlit as st
import json
import pickle
from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.preprocessing import normalize
from collections import defaultdict

# Step 1: Load the data
def load_data(masters_file, jobs_file):
    with open(masters_file, 'r', encoding='utf-8') as mf, open(jobs_file, 'r', encoding='utf-8') as jf:
        masters_data = json.load(mf)
        jobs_data = json.load(jf)
    return masters_data, jobs_data

# Step 2: Preprocess the data
def preprocess_data(masters, jobs):
    masters_texts = []
    jobs_texts = []

    for master in masters:
        text = ' '.join(master.get('Skills', []) + master.get('Subjects', []) + master.get('Careers', []))
        masters_texts.append(text.lower())

    for job in jobs:
        text = ' '.join(job.get('Skills', []) + job.get('Tasks', []) + job.get('Knowledge', []))
        jobs_texts.append(text.lower())

    return masters_texts, jobs_texts

# Step 3: Categorize jobs and masters
def categorize_items(items, key):
    categories = defaultdict(list)
    for item in items:
        category = item.get(key, "Uncategorized")
        categories[category].append(item)
    return categories

# Step 4: Generate embeddings with BERT on GPU
def generate_embeddings(texts, model, tokenizer, device):
    embeddings = []
    for text in texts:
        inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512, padding=True).to(device)
        with torch.no_grad():
            outputs = model(**inputs)
        embeddings.append(outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy())
    return normalize(np.array(embeddings))  # Normalize embeddings for better comparison

# Step 5: Calculate cosine similarities
def calculate_similarities(master_embeddings, job_embeddings):
    return cosine_similarity(master_embeddings, job_embeddings)

# Step 6: Get top recommendations with a similarity threshold
def get_top_recommendations_with_threshold(similarity_matrix, masters, jobs, top_n=5, threshold=0.2):
    recommendations = {}
    for i, master in enumerate(masters):
        similar_jobs = [(j, similarity_matrix[i, j]) for j in np.argsort(-similarity_matrix[i])[:top_n]]
        filtered_jobs = [(jobs[j]['Occupation'], sim) for j, sim in similar_jobs if sim >= threshold]
        if filtered_jobs:
            recommendations[master['Title']] = filtered_jobs
        else:
            recommendations[master['Title']] = "No suitable match found."
    return recommendations

def recommend_jobs_for_master(master_index, similarity_matrix, masters, jobs, top_n=5, threshold=0.2):
    similar_jobs = [(j, similarity_matrix[master_index, j]) for j in np.argsort(-similarity_matrix[master_index])[:top_n]]
    filtered_jobs = [jobs[j]['Occupation'] for j, sim in similar_jobs if sim >= threshold]
    return filtered_jobs if filtered_jobs else ["No suitable match found."]

def recommend_masters_for_job(job_index, similarity_matrix, masters, jobs, top_n=3, threshold=0.2):
    similar_masters = [(i, similarity_matrix[i, job_index]) for i in np.argsort(-similarity_matrix[:, job_index])[:top_n]]
    filtered_masters = [masters[i]['Title'] for i, sim in similar_masters if sim >= threshold]
    return filtered_masters if filtered_masters else ["No suitable match found."]

def save_embeddings_to_pickle(file_path, data):
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)

def load_embeddings_from_pickle(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

# Step 7: Streamlit UI
def main():
    st.set_page_config(page_title="Master to Job & Job to Master Recommendation", layout="wide")

    st.title("Master to Job & Job to Master Recommendation System")
    st.markdown("""
        This application helps you find the best job recommendations based on master programs and vice versa. 
        You can explore different categories of masters and jobs, and the system will suggest suitable matches.
    """)

    # File paths
    masters_file = "L+MFinal (1).json"
    jobs_file = "jobsFinal (1).json"
    masters_embeddings_file = "masters_embeddings.pkl"
    jobs_embeddings_file = "jobs_embeddings.pkl"

    # Load data
    masters, jobs = load_data(masters_file, jobs_file)

    # Preprocess data
    masters_texts, jobs_texts = preprocess_data(masters, jobs)

    # Categorize jobs and masters
    job_categories = categorize_items(jobs, "Career_cluster")
    master_categories = categorize_items(masters, "Degree")

    # Load BERT model and tokenizer
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertModel.from_pretrained("bert-base-uncased")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    # Check if embeddings are already saved, otherwise generate them
    try:
        st.write("Loading saved embeddings...")
        master_embeddings = load_embeddings_from_pickle(masters_embeddings_file)
        job_embeddings = load_embeddings_from_pickle(jobs_embeddings_file)
    except FileNotFoundError:
        st.write("Saved embeddings not found. Generating embeddings...")
        master_embeddings = generate_embeddings(masters_texts, model, tokenizer, device)
        job_embeddings = generate_embeddings(jobs_texts, model, tokenizer, device)
        save_embeddings_to_pickle(masters_embeddings_file, master_embeddings)
        save_embeddings_to_pickle(jobs_embeddings_file, job_embeddings)

    # Calculate similarities
    st.write("Calculating similarities...")
    similarity_matrix = calculate_similarities(master_embeddings, job_embeddings)

    # Sidebar navigation
    with st.sidebar:
        st.header("Navigation")
        choice = st.radio("Choose an option:", ["Master to Jobs", "Job to Masters"])

    if choice == "Master to Jobs":
        # Master to Jobs interface
        st.subheader("Find Jobs for a Master Program")
        
        selected_master_category = st.selectbox("Select a Master Program Category:", list(master_categories.keys()))
        category_masters = master_categories[selected_master_category]

        selected_master = st.selectbox("Select a Master Program:", [master['Title'] for master in category_masters])
        master_index_global = masters.index(next(master for master in category_masters if master['Title'] == selected_master))

        selected_job_category = st.selectbox("Select a Job Category:", list(job_categories.keys()))
        category_jobs = job_categories[selected_job_category]
        category_indices = [jobs.index(job) for job in category_jobs]

        # Show a progress bar during the calculation
        with st.spinner("Calculating job recommendations..."):
            category_similarities = similarity_matrix[master_index_global, category_indices]
            top_indices = np.argsort(-category_similarities)[:5]
            top_jobs = [(category_jobs[i]['Occupation'], category_similarities[i]) for i in top_indices if category_similarities[i] >= 0.2]

            if top_jobs:
                st.write(f"### Top job recommendations for '{selected_master}' in '{selected_job_category}':")
                for job, score in top_jobs:
                    st.markdown(f"- **{job}** (similarity: {score:.2f})")
            else:
                st.markdown("### No suitable match found in this category.")

    elif choice == "Job to Masters":
        # Job to Masters interface
        st.subheader("Find Master Programs for a Job")

        selected_job_category = st.selectbox("Select a Job Category:", list(job_categories.keys()))
        category_jobs = job_categories[selected_job_category]

        selected_job = st.selectbox("Select a Job:", [job['Occupation'] for job in category_jobs])
        job_index_global = jobs.index(next(job for job in category_jobs if job['Occupation'] == selected_job))

        # Show a progress bar during the calculation
        with st.spinner("Calculating master program recommendations..."):
            recommendations = recommend_masters_for_job(job_index_global, similarity_matrix, masters, jobs)
            st.write(f"### Top master program recommendations for '{selected_job}':")
            for recommendation in recommendations:
                st.markdown(f"- **{recommendation}**")

if __name__ == "__main__":
    main()
