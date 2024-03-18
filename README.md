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

## Initial Setup
- Run `python3 setup.py`

## Alternatively Run Bash Script to Run ALL from Backend to Messaging
- Run `bash run_all.sh`
Note: pls update the host domain in the script and you may want to remvove ngrock step.

## Authentication
- Visit `host/reddit_auth` on your React client to authenticate with your Reddit account.
- Ensure the Reddit username used for authentication is listed in the admins list.
Note: before authentication pls make sure to add the user as admin and their subreddits, keywords etc 
on this route `/admin-subreddits`

## More Commands (Use If Needed)
For Listing screen sessions that are running
- Run `screen -ls`
For re-attaching to a screen session
- Run `screen -r server`
- Run `screen -r ngrock`
- Run `screen -r post_fetching`
- Run `screen -r messaging`

## Client build if not aready done
- Run `./client_build.bat` (for Windows)

