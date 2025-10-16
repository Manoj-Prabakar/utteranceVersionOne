#!/usr/bin/env python3
"""
Utterance Intention Generator using Google ADK and Gemini Flash LLM
Simple script to generate diverse utterances for a given intention.
"""

import csv
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService


def setup_authentication():
    """Set up Google Cloud authentication for ADK."""
    print("🔐 Setting up authentication...")
    
    # Method 1: Check for API key (most common for this project)
    api_key = os.getenv('GOOGLE_API_KEY')
    if api_key:
        print(" Using Google API key from environment")
        return True
    
    # Method 2: Check for service account key file
    service_account_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if service_account_path and os.path.exists(service_account_path):
        print(f" Using service account: {service_account_path}")
        return True
    
    # Method 3: Check for gcloud auth
    try:
        import subprocess
        result = subprocess.run(['gcloud', 'auth', 'list', '--format=value(account)'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and result.stdout.strip():
            print(" Using gcloud authentication")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # Method 4: Check environment variables
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT') or os.getenv('GCP_PROJECT')
    if project_id:
        print(f" Using project: {project_id}")
        return True
    print("No valid Google authentication found!")
    
    return False


def get_user_input():
    """Get user input for the intention/context."""
    print("Hello! 👋 Welcome to the Utterance Generator.")
    intention = input("Please enter an intention: ").strip()
    
    if not intention:
        print("No intention provided. Exiting.")
        return None
    
    return intention


def create_agent() -> LlmAgent:
    """Create the ADK LLM agent for utterance generation using standard authentication."""
    return LlmAgent(
        model="gemini-2.5-flash",
        name="Utterance_Generator",
        instruction="""
        **Role:** You are an expert utterance generator. 
        Your responsibility is to generate diverse, natural utterances for given intentions or contexts.
        
        **Core Directives:**
        * Generate exactly 10 diverse utterances for the given intention
        * Make each utterance unique in structure, tone, and wording
        * Vary sentence length, formality, and perspective
        * Keep utterances natural and conversational
        * Focus on different ways people might express the same intent
        * Return only the utterances, one per line, without numbering or formatting
        """,
    )


def create_agent_with_api_key(api_key: str = None) -> LlmAgent:
    """Create the ADK LLM agent with direct API key (alternative method)."""
    if not api_key:
        api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        raise ValueError("API key not provided. Set GOOGLE_API_KEY environment variable or pass api_key parameter.")
    
    # Configure with API key
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    
    return LlmAgent(
        model="gemini-2.5-flash",
        name="Utterance_Generator",
        instruction="""
        **Role:** You are an expert utterance generator. 
        Your responsibility is to generate diverse, natural utterances for given intentions or contexts.
        
        **Core Directives:**
        * Generate exactly 10 diverse utterances for the given intention
        * Make each utterance unique in structure, tone, and wording
        * Vary sentence length, formality, and perspective
        * Keep utterances natural and conversational
        * Focus on different ways people might express the same intent
        * Return only the utterances, one per line, without numbering or formatting
        """,
    )


async def generate_utterances_direct_api(intention: str):
    """Generate utterances using Google Generative AI directly (fallback method)."""
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""Generate 10 diverse utterances for this intention: "{intention}"

Make each utterance unique and natural. Vary the:
- Sentence structure and length
- Level of formality
- Perspective (first person, questions, statements)
- Specific words and phrasing

Return exactly 10 utterances, one per line, without numbers or bullet points."""

        print("Using direct Generative AI API...")
        response = model.generate_content(prompt)
        
        if response and response.text:
            utterances = []
            
            for line in response.text.split('\n'):
                cleaned = line.strip()
                if cleaned and not cleaned.startswith(('-', '•', '*', '1.', '2.')):
                    # Remove any numbering at the start
                    if cleaned and cleaned[0].isdigit() and '.' in cleaned[:5]:
                        cleaned = cleaned.split('.', 1)[1].strip()
                    if cleaned:
                        utterances.append(cleaned)
            
            # Ensure we have exactly 10 utterances
            while len(utterances) < 10:
                utterances.append(f"Alternative expression: {intention}")
            
            return utterances[:10]
        
        return None
        
    except Exception as e:
        print(f"Error with direct API: {e}")
        return None


async def generate_utterances(agent: LlmAgent, intention: str):
    """Generate utterances using the ADK agent."""
    try:
        print("Generating utterances using Gemini Flash...")
        
        # Create runner for the agent
        runner = Runner(
            app_name=agent.name,
            agent=agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )
        
        # Create prompt for utterance generation
        prompt = f"""Generate 10 diverse utterances for this intention: "{intention}"
        
Make each utterance unique and natural. Vary the:
- Sentence structure and length
- Level of formality
- Perspective (first person, questions, statements)
- Specific words and phrasing

Return exactly 10 utterances, one per line, without numbers or bullet points."""
        
        # Create session and run agent
        session_id = "utterance_session"
        user_id = "utterance_user"
        
        # Create session
        session = await runner.session_service.create_session(
            app_name=runner.app_name,
            user_id=user_id,
            session_id=session_id
        )
        
        # Create message content
        from google.genai import types
        message_content = types.Content(
            role="user",
            parts=[types.Part(text=prompt)]
        )
        
        # Run the agent and collect response
        response_text = ""
        async for event in runner.run_async(
            session_id=session_id,
            user_id=user_id,
            new_message=message_content
        ):
            if hasattr(event, 'response') and event.response:
                if hasattr(event.response, 'candidates') and event.response.candidates:
                    for candidate in event.response.candidates:
                        if hasattr(candidate, 'content') and candidate.content:
                            for part in candidate.content.parts:
                                if hasattr(part, 'text'):
                                    response_text += part.text
            elif hasattr(event, 'text'):
                response_text += event.text
        
        # Parse the response to get utterances
        if response_text.strip():
            utterances = []
            
            for line in response_text.split('\n'):
                cleaned = line.strip()
                if cleaned and not cleaned.startswith(('-', '•', '*', '1.', '2.')):
                    # Remove any numbering at the start
                    if cleaned and cleaned[0].isdigit() and '.' in cleaned[:5]:
                        cleaned = cleaned.split('.', 1)[1].strip()
                    if cleaned:
                        utterances.append(cleaned)
            
            # Ensure we have exactly 10 utterances
            while len(utterances) < 10:
                utterances.append(f"Alternative expression: {intention}")
            
            return utterances[:10]
        
        return None
        
    except Exception as e:
        print(f"Error generating utterances: {e}")
        import traceback
        traceback.print_exc()
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
        
        print(f"Done! 10 utterances saved in {filepath} ")
        return filepath
        
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return None


async def main():
    """Main function to run the utterance generator."""
    try:
        # Setup authentication
        if not setup_authentication():
            print("\n💡 Tip: You can also use direct API key by setting GOOGLE_API_KEY environment variable")
            use_api_key = input("\nDo you have a Google API key to use instead? (y/n): ").lower().strip()
            if use_api_key == 'y':
                api_key = input("Enter your Google API key: ").strip()
                if api_key:
                    os.environ['GOOGLE_API_KEY'] = api_key
                else:
                    print("No API key provided. Exiting.")
                    return
            else:
                print("Please set up authentication and try again.")
                return
        
        # Get user input
        intention = get_user_input()
        if not intention:
            return
        
        # Create ADK agent (try API key method if standard auth failed)
        try:
            agent = create_agent()
        except Exception as e:
            print(f"Standard authentication failed: {e}")
            print("Trying with API key...")
            agent = create_agent_with_api_key()
        
        # Generate utterances using ADK
        utterances = await generate_utterances(agent, intention)
        
        # If ADK method fails, try direct API method
        if not utterances:
            print("ADK method failed, trying direct API...")
            utterances = await generate_utterances_direct_api(intention)
        
        if not utterances:
            print("Failed to generate utterances. Please try again.")
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
    asyncio.run(main())