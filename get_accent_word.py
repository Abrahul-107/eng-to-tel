import requests
import json
from load_dotenv import load_dotenv
load_dotenv()
import os


# --- CONFIGURATION ---
API_KEY = os.getenv("API_KEY")  # Load from environment variable
if not API_KEY:
    raise ValueError("API_KEY not found in environment variables. Please set it in the .env file.") 
MODEL = "meta-llama/Llama-3-70b-chat-hf"

# --- FUNCTION TO CALL LLaMA 70B ---
def get_pronunciation(word):
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

NNote: Do not include any additional text or explanations, only the JSON object. Do not include any markdown formatting. Ensure the Telugu representation captures the phonetic sounds accurately.
Now process the following word: '{word}'
"""

    url = "https://api.together.xyz/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "prompt": prompt,
        "max_tokens": 200,
        "temperature": 0
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        output_text = result["choices"][0]["text"]

        # --- CLEAN OUTPUT ---
        cleaned_text = output_text.strip().strip("```").strip()
        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON from LLM output", "raw_output": output_text}
    else:
        return {"error": f"API request failed with status {response.status_code}", "details": response.text}

# --- PROCESS WORDS AND STORE OUTPUT ---
words = ["toilet", "computer", "water"]
all_outputs = []

for w in words:
    output = get_pronunciation(w)
    all_outputs.append(output)

# --- SAVE TO JSON FILE ---
with open("pronunciations.json", "w", encoding="utf-8") as f:
    json.dump(all_outputs, f, ensure_ascii=False, indent=2)

print("Output saved to pronunciations.json")
