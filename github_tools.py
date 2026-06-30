import ast
from pathlib import Path
from git import Repo

WORKSPACE = Path("repos")
WORKSPACE.mkdir(exist_ok=True)


def clone_repo(repo_url: str) -> Path:
    repo_name = repo_url.rstrip("/").split("/")[-1]
    repo_path = WORKSPACE / repo_name

    if repo_path.exists():
        print(f"Repository already exists: {repo_path}")
        return repo_path

    print("Cloning repository...")
    Repo.clone_from(repo_url, repo_path)

    return repo_path


def list_files(repo_path: Path):
    files = []

    for file in repo_path.rglob("*"):
        if file.is_file() and ".git" not in str(file):
            files.append(str(file.relative_to(repo_path)))

    return files


def read_readme(repo_path: Path):

    for filename in (
        "README.md",
        "README.rst",
        "README.txt",
        "README",
    ):
        path = repo_path / filename

        if path.exists():
            return path.read_text(
                encoding="utf-8",
                errors="ignore"
            )

    return "No README found."


def detect_languages(repo_path: Path):

    languages = {}

    for file in repo_path.rglob("*"):

        if file.is_file():

            ext = file.suffix.lower()

            if ext:

                languages[ext] = languages.get(ext, 0) + 1

    return dict(
        sorted(
            languages.items(),
            key=lambda x: x[1],
            reverse=True,
        )
    )

def read_file(repo_path, file_path):

    path = repo_path / file_path

    if not path.exists():
        return None

    return path.read_text(
        encoding="utf-8",
        errors="ignore"
    )

def find_file(repo_path, filename):

    matches = []

    for file in repo_path.rglob("*"):

        if file.is_file():

            if file.name.lower() == filename.lower():

                matches.append(file)

    return matches

def search_code(repo_path, keyword):

    matches = []

    for file in repo_path.rglob("*"):

        if not file.is_file():
            continue

        if ".git" in str(file):
            continue

        try:
            text = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            if keyword.lower() in text.lower():

                matches.append({
                    "path": str(file.relative_to(repo_path)),
                    "content": text
                })

        except Exception:
            pass

    return matches

def find_symbol_usages(repo_path, symbol):

    usages = []

    for file in Path(repo_path).rglob("*.py"):

        if ".git" in str(file):
            continue

        try:

            source = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            tree = ast.parse(source)

        except Exception:
            continue

        class SymbolVisitor(ast.NodeVisitor):

            def visit_Name(self, node):

                if node.id == symbol:

                    usages.append({
                        "module": file.stem,
                        "path": str(file.relative_to(repo_path)),
                        "line": node.lineno,
                        "type": "Reference"
                    })

                self.generic_visit(node)

            def visit_ImportFrom(self, node):

                for alias in node.names:

                    if alias.name == symbol:

                        usages.append({
                            "module": file.stem,
                            "path": str(file.relative_to(repo_path)),
                            "line": node.lineno,
                            "type": "Import"
                        })

            def visit_ClassDef(self, node):

                if node.name == symbol:

                    usages.append({
                        "module": file.stem,
                        "path": str(file.relative_to(repo_path)),
                        "line": node.lineno,
                        "type": "Class Definition"
                    })

                self.generic_visit(node)

            def visit_FunctionDef(self, node):

                if node.name == symbol:

                    usages.append({
                        "module": file.stem,
                        "path": str(file.relative_to(repo_path)),
                        "line": node.lineno,
                        "type": "Function Definition"
                    })

                self.generic_visit(node)

        SymbolVisitor().visit(tree)

    return usages