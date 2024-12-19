# Election-Insight-App

![Screenshot 2024-09-15 231026](https://github.com/user-attachments/assets/dca794e6-aeb2-4335-b72b-a852d0154d3c)
![Screenshot 2024-09-15 233006](https://github.com/user-attachments/assets/c97be96d-521d-41f9-b498-b1900aa53180)
![Screenshot 2024-09-16 171718](https://github.com/user-attachments/assets/20c0f2b8-8291-4581-8d5f-4841416dd0c4)


The Election Insight App is a real-time, AI-powered tool designed to help voters make informed decisions during elections by providing accurate and transparent insights. It utilizes the power of LangChain and Large Language Models (LLMs) to analyze candidate manifestos, verify campaign claims, and provide reliable election-related information.

## 🚀 Features

1. Manifesto Comparator
- Side-by-Side Comparison: Easily compare candidate manifestos on key issues such as economy, healthcare, education, and environment.
- LangChain-Powered Insights: Breaks down and summarizes key promises, goals, and policies to help voters assess candidates.
- Search & Filter: Filter manifestos by specific topics or search for relevant promises to make an informed decision.
  
2. Fact-Checker & Claim Verification
- AI-Powered Fact-Checking: Verify claims made by candidates in real-time by cross-referencing them with trusted public databases.
- Misinformation Alerts: Get notified when suspicious or exaggerated claims are made during campaigns.
- Historical Record Comparison: See how campaign promises align with previous performance or public statements.
  
3. AI Chatbot for Manifesto & Election Queries
- AI Q&A Bot: Get quick and reliable answers to questions about candidate manifestos, election details, and campaign topics.
- Verified Information: The chatbot is trained on validated election data, ensuring accurate and trustworthy responses.
- Contextual Answers: Ask complex questions like “Which candidate focuses on climate change?” or “Who has a better track record on healthcare?”
  
## 🔧 Tech Stack

- LangChain: Manages the logic and workflow for LLM-powered features like manifesto comparison, fact-checking, and the AI chatbot.
- Large Language Model (LLM): The core AI model that provides natural language understanding and generation capabilities.
- Pinecone : For efficient vector search and retrieval of campaign data and manifestos.
- Hugging Face Models : Leverage specific LLMs from Hugging Face for enhanced natural language processing and query handling.
  

## 🛠️ Installation

To get started with the Election Insight App, follow these steps:

1. Clone the Repository:
   
```
git clone https://github.com/yourusername/election-insight-app.git
cd election-insight-app
```

2. Install Dependencies: Install the necessary Python libraries by running:
   
```
pip install -r requirements.txt
```

3. Configure API Keys:
   
Set up your API keys for LLM services.
If using Pinecone for vector storage, add your API key in the .env file.

4. Run the Application:
   
```
streamlit run app.py
```

5. Access the App:

Open your browser and navigate to http://localhost:8501/ to start using the Election Insight App.

## 🤖 Usage

1. Manifesto Comparison: Use the "Compare Manifestos" feature to see the promises of different candidates side by side.
2. Fact-Checker: Enter claims or campaign statements to verify their truthfulness.
3. Ask the Bot: Use the AI chatbot to ask questions related to the election, candidates, or manifestos.
4. Trending Insights: Stay updated with real-time trends and sentiment analysis of election campaigns.

## 🌟 Contribution

We welcome contributions! If you would like to add new features or fix bugs, feel free to fork the repository and submit a pull request.

1. Fork the repository.
2. Create a new branch: git checkout -b feature-branch.
3. Commit your changes: git commit -m "Add some feature".
4. Push to the branch: git push origin feature-branch.
5. Submit a pull request.

## 📄 License

This project is licensed under the MIT License

## 🙌 Acknowledgments

Special thanks to the developers of LangChain and LLMs for providing the core technologies behind this project!
