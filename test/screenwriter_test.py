from agents.screenwriter import Screenwriter
from langchain.chat_models import init_chat_model
import asyncio
import json
import os

chat_model = init_chat_model(
    model="gemini-pro-latest",
    api_key="sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB",
    base_url=r"https://yunwu.ai/v1",
    model_provider="openai",
)

screenwriter = Screenwriter(
    chat_model=chat_model,
)

user_input = json.load(open(r"examples_for_test\screenwriter\inputs\秦始皇穿越到现代.json", "r", encoding="utf-8"))

if os.path.exists(r"examples_for_test\screenwriter\outputs\秦始皇穿越到现代_story.txt"):
    story = open(r"examples_for_test\screenwriter\outputs\秦始皇穿越到现代_story.txt", "r", encoding="utf-8").read()
else:
    story = asyncio.run(screenwriter.develop_story(idea=user_input["idea"], user_requirement=user_input["story_requirement"]))
    with open(r"examples_for_test\screenwriter\outputs\秦始皇穿越到现代_story.txt", "w", encoding="utf-8") as f:
        f.write(story)

if os.path.exists(r"examples_for_test\screenwriter\outputs\秦始皇穿越到现代_script.json"):
    script = json.load(open(r"examples_for_test\screenwriter\outputs\秦始皇穿越到现代_script.json", "r", encoding="utf-8"))
else:
    script = asyncio.run(screenwriter.write_script_based_on_story(story=story, user_requirement=user_input["script_requirement"]))
    with open(r"examples_for_test\screenwriter\outputs\秦始皇穿越到现代_script.json", "w", encoding="utf-8") as f:
        json.dump(script, f, ensure_ascii=False, indent=4)