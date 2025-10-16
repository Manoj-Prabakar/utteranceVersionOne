#!/usr/bin/env python3
"""
Simple Utterance Generator using Google Generative AI
Direct API approach for reliable utterance generation.
"""

import csv
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_user_input():
    """Get user input for the intention/context."""
    print("Hello! 👋 Welcome to the Utterance Generator.")
    intention = input("Please enter an intention: ").strip()
    
    if not intention:
        print("No intention provided. Exiting.")
        return None
    
    return intention


def generate_utterances_simple(intention: str):
    """Generate utterances using Google Generative AI directly."""
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("❌ GOOGLE_API_KEY not found!")
            print("Please set your API key in the .env file")
            return None
        
        print("Generating utterances using Gemini Flash...")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""Generate 10 diverse utterances for this intention: "{intention}"

Make each utterance unique and natural. Vary the:
- Sentence structure and length
- Level of formality  
- Perspective (first person, questions, statements)
- Specific words and phrasing

Return exactly 10 utterances, one per line, without numbers or bullet points."""

        response = model.generate_content(prompt)
        
        if response and response.text:
            utterances = []
            
            for line in response.text.split('\n'):
                cleaned = line.strip()
                if cleaned and not cleaned.startswith(('-', '•', '*')):
                    # Remove any numbering at the start
                    if cleaned and len(cleaned) > 2 and cleaned[0].isdigit() and '.' in cleaned[:5]:
                        cleaned = cleaned.split('.', 1)[1].strip()
                    if cleaned:
                        utterances.append(cleaned)
            
            # Ensure we have exactly 10 utterances
            while len(utterances) < 10:
                utterances.append(f"Alternative way to say: {intention}")
            
            return utterances[:10]
        
        return None
        
    except Exception as e:
        print(f"Error generating utterances: {e}")
        return None


def save_to_csv(utterances, intention):
    """Save utterances to CSV with timestamp filename in separate folder."""
    try:
        # Create output directory with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"utterance_outputs_{datetime.now().strftime('%Y%m%d')}"
        
        # Create directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"📁 Created output directory: {output_dir}")
        
        # Create filename with full timestamp
        filename = f"utterances_{timestamp}.csv"
        filepath = os.path.join(output_dir, filename)
        
        # Prepare data for CSV
        csv_data = []
        for i, utterance in enumerate(utterances, 1):
            csv_data.append({
                'id': i,
                'utterance': utterance,
                'original_intention': intention
            })
        
        # Write to CSV
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'utterance', 'original_intention']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for row in csv_data:
                writer.writerow(row)
        
        print(f"Done! 10 utterances saved in {filepath} ✅")
        return filepath
        
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return None


def main():
    """Main function to run the utterance generator."""
    try:
        # Get user input
        intention = get_user_input()
        if not intention:
            return
        
        # Generate utterances
        utterances = generate_utterances_simple(intention)
        
        if not utterances:
            print("Failed to generate utterances. Please check your API key.")
            return
        
        # Display generated utterances
        print(f"\n📝 Generated utterances for '{intention}':")
        print("-" * 50)
        for i, utterance in enumerate(utterances, 1):
            print(f"{i:2d}. {utterance}")
        
        # Save to CSV
        save_to_csv(utterances, intention)
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()