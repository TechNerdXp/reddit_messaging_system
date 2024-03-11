# Reddit Application with Python Flask and React JS

This project demonstrates how to create a Reddit application using Python Flask for the backend and React JS for the frontend.

## Prerequisites

- Python 3.6 or higher
- Node.js and npm
- A Reddit account

## Setup

1. **Create a Reddit App**
   - Visit `https://www.reddit.com/prefs/apps` and create a new application.
   - Note down the `client_id` and `client_secret`.
   - Update the about and callback urls according to the host

2. **Update Environment Variables**
   - Update the `.env` file with the `client_id`, `client_secret`, and `redirect_uri` (should be in the format `host/reddit_callback`).
   - Update OpenAI API key and Assistant ID

3. **Install Python Virtual Environment**
   - Run `pip install venv` to install Python's virtual environment package.

4. **Activate the Virtual Environment**
   - Activate the virtual environment using the appropriate command for your operating system.

5. **Install Python Dependencies**
   - Run `pip install -r requirements.txt` to install the necessary Python packages.

## Running the Backend
- Run `screen -S server` to create sceen session for server.
- Run `flask run --port 5010` to start the Flask server.
- Press `CTRL + A + D` to detatch from this session.

## Optional Ngrock Step
- Run `screen -S ngrock` to create screen session for ngrock.
- Run `ngrok http --domain=https://reddiappinterface.ngrok-free.app 5010` to start the Flask server.
- Press `CTRL + A + D` to detatch from this session.


## Authentication
- Visit `host/reddit_auth` on your React client to authenticate with your Reddit account.
- Ensure the Reddit username used for authentication is listed in the admins list.

## Running Messaging Module
- Run `screen -S messaging` to start the Flask server.
- Run `python3 messaging.py` to start fetching posts and sending messages.
- Press `CTRL + A + D` to detatch from this session.

## More Commands (Run If Needed)
For re-attaching to a screen session
- Run `screen -r server`
- Run `screen -r ngrock`
- Run `screen -r messaging`

## Alternatively Run Bash Script to Run ALL
- Run `bash run_all.sh`


