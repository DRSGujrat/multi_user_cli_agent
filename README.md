# LangChain Agent

This project is a FastAPI-based LangChain conversational agent that stores users, sessions, and message memory in a local SQLite database. It uses a Google API key for the model connection and provides a chat endpoint for user conversations.

## What this project does

- Runs a FastAPI server with a `/chat/{username}` endpoint
- Tracks users and conversation sessions in SQLite
- Keeps recent messages and summaries for better context
- Uses LangChain prompts and an LLM model for AI response generation
- Loads the Google API key from `Agent/keys.env`

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

## Notes

- Make sure the virtual environment is activated before running the project.
- The API key is loaded from `Agent/keys.env` by `Agent/config.py`.
- Use DB Browser for SQLite to open the `database.db` or any SQLite database files created by the app.
- If uvicorn or fast api error try python -m pip install fastapi uvicorn
