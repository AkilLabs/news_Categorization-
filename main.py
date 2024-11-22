import streamlit as st
import time
import google.generativeai as genai
import google.api_core.exceptions
import json
import pandas as pd
import re
import os
import pdfplumber
import pytesseract
from PIL import Image
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import psutil
from sqlalchemy import create_engine
import pymysql

# Set path to tesseract executable (adjust if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Configure the Google Generative AI API
genai.configure(api_key="AIzaSyCGo58KpEwlSchahYyR8GLLfRRHdnUjTRM")  # Replace with your actual API key
model = genai.GenerativeModel('gemini-1.5-flash')  # Set the model to use

# Set up logging
logging.basicConfig(level=logging.INFO)

# Database connection details for MySQL
database_type = 'mysql+pymysql'
username = 'root'
password = ''
host = 'localhost'
database_name = 'newspaper3'

# Create the SQLAlchemy engine
try:
    engine = create_engine(f"{database_type}://{username}:{password}@{host}/{database_name}")
except Exception as e:
    st.error(f"Error establishing database connection: {e}")

# Function to clean extracted text
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'Advertisement|Sponsored|Click here', '', text, flags=re.IGNORECASE)
    return text.strip()

# Function to process each PDF page
def process_page(page):
    page_text = page.extract_text(x_tolerance=3, y_tolerance=3, layout=True)

    if page_text:
        return clean_text(page_text)

    page_image = page.to_image(resolution=150)  # Reduced resolution for faster processing
    img = page_image.original
    ocr_text = pytesseract.image_to_string(img)
    return clean_text(ocr_text)

# Function to extract text from PDF using multithreading for faster processing
def extract_text_from_pdf(pdf_file):
    all_text = []

    with pdfplumber.open(pdf_file) as pdf:
        total_pages = len(pdf.pages)
        progress_bar = st.progress(0)

        def process_single_page(page_num):
            page = pdf.pages[page_num]
            text = process_page(page)
            if text.strip():
                return f"\n###page {page_num + 1}\n" + text + "\n"
            return ""

        with ThreadPoolExecutor(max_workers=4) as executor:  # Limit threads for resource management
            future_to_page = {executor.submit(process_single_page, page_num): page_num for page_num in range(total_pages)}
            for i, future in enumerate(as_completed(future_to_page)):
                page_num = future_to_page[future]
                try:
                    all_text.append(future.result())
                except Exception as exc:
                    logging.error(f'Page {page_num} generated an exception: {exc}')
                progress_bar.progress((i + 1) / total_pages)

    return ''.join(all_text)

# Function to extract text from image files
def extract_text_from_image(image_file):
    img = Image.open(image_file)
    ocr_text = pytesseract.image_to_string(img)
    return clean_text(ocr_text)

# Function to categorize the news text for each chunk (page)
def categorize_text_chunk(model, chunk):
    prompt = f"""
    This is an extracted text from a newspaper. Please analyze the text, extract the meta details, and categorize the news articles into the following categories with specific sub-categories where applicable:
    you will be given a large chunk of news extracted text, which may not be aligned correctly. You have to correctly categorize the data according to the respective news, every text of news has to be categorized, ignore advertisements parts, from start to end, every news has to be categorized.
    Do not use comments or symbols like ##, **, etc. Give the categorized details in the respective json of each category.
Categories: Crime, Politics, Business, Health, Technology, Sport, Entertainment, Economics, World News, Local News, Science, Lifestyle, Education.
    Provide output in a structured json format with key details for each article.
        Crime:
    - Location: City, state, or country where the crime occurred.
    - Type of Crime: Theft, murder, cybercrime, fraud, assault, etc.
    - Suspects: Names and details of suspects.
    - Victims: Names and details of victims.
    - Date and Time: When the crime happened.
    - Authorities Involved: Law enforcement or government officials.
    - Motive: Possible reasons behind the crime.
    - Status: Investigation status, arrests made, trial updates.
    - Published Date:
    - Published Day:
    - Event Date:
    - Gist: A summary of the news in a single statement.
    
    Politics:
    - Region: Local, national, or international politics.
    - Government Policies: Legislation, regulations, and policy announcements.
    - Elections: Details about candidates, campaigns, results, election dates.
    - Political Parties: Name of the political party involved.
    - Officials: Politicians, leaders, and authorities.
    - Meetings and Summits: Important meetings, conferences, summits.
    - Reforms: Specific government reforms and their impact.
    - Published Date:
    - Published Day:
    - Event Date:
    - Gist: A summary of the news in a single statement.
    
    Business:
    - Industry: Sector such as technology, healthcare, finance, retail, energy, etc.
    - Companies: Specific companies involved, mergers, acquisitions.
    - Markets: Stock market, commodity market updates, foreign exchange.
    - Economic Policies: Policies affecting the business landscape.
    - Financial Results: Earnings, quarterly results, revenue, profit/loss.
    - Investments: Venture capital, foreign investments, funding rounds.
    - Startups: Startup news, funding, growth, and challenges.
    - Published Date:
    - Published Day:
    - Event Date:
    - Gist: A summary of the news in a single statement.
    
    Health:
    - Medical: Diseases, treatments, healthcare advancements, research findings.
    - Public Health: Health advisories, vaccination campaigns, awareness programs.
    - Fitness and Wellness: Exercise routines, nutrition tips, mental health.
    - Medical Institutions: Hospitals, healthcare centers, medical universities.
    - Health Policies: Government health policies, insurance updates.
    - Epidemics and Pandemics: Updates on health crises, measures taken.
    - Published Date:
    - Published Day:
    - Event Date:
    - Gist: A summary of the news in a single statement.
    
    Technology:
    - Industry: AI, software, hardware, cybersecurity, biotech.
    - Companies: Specific tech companies and startups, mergers, acquisitions.
    - Products and Gadgets: New launches, reviews, tech specifications.
    - Innovation: Research, patents, inventions, breakthroughs.
    - Cybersecurity: Data breaches, hacking incidents, security updates.
    - Emerging Technologies: Blockchain, quantum computing, IoT, etc.
    - Published Date:
    - Published Day:
    - Event Date:
    - Gist: A summary of the news in a single statement.
    
    Sport:
    - Level: Local, national, international, collegiate.
    - Sport Type: Football, cricket, tennis, basketball, athletics, etc.
    - Players: Names, biographies, achievements, injuries.
    - Match Details: Venue, teams, scores, key highlights, statistics.
    - Events: Tournaments, championships, leagues, medals.
    - Records: Records set or broken, milestones achieved.
    - Controversies: Doping, on-field disputes, rule violations.
    - Event Type: (e.g., IPL, T20, World Cup)
    - Event Level: (e.g., International, Domestic)
    - Published Date:
    - Published Day:
    - Event Date:
    - Gist: A summary of the news in a single statement.
    
    Entertainment:
    - Industry: Movies, music, theatre, television, OTT platforms.
    - Celebrities: Names, interviews, controversies, social media updates.
    - Events: Award shows, concerts, premieres, red carpet events.
    - Movies/Shows: Release dates, reviews, box office collections.
    - Music: Album releases, singles, concerts, chart performances.
    - Gossip: Rumors, relationships, celebrity feuds.
    - Published Date:
    - Published Day:
    - Event Date:
    - Gist: A summary of the news in a single statement.
    
    Economics:
    - Indicators: GDP, inflation, unemployment rates, consumer index.
    - Market Trends: Global economic trends, financial predictions.
    - Government Policies: Economic measures, regulations, fiscal policies.
    - Financial Institutions: Banks, IMF, World Bank activities.
    - International Trade: Import/export data, trade agreements, tariffs.
    - Economic Challenges: Recession, inflation, economic downturns.
    - Published Date:
    - Published Day:
    - Event Date:
    - Gist: A summary of the news in a single statement.
    
    World News:
    - Region: Continent or country-specific news.
    - Events: Major events such as conflicts, peace talks, summits, disasters.
    - Leaders: Presidents, prime ministers, international organizations.
    - Agreements: Treaties, pacts, international collaborations.
    - Conflicts: Wars, protests, disputes, humanitarian crises.
    - Published Date:
    - Published Day:
    - Event Date:
    - Gist: A summary of the news in a single statement.
    
    Local News:
    - Community Events: Fairs, festivals, gatherings, cultural events.
    - Development: Infrastructure projects, urban developments, new facilities.
    - Public Issues: Local government actions, citizen concerns, civic issues.
    - Education: Local school events, new programs, community classes.
    - Crime: Local incidents, neighborhood safety concerns.
    - Published Date:
    - Published Day:
    - Event Date:
    - Gist: A summary of the news in a single statement.
    
    Science:
    - Field: Physics, biology, chemistry, astronomy, environmental science.
    - Discoveries: Breakthroughs, research findings, experiments.
    - Institutions: Research institutions, universities, notable scientists.
    - Space Exploration: Missions, satellite launches, discoveries in space.
    - Environmental Science: Climate change, conservation, biodiversity.
    - Technological Applications: Practical use of scientific discoveries.
    - Published Date:
    - Published Day:
    - Event Date:
    - Gist: A summary of the news in a single statement.
    
    Lifestyle:
    - Category: Fashion, travel, food, home decor, wellness.
    - Trends: Popular trends in fashion, food, travel destinations.
    - Tips: Health tips, relationship advice, home improvement.
    - Personal Stories: Interviews, experiences, lifestyle changes.
    - Luxury: High-end fashion, luxury travel, exclusive events.
    - Published Date:
    - Published Day:
    - Event Date:
    - Gist: A summary of the news in a single statement.
    
    Education:
    - Institutions: Schools, colleges, universities, rankings.
    - Programs: New courses, online programs, vocational training.
    - Exams: Examination schedules, results, guidelines, preparation tips.
    - Scholarships: Scholarships, fellowships, grants, application details.
    - Reforms: Changes in educational policies, curriculum updates.
    - Achievements: Student achievements, awards, academic milestones.
    - Published Date:
    - Published Day:
    - Event Date:
    - Gist: A summary of the news in a single statement.
    Extract and include the *published date, **published day, and **event date* where applicable.
    the published day should be correctly calculated based in the date and year of the newspaper.
    The extracted text is:



    {chunk}
    """

    retries = 3
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except google.api_core.exceptions.RetryError:
            if attempt < retries - 1:
                time.sleep(5)  # Wait before retrying
            else:
                st.error("Failed to connect to the Generative AI service after multiple attempts.")
                return ""
        except google.api_core.exceptions.GoogleAPICallError as e:
            st.error(f"An error occurred: {e}")
            return ""

# Function to clean and parse large AI response into JSON format
def parse_categorized_response_to_json(response_text):
    try:
        cleaned_response = re.sub(r'\s*json\s*||\s*```', '', response_text.strip())
        cleaned_response = re.sub(r'(?<=[}\]])(?=\s*[{[]|\s*$)', ',', cleaned_response)
        cleaned_response = cleaned_response.replace('\n', '')
        cleaned_response = re.sub(r',\s*([}\]])', r'\1', cleaned_response)
        cleaned_response = re.sub(r'(?<!\\)\'([a-zA-Z0-9_]+)\':', r'"\1":', cleaned_response)

        last_valid_brace = max(cleaned_response.rfind('}'), cleaned_response.rfind(']'))
        if last_valid_brace != -1:
            cleaned_response = cleaned_response[:last_valid_brace + 1]

        categorized_data = json.loads(cleaned_response)

        if isinstance(categorized_data, list):
            categorized_data = {"Uncategorized": categorized_data}

    except json.JSONDecodeError:
        return {}

    return categorized_data

# Function to convert JSON response to DataFrames
def convert_json_to_dataframes(categorized_data):
    dataframes = {}
    for category, articles in categorized_data.items():
        if isinstance(articles, list) and articles:
            dataframes[category] = pd.DataFrame(articles)
    return dataframes

# Function to save data directly to SQL database
def save_to_sql(dataframes):
    with engine.connect() as connection:
        for category, df in dataframes.items():
            try:
                df.to_sql(category.lower(), con=engine, if_exists='append', index=False)
                logging.info(f"Data from category '{category}' saved to table '{category.lower()}'.")
            except Exception as e:
                logging.error(f"Error saving data from category '{category}': {e}")

# Function to split the extracted text into individual news articles
def split_text_into_articles(extracted_text):
    article_pattern = r"(?<=\n)\s*(?=\w)"
    articles = re.split(article_pattern, extracted_text)
    cleaned_articles = [article.strip() for article in articles if article.strip()]
    return cleaned_articles

# Function to categorize all articles
def categorize_articles(articles):
    final_result = {}
    batch_size = 5
    if len(articles) == 0:
        st.warning("No articles to categorize.")
        return final_result

    progress_bar = st.progress(0)
    total_batches = (len(articles) + batch_size - 1) // batch_size

    with ThreadPoolExecutor(max_workers=min(psutil.cpu_count(logical=False), 4)) as executor:
        for i in range(0, len(articles), batch_size):
            batch = articles[i:min(i + batch_size, len(articles))]
            results = list(executor.map(lambda article: categorize_text_chunk(model, article), batch))
            for response_text in results:
                if response_text:
                    categorized_data = parse_categorized_response_to_json(response_text)
                    if categorized_data:
                        for category, articles in categorized_data.items():
                            if category not in final_result:
                                final_result[category] = articles
                            else:
                                if isinstance(articles, list):
                                    final_result[category].extend(articles)
                                else:
                                    final_result[category].append(articles)
            
    return final_result

# Streamlit UI
def app():
    st.markdown("""
        <style>
            /* Gradient Background */
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Main container styles with glass morphism */
.main {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Container styles */
.css-1d391kg, .css-12oz5g7 {
    background: rgba(255, 255, 255, 0.1) !important;
    border-radius: 1rem !important;
    padding: 2rem !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

/* Title styles */
.css-10trblm.e16nr0p30 {
    color: white;
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

/* Enhanced File Uploader Styles */
[data-testid="stFileUploader"] {
    width: 100%;
    margin: 2rem 0;
}

/* Modern File Upload Container */
[data-testid="stFileUploadDropzone"] {
    min-height: 300px !important;
    background: rgba(255, 255, 255, 0.1) !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    border: 2px dashed rgba(255, 255, 255, 0.3) !important;
    border-radius: 1.5rem !important;
    transition: all 0.3s ease !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-direction: column !important;
    gap: 1rem !important;
    padding: 2rem !important;
    position: relative !important;
    cursor: pointer !important;
}

[data-testid="stFileUploadDropzone"]:hover {
    background: rgba(255, 255, 255, 0.2) !important;
    border-color: rgba(255, 255, 255, 0.5) !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

[data-testid="stFileUploadDropzone"]::before {
    content: "📄";
    font-size: 3rem;
    margin-bottom: 1rem;
}

[data-testid="stFileUploadDropzone"]::after {
    content: "Drag and Drop or Click to Upload";
    font-size: 1.25rem;
    font-weight: 600;
    color: white;
    text-align: center;
    position: absolute;
    top: 60%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 100%;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
}

/* File Upload Instructions */
[data-testid="stFileUploadDropzone"] small {
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.8);
    position: absolute;
    bottom: 2rem;
    text-align: center;
}

/* Upload Button Style */
[data-testid="stFileUploadDropzone"] button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    padding: 0.75rem 2rem !important;
    border-radius: 2rem !important;
    border: none !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    margin-top: 1rem !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}

[data-testid="stFileUploadDropzone"] button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3) !important;
}

/* Uploaded File Container */
[data-testid="stFileUploader"] section[data-testid="stFileUploadResults"] {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 1rem;
    padding: 1.5rem;
    margin-top: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* File Details */
[data-testid="stMarkdownContainer"] p {
    margin: 0;
    padding: 0.5rem 0;
    color: white;
}

/* Clear File Button */
button[kind="secondary"] {
    background: linear-gradient(135deg, #f43f5e 0%, #ef4444 100%) !important;
    color: white !important;
    border: none !important;
    padding: 0.75rem 1.5rem !important;
    border-radius: 2rem !important;
    font-size: 0.875rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}

button[kind="secondary"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3) !important;
}

/* Primary Button styles */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white;
    padding: 0.75rem 2rem;
    border-radius: 2rem;
    border: none;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    text-transform: uppercase;
    letter-spacing: 1px;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

/* Progress bar styles */
.stProgress > div > div {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 1rem;
}

/* Expander styles */
.streamlit-expanderHeader {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 1rem;
    padding: 1rem;
    margin-bottom: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: white;
}

.streamlit-expanderContent {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 1rem;
    padding: 1rem;
    margin-top: 0.5rem;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Text area styles */
.stTextArea > div > textarea {
    background: rgba(255, 255, 255, 0.1) !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 1rem !important;
    padding: 1rem !important;
    font-family: monospace !important;
    font-size: 0.875rem !important;
    line-height: 1.5 !important;
    color: white !important;
}

/* Info/Warning/Success message styles */
.stAlert {
    background: rgba(255, 255, 255, 0.1) !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    border-radius: 1rem !important;
    padding: 1rem !important;
    margin: 1rem 0 !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    color: white !important;
}

/* JSON viewer styles */
.element-container:has(pre) {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 1rem;
    padding: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: white;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .main {
        padding: 1rem;
    }
    
    .css-10trblm.e16nr0p30 {
        font-size: 2rem;
    }
    
    [data-testid="stFileUploadDropzone"] {
        min-height: 200px !important;
    }
    
    [data-testid="stFileUploadDropzone"]::before {
        font-size: 2rem;
    }
    
    [data-testid="stFileUploadDropzone"]::after {
        font-size: 1rem;
    }
}
                </style>
    """, unsafe_allow_html=True)
    st.title("📰 News Categorization Tool")

    # File uploader for PDF or Image
    uploaded_file = st.file_uploader("Upload a PDF file or an Image (PNG, JPEG)", type=["pdf", "png", "jpg", "jpeg"])

    if uploaded_file is not None:
        extraction_placeholder = st.empty()
        extraction_placeholder.info("Extracting text from the uploaded file...")
        
        if uploaded_file.name.lower().endswith(('.pdf')):
            extracted_text = extract_text_from_pdf(uploaded_file)
        else:
            extracted_text = extract_text_from_image(uploaded_file)

        extraction_placeholder.empty()

        # Button to view extracted text
        with st.expander("View Extracted Text"):
            st.text_area("Extracted Data", extracted_text, height=400)

        # Button to categorize the text
        if st.button("Categorize"):
            if extracted_text.strip() == "":
                st.warning("No text found to categorize.")
            else:
                categorization_placeholder = st.empty()
                categorization_placeholder.info("Splitting and categorizing articles...")
                articles = split_text_into_articles(extracted_text)
                final_result = categorize_articles(articles)

                categorization_placeholder.empty()

                if final_result:
                    # Button to view categorized JSON
                    with st.expander("View Categorized JSON"):
                        st.json(final_result)

                    # Convert JSON to DataFrames and save to SQL database
                    dataframes = convert_json_to_dataframes(final_result)
                    save_to_sql(dataframes)

                    st.success("Categorized data saved to database successfully.")

if __name__ == "__main__":
    app()
