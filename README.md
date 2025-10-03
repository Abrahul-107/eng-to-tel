# English to Telugu Pronunciation Converter

A Streamlit-based web application that converts English words into their phonetic pronunciation and Telugu transliteration using the LLaMA 3 70B language model.

## Features

- 🔤 **Phonetic Conversion**: Converts English words to USA-style pronunciation
- 🇮🇳 **Telugu Transliteration**: Provides Telugu script representation of pronunciations
- 📊 **Batch Processing**: Process multiple words at once (comma-separated)
- 📝 **Comprehensive Logging**: Detailed logging of all operations for debugging and monitoring
- 💾 **Export Functionality**: Download results as JSON files with timestamps
- 📈 **Statistics Dashboard**: Real-time success/failure metrics
- 🔍 **Log Viewer**: Built-in sidebar to view recent log entries

## Prerequisites

- Python 3.7 or higher
- Active Together AI API key
- Internet connection for API calls

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pronunciation-converter
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   - Open the Python script
   - Replace the `API_KEY` value with your Together AI API key:
     ```python
     API_KEY = "your_api_key_here"
     ```

## Requirements

Create a `requirements.txt` file with:

```
streamlit>=1.28.0
requests>=2.31.0
```

## Usage

### Running the Application

1. **Start the Streamlit app**
   ```bash
   streamlit run app.py
   ```

2. **Access the application**
   - The app will automatically open in your default browser
   - Default URL: `http://localhost:8501`

### Using the Interface

1. **Enter Words**
   - Type English words in the text area
   - Separate multiple words with commas
   - Example: `toilet, computer, water, elephant`

2. **Convert**
   - Click the "Convert" button
   - Wait for processing (spinner will appear)

3. **View Results**
   - Results appear in JSON format
   - Statistics show success/failure counts
   - Download JSON file with the "Download JSON" button

4. **Check Logs** (Sidebar)
   - View log file information
   - Toggle "Show recent logs" to see last 20 log entries
   - Check processing details and errors

## Output Format

The application returns JSON with the following structure:

```json
[
  {
    "word": "toilet",
    "pronunciation": "TOy Luht",
    "pronunciation_telugu": "టాయ్ లహ్ట్"
  },
  {
    "word": "computer",
    "pronunciation": "kuhm-PYOO-ter",
    "pronunciation_telugu": "కమ్ ప్యూ టర్"
  }
]
```

### Error Format

If an error occurs, the output includes error details:

```json
{
  "error": "API request failed with status 429",
  "details": "Rate limit exceeded",
  "word": "example"
}
```

## Logging

### Log Files

- **Location**: `logs/` directory (created automatically)
- **Naming**: `pronunciation_app_YYYYMMDD.log`
- **Encoding**: UTF-8 (supports Telugu characters)
- **Rotation**: Daily log files

### Log Levels

| Level | Description |
|-------|-------------|
| DEBUG | Detailed diagnostic information |
| INFO | General informational messages |
| WARNING | Warning messages for potential issues |
| ERROR | Error messages with details |
| EXCEPTION | Critical errors with full stack traces |

### What Gets Logged

- ✅ Application startup and configuration
- ✅ User input and parsed words
- ✅ API requests (with masked API keys)
- ✅ API responses and status codes
- ✅ JSON parsing attempts
- ✅ Processing time and batch statistics
- ✅ Success/failure counts
- ✅ All errors with full context
- ✅ Download interactions

### Log Format

```
2025-01-15 10:30:45 | INFO     | get_pronunciation:45 | Processing word: 'toilet'
2025-01-15 10:30:46 | DEBUG    | get_pronunciation:67 | API Request parameters - max_tokens: 200, temperature: 0
2025-01-15 10:30:47 | INFO     | get_pronunciation:73 | API response received - Status code: 200
```

## Configuration

### API Settings

```python
API_KEY = "your_together_ai_api_key"
MODEL = "meta-llama/Llama-3-70b-chat-hf"
```

### Request Parameters

- **max_tokens**: 200 (maximum response length)
- **temperature**: 0 (deterministic output)
- **timeout**: 30 seconds per request

## Error Handling

The application handles various error scenarios:

- **Timeout Errors**: API requests exceeding 30 seconds
- **Connection Errors**: Network connectivity issues
- **JSON Parse Errors**: Invalid JSON responses from API
- **Rate Limiting**: Together AI API rate limits
- **Invalid Input**: Empty or malformed word lists

## Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure your API key is valid
   - Check for extra spaces or quotes
   - Verify API key hasn't expired

2. **Connection Timeout**
   - Check internet connection
   - Verify Together AI service status
   - Consider increasing timeout value

3. **JSON Parse Error**
   - Check logs for raw API response
   - Verify model is returning expected format
   - May indicate API changes or issues

4. **Rate Limiting**
   - Wait before retrying
   - Consider upgrading Together AI plan
   - Process words in smaller batches

### Viewing Logs

1. Navigate to the `logs/` directory
2. Open the current day's log file
3. Use the sidebar log viewer in the app
4. Search for ERROR or WARNING levels

## Performance

- **Average Processing Time**: ~2-5 seconds per word
- **Batch Processing**: Sequential (one word at a time)
- **Concurrent Users**: Supported by Streamlit
- **Log File Size**: Grows with usage (monitor regularly)

## Best Practices

1. **Word Input**
   - Use lowercase for consistency
   - Avoid special characters
   - Separate multiple words with commas only

2. **API Usage**
   - Monitor your Together AI quota
   - Process in reasonable batch sizes
   - Check logs for failed requests

3. **Log Management**
   - Review logs periodically
   - Archive old log files
   - Monitor disk space usage

## API Documentation

- **Together AI**: https://docs.together.ai/
- **Model Info**: https://docs.together.ai/docs/inference-models
- **Rate Limits**: Check your Together AI account dashboard

## Project Structure

```
pronunciation-converter/
│
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── logs/                 # Log files directory (auto-created)
│   └── pronunciation_app_YYYYMMDD.log
└── .gitignore           # Git ignore file (recommended)
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add appropriate logging
5. Test thoroughly
6. Submit a pull request

## Security Notes

- ⚠️ **Never commit API keys** to version control
- ⚠️ Use environment variables for sensitive data
- ⚠️ Rotate API keys regularly
- ⚠️ Monitor API usage for unauthorized access

## License

[Specify your license here]

## Support

For issues and questions:

- Check the logs directory for detailed error information
- Review the troubleshooting section
- Open an issue on GitHub
- Contact: [your-email@example.com]

## Acknowledgments

- **Together AI** for providing the LLaMA API
- **Streamlit** for the web framework
- **Meta** for the LLaMA model

## Version History

### v1.0.0 (Current)
- Initial release
- Basic pronunciation conversion
- Comprehensive logging system
- Batch processing support
- JSON export functionality
- Statistics dashboard

---

**Last Updated**: October 2025  
**Author**: Rahul Parida
**Status**: Active Development