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
    - Put the required endpoints in order to run the app.
3. **Execution**
    - use `python -m app.main` in the project directory to run this app`
4. **Test endponts**
    - Use your *host name* (e.g., http://127.0.0.1:8000/) along with some of the allowed paths
    - `{host}/messages`: With this enpoint you will be able to test the conversation feature
    - `{host}/documents`: With this enpoint you can test the document upload feature, note that the Content-Type must be `multipart/form-data`, the title field must have the desired `title` for the document, the `file` field must have the PDF file.