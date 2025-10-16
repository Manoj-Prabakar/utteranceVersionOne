# Utterance Intention Generator

A simple Python project using Google's Agent Development Kit (ADK) and Gemini Flash LLM model to generate diverse utterances for given intentions.

## Features

- 🤖 Uses Google ADK with Gemini Flash LLM
- 💬 Interactive command-line interface  
- 📝 Generates 10 diverse utterances for any intention
- 📊 Automatically saves results to timestamped CSV files
- ⚡ Simple and clean code structure
- 🔧 Proper function separation

## Project Structure

```
UtterenceIntentionVersion1/
├── main.py              # Main script
├── requirements.txt     # Dependencies
├── pyproject.toml      # Project configuration
└── README.md           # This file
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Authentication (Choose ONE method):**

   ### Method 1: Service Account Key (Recommended)
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a service account with Vertex AI permissions
   - Download the JSON key file
   - Set environment variable:
     ```bash
     set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\service-account-key.json
     ```

   ### Method 2: gcloud CLI Authentication
   ```bash
   gcloud auth login
   gcloud auth application-default login
   set GOOGLE_CLOUD_PROJECT=your-project-id
   ```

   ### Method 3: Direct API Key
   - Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Set environment variable:
     ```bash
     set GOOGLE_API_KEY=your-api-key-here
     ```

   ### Method 4: Using .env file
   - Copy `.env.template` to `.env`
   - Fill in your credentials in the `.env` file

## Usage

Run the script:
```bash
python main.py
```

### Example Flow

```
Hello! 👋 Welcome to the Utterance Generator.
Please enter an intention: Order coffee
Generating utterances using Gemini Flash...

📝 Generated utterances for 'Order coffee':
--------------------------------------------------
 1. I'd like to order a coffee, please
 2. Can I get a cup of coffee?
 3. I need my morning coffee fix
 4. Could you make me a coffee?
 5. I want to buy some coffee
 6. May I have a coffee to go?
 7. I'm looking to purchase a coffee
 8. Can you brew me a fresh coffee?
 9. I'd love a hot cup of coffee
10. Let me get a coffee order in

Done! 10 utterances saved in utterances_20251016.csv ✅
```

## Output

The generated utterances are saved to organized folders with timestamps:

### Folder Structure
```
UtterenceIntentionVersion1/
├── utterance_outputs_20251016/     # Daily folder
│   ├── utterances_20251016_143052.csv
│   ├── utterances_20251016_144123.csv
│   └── ...
├── utterance_outputs_20251017/     # Next day's folder
│   └── utterances_20251017_090315.csv
└── ...
```

### File Naming Convention
- **Folder**: `utterance_outputs_YYYYMMDD` (daily folders)
- **File**: `utterances_YYYYMMDD_HHMMSS.csv` (with exact timestamp)

### CSV Content
Each CSV file contains:
- `id` - Sequential number (1-10)
- `utterance` - Generated text
- `original_intention` - User's input
- `generated_at` - Timestamp of generation

### Folder Management
Use the included utility script to manage output folders:
```bash
python manage_outputs.py
```

Features:
- List all output folders
- Show folder statistics
- Clean old folders (7+ days)
- Interactive management interface

## Functions

- `get_user_input()` - Handles user interaction and input validation
- `create_agent()` - Creates and configures the ADK LLM agent
- `generate_utterances()` - Uses the agent to generate diverse utterances
- `save_to_csv()` - Exports results to timestamped CSV file

## Requirements

- Python 3.10+
- Google ADK library
- Valid Google Cloud authentication
- Internet connection for LLM API calls