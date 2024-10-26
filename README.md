# Document Understanding App
### Assignment submitted by: Kofi Adom

This app implements a document understanding application that leverages LangChain, OpenAI's language model, and ChromaDB for interactive question answering and document analysis. 

### Features

- Processes PDF and CSV files for document ingestion.
- Utilizes OpenAI's language model via LangChain for document understanding.
- Stores document content and conversational context in ChromaDB for efficient retrieval.
- Provides a simple interface for file upload and user interactions with Streamlit. 
- Enables context-aware multi-turn conversations, remembering previous interactions.
- Includes a feedback mechanism for users to refine answers or provide additional context.

### Project Structure

- `app.py`: Main Streamlit application code (or your chosen filename).
- `process_files.py`: Functions for parsing and processing files.
- `vector_db_dir/`: Directory for storing ChromaDB database files.
- `feedback_data.json`: File to store user feedback.
- `.env`: Environment variables for API keys and configurations (optional).

### Installation and Setup

1. **Set Up a Python Environment:** Create a virtual environment and activate it. 
   ```bash
   python -m venv venv
   venv\Scripts\activate #source venv/bin/activate (if on Mac)
   ```

2. **Install Dependencies**: Install the required libraries from requirements.txt (if you created one) or install them directly

    ```bash
    pip install -r requirements.txt
    ```


3. **Configure OpenAI API Key**:

    Obtain an API key from https://platform.openai.com/account/api-keys.
Store it securely in an environment variable (e.g., in a .env file):

    ```bash
    OPENAI_API_KEY=your_openai_api_key
    ```

4. **Run the app**
    ```bash
    streamlit run app.py
    ```


### Usage

**1. Upload Files**: Use the file uploader to upload PDF or CSV files.

**2. Process Documents**: Click the "Process" button to ingest the document content.

**3. Ask Questions**: Type your questions in the chat interface.
The model will respond based on the context of the uploaded documents.

**4. Provide Feedback**: Select the a radio button to provide a feedback. You can use this feedback mechanism provide additional context to refine responses.

### Contact

Reach out to me on LinkedIn for further guide or questions: www.linkedin.com/in/kofi-adom