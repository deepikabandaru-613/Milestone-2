import streamlit as st
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import PyPDF2

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Title
st.title("Smart Renewable Energy Report Analyzer")

# Upload file
uploaded_file = st.file_uploader(
    "Upload Energy Report",
    type=["txt" , "pdf"]
)

# If file uploaded
if uploaded_file is not None:

    # Read content
    # Read TXT File
    if uploaded_file.type == "text/plain":

       content = uploaded_file.read().decode("utf-8")

    # Read PDF File  
    else:

        pdf_reader = PyPDF2.PdfReader(uploaded_file)

        content = ""

    for page in pdf_reader.pages:

        content += page.extract_text()

    # Show report
    st.subheader("Uploaded Report")

    st.write(content)

    # Sentiment Analysis
    blob = TextBlob(content)

    sentiment = blob.sentiment.polarity

    st.subheader("Sentiment Analysis")

    if sentiment > 0:

        st.success("Positive Sentiment 😊")

    elif sentiment < 0:

        st.error("Negative Sentiment 😞")

    else:

        st.info("Neutral Sentiment 😐")

    # Report Summary
    st.subheader("Report Summary")

    parser = PlaintextParser.from_string(
        content,
        Tokenizer("english")
    )

    summarizer = LsaSummarizer()

    summary = summarizer(parser.document, 2)

    for sentence in summary:

        st.write(sentence)
        
    # Word Cloud
    st.subheader("Word Cloud")      
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(content)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)
   
    # Download Report

    final_report = f"""
    SMART RENEWABLE ENERGY REPORT ANALYSIS

    Uploaded Report:
    {content}

    Sentiment Result:
    {"Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"}

    Summary:
    """

    for sentence in summary:

      final_report += str(sentence) + "\n"

    st.download_button(

      label="Download Analyzed Report",

      data=final_report,

      file_name="analyzed_report.txt",

      mime="text/plain"
    )
    
    # Chatbot Section

st.subheader("Energy Report Chatbot")

question = st.text_input("Ask a question about the report")

if question:

    question = question.lower()

    if "solar" in question:

        st.write("The report discusses solar energy performance.")

    elif "wind" in question:

        st.write("The report contains wind energy information.")

    elif "growth" in question:

        st.write("The report mentions project growth analysis.")

    elif "summary" in question:

        st.write("Summary:")
        
        for sentence in summary:

            st.write(sentence)

    else:

        st.write("Information not found in report.")