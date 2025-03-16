**A cold email generator tool which will help you to generate them quickly, simply to fire up your application process.** 

---

Usage:
1. Fill your portfolio info with relevant skills and links for it in the portfolio.csv
2. Copy and Paste a Job Posting URL on the streamlit app
3. Get a cold email personalized according to your relevant portfolio links and the job description.

---

Technologies Used :
1. Llama 3.1 (70b parameters): For extracting Info & generating Emails - ran using Groq
2. ChromaDB: To store and retrieve skills and portfolio information
3. Streamlit: For the end user UI
4. Langchain: For web scraping and building the LLM Application.
