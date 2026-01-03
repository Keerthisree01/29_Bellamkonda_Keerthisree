AI Customer Service Agent (RAG over Tickets & Dialogues)

Hackathon Project Submission

--------------------------------------------------

Problem Statement  
Telecom companies handle a large volume of repetitive customer support queries related to billing issues, network problems, SIM services, and subscription plans.
Manual handling of these queries leads to delayed responses, increased operational costs, and reduced customer satisfaction.

The challenge is to build an AI-powered customer support assistant that can automatically answer common telecom queries using past support data, while escalating complex or sensitive issues to human agents.

--------------------------------------------------

Proposed Solution  
This project implements an AI Customer Service Agent using Retrieval-Augmented Generation (RAG). 
The system retrieves relevant information from historical telecom agent–customer conversations and customer support tickets, and then generates accurate, context-aware responses using a Large Language Model (LLM).

To ensure reliability and trust, the system returns source references for every answer and applies simple escalation rules when human intervention is required.

--------------------------------------------------

Key Features  
- Automatic answering of common telecom support queries  
- Retrieval-Augmented Generation to reduce hallucinations  
- Source IDs returned with each answer for transparency  
- Rule-based escalation for unresolved or critical queries  
- Modular and scalable architecture  
- Supports multiple datasets  

--------------------------------------------------

Datasets Used  

Telecom Agent–Customer Interaction Dataset  
Source: Kaggle  
Link: https://www.kaggle.com/datasets/avinashok/telecomagentcustomerinteractiontext  
Description: Real-world telecom customer–agent conversation data covering common support issues.

Customer Support Ticket Dataset (Optional)  
Source: Kaggle  
Link: https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset  
Description: Structured customer support tickets with issue descriptions and resolutions.

--------------------------------------------------

System Architecture (RAG Pipeline)  
1. Load and preprocess telecom conversations and ticket data  
2. Split text into chunks with source metadata  
3. Generate vector embeddings  
4. Store embeddings in a vector database (ChromaDB or FAISS)  
5. Retrieve top relevant documents for a query  
6. Generate final answer using an LLM with retrieved context  
7. Apply escalation rules to determine human handoff  

--------------------------------------------------

Tech Stack  
Programming Language: Python  
Framework: LangChain  
Vector Database: ChromaDB / FAISS  
LLM: OpenAI or HuggingFace  
Backend API: FastAPI or Flask  
Data Processing: Pandas  

--------------------------------------------------

API Endpoint  

POST /ask  

Request:

{
  "query": "Why is my internet connection slow?"
}

{
  "answer": "Your internet may be slow due to temporary network congestion or router issues. Restarting your router may help.",
  "sources": ["conversation_102", "ticket_45"],
  "escalation_required": false
}

-------------------------------------------------
Project structure

AI-Customer-Service-Agent/
├── data/
├── src/
│ ├── rag_pipeline.py
│ ├── retriever.py
│ ├── escalation.py
│ └── app.py
├── requirements.txt
├── README.md
└── .env

-------------------------------------------------

Setup Instructions

git clone https://github.com/your-username/AI-Customer-Service-Agent.git
cd AI-Customer-Service-Agent
pip install -r requirements.txt
python src/app.py

------------------------------------------------

Future Scope

Multi-language support

Voice-based customer interaction

Advanced sentiment analysis

CRM and live ticket system integration

------------------------------------------------

Team / Author

Bellamkonda Keerthisree
AI Alchemists | Hackathon Team name
Team members 
Veedula Rishitha|Gadamsetty Sujitha
-------------------------------------------------
License

This project is intended for hackathon and educational purposes only.


