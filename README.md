# Conversational AI Platform

> **A FastAPI application for conversational queries.**  
> Combines **RAG** (Retrieval Augmented Generation) for food-related queries with an **OpenWeather** integration for weather updates. Supports **PDF** document processing and vector storage in **ChromaDB**.

---

## Table of Contents
- [Conversational AI Platform](#conversational-ai-platform)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Architecture \& Approach](#architecture--approach)
  - [Assumptions](#assumptions)
  - [Setup Instructions](#setup-instructions)
  - [Challenges](#challenges)
  - [License](#license)
  - [Thank You!](#thank-you)

---

## Project Overview

This **Conversational AI Platform** focuses on providing a user-friendly interface to:
- **Answer food-related queries** using **RAG** (Retrieval Augmented Generation) with the **llama-3.3-70b** model.
- **Answer weather queries** by retrieving data from **OpenWeather** and summarizing it with **GPT-4o**.
- **Upload and process PDF documents** into chunks, embed them, and store these embeddings in **ChromaDB** for future retrieval.

The project demonstrates how to seamlessly combine local LLM-based classification, advanced large models, and third-party APIs to build a robust backend system.

---

## Architecture & Approach

1. **FastAPI Backend**  
   - Provides **API endpoints** to handle **messages** and **documents**.  
   - Auto-generates **Swagger** (OpenAPI) documentation at `/docs`.

2. **SQLAlchemy ORM**  
   - Manages relational data for **Messages**, **Documents**, and **DocumentPages**.  

3. **Message Classification**  
   - Uses a **lightweight LLM** to classify user messages as either **food** or **weather**.

4. **RAG for Food Queries**  
   - On a **food** query, the system performs a **ChromaDB** similarity search to find relevant chunks.  
   - These chunks and the user’s prompt are fed into **llama-3.3-70b** (Groq) for context-based answers.

5. **Weather Queries**  
   - For **weather** classification, the system calls **OpenWeather** to get current weather data for New York.  
   - Uses **GPT-4o** to transform this data into a human-friendly summary.

6. **ChromaDB Vector Storage**  
   - PDF chunks are stored and retrieved from **ChromaDB**, enabling quick semantic lookups.

7. **Document Processing**  
   - **PDF** uploads are processed to extract text per page, split into chunks, embed with **OpenAI Embeddings**, and save vector data in ChromaDB.

---

## Assumptions

- **Local Setup**: You have Python (3.8+) and PostgreSQL installed locally.  
- **Database URL**: The system reads the DB connection info from `.env`.  
- **API Keys**:
  - **OpenAI** key is set as `OPENAI_API_KEY` in `.env`.  
  - **Groq** key (`GROQ_API_KEY`) needs to be generated from [Groq’s platform](https://groq.com).  
  - **OpenWeather** key (`WEATHER_API_KEY`) is used for fetching weather data.

- **Document Upload**: Only **PDF** files are supported. Large PDF uploads may take time to process.

- **Model Endpoints**:  
  - Llama 3.3 70b (Groq) endpoint is assumed to be accessible via a custom API route.  
  - GPT-4o is accessed via the **OpenAI** library (assuming a valid subscription or dev token).

---

## Setup Instructions

1. **Clone Repository & Install Dependencies**  
   ```bash
   git clone https://github.com/username/conversational-ai-platform.git
   cd conversational-ai-platform
   pip install -r requirements.txt
   cp .env.example .env 
2. **Edit .env file**
    - Update the following variables in .env
      - DATABASE_URL: Replace user, password, and dbname with your PostgreSQL credentials and desired database name.
      - OPENAI_API_KEY: Your OpenAI API key for accessing OpenAI services.
      - GROQ_API_KEY: Your Groq API key for accessing Groq services.
      - WEATHER_API_KEY: Your OpenWeather API key for fetching weather data.
      - WEATHER_API_BASE_URL: Base URL for the OpenWeather API (usually remains as provided).
3. **Run the Application**
    - Start the FastAPI application using Uvicorn with the --reload flag for development purposes. This flag enables automatic reloads on code changes.
   `uvicorn app.main:app --reload`
   The API should now be running and accessible at:
   `http://127.0.0.1:8000`
4. **View API Documentation**
   - FastAPI provides interactive API documentation out of the box. You can access two different documentation interfaces:
     - Swagger UI: A user-friendly interface for testing API endpoints. `http://127.0.0.1:8000/docs`
     Body (raw):
     {
      "content": "How do I make the best spaghetti carbonara?"
     }
     - ReDoc: A more detailed and structured API documentation interface.`http://127.0.0.1:8000/redoc`
5. **Testing Instructions**
    - Use your *host name* (e.g., http://127.0.0.1:8000/) along with some of the allowed paths
    - `{host}/messages` POST: With this enpoint you will be able to test the conversation feature
    - `{host}/documents` POST: With this enpoint you can test the document upload feature, note that the Content-Type must be `multipart/form-data`,`the title field must have the desired `title` for the document, the `file` field must have the PDF file.

## Challenges
Developing this Conversational AI Platform involved navigating several complex challenges. Below are the key obstacles encountered and the strategies employed to overcome them:
 1.	RAG Integration Complexity
- Challenge: Combining multiple vector operations, LLM calls, and chunked PDFs for food queries was intricate. Ensuring data alignment between embeddings and text required meticulous orchestration.
- Solution: Implemented a streamlined processing pipeline with clear separation of concerns, utilizing robust logging to trace data flow and troubleshoot alignment issues.
 2.	Large PDF Handling
- Challenge: Splitting, embedding, and storing large files in ChromaDB was time-intensive, leading to potential performance bottlenecks.
- Solution: Optimized chunk size and implemented concurrency where possible to enhance processing speed. Employed efficient text extraction and embedding techniques to handle large volumes of data effectively.
 3.	Database & Vector Store Synchronization
- Challenge: Maintaining a consistent flow from SQL-based document/page records to ChromaDB vectors demanded careful transactional logic to avoid partial states.
- Solution: Implemented transactional operations with SQLAlchemy sessions to ensure atomicity. Utilized comprehensive logging to monitor synchronization processes and quickly identify discrepancies.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Thank You!

Thank you for exploring this Conversational AI Platform! This project showcases the integration of advanced technologies like RAG, LLMs, and vector databases to create a seamless and intelligent backend system.

**Contributions:**
- Feel free to contribute, open issues, and propose enhancements to make this project even better.
- Whether it’s optimizing existing functionalities, adding new features, or improving documentation, your input is highly valued.

**Questions & Support:**
- If you have any questions, need assistance, or want to share feedback, please reach out via GitHub Issues or email me at uziel.francotorres@gmail.com.

**Stay Connected:**
- Follow the project for updates and new releases.
- Engage with other contributors and users to foster a collaborative community.