# Import libraries
import nltk
import streamlit as st
import requests
import matplotlib.pyplot as plt
import io
import re
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from googletrans import Translator

import os
import pandas as pd
from datetime import datetime

# Download stopwords for nltk
nltk.download('punkt')
nltk.download('stopwords')

# Define the fixed path to save the Excel file
dataset_path = r'D:\KULIAH\SEMESTER 5\STKI\GNews_Summarization\news_summaries.xlsx'

# Function to save data to Excel
def save_to_excel(dataset):
    # Membuat folder jika belum ada
    folder_path = os.path.dirname(dataset_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Check if the file exists
    if os.path.exists(dataset_path):
        # Append data to the existing Excel file
        with pd.ExcelWriter(dataset_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            dataset.to_excel(writer, index=False, sheet_name='Summarizations', header=False, startrow=writer.sheets['Summarizations'].max_row)
    else:
        # Create a new file if it doesn't exist
        with pd.ExcelWriter(dataset_path, engine='xlsxwriter') as writer:
            dataset.to_excel(writer, index=False, sheet_name='Summarizations')

# Function to display dataset
@st.cache_data
def load_dataset():
    # Clear cache before loading the dataset
    st.cache_data.clear()

    if os.path.exists(dataset_path):
        return pd.read_excel(dataset_path, sheet_name='Summarizations')
    return pd.DataFrame(columns=['Title', 'Summary', 'Detailed Summary', 'Hashtags', 'Date'])



# Initialize stop words for multiple languages
stop_words = {
    'en': set(stopwords.words('english')).union({'said', 'will', 'also', 'one', 'new', 'make'}),
    'id': set(stopwords.words('indonesian')).union({'dan', 'yang', 'di', 'dari', 'pada', 'untuk', 'dengan', 'ke', 'dalam', 'adalah'}),
    'es': set(stopwords.words('spanish')).union({'y', 'el', 'en', 'con', 'para', 'de'}),
    'fr': set(stopwords.words('french')).union({'et', 'le', 'est', 'dans', 'sur', 'avec'})
}

# Function to fetch and parse the article from the given URL
def fetch_article(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else 'No Title Found'
        paragraphs = soup.find_all('p')
        article = ' '.join([para.get_text() for para in paragraphs])
        
        # Remove common ad phrases
        ad_patterns = re.compile(r"(Advertisement|Scroll to Continue|Baca Juga|Lanjutkan dengan Konten)", re.IGNORECASE)
        article_cleaned = ad_patterns.sub('', article)
        
        return title, article_cleaned.strip()
    else:
        return None, None

# Function to summarize the article into key points and generate infographic
def summarize_article_flexible(article, num_clusters=2):
    sentences = sent_tokenize(article)
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(sentences)
    kmeans = KMeans(n_clusters=num_clusters, n_init=10)
    kmeans.fit(X)

    # Get key points from each cluster
    point_summary = []
    for i in range(num_clusters):
        cluster_sentences = [sentences[j] for j in range(len(sentences)) if kmeans.labels_[j] == i]
        if cluster_sentences:
            point_summary.append(max(cluster_sentences, key=len))  # Longest sentence as key point

    # Short paragraph summary
    paragraph_summary = ' '.join(point_summary)

    # Infographic: Visualizing word counts
    sentence_lengths = [len(sentence.split()) for sentence in point_summary]
    plt.figure(figsize=(6, 4))
    plt.bar(range(1, len(point_summary) + 1), sentence_lengths, color='skyblue')
    plt.xlabel('Point Number')
    plt.ylabel('Word Count')
    plt.title('Word Count per Key Point')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    return point_summary, paragraph_summary, buf

# Function to generate a longer summary using all sentences
def long_summary(article):
    sentences = sent_tokenize(article)
    return ' '.join(sentences)

# Function to translate the article to a specific language
def translate_article(article, dest_language='en'):
    translator = Translator()
    try:
        detected_lang = translator.detect(article).lang
        if detected_lang != dest_language:
            translated = translator.translate(article, dest=dest_language)
            return translated.text
        else:
            return article
    except Exception as e:
        st.error(f'Translation failed: {e}')
        return None

# Function to generate hashtags from title and content
def generate_hashtags(title, content, lang='en', num_hashtags=5):
    stop_words_set = stop_words.get(lang, set())
    title_words = [word for word in word_tokenize(title.lower()) if word.isalnum() and len(word) > 3 and word not in stop_words_set]
    content_words = [word for word in word_tokenize(content.lower()) if word.isalnum() and len(word) > 3 and word not in stop_words_set]
    
    # Combine title and content words, giving more weight to title words
    keywords = title_words * 2 + content_words  # Doubling title words to increase their weight

    # Generate TF-IDF scores
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform([' '.join(keywords)])
    
    tfidf_scores = X.toarray().flatten()
    feature_names = vectorizer.get_feature_names_out()
    scored_keywords = sorted(zip(feature_names, tfidf_scores), key=lambda x: x[1], reverse=True)
    
    top_keywords = [f"#{keyword.capitalize()}" for keyword, score in scored_keywords[:num_hashtags]]
    return top_keywords

def main():
    st.title('GNews Summarization & Hashtag Generator App')

    # Store URL and selected language in session state
    if 'url' not in st.session_state:
        st.session_state.url = ""
    if 'lang' not in st.session_state:
        st.session_state.lang = "en"

    st.session_state.url = st.text_input('Enter the URL of the news article:', st.session_state.url)
    st.session_state.lang = st.selectbox('Select language for translation:', ['en', 'id', 'es', 'fr'], index=['en', 'id', 'es', 'fr'].index(st.session_state.lang))

    if st.button('Summarize and Generate Hashtags'):
        if st.session_state.url:
            if not (st.session_state.url.startswith('http://') or st.session_state.url.startswith('https://')):
                st.error('Please enter a valid URL starting with http:// or https://')
                return
            
            title, article = fetch_article(st.session_state.url)
            if article:
                if not article.strip():
                    st.error('The article is empty or could not be fetched.')
                    return

                # Translate title if necessary
                translated_title = translate_article(title, st.session_state.lang)
                st.subheader('Article Title:')
                st.write(translated_title)

                # Translate the article if necessary
                translated_article = translate_article(article, st.session_state.lang)
                if translated_article is None:
                    return

                num_clusters = st.slider('Select the number of clusters for summarization:', 1, 5, 2)
                point_summary, paragraph_summary, infographic_buf = summarize_article_flexible(translated_article, num_clusters)

                # Display flexible summary options
                st.subheader('Flexible Summary Options:')
                
                # Key Points
                st.write("### Key Points:")
                for idx, point in enumerate(point_summary, 1):
                    st.write(f"{idx}. {point}")

                # Short Paragraph
                st.write("### Short Paragraph:")
                st.write(paragraph_summary)

                # Longer summary
                detailed_summary = long_summary(translated_article)
                st.write("### Detailed Summary:")
                st.write(detailed_summary)

        
                # Generate hashtags
                hashtags = generate_hashtags(translated_title, translated_article, st.session_state.lang)
                st.subheader('Generated Hashtags:')
                st.write(', '.join(hashtags))

                st.success("Summary and hashtags generated successfully!")

                # Inisialisasi DataFrame kosong
                if 'dataset' not in st.session_state:
                    st.session_state.dataset = pd.DataFrame(columns=['Title', 'Summary', 'Detailed Summary', 'Hashtags', 'Date'])

                # Prepare new data to append
                new_data = pd.DataFrame({
                    'Title': [translated_title],
                    'Summary': [paragraph_summary],
                    'Detailed Summary': [detailed_summary],
                    'Hashtags': [', '.join(hashtags)],
                    'Date': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
                })

                # Save the new data to Excel
                save_to_excel(new_data)

                st.success('Data added to dataset and saved to Excel!')

                # Display dataset in main area
                st.subheader('Dataset Viewer')
                df = load_dataset()
                if not df.empty:
                    
                    st.dataframe(df)
                else:
                    st.warning('No dataset found. Please generate summaries to create the dataset.')


# Run the app
if __name__ == "__main__":
    main()
    
