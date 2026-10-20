# 🔎 AI Research Assistant

## 📌 About the Project

The **AI Research Assistant** is an AI-powered application that helps users research topics, find relevant information, perform calculations, and generate answers with source links.

The application uses **Python, Google Gemini, LangChain, and Streamlit**. It demonstrates Agentic AI by allowing an AI agent to decide which tools are needed to answer a user's question.

Instead of relying only on a direct response from an AI model, the research agent can select and use available tools to gather additional information before generating its final answer.

## 🎯 Project Objectives

- Simplify the process of researching different topics.
- Retrieve relevant information from the web.
- Analyse webpage content when additional details are required.
- Perform mathematical calculations.
- Generate informative answers with relevant source links.
- Demonstrate how an AI agent selects and uses tools to complete a task.

## ✨ Key Features

- 🤖 **Agentic AI:** Selects appropriate tools based on the user's question.
- 🔎 **Web Search:** Searches for relevant information.
- 🌐 **Webpage Analysis:** Retrieves webpage content for further analysis.
- 🧮 **Calculator:** Performs mathematical calculations.
- 📚 **Source Collection:** Collects relevant source URLs during research.
- 🎯 **Source Selection:** Uses the AI model to identify relevant sources for the answer.
- 🔗 **Clickable Sources:** Displays source links alongside the final answer.
- ⏳ **Controlled Execution:** Limits each research request to a maximum of five tool calls.
- 💻 **Interactive Interface:** Provides a web interface using Streamlit.
- 🖥️ **Command-Line Interface:** Also supports research through the terminal.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Google Gemini | Understands questions, selects tools, and generates responses |
| LangChain | Connects the language model with tools and messages |
| Streamlit | Provides the user interface |
| python-dotenv | Loads configuration from environment variables |

## 🏗️ System Architecture

The application follows a tool-based AI agent workflow.

```text
                 User
                  |
                  v
          Enter Research Question
                  |
                  v
            Streamlit UI
                  |
                  v
           Research Agent
           (Google Gemini)
                  |
                  v
           Select a Tool
                  |
        +---------+---------+
        |         |         |
        v         v         v
    Web Search  Web Fetch  Calculator
        |         |         |
        +---------+---------+
                  |
                  v
        Collect Relevant Information
                  |
                  v
          Collect Source URLs
                  |
                  v
          Select Relevant Sources
                  |
                  v
           Generate Final Answer
                  |
                  v
       Display Answer and Source Links
```

## ⚙️ How Does the Application Work?

### 1. User Enters a Question

The user enters a research question through the Streamlit interface or the command-line interface.

For example:

"What are the applications of Artificial Intelligence in healthcare?"

### 2. The AI Agent Understands the Request

Google Gemini processes the question and determines whether additional tools are required.

The agent can choose from three available tools.

### 3. The Agent Uses the Appropriate Tool

**Web Search**

Searches for relevant information when the question requires external information.

Example:

"What are the recent developments in Python?"

**Web Fetch**

Retrieves the contents of a webpage when the agent needs to analyse the actual page rather than just its search results.

Example:

"Read the official Python documentation and explain its important features."

**Calculator**

Performs mathematical calculations when required.

Example:

"Calculate the compound annual growth rate of an investment."

### 4. Information Is Collected

The application processes the information returned by the selected tools.

Relevant source URLs are also collected during the research process.

### 5. Relevant Sources Are Selected

Google Gemini evaluates the collected sources and selects those that are relevant to the final answer.

The system is designed to favour sources that directly support the research findings.

### 6. The Final Answer Is Generated

The AI model prepares a response using the information gathered during the research process.

The application displays the answer and relevant source links to the user.

## 🤖 Where Is Agentic AI Used?

The project demonstrates agentic behaviour through **AI-based tool selection and execution**.

A traditional question-answering system may respond directly to a question. In this application, the agent can determine whether it needs additional information and select a suitable tool to obtain it.

The process involves:

1. Understanding the user's request.
2. Deciding whether a tool is needed.
3. Selecting an appropriate tool.
4. Using the tool's output to support the research.
5. Generating the final response with relevant sources.

This allows the AI agent to perform multiple steps towards completing a research task.

The system also has a maximum limit of five tool calls per research request to help control execution.

## 📁 Project Structure

```text
ai-research-agent/
│
├── app.py                  # Streamlit web interface
├── main.py                 # Command-line interface
├── agent.py                # AI agent and research workflow
├── requirements.txt        # Python dependencies
├── .env.example            # Example environment configuration
├── .gitignore              # Files excluded from Git
│
└── tools/
    ├── __init__.py
    ├── calculator.py       # Mathematical calculations
    ├── web_search.py       # Web search functionality
    └── web_fetch.py        # Webpage content retrieval
```

## 🚀 Installation and Setup

### Prerequisites

- Python installed on your system
- pip package installer
- Google Gemini API key
- Internet connection for web research

### Step 1: Open the Project Directory

Open the project folder in VS Code and launch the integrated terminal.

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment

For Windows:

```powershell
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure the API Key

Create a `.env` file in the project directory and add your Google Gemini API key.

```env
GOOGLE_API_KEY=your_google_api_key_here
```

Replace the placeholder with your actual API key.

**Security note:** Never upload your API key or `.env` file to a public repository.

## ▶️ Running the Application

### Run the Streamlit Interface

Execute the following command from the project directory:

```bash
streamlit run app.py
```

The application will open in your browser.

Enter a research question to begin.

### Run the Command-Line Interface

Alternatively, execute:

```bash
python main.py
```

Enter your research question when prompted in the terminal.

## 💡 Example Questions

### General Research

```text
Explain the applications of Artificial Intelligence in healthcare.
```

### Web Research

```text
Find information about recent developments in Python.
```

### Mathematical Calculation

```text
Calculate the compound annual growth rate of an investment
that grows from 10000 to 18000 over five years.
```

### Webpage Analysis

```text
Read the official Python documentation and explain its important features.
```

## ⚠️ Limitations

- AI-generated answers may contain inaccurate or incomplete information.
- Search results and source links should be checked before relying on the findings.
- Web research requires an internet connection.
- Google Gemini access requires a configured API key.
- The number of tool calls is limited to five per research request.
- The quality of the final answer depends on the question, available tools, and retrieved information.

## 🔮 Future Enhancements

- Maintain conversation history across research questions.
- Export research reports as PDF or Markdown files.
- Improve source ranking and verification.
- Save previous research sessions.
- Add more specialised research tools.
- Improve error handling and user feedback.
- Deploy the application for public access.

## 📌 Conclusion

The AI Research Assistant demonstrates how an LLM can work with external tools to support research tasks.

By combining Python, Google Gemini, LangChain, and Streamlit, the application provides a way to search for information, analyse webpages, perform calculations, and generate answers with relevant sources.

The project introduces important concepts such as prompt engineering, LLMs, tool calling, and the fundamentals of Agentic AI.