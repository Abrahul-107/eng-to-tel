import streamlit as st
import requests
import json
import logging
from datetime import datetime
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()


# --- LOGGING CONFIGURATION ---
# Create logs directory if it doesn't exist
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Configure logging with both file and console handlers
log_filename = logs_dir / f"pronunciation_app_{datetime.now().strftime('%Y%m%d')}.log"

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Prevent duplicate handlers if Streamlit reruns
if not logger.handlers:
    # File handler - captures everything
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    # Console handler - for development
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

logger.info("="*80)
logger.info("Application started")
logger.info("="*80)

# --- CONFIGURATION --- 
API_KEY = os.getenv("API_KEY")  # Load from environment variable
if not API_KEY:
    logger.error("API_KEY not found in environment variables. Please set it in the .env file.")
    st.error("API_KEY not found. Please contact the administrator.")
    st.stop()
MODEL = "meta-llama/Llama-3-70b-chat-hf"

logger.info(f"Configuration loaded - Model: {MODEL}")

# --- FUNCTION TO CALL LLaMA 70B ---
def get_pronunciation(word):
    """
    Get pronunciation for a given word using LLaMA API
    
    Args:
        word (str): The English word to get pronunciation for
        
    Returns:
        dict: JSON response containing word, pronunciation, and Telugu pronunciation
    """
    logger.info(f"Processing word: '{word}'")
    
    prompt = f"""
You are a language assistant. I will provide an English word. Your task is to:

1. Convert the English word into its correct pronunciation in English in USA style (like Toilet: 'TOy Luht').
2. Convert that pronunciation into a Telugu representation of the sounds.

Respond in JSON format as shown in the example.

Example input: 'toilet'
Example output:
{{
  "word": "toilet",
  "pronunciation": "TOy Luht",
  "pronunciation_telugu": "టాయ్ లహ్ట్"
}}

Note: Do not include any additional text or explanations, only the JSON object. Do not include any markdown formatting. Ensure the Telugu representation captures the phonetic sounds accurately.
Now process the following word: '{word}'
"""

    logger.debug(f"Prompt created for word '{word}' - Length: {len(prompt)} characters")

    url = "https://api.together.xyz/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",  # Masked for logging
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "prompt": prompt,
        "max_tokens": 200,
        "temperature": 0
    }       



    logger.debug(f"API Request parameters - max_tokens: {data['max_tokens']}, temperature: {data['temperature']}")

    try:
        logger.info(f"Sending API request for word: '{word}'")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        logger.info(f"API response received - Status code: {response.status_code}")
        logger.debug(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            logger.debug(f"Raw API response: {json.dumps(result, indent=2)}")
            
            output_text = result["choices"][0]["text"]
            logger.debug(f"Extracted output text: {output_text}")
            
            cleaned_text = output_text.strip().strip("```").strip()
            logger.debug(f"Cleaned text: {cleaned_text}")
            
            try:
                parsed_json = json.loads(cleaned_text)
                logger.info(f"Successfully parsed JSON for word '{word}'")
                logger.debug(f"Parsed result: {json.dumps(parsed_json, ensure_ascii=False)}")
                return parsed_json
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error for word '{word}': {str(e)}")
                logger.error(f"Failed to parse text: {cleaned_text}")
                return {
                    "error": "Failed to parse JSON from LLM output",
                    "raw_output": output_text,
                    "word": word
                }
        else:
            logger.error(f"API request failed with status {response.status_code}")
            logger.error(f"Error details: {response.text}")
            return {
                "error": f"API request failed with status {response.status_code}",
                "details": response.text,
                "word": word
            }
            
    except requests.exceptions.Timeout:
        logger.error(f"API request timeout for word '{word}'")
        return {"error": "Request timeout", "word": word}
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error for word '{word}': {str(e)}")
        return {"error": "Connection error", "details": str(e), "word": word}
    except Exception as e:
        logger.exception(f"Unexpected error processing word '{word}': {str(e)}")
        return {"error": "Unexpected error", "details": str(e), "word": word}

# --- STREAMLIT UI ---
logger.info("Initializing Streamlit UI")

st.set_page_config(page_title="English to Telugu Pronunciation", layout="centered")
st.title("English to Telugu Pronunciation Converter")

st.write("Enter English words (comma-separated) to get their pronunciation in English and Telugu:")

words_input = st.text_area("Words", value="toilet, computer, water")

logger.debug(f"Current input in text area: '{words_input}'")

if st.button("Convert"):
    logger.info("Convert button clicked")
    logger.info(f"Raw input received: '{words_input}'")
    
    words = [w.strip() for w in words_input.split(",") if w.strip()]
    logger.info(f"Parsed {len(words)} words: {words}")
    
    if not words:
        logger.warning("No valid words entered by user")
        st.warning("Please enter at least one word.")
    else:
        all_outputs = []
        successful_conversions = 0
        failed_conversions = 0
        
        logger.info(f"Starting batch processing of {len(words)} words")
        start_time = datetime.now()
        
        with st.spinner("Processing..."):
            for idx, w in enumerate(words, 1):
                logger.info(f"Processing word {idx}/{len(words)}: '{w}'")
                
                try:
                    output = get_pronunciation(w)
                    all_outputs.append(output)
                    
                    if "error" in output:
                        failed_conversions += 1
                        logger.warning(f"Failed conversion for word '{w}': {output.get('error')}")
                    else:
                        successful_conversions += 1
                        logger.info(f"Successful conversion for word '{w}'")
                        
                except Exception as e:
                    logger.exception(f"Critical error processing word '{w}': {str(e)}")
                    all_outputs.append({
                        "error": "Critical processing error",
                        "details": str(e),
                        "word": w
                    })
                    failed_conversions += 1
        
        end_time = datetime.now()
        processing_duration = (end_time - start_time).total_seconds()
        
        logger.info(f"Batch processing completed in {processing_duration:.2f} seconds")
        logger.info(f"Results - Successful: {successful_conversions}, Failed: {failed_conversions}")

        # Display output
        st.subheader("Results")
        logger.debug("Displaying results to user")
        st.json(all_outputs)

        # Display statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Words", len(words))
        with col2:
            st.metric("Successful", successful_conversions)
        with col3:
            st.metric("Failed", failed_conversions)

        # Save to JSON file and provide download link
        json_str = json.dumps(all_outputs, ensure_ascii=False, indent=2)
        logger.info(f"Generated JSON output - Size: {len(json_str)} bytes")
        
        st.download_button(
            label="Download JSON",
            data=json_str,
            file_name=f"pronunciations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
        logger.info("Download button rendered for user")

# --- SIDEBAR WITH LOG INFO ---
with st.sidebar:
    st.header("Logging Information")
    st.info(f"📝 Log file: {log_filename.name}")
    st.caption(f"Location: {log_filename.absolute()}")
    
    if log_filename.exists():
        log_size = log_filename.stat().st_size
        st.caption(f"Size: {log_size:,} bytes")
        
        # Show recent log entries
        if st.checkbox("Show recent logs"):
            try:
                with open(log_filename, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    recent_logs = ''.join(lines[-20:])  # Last 20 lines
                    st.text_area("Recent Log Entries", recent_logs, height=300)
            except Exception as e:
                st.error(f"Error reading log file: {e}")

logger.debug("UI rendering complete")
logger.info("Waiting for user interaction...")