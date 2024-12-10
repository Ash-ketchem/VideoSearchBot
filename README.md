# Social Media Video Downloader Bot

This is a bot that downloads videos from Social Media based on user-specified keywords and uploads them to EmpowerVerse. The bot performs a Google search for the given keyword, finds relevant Social Media posts, downloads the videos, and then uploads them to the designated platform.

## Features

- **Google Search Integration**: Performs a Google search to find Social Media posts matching a given keyword.
- **Video Downloading**: Downloads videos from Social Media posts.
- **Cross-Platform Uploading**: Uploads the downloaded videos to EmpowerVerse.

## Requirements

- Python 3.7+ (recommended version: 3.9 or higher)
- Required libraries (listed in requirements.txt)
- API credentials for the platform where videos will be uploaded

## Installation

1. Clone this repository:

   ```bash
   git clone <repo name>
   cd VideoSearchBot
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/macOS
   venv\Scripts\activate     # For Windows
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the platform API:
   - Obtain the API credentials.
   - Save the credentials in a configuration file or environment variables.
   - FLICK_TOKEN = your_token

## Running the Bot

1. **Run the bot**:

   ```bash
   python3 main.py # for running the directory observer
   python3 bot.py # for searching videos
   ```

2. **The bot will**:

   ### 1. Media Directory Monitoring

   - After running `main.py`, the bot will:
     - Continuously monitor the **media directory** for new files.
     - Upload files to Empowerverse

   ### 2. Instagram Search & Video Download

   - After running `bot.py`, the bot will:
     - Perform a **Google search** for Instagram posts related to a specified keyword.
     - Download the **videos** found on Instagram posts related to the keyword.

## TODOs

- [ ] **Add Progress for platform uploads**
- [ ] **Add retry Mechanisms for video downloads**
- [ ] **Add a Configuration file**
- [ ] **Logging**
