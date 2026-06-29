### 🤖 GitHub Repository AI Assistant

An AI-powered command-line assistant that analyzes GitHub repositories and helps developers quickly understand unfamiliar codebases.

Built with Python, the Gemini API, and the GitHub API, it can summarize repositories, explain source files, locate classes/functions, generate README files, and cache previous analyses for faster follow-up questions.

-------------------------------------------------------------------------------------

✦ **Features**

• Analyze any public GitHub repository

• Explain individual source files

• Search where classes and functions are implemented

• Generate professional README files

• Persistent local memory for previously analyzed repositories

• Automatic repository cloning and caching

• Interactive menu-driven CLI

• Repository language detection and file indexing

-------------------------------------------------------------------------------------

✦ **Tech Stack**

• Python

• Google Gemini API

• GitHub API (PyGithub)

• GitPython

• JSON-based local memory

-------------------------------------------------------------------------------------

✦ **How It Works**

1. Enter a public GitHub repository URL

2. Choose an operation:
   - Analyze Repository
   - Explain a File
   - Search Symbol/Class
   - Generate README

3. The assistant clones the repository (or uses the local cached copy)

4. Repository structure, README, languages and files are analyzed

5. Gemini generates a context-aware response

-------------------------------------------------------------------------------------

✦ **Installation**

Clone the repository

```bash
git clone https://github.com/zeemofukaa/github-ai-assistant.git
cd github-repository-ai-assistant
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GEMINI_API_KEY=your_api_key
GITHUB_TOKEN=your_github_token
```

Run

```bash
python agent.py
```

-------------------------------------------------------------------------------------

✦ **Example Capabilities**

Repository Analysis

```
Summarize this repository
```

File Explanation

```
Explain routing.py
```

Symbol Search

```
Where is APIRouter implemented?
```

README Generation

```
Generate README
```

-------------------------------------------------------------------------------------

✦ **Project Structure**

```
github-repository-ai-assistant/
│
├── agent.py
├── github_tools.py
├── gemini_client.py
├── memory.py
├── requirements.txt
├── .env.example
└── .gitignore
```

-------------------------------------------------------------------------------------

✦ **Status**

This is a personal project built to explore AI-assisted developer tools and repository analysis workflows.

The project focuses on improving developer productivity through automated code understanding and documentation generation.

-------------------------------------------------------------------------------------

✦ **Author**

Made by **zeemofukaa_**
