import os
from datetime import datetime
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_experimental.agents import create_csv_agent
from process_files import get_pdf_docs, create_db_for_pdf_docs
import streamlit as st

CHROMA_PATH = 'vector_db_dir'
load_dotenv()

def save_feedback(question: str, response: str, feedback: dict, context: str = None):
    """Save feedback to a JSON file."""
    feedback_data = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "response": response,
        "feedback": feedback,
        "context": context
    }
    
    try:
        # Attempt to read existing feedback data
        with open('feedback_data.json', 'r+') as f:
            try: 
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

            data.append(feedback_data)
            f.seek(0) 
            json.dump(data, f, indent=2)

    except FileNotFoundError:
        # Create a new file if it doesn't exist
        with open('feedback_data.json', 'w') as f:
            json.dump([feedback_data], f, indent=2)


def refine_response(question: str, original_response: str, context: str, chain):
    """Generate a refined response based on feedback context."""
    if chain is None:
        return "Error: No valid chain available for refining the response."

    refinement_prompt = f"""
    Original Question: {question}
    Original Response: {original_response}
    User Feedback: {context}
    
    Please provide an improved response addressing the user's feedback while incorporating information from the provided documents.
    """
    
    refined_response = chain({"question": refinement_prompt})
    return refined_response["answer"]


def collect_feedback(question: str, response: str, chain):
    """Collect feedback and refine response if needed."""
    feedback_key = f"feedback_{hash(response)}"

    # Initialize feedback state
    if feedback_key not in st.session_state:
        st.session_state[feedback_key] = {"feedback_option": None, "context": ""}

    st.write("Was this response helpful?")
        
    # Radio buttons for feedback selection
    feedback_option = st.radio(
        "Select Feedback",
        options=["👍 Yes, it was helpful", "👎 No, it could be improved"],
        index=0 if st.session_state[feedback_key]["feedback_option"] is None else 1 if st.session_state[feedback_key]["feedback_option"] == "👎 No, it could be improved" else 0
    )

    # Update session state with the radio button is rendered
    st.session_state[feedback_key]["feedback_option"] = feedback_option

    # Conditional text input 
    if feedback_option == "👎 No, it could be improved": 
        context = st.text_input("What could be improved?", value=st.session_state[feedback_key]["context"])
        st.session_state[feedback_key]["context"] = context  # Update session state 

    # Button to submit feedback
    if st.button("Submit Feedback"):
        feedback_data = {"rating": "positive" if feedback_option == "👍 Yes, it was helpful" else "negative"}
        if feedback_option == "👎 No, it could be improved" and context:
            feedback_data["context"] = context
            
        save_feedback(question, response, feedback_data, context)
        st.success("Thank you for your feedback!")

        if chain is not None:
            # Generate a refined response if feedback is negative and context is provided
            if feedback_option == "👎 No, it could be improved" and context:
                st.write("Generating refined response based on your feedback...")
                refined_response = refine_response(
                    question,
                    response,
                    context,
                    chain
                )
                
                # Display the refined response in chat
                with st.chat_message("assistant"):
                    st.markdown("**Refined Response:**")
                    st.markdown(refined_response)
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": f"**Refined Response:** {refined_response}"}
                    )
        else:
            st.error("Error: No valid chain available for refining the response.")


def handle_uploaded_files(uploaded_files):
    pdf_docs = []
    csv_files = []
    
    for uploaded_file in uploaded_files:
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        # Check the file type and call the appropriate function
        if file_extension == '.pdf': 
            pdf_docs.extend(get_pdf_docs([uploaded_file]))
        elif file_extension == '.csv':
            csv_files.append(uploaded_file)
        else:
            print(f"Unsupported file type: {file_extension}. Please upload a PDF or CSV file.")
    
    return pdf_docs, csv_files

def get_vectorstore():
    embedding_function = OpenAIEmbeddings()
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    return vectorstore

def chat_chain(vectorstore):
    llm = ChatOpenAI()
    retriever = vectorstore.as_retriever()
    
    memory = ConversationBufferMemory(
        llm=llm,
        output_key="answer",
        memory_key="chat_history",
        return_messages=True
        )
    
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        memory=memory,
        verbose=True,
        return_source_documents=True
        )
    
    return chain

def get_csv_agent(csv_files):
    if csv_files:  # Ensure there are CSV files
        csv_agent = create_csv_agent(ChatOpenAI(), path=csv_files[0], verbose=True, allow_dangerous_code=True)
        return csv_agent
    else:
        raise ValueError("No CSV files provided to create the agent.")
    

def main():
    st.set_page_config(page_title="Document Understanding App", page_icon=":books:")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
    
    if "conversationsal_chain" not in st.session_state:
        st.session_state.conversationsal_chain = None

    if "csv_agent" not in st.session_state:
        st.session_state.csv_agent = None

    if "current_chain" not in st.session_state:
        st.session_state.current_chain = None 
    
    st.header("Document Understanding App :books:")

    # Containers for structure
    chat_history_container = st.container() 
    feedback_container = st.container()

    with chat_history_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
        user_question = st.chat_input("Ask a question about your documents:")

        if user_question:
            st.session_state.chat_history.append({"role": "user", "content": user_question})
            with st.chat_message("user"):
                st.markdown(user_question)
                
            # Determine if the question should go to the CSV agent or the conversational chain
            if st.session_state.csv_agent:
                response = st.session_state.csv_agent({"input": user_question})
                assistant_response = response["output"]
                st.session_state.current_chain = st.session_state.csv_agent
            elif st.session_state.conversational_chain:
                response = st.session_state.conversational_chain({"question": user_question})
                assistant_response = response["answer"]
                st.session_state.current_chain = st.session_state.conversational_chain
            else:
                assistant_response = "The conversational chain is not initialized."
                st.session_state.current_chain = None
      
            with st.chat_message("assistant"):
                st.markdown(assistant_response)
                st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})


    with feedback_container:
        if st.session_state.chat_history:  # Only show feedback if there is chat history
            user_question = st.session_state.chat_history[-1]["content"]
            assistant_response = st.session_state.chat_history[-1]["content"]  # Get the last assistant response

            # Debugging: Print the current_chain status
            #st.write(f"Current Chain: {st.session_state.current_chain}")

            # Pass the current_chain from the session state to collect_feedback
            collect_feedback(user_question, assistant_response, st.session_state.current_chain) 


    with st.sidebar:
        st.subheader("Your documents")
        uploaded_files = st.file_uploader(
            "Upload your PDFs or CSV here and click on 'Process'", 
            accept_multiple_files=True
            )
        if st.button("Process"):
            with st.spinner("Processing"):
                pdf_docs, csv_files = handle_uploaded_files(uploaded_files)
                # create the db for pdf if pdf docs are uploaded
                if pdf_docs:
                    create_db_for_pdf_docs(pdf_docs)
                # create csv agent if csv files are uploaded
                if csv_files:
                    st.session_state.csv_agent = get_csv_agent(csv_files)

                # Create vector store
                try:
                    st.session_state.vectorstore = get_vectorstore()
                    print("Updated vectorstore after processing files.")
                except Exception as e:
                    print(f"Error creating vectorstore: {e}")

                # Create conversation chain if vector store is valid
                if st.session_state.vectorstore:
                    try:
                        st.session_state.conversational_chain = chat_chain(st.session_state.vectorstore)
                        print("Updated conversational_chain after processing files.")
                    except Exception as e:
                        print(f"Error initializing conversational_chain: {e}")
                else:
                    print("Error: Vectorstore is not valid.")

                # Check if conversational_chain is initialized after processing
                if "conversational_chain" not in st.session_state:
                    print("Error: conversational_chain was not initialized after processing files.")
                    
        
if __name__ == '__main__':
    main()
