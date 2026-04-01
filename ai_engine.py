#The brain: This module contains the core backend logic. it contains functions that interact with OpenAI's API to generate story content based on user input and story history. It handles 'Prompt Engineering' by constructing effective prompts that guide the AI to produce coherent and engaging story segments and 'Context Management' by maintaining the story history and using it to provide context for generating the next part of the story. This ensures that the AI's responses are consistent with the established narrative and characters (ie AI doesn't forget the story so far). The main function is generate_story which takes in the story history, selected genre, prompt type (start, continue, choices), user input, and temperature for creativity. It constructs a prompt based on these inputs and calls the OpenAI API to get the next part of the story or choices for branching paths.
import os
from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4o-mini"

def generate_story(history, genre, prompt_type = "continue", user_input="", temp=0.7):
    #constructing context from history list
    full_story = "\n".join([f"{h['role'].upper()}: {h['text']}" for h in history])

    system_instructions = {
        "start": f"Write a gripping 150-250 word opening for a {genre} story based on this hook: {user_input}", 
        "continue":f"Continue this {genre} story. Stay consistent with characters, tone, and plot.",
        "choices": f"Suggest 3 short, distinct branching paths (Option 1, 2, 3) for what happens next.",
        "end": f"Write a satisfying conclusion to this {genre} story."
        }

    if prompt_type == "start":
        messages = [{"role": "user", "content": system_instructions["start"]}]
    else:
        user_content = full_story
        if user_input:
            user_content += "\n\nUser Input = " + user_input
        messages = [
            {"role": "system", "content": system_instructions[prompt_type]},
            {"role": "user", "content": user_content}
        ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=temp
    )
    return response.choices[0].message.content.strip()