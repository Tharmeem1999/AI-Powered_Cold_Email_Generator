# 📧 AI-Powered Cold Email Generator

This project automates the creation of personalized cold emails for B2B sales in the software services industry. By scraping a potential client's career page, the application identifies their hiring needs and crafts a tailored email offering relevant services, complete with portfolio examples to showcase expertise.

The core of this project uses **Llama 3.3** via the Groq API for fast generation, **ChromaDB** as a local vector store for portfolio matching, **LangChain** to orchestrate the workflow, and **Streamlit** for a simple, interactive user interface.

-----

## Overview

In the software services industry, **cold mailing** is a key business development strategy. It involves sending unsolicited emails to potential clients to offer services. This project streamlines that process. For example, if a company like Nike posts a job for an "AI/ML Engineer," this tool can generate an email to Nike. The email will highlight the skills mentioned in the job post and propose fulfilling their needs with contract-based services from our company, "Pearl Systems," emphasizing benefits like cost-efficiency and flexibility.

The application works by:

1.  Scraping job postings from a company's career page URL.
2.  Extracting key details like **role, experience, and required skills**.
3.  Searching a **portfolio database** for the most relevant past projects based on those skills.
4.  Generating a persuasive, personalized cold email that incorporates the job details and portfolio links.

-----

## ⚙️ Technical Architecture

The project follows a simple, powerful, end-to-end workflow that integrates web scraping, vector search, Large Language Model (LLM) generation, and a front-end UI.

**The data flows through these steps:**

1.  **Scrape Job Posting**: The user provides a URL to a careers page. LangChain's `WebBaseLoader` scrapes the raw HTML content.
2.  **Extract Job Data**: The scraped text is cleaned and fed to **Llama 3.3**. The LLM extracts structured information (role, skills, experience) and returns it in a clean JSON format.
3.  **Query Portfolio**: The extracted skills are used to perform a similarity search in **ChromaDB**. This vector store contains embeddings of our company's portfolio, where each entry links a tech stack to a project URL. The query returns the most relevant project links.
4.  **Generate Cold Email**: The structured job data and the relevant portfolio links are combined in a final prompt. **Llama 3.3** uses this context to generate a persuasive and highly relevant cold email from the perspective of a Business Development Executive.
5.  **Display Email**: The final email is displayed to the user in the **Streamlit** web interface.

-----

## 🛠️ Technologies & Packages Used

This project leverages a modern stack for generative AI applications:

  * **Large Language Model**: Llama 3.3 (via Groq API for high-speed inference)
  * **LLM Framework**: LangChain
  * **Vector Database**: ChromaDB (for local, efficient similarity search)
  * **Web UI Framework**: Streamlit
  * **Data Handling**: Pandas
  * **Environment Management**: python-dotenv

-----

## 🚀 Set Up

Follow these steps to set up and run the project on your local machine.


### 1\. Install Dependencies

Install all the required Python packages using the `requirements.txt` file.

```bash
pip install streamlit langchain-groq langchain chromadb pandas python-dotenv langchain-community
```

### 2\. Configure Environment Variables

You need a Groq API key to use Llama 3.3.

1.  Create a file named `.env` in the root directory of the project.
2.  Get your free API key from the **[Groq Console](https://console.groq.com/keys)**.
3.  Add the key to your `.env` file:
    ```
    GROQ_API_KEY="your-groq-api-key-here"
    ```

### 3\. Prepare the Portfolio Data

The `my_portfolio.csv` file acts as the knowledge base for your company's projects. Make sure it is located at `app/resource/my_portfolio.csv`. The current file uses dummy URLs, which you should replace with your actual project links.

The CSV file must contain the following columns:

  * `Techstack`: A description of the technologies and skills used in the project.
  * `Links`: The URL to the project or case study.

### 4\. Coding

This project includes three main Python files that you will need. Use them as provided or adapt them to suit your requirements.

### 5\. Run the Application

Once the setup is complete, you can run the Streamlit application with the following command:

```bash
streamlit run main.py
```

Open your web browser and navigate to the local URL provided by Streamlit (usually `http://localhost:8501`).

-----

  * **`main.py`**: Entry point for the Streamlit application. It handles the user interface and orchestrates calls to other modules.
  * **`chains.py`**: Defines the logic for interacting with the LLM. It includes prompt templates for extracting job details and writing the final email.
  * **`portfolio.py`**: Manages the ChromaDB vector store. It loads data from the CSV, creates embeddings, and provides a query interface to find relevant projects.
