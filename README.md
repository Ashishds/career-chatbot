# AI Agent Chat Interface

A modular, production-ready AI agent application that provides an interactive chat interface for representing a person's professional profile. The application uses OpenAI's GPT models with function calling capabilities and includes notification features via Pushover.

## 🚀 Features

- **Interactive Chat Interface**: Clean Gradio-based web interface for user interactions
- **AI Agent with Function Calling**: Uses OpenAI's function calling to handle user registrations and unknown questions
- **Modular Architecture**: Clean separation of concerns with dedicated modules for configuration, notifications, tools, and web interface
- **Notification System**: Pushover integration for real-time notifications about user interactions
- **Professional Profile Integration**: Incorporates LinkedIn profile and summary information
- **Production Ready**: Comprehensive error handling, logging, and configuration management

## 📁 Project Structure

```
ai-agent/
├── app.py                     # Main application entry point
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore rules
├── README.md                 # This file
├── config/                   # Configuration management
│   ├── __init__.py
│   └── settings.py           # Environment variables and settings
├── notifications/            # Notification system
│   ├── __init__.py
│   └── pushover_client.py   # Pushover notification client
├── tools/                    # Function tools for AI agent
│   ├── __init__.py
│   └── function_tools.py     # Tool definitions and handlers
├── ai_agent/                 # AI agent core
│   ├── __init__.py
│   └── agent.py              # Main AI agent class
├── web_interface/            # Web interface
│   ├── __init__.py
│   └── gradio_app.py         # Gradio web interface
└── me/                       # Agent profile data
    ├── linkedin.pdf          # LinkedIn profile PDF
    └── summary.txt           # Professional summary
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Pushover account (optional, for notifications)
  - Sign up at [Pushover.net](https://pushover.net)
  - Create an application to get your API token
  - Get your user key from your account

### Local Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ai-agent
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```env
   # Required
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Optional (for notifications)
   PUSHOVER_TOKEN=your_pushover_token_here
   PUSHOVER_USER=your_pushover_user_key_here
   
   # Agent Configuration
   AGENT_NAME=Your Name
   LINKEDIN_PDF_PATH=me/linkedin.pdf
   SUMMARY_FILE_PATH=me/summary.txt
   APP_TITLE=AI Agent Chat Interface
   APP_DESCRIPTION=Chat with an AI agent
   ```

5. **Prepare profile data**:
   Create the `me/` directory and add:
   - `linkedin.pdf`: Your LinkedIn profile exported as PDF
   - `summary.txt`: A text file with your professional summary

6. **Run the application**:
   ```bash
   python app.py
   ```

The application will be available at `http://localhost:7860`.

## 🚀 Hugging Face Deployment

### Deploy as Hugging Face Space

1. **Create a new Space** on Hugging Face:
   - Go to [Hugging Face Spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Choose "Gradio" as the SDK
   - Set visibility (public/private)

2. **Upload your code**:
   - Upload all files to your Space repository
   - Ensure `app.py` is in the root directory

3. **Set up secrets**:
   - Go to your Space settings
   - Add the following secrets:
     - `OPENAI_API_KEY`: Your OpenAI API key
     - `PUSHOVER_TOKEN`: Your Pushover token (optional)
     - `PUSHOVER_USER`: Your Pushover user key (optional)

4. **Configure Space settings**:
   - Set the title and description
   - The Space will automatically build and deploy

## 📖 Usage

### Basic Usage

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to `http://localhost:7860`

3. **Start chatting** with the AI agent about your professional background

### Example Conversations

- "Tell me about your background"
- "What are your skills and experience?"
- "How can I contact you?"
- "What projects have you worked on?"

## 🔧 Development

### Code Structure

The application follows a modular architecture:

- **`config/`**: Configuration management and environment variables
- **`notifications/`**: Pushover notification system
- **`tools/`**: Function tools for AI agent interactions
- **`ai_agent/`**: Core AI agent logic and conversation handling
- **`web_interface/`**: Gradio web interface implementation

### Adding New Features

1. **New Tools**: Add function definitions in `tools/function_tools.py`
2. **New Notifications**: Extend `notifications/pushover_client.py`
3. **UI Changes**: Modify `web_interface/gradio_app.py`
4. **Agent Behavior**: Update `ai_agent/agent.py`

## 📝 API Reference

### Configuration

The `Config` class manages all application settings:

```python
from config import config

# Validate configuration
if config.validate_config():
    print("Configuration is valid")

# Get missing variables
missing = config.get_missing_config()
```

### AI Agent

The `AIAgent` class handles conversations:

```python
from ai_agent import AIAgent

agent = AIAgent()
response = agent.chat("Hello!", [])
```

### Notifications

The `PushoverClient` handles notifications:

```python
from notifications import notification_client

notification_client.send_notification("Test message")
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Commit your changes: `git commit -m "Add feature"`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check the configuration and ensure all required environment variables are set
2. Verify that all required files exist in the correct locations
3. Check the console output for error messages
4. Ensure your OpenAI API key is valid and has sufficient credits

## 🔗 Links

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Gradio Documentation](https://gradio.app/docs/)
- [Pushover API Documentation](https://pushover.net/api)
- [Hugging Face Spaces](https://huggingface.co/spaces)
