# UOM_info_mate
A smart AI chatbot for Malakand University using Cohere LLM and ChromaDB for semantic search and context-aware responses.
# UOM_info_mate 🤖🎓

UOM_info_mate is an AI-powered chatbot designed to assist users with queries related to the University of Malakand. It leverages **Cohere's Large Language Model (LLM)** and **ChromaDB** for intelligent, context-aware responses based on university data.

---

## 🚀 Features

- 🔍 **Semantic Search** with ChromaDB  
- 🧠 **Embeddings & Text Generation** using Cohere LLM  
- 📚 **Re-ranking documents** based on relevance and length  
- 💬 **Natural language responses** based on retrieved context  
- 🛡️ API key security tip: use `.env` to protect sensitive keys  

---

## 🛠️ Technologies Used

- Python
- Cohere API (`cohere`)
- ChromaDB (`chromadb`)
- dotenv for secure environment variable handling

---

## 🧪 How It Works

1. User enters a query (e.g., *"What departments are in UOM?"*)
2. Query is embedded using Cohere's model.
3. Vector similarity search is performed in ChromaDB.
4. Top documents are re-ranked.
5. The chatbot generates a response using context and the system prompt.

---

## ⚠️ Security Note

**Do not hardcode your API key in the source code.**  
Use a `.env` file and add it to `.gitignore`:

```bash
# .env
COHERE_API_KEY=your_actual_key_here
