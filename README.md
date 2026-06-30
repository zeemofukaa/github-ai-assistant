### 🤖 GitHub Repository AI Assistant

An AI-powered command-line assistant that helps developers quickly understand unfamiliar GitHub repositories through automated code analysis.

Built with Python, the Google Gemini API, GitPython, and the GitHub API, it can summarize repositories, explain source files, locate classes/functions, analyze project architecture, generate README files, and cache previous analyses for faster follow-up questions.

-------------------------------------------------------------------------------------

✦ **Features**

• Analyze any public GitHub repository

• Explain individual source files

• Search where classes, functions, and variables are defined or referenced

• Analyze project architecture using an automatically generated dependency graph

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

• Python AST (Abstract Syntax Tree)

• JSON-based local memory

• Regular Expressions (Regex)

-------------------------------------------------------------------------------------

✦ **How It Works**

1. Enter a public GitHub repository URL

2. Choose an operation:
   - Analyze Repository
   - Explain a File
   - Search Symbol/Class
   - Analyze Project Architecture
   - Generate README

3. The assistant clones the repository (or reuses the locally cached copy)

4. Repository structure, README, programming languages, dependency information, and source files are analyzed

5. Gemini generates repository-aware responses using the extracted context

-------------------------------------------------------------------------------------

✦ **Installation**

Clone the repository

```bash
git clone https://github.com/zeemofukaa/github-ai-assistant.git
cd github-ai-assistant
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

```text
Summarize this repository
```

File Explanation

```text
Explain routing.py
```

Symbol Search

```text
Where is APIRouter implemented?
```

Architecture Analysis

```text
Explain project architecture
```

README Generation

```text
Generate README
```

-------------------------------------------------------------------------------------

✦ **Project Structure**

```text
github-ai-assistant/
│
├── agent.py
├── github_tools.py
├── dependency_graph.py
├── gemini_client.py
├── memory.py
├── requirements.txt
├── .env.example
└── .gitignore
```

-------------------------------------------------------------------------------------

✦ **Notes**

• Repository analyses are cached locally for faster repeated queries

• Dependency graph analysis currently supports Python repositories through AST-based static analysis

• Large repositories are summarized before being sent to Gemini to reduce context size

-------------------------------------------------------------------------------------

✦ **Status**

This is a personal project built to explore AI-assisted developer tools and repository analysis workflows.

The project combines static code analysis with large language models to help developers understand unfamiliar Python codebases more efficiently.

-------------------------------------------------------------------------------------

✦ **Author**

Made by **zeemofukaa_**
