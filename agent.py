import re
import textwrap
import os


from github_tools import (
    clone_repo,
    detect_languages,
    list_files,
    read_readme,
    read_file,
    find_file,
    search_code
)

from gemini_client import ask_gemini
from memory import save_analysis, recall_analysis

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def analyze_repository(repo_url, question):

    try:
        repo = clone_repo(repo_url)
    except Exception as e:
        return f"!! Failed to clone repository.\n\n{e}"
    print("[✓] Repository ready")

    file_extensions = (
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".java",
        ".cpp",
        ".c",
        ".h",
        ".hpp",
        ".go",
        ".rs",
    )

    requested_file = None

    for word in question.split():

        if word.endswith(file_extensions):
            requested_file = word
            break
        
    if requested_file:

        matches = find_file(repo, requested_file)

        if len(matches) == 0:
            return f"Couldn't find {requested_file}"

        if len(matches) > 1:

            print("\nMultiple files found:\n")

            for i, path in enumerate(matches):
                print(f"{i+1}. {path.relative_to(repo)}")

            choice = int(input("\nChoose file: ")) - 1

            requested_file = str(matches[choice].relative_to(repo))

        else:

            requested_file = str(matches[0].relative_to(repo))

        print(f"[•] Reading {requested_file}...")
        code = read_file(repo, requested_file)
        print("[✓] File loaded")
        print("[•] Explaining file with Gemini...")

        if code is None:
            return f"Couldn't find {requested_file}"

        prompt = f"""
You are a senior software engineer.

Explain this source file.

File:
{requested_file}

Code:

{code[:15000]}

Explain:

1. What is the purpose of this file?
2. What are its main classes and functions?
3. How does it fit into the project?
4. What other files does it likely interact with?
5. Why is this file important?

Formatting requirements:

- Return plain text only.
- Do not use Markdown.
- Write exactly 3 paragraphs.
- Each paragraph should contain 2–3 sentences.
- Leave one blank line between paragraphs.
- Keep the total response under 300 words.
"""

        return ask_gemini(prompt)
    

    search_words = (
        "where",
        "implemented",
        "implementation",
        "defined",
        "definition",
        "class",
        "function",
    )

    is_search = any(
        word in question.lower()
        for word in search_words
    )


    match = re.search(
        r"(?:where\s+is|where\s+are)\s+([A-Za-z_][A-Za-z0-9_]*)",
        question,
        re.IGNORECASE
    )

    symbol = match.group(1) if match else None
        
    if is_search and symbol:
        
        print(f"[•] Searching for '{symbol}'...")
        results = search_code(repo, symbol)
        print(f"[✓] Found {len(results)} matching file(s)")
        print("[•] Analyzing search results...")

        if len(results) == 0:
            return f"No occurrences of {symbol} found."

        context = ""

        for result in results[:5]:

            context += f"""

    FILE:
    {result['path']}

    CODE:

    {result['content'][:3000]}

    """
    
        prompt = f"""
    You are a senior software engineer.

    The developer wants to understand the symbol:

    {symbol}

    The repository search found these files:

    {context}

    Explain:

    1. What is {symbol}?

    2. Where is it implemented?

    3. Which file should the developer read first?

    4. How is it used throughout the project?

    5. Summarize its purpose.

    Formatting requirements:

    - Return plain text only.
    - Do not use Markdown.
    - Write exactly 3 paragraphs.
    - Each paragraph should contain 2–3 sentences.
    - Leave one blank line between paragraphs.
    - Keep the total response under 300 words.
    """
    
        return ask_gemini(prompt)
            

    cached = recall_analysis(repo_url)

    generate_readme = (
        "generate readme" in question.lower()
        or "create readme" in question.lower()
    )

    if generate_readme:

        print("[•] Reading README...")
        readme = read_readme(repo)
        print("[✓] README loaded")

        print("[•] Detecting programming languages...")
        languages = detect_languages(repo)
        print("[✓] Languages detected")

        print("[•] Indexing repository files...")
        files = list_files(repo)
        print(f"[✓] Indexed {len(files)} files")

        prompt = f"""
    You are an expert technical writer.

    Generate a professional GitHub README for this repository.

    Repository:
    {repo_url}

    Existing README:

    {readme[:4000]}

    Programming Languages:

    {languages}

    Repository Files:

    {chr(10).join(files[:200])}

    Write a README with:

    # Project Title

    ## Overview

    ## Features

    ## Technologies Used

    ## Installation

    ## Usage

    ## Folder Structure

    ## Contributing

    ## License

    Use markdown formatting.
    """

        generated = ask_gemini(prompt)

        with open("README_generated.md", "w", encoding="utf-8") as f:
            f.write(generated)

        return "README successfully generated as README_generated.md"

    if cached:

        print("[✓] Using cached repository analysis")
        print("[•] Asking Gemini to answer your question...")

        prompt = f"""
Repository Analysis:

{cached}

User Question:

{question}

Answer the user's question using the repository analysis above.
"""

        return ask_gemini(prompt)

    print("\nAnalyzing repository...\n")

    

    print("[•] Reading README...")
    readme = read_readme(repo)
    print("[✓] README loaded")

    print("[•] Detecting programming languages...")
    languages = detect_languages(repo)
    print("[✓] Languages detected")

    print("[•] Indexing repository files...")
    files = list_files(repo)
    print(f"[✓] Indexed {len(files)} files")

    prompt = f"""
You are an expert software engineer.

Analyze this GitHub repository.

Repository:
{repo_url}

Programming Languages:
{languages}

README:

{readme[:5000]}

Repository Files:

{chr(10).join(files[:300])}

User Question:
{question}

Formatting requirements:

- Return plain text only.
- Do not use Markdown.
- Write exactly 3 paragraphs.
- Each paragraph should contain 2–3 sentences.
- Leave one blank line between paragraphs.
- Keep the total response under 300 words.
"""

    print("[•] Asking Gemini to analyze the repository...")
    answer = ask_gemini(prompt)
    print("[✓] Analysis complete!")

    save_analysis(repo_url, answer)

    return answer

def format_output(text, width=68):
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    paragraphs = []

    # Group every 2 sentences
    for i in range(0, len(sentences), 2):
        paragraph = " ".join(sentences[i:i+2])
        paragraphs.append(textwrap.fill(paragraph, width=width))

    return "\n\n".join(paragraphs)

def main():

    # clear_screen()

    WIDTH=70

    print("=" * WIDTH)
    print("GitHub AI Repository Assistant".center(WIDTH))
    print("Analyze, Explore and Understand Any GitHub Repository".center(WIDTH))
    print("=" * WIDTH)

    while True:

        print("\n" + "=" * 70)
        print("MENU")
        print("-" * 70)
        print("1. Analyze Repository")
        print("2. Explain a File")
        print("3. Search Symbol/Class")
        print("4. Generate README")
        print("5. Exit")
        print("=" * 70)

        choice = input("\nEnter your choice: ")

        if choice == "5":
            print("\nGoodbye!")
            break
        
        repo = input("\nRepository URL: ")

        if choice == "1":

            question = input(
                "\nWhat would you like to know about this repository?\n> "
            )

        elif choice == "2":

            filename = input(
                "\nEnter the filename (e.g. routing.py): "
            )

            question = f"Explain {filename}"

        elif choice == "3":

            symbol = input(
                "\nEnter class/function name: "
            )

            question = f"Where is {symbol} implemented?"

        elif choice == "4":

            question = "Generate README"

        else:

            print("\nInvalid choice!")

            continue
        
        answer = analyze_repository(repo, question)

        print("\n" + "=" * WIDTH)
        print("RESULT".center(WIDTH))
        print("-" * WIDTH)
        print(format_output(answer))
        print("=" * WIDTH)

        input("\nPress Enter to return to the menu...")

if __name__ == "__main__":
    main()