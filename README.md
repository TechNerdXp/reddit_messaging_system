# Reddit Application with Python Flask and React JS

This project demonstrates how to create a Reddit application using Python Flask for the backend and React JS for the frontend.

## Prerequisites

- Python 3.6 or higher
- Node.js and npm
- A Reddit account

## Setup

1. **Create a Reddit App**
   - Visit Reddit Apps and create a new application.
   - Note down the `client_id` and `client_secret`.

2. **Update Environment Variables**
   - Update the `.env` file with the `client_id`, `client_secret`, and `redirect_uri` (should be in the format `host/reddit_callback`).

3. **Install Python Virtual Environment**
   - Run `pip install venv` to install Python's virtual environment package.

4. **Activate the Virtual Environment**
   - Activate the virtual environment using the appropriate command for your operating system.

5. **Install Python Dependencies**
   - Run `pip install -r requirements.txt` to install the necessary Python packages.

## Running the Backend

- Run `python app.py` to start the Flask server.

## Running the Frontend

1. Navigate to the client directory: `cd client`
2. Install the necessary npm packages: `npm install`
3. Start the React app: `npm start`

## Authentication

- Visit `host/reddit_auth` on your React client to authenticate with your Reddit account.
- Ensure the Reddit username used for authentication is listed in the `.env` file's comma-separated `admins` list.


