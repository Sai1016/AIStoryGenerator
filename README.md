# MyAvatar - Interactive Story Generator

An AI-powered interactive storytelling application that creates personalized stories based on user input, genre selection, and branching narratives.

## Features

- **Genre Selection**: Choose from Fantasy, Sci-Fi, Mystery, Romance, Horror, and Comedy
- **Dynamic Storytelling**: AI generates coherent, engaging story segments that maintain character consistency and plot continuity
- **Branching Paths**: Get multiple story continuation options at key decision points
- **Creativity Control**: Adjustable temperature setting for story creativity level
- **Session Management**: Maintains story history throughout the session
- **Turn Limits**: Automatic story conclusion after maximum turns to ensure satisfying endings

## How to Run

### Prerequisites
- Python 3.11 or higher
- OpenAI API key

### Installation

1. **Clone or download the project**
   ```bash
   cd /path/to/MyAvatar
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv myvenv
   source myvenv/bin/activate  # On Windows: myvenv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Create a `.env` file in the project root
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the app**
   - Open your browser to `http://localhost:8501`

## Usage

1. **Start a Story**: Select a genre, adjust creativity level, and enter an initial story hook
2. **Continue Interactively**: Add your input and choose to continue with AI or get branching choices
3. **Branching Decisions**: When getting choices, the AI suggests 3 distinct paths forward
4. **Story Conclusion**: The app automatically concludes the story after reaching the turn limit

## Project Structure

```
MyAvatar/
├── app.py              # Streamlit frontend application
├── ai_engine.py        # OpenAI API integration and story generation logic
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── .env               # Environment variables (create this)
└── myvenv/            # Virtual environment (created during setup)
```

## Technical Choices

### Architecture
- **Frontend**: Streamlit for rapid UI development and interactive web interface
- **Backend**: Modular design with separate AI engine for clean separation of concerns
- **State Management**: Streamlit's session state for maintaining story history across interactions

### AI Integration
- **Model**: GPT-4o-mini for cost-effective, high-quality text generation
- **Prompt Engineering**: Structured prompts for different story phases (start, continue, choices, end)
- **Context Management**: Full story history passed to maintain narrative consistency
- **Temperature Control**: User-adjustable creativity parameter (0.0-1.0)

### Key Design Decisions
- **Turn Limits**: Prevents infinite stories and ensures satisfying conclusions
- **Branching Choices**: Provides user agency while maintaining AI-driven narrative
- **Genre-Specific Prompts**: Tailored instructions for different storytelling styles
- **Error Handling**: Graceful handling of API errors and invalid inputs

### Dependencies
- **streamlit**: Web UI framework
- **openai**: Official OpenAI Python client
- **python-dotenv**: Secure environment variable management

## API Usage
The application uses OpenAI's Chat Completions API with structured message formats:
- System messages for AI instructions
- User messages containing story context and input
- Assistant responses for generated story content

## Contributing
Feel free to submit issues, feature requests, or pull requests to improve the application.

## License
This project is open source. Please check individual component licenses for details. 
