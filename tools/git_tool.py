from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
import subprocess


@tool
def git_operations(
    operation: str,
    filename: str = "",
    message: str = ""
):
    """
    Perform Git operations such as status, add, commit, push, and remote.
    """

    # ---------------- STATUS ----------------
    if operation == "status":

        result = subprocess.run(
            ["git", "status"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return result.stdout
        else:
            return f"Git status failed:\n{result.stderr}"


    # ---------------- ADD ----------------
    elif operation == "add":

        if not filename:
            return "Please provide a filename."

        result = subprocess.run(
            ["git", "add", filename],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return f"Successfully staged: {filename}"
        else:
            return f"Git add failed:\n{result.stderr}"


    # ---------------- COMMIT ----------------
    elif operation == "commit":

        if not filename:
            return "Please provide the filename to commit."

        if not message:
            return "Please provide a commit message."

        # First stage the file
        add_result = subprocess.run(
            ["git", "add", filename],
            capture_output=True,
            text=True
        )

        if add_result.returncode != 0:
            return f"Git add failed:\n{add_result.stderr}"

        # Then commit
        commit_result = subprocess.run(
            ["git", "commit", "-m", message],
            capture_output=True,
            text=True
        )

        if commit_result.returncode == 0:
            return f"Successfully committed {filename} with message: '{message}'"
        else:
            return f"Git commit failed:\n{commit_result.stderr}"


    # ---------------- PUSH ----------------
    elif operation == "push":

        result = subprocess.run(
            ["git", "push"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return f"Push successful:\n{result.stdout}"
        else:
            return f"Git push failed:\n{result.stderr}"


    # ---------------- REMOTE ----------------
    elif operation == "remote":

        result = subprocess.run(
            ["git", "remote", "-v"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return result.stdout
        else:
            return f"Git remote failed:\n{result.stderr}"


    else:
        return (
            "Invalid operation. "
            "Use: status, add, commit, push, or remote."
        )


# ------------------------------------------------
# LLM
# ------------------------------------------------

llm = ChatOllama(
    model="qwen2.5:3b-instruct"
)


# ------------------------------------------------
# AGENT
# ------------------------------------------------

agent = create_agent(
    model=llm,
    tools=[git_operations],
    system_prompt="""You are a Git assistant.

Use the git_operations tool to perform Git operations for the user.

Available operations:
- status: Check Git status.
- add: Add/stage a file.
- commit: Commit a file with a commit message.
- push: Push changes to the remote repository.
- remote: Show Git remote information.

Rules:
- Use the tool for Git operations.
- Do not make up filenames or commit messages.
- Ask for the filename if the user wants to add or commit a file but does not provide one.
- Ask for a commit message if the user wants to commit but does not provide one.
- Use "." only when the user explicitly asks to add all files.
- Tell the user whether the operation succeeded or failed."""
)


# ------------------------------------------------
# USER INPUT
# ------------------------------------------------

query = input("Enter the prompt: ")

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    }
)


print(response["messages"][-1].content)