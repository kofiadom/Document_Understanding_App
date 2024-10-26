# Document Understanding App - Detailed Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [System Setup](#system-setup)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Configuration](#configuration)
3. [System Architecture](#system-architecture)
4. [Usage](#usage)
    - [Uploading Documents](#uploading-documents)
    - [Asking Questions](#asking-questions)
    - [Providing Feedback](#providing-feedback)
5. [Application Process Flow](#application-process-flow)
6. [Design Choices](#design-choices)
    - [LangChain Framework](#langchain-framework)
    - [OpenAI Language Model](#openai-language-model)
    - [ChromaDB Vector Database](#chromadb-vector-database)
    - [Streamlit Framework](#streamlit-framework)
    - [Feedback Mechanism](#feedback-mechanism)
6. [Challenges Faced](#challenges-faced)
7. [Future Enhancement](#future-enhancements)
8. [Contributing](#contributing)
9. [Troubleshooting](#troubleshooting)
9. [Lessons Learned](#lessons-learned)


## 1. Introduction

This document provides a comprehensive overview of the Document Understanding App, a system designed for interactive document analysis and question-answering.  The application utilizes the power of OpenAI's language model, LangChain for streamlined interaction, and ChromaDB for efficient document storage and retrieval.

## 2. System Setup

### 2.1. Prerequisites

- **Python 3.7+:**  Ensure you have a compatible Python version installed.
- **Virtual Environment (Recommended):** Create a virtual environment to isolate project dependencies.
- **OpenAI API Key:** Obtain an API key from OpenAI's website ([https://platform.openai.com/](https://platform.openai.com/)). 

### 2.2. Installation

1. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install Required Packages**:
    ```bash
    pip install -r requirements.txt   
    ```
    This will install the necessary packages, including LangChain, ChromaDB, and Streamlit.

### 2.3. Configuration

- **OpenAI API Key:** Set the `OPENAI_API_KEY` environment variable with your OpenAI API key.

- Create a .env file in your project's root directory.

- Store your OpenAI API key in the .env file:

    ```bash
    OPENAI_API_KEY=your_actual_api_key_here
    ```

## 3. System Architecture
The application follows a modular architecture with the following key components:

- **User Interface (Streamlit)**: Provides a web-based interface for file uploads, user interactions (questions), and displaying responses.
- **File Processing Module** (process_files.py): Contains functions to handle document uploads, parse PDF and CSV files, and extract relevant text content.

- **LangChain Integration**:
    - Uses LangChain to interface with OpenAI's language model for question-answering and document understanding.
    - Manages conversational context using ConversationBufferMemory.

- **ChromaDB Vector Database**:

    - Stores processed document content as embeddings in ChromaDB for efficient similarity search.
    
    - Allows for context-aware retrieval based on previous interactions.

- **Feedback Mechanism**:
    - Collects user feedback on response relevance.
    - Provides options to refine responses or add additional context.
    - Stores feedback data in feedback_data.json.



## 4. Usage

### 4.1. Uploading Documents
- Launch the application: ```streamlit run app.py```

- In the sidebar, use the file uploader to select PDF or CSV files.

- Click the **"Process"** button to ingest and process the documents.

### 4.2. Asking Questions
- Once documents are processed, type your questions into the chat interface.

- The system will provide responses based on the uploaded content and conversational history.

### 4.3. Providing Feedback
- After receiving a response, use the radio buttons to indicate whether the answer was helpful.
- If needed, provide additional context in the text input area.
- Click "Submit Feedback" to save your feedback.


## 5. Application Process Flow

The Document Understanding App follows these key steps to process documents and answer user questions. Note that the Document Understanding App uses two main pathways for answering user questions, depending on the uploaded file type:

**A.  PDF Document Pathway:**

1. **Document Upload:**
   - The user uploads one or more PDF or CSV files through the Streamlit interface.

2. **File Type Detection:**
   - The application identifies the file type of each uploaded document based on its extension.

3. **Parsing and Processing:**

   - Text content is extracted from the PDF using the PyPDF library.
   - The extracted text is split into smaller chunks (e.g., sentences or paragraphs).
 

4. **Content Embedding and Storage:**
   - The processed text content from both PDF files is converted into numerical representations (embeddings) using OpenAI's embedding model.
   - These embeddings, along with associated metadata (e.g., file name, chunk source), are stored in the ChromaDB vector database.
   - The ChromaDB is persisted on the local disk. 

5. **Question Input:**
   - The user enters a question in the chat interface. 

6. **Context Retrieval:**
   - The user's question is embedded using the same embedding model.
   - ChromaDB performs a similarity search to find the most relevant document chunks based on the question embedding.

7. **Answer Generation (LLM Interaction):**
   -  The retrieved relevant chunks, along with the user's question and potentially previous conversational context, are passed to OpenAI's gpt language model via LangChain.
   -  The language model generates a response based on the provided information.

8. **Response Display and Feedback:**
   - The generated response is displayed to the user in the chat interface.
   - The user can provide feedback on the response's helpfulness and give additional context if needed.

9. **Feedback Processing:**
   - User feedback is stored to help improve future responses (e.g., by retraining the language model or adjusting retrieval parameters). 



**B.  CSV File Pathway:**

1.  **Document Upload:** The user uploads a CSV file.

2.  **File Type Detection:**  The app identifies the uploaded file as CSV.

3.  **CSV Agent Initialization:**
    - A LangChain CSV agent is created, which directly loads and interacts with the CSV data.

4.  **Question Input:** The user asks a question.

5.  **Answer Generation (CSV Agent):**
    - The user's question is passed to the CSV agent.
    - The agent uses its knowledge of the CSV data and the OpenAI's gpt model to formulate a response. 

6.  **Response Display and Feedback:**  The response is shown to the user, who can provide feedback.

7.  **Feedback Processing:** User feedback is stored for system improvement.

[![2qYd4MG.md.png](https://iili.io/2qYd4MG.md.png)](https://freeimage.host/i/2qYd4MG)

[![2qY2liG.md.png](https://iili.io/2qY2liG.md.png)](https://freeimage.host/i/2qY2liG)

## 6. Design Choices

### 6.1. LangChain Framework

- Chosen for its ease of use in building conversational interfaces and integrating with various LLMs and data sources.
- Simplifies the process of handling conversational context and managing user interactions.

### 6.2. OpenAI Language Model
- Utilized for its powerful language understanding capabilities and ability to generate human-like responses.

- Enables the system to provide accurate answers based on the uploaded document content.

### 6.3. ChromaDB Vector Database
- Selected for its efficient storage and retrieval of high-dimensional vector data.

- Allows for fast similarity searches and context-aware retrieval of relevant document content.

### 6.4. Streamlit Framework
- Chosen for its ease of use in building web-based interfaces and rapid prototyping capabilities.

- Enables the creation of an interactive and user-friendly interface for file uploads, questions, and feedback.

### 6.5. Feedback Mechanism
- Wrote an algorithm to implemented a feedback mechanism to improve the system's accuracy and adaptability over time.

- Enables users to provide feedback on response and provide additional context for refined responses (if feedback was negative)

## 7. Challenges Faced
- **Feedback option selection**: After selecting a feedback option (whether yes or no) the radio buttons disappear and the feedback is not recorded in the `feedback_data.json file`. To solve the problem, I isolated the collect_feedback() to test radio button selection. In isolation, it worked and the selected feedback option was recorded in the json file. Still investigating the problem.

## 8. Future Enhancements

- **Enhanced Error Handling**: Implement more robust error handling for file processing, API calls, and user input.

- **Advanced UI Components**: Explore more interactive UI components for better user experience.

- **Performance Optimizations**: Implement caching strategies for faster response times

## 9. Troubleshooting
- **Check the Console Output**: Review the console output for error messages or debugging information.

- **Verify API Key and Configuration**: Ensure the OpenAI API key is correctly configured and stored in the .env file.

## 10. Contributing
- **Fork the Repository**: Create a fork of this repository to contribute to the project.

- **Create a Pull Request**: Submit your changes as a pull request for review.

## 11. Lessons Learned
- **Successful implementation of ChromaDB**
- **Streamlit Rendering Quirks:** Streamlit's dynamic rendering model, while powerful, can sometimes lead to unexpected behavior. It's crucial to pay close attention to component rendering order, state updates, and the potential for unintended re-renders, especially when working with interactive elements like radio buttons. 

- **Session State Management is Key:** 
    - Carefully planning how you use `st.session_state` is essential for preventing bugs, especially when dealing with user interactions and dynamic updates.
    - Consider using unique keys for different interaction types or contexts to avoid key collisions and unintentional overwrites. 

- **The Importance of Minimal Examples:**  When encountering persistent bugs, creating a minimal reproducible example (reprex) that isolates the issue is crucial for effective debugging.  

