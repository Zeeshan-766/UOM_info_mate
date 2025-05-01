import cohere
import chromadb

class ChatBot:
    def __init__(self, cohere_api_key):
        # Initialize Cohere client with your API key
        self.llm_client = cohere.Client(api_key=cohere_api_key)
        
        # Initialize ChromaDB client
        chroma_client = chromadb.PersistentClient(path="/path/to/save/to/desktop")
        
        # Access the collection
        self.collection = chroma_client.get_collection(name="Malakand_BoT")

    # Function to generate embeddings for the query using the LLM
    def get_llm_embeddings(self, text):
        # Ensure using the same model as used for adding documents to the collection
        response = self.llm_client.embed(texts=[text], model='large')  # Change to 'large' if that matches the collection's dimensionality
        embeddings = response.embeddings
        return embeddings[0]

    # Function to query the vector database and return relevant document titles
    def query_documents(self, user_query):
        try:
            # Generate embeddings for the user query using LLM
            query_embedding = self.get_llm_embeddings(user_query)
            
            # Query the vector database for relevant documents based on the query embedding
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=14  # Retrieve at least 14 most relevant documents
            )
            
            # Access the documents and their metadata from the results
            documents = results['documents'][0]
            metadatas = results['metadatas'][0]
            
            # Re-ranking based on document length (shorter documents ranked higher)
            ranked_documents = sorted(zip(documents, metadatas), key=lambda x: len(x[0]))
            
            # Extract re-ranked documents and metadata
            re_ranked_documents = [doc for doc, meta in ranked_documents]
            re_ranked_metadatas = [meta for doc, meta in ranked_documents]
            
            # Concatenate the top documents for context
            concatenated_documents = " ".join(re_ranked_documents)
            
            return concatenated_documents
        except Exception as e:
            print("something went wrong", e)
            return None

    # Function to generate a response using LLM with the relevant document as context
    def generate_response_with_context(self, user_query, context):
        system_prompt = """Welcome! You are an AI assistant for Malakand University. Your role
        is to assist with any questions users may have.
        If you're unable to find the information they need, simply respond with 'I'm sorry, 
        but I couldn't find useful information.'"""
        
        combined_input = f"system_prompt: {system_prompt}\n\nContext: {context}\n\nQuestion: {user_query}"
        
        response = self.llm_client.generate(
            model='command-nightly',  # Use a valid model identifier
            prompt=combined_input,
            max_tokens=500  # Adjust as needed
        )
        
        return response.generations[0].text.strip()

# Example usage
# cohere_api_key = 'your_api_key'
# chat_bot = ChatBot(cohere_api_key)

# user_query = "can you tell me about the research center at the university?"
# relevant_documents = chat_bot.query_documents(user_query)
# response = chat_bot.generate_response_with_context(user_query, relevant_documents)
# print("Response:", response)