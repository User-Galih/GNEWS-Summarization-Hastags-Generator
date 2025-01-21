# GNews Summarization
## Creator: Galih Putra Pratama

GNews Summarization is an application that combines natural language processing (NLP) and machine learning to automatically summarize news articles. This project aims to help users extract relevant information from news articles without being distracted by ads or unnecessary elements. Additionally, it generates relevant hashtags based on the article.

## Background:
Often, when reading news articles online, users are faced with various distractions such as pop-up ads or overly long and tedious articles. These factors reduce reading comfort and hinder understanding of the information. GNews Summarization aims to solve this issue by efficiently summarizing articles and removing those distractions.

### NOTE: The summarized articles will be automatically saved in the path D:\KULIAH\SEMESTER 5\STKI\GNews_Summarization\news_summaries.xlsx, so users do not need to manually create the folder.

## Methods Used:
GNews Summarization uses various methods and techniques to process and summarize articles. Here are the details:
1. Article Retrieval (Web Scraping):
Techniques Used: requests, BeautifulSoup
Description: The article is retrieved using the URL provided by the user. The requests library downloads the HTML page, and BeautifulSoup is used to parse the HTML and extract the article text, ignoring irrelevant elements such as ads or sidebars.
2. Article Translation (Optional):
Techniques Used: googletrans API (Google Translate)
Description: The retrieved article can be translated into the user-selected language using the googletrans API. If the article is already in the selected language, it is not translated.
3. Article Summarization:
GNews Summarization offers two methods for summarizing articles:
    - Flexible Summary (Clustering):
    Techniques Used: KMeans Clustering, TF-IDF (Term Frequency-Inverse Document Frequency)
    Description: The article is divided into clusters using KMeans algorithm, based on a TF-IDF representation of the text. This method identifies the importance of words based on frequency    (TF) and rarity across the entire corpus (IDF). Sentences from each cluster are selected to form a more focused summary.
    - Long Summary:
    Techniques Used: Direct Sentence Composition
    Description: A longer summary is created by combining all sentences in the article into a single paragraph, providing a general overview of the entire article.
4. Hashtag Generation:
Techniques Used: TF-IDF to select the most relevant words
Description: The system analyzes the article's title and content to generate relevant hashtags. By using TF-IDF, the system identifies the most frequent and important words in the article. These hashtags help users understand the main topic and facilitate finding related articles on social media or other platforms.
5. Data Storage and Management:
Techniques Used: Pandas (for data management), Excel (for storage)
Description: All generated summaries and hashtags are saved in an Excel file (news_summaries.xlsx). This file acts as a database containing the summary results, which can be loaded later for further analysis or review.

## User Interface (Streamlit):
- Streamlit is used to build the user interface. Users can input the article URL, select the language, and view the generated summaries and hashtags. The results can also be saved and viewed in tabular format.
- Visualization: An infographic showing the number of words per summary point is displayed using matplotlib, providing a clearer view of the summary structure.
- 
## Usage Instructions:
1. Input Article URL: The user enters the URL of the article to be analyzed.
2. Select Language: The user selects the language for article translation (if needed).
3. Process Summarization: The user presses the "Summarize and Generate Hashtags" button to start the summarization and hashtag generation process.
4. View Summary and Hashtags: The generated summary and hashtags will be displayed.
5. Save and View Dataset: The generated summary data will be saved to an Excel file and can be viewed within the app.

## Code Explanation:
### 1. Import Libraries:
The code uses several Python libraries for text processing, web application building, and data management and visualization. Some of the key libraries include:
- nltk: For text processing, such as tokenization.
- streamlit: For building the interactive web application.
- requests: For fetching data from the URL (downloading the article).
- BeautifulSoup: For parsing HTML articles.
- matplotlib: For visualizing the infographic.
- sklearn: For data processing and clustering.
- googletrans: For text translation.
- pandas: For data manipulation (e.g., saving and loading datasets).

### 2. Function Explanations:
- save_to_excel: This function saves or updates the dataset containing the article summaries and generated hashtags in an Excel file. If the file doesn't exist, it will create a new one.
- load_dataset: This function loads the dataset from an existing Excel file, allowing users to view the history of generated summaries.
- Stopwords for Different Languages: The stop_words variable contains stopwords (common words that have little significance) for various languages, including English, Indonesian, Spanish, and French.
- fetch_article: This function retrieves the article from the provided URL, extracts the title and content, and cleans the article from irrelevant elements like ads using regex.
- summarize_article_flexible: This function analyzes and summarizes the article using KMeans clustering based on TF-IDF. The article is divided into clusters, and key sentences from each cluster are selected for the summary.
- long_summary: This function generates a longer summary by combining all the sentences from the article.
- translate_article: This function translates the article into the user-selected language. If the article is already in the selected language, no translation is done.
- generate_hashtags: This function analyzes the article's title and content to generate relevant hashtags using TF-IDF to determine the most important words.
- main: The main function of the Streamlit app where users can:
  - Enter the article URL.
  - Select the translation language.
  - Click the button to start the summarization and hashtag generation.
  - View the generated summary and hashtags.
  - Save the results to the dataset and display them in the app interface.
    
Feel free to adjust or expand this README further based on additional details or specific instructions for users.
