# LangChain Agent

This project is a FastAPI-based LangChain conversational agent that stores users, sessions, and message memory in a local SQLite database. It uses a Google API key for the model connection and provides a chat endpoint for user conversations.

## What this project does

- Runs a FastAPI server with a `/chat/{username}` endpoint
- Tracks users and conversation sessions in SQLite
- Keeps recent messages and summaries for better context
- Uses LangChain prompts and an LLM model for AI response generation
- Loads the Google API key from `Agent/keys.env`



## Summarizer and profile extractor

This project includes two memory-enhancement features that help keep conversations personalized over time:

- The summarizer turns a recent conversation chunk into a concise long-term summary.
- The profile extractor builds a structured user profile from the conversation, such as preferences, goals, or important personal facts.

### Summarizer

#### USER NAMES ARE CASE SENSITIVE.
The summarizer is implemented in `Agent/utils/summarizer.py` and is run through `Agent/utils/summarizer_routine.py`.

How it works:
- It reads the latest stored conversation messages for a user.
- It combines those messages with the previous summary.
- It sends the content to the configured LLM model.
- It saves the updated summary back to the database.

Example usage:

```python
from Agent.utils.summarizer_routine import summarizer_routine

summarizer_routine("alice")
```

### Profile extractor

The profile extractor is implemented in `Agent/utils/extractor.py` and is run through `Agent/utils/extractor_routine.py`.

How it works:
- It collects messages after the last profile update.
- It asks the model to extract a structured user profile.
- It merges the new profile into the stored profile.
- It updates the profile tracking information in the database.


### Setup notes for these features

- These routines require a valid Google API key in `Agent/keys.env`.
- They depend on the SQLite database already having the user and message records created by the app.
- They should be run after new messages are stored, so the system can summarize or extract from the latest conversation history.
- Make sure the Python environment is activated and the dependencies from `requirements.txt` are installed.

## Setup

1. Create a virtual environment outside the `Agent` folder.

   Example:
   ```powershell
   python -m venv venv
   ```

2. Activate the virtual environment.

   On VSCODE PowerShell:
   ```powershell
   venv\Scripts
   .\Activate.ps1
   ```

3. Install dependencies.

   ```powershell
   python -m pip install -r requirements.txt
   ```
4. Create the `Agent/keys.env` file in the `Agent` folder.

   ```text
   GOOGLE_API_KEY=your_google_api_key_here
   ```

5. Download DB Browser for SQLite to inspect and manage the SQLite database file.
6. If uvicorn or fast api error, properly acitvate the environment and try python -m pip install fastapi uvicorn

7. To run
   ```text
   (venv) PS D:\VSCODE\Testing\multi_user_cli_agent> uvicorn Agent.main:app --reload
   ```
8. You will see the passed conversation, passed history, passed userprofile and basic latencies in the vs code terminal. 

## Notes

- Make sure the virtual environment is activated before running the project.
- The API key is loaded from `Agent/keys.env` by `Agent/config.py`.
- Use DB Browser for SQLite to open the `database.db` or any SQLite database files created by the app.
