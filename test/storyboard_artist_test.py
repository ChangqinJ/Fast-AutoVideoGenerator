import os
from agents import StoryboardArtist
from agents.character_extractor import CharacterExtractor
import asyncio
import json
from interfaces import CharacterInScene, ShotBriefDescription, ShotDescription, Camera
from langchain.chat_models import init_chat_model
from utils.timer import Timer

import logging
logging.basicConfig(level=logging.INFO)

version = "version_1"

script_path = r"examples_for_test\storyboard_artist\inputs\秦始皇穿越到现代_script.json"
script = json.load(open(script_path, "r", encoding="utf-8"))[0]
user_requirement = "搞笑短剧风格"

chat_model = init_chat_model(
    model="gemini-pro-latest",
    api_key="sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB",
    base_url=r"https://yunwu.ai/v1",
    model_provider="openai",
)

character_extractor = CharacterExtractor(
    chat_model=chat_model,
)

storyboard_artist = StoryboardArtist(
    chat_model=chat_model,
)

output_dir = r"examples_for_test\storyboard_artist\outputs\秦始皇穿越到现代"
os.makedirs(output_dir, exist_ok=True)

if os.path.exists(os.path.join(output_dir, "characters.json")):
    with open(os.path.join(output_dir, "characters.json"), "r", encoding="utf-8") as f:
        characters = json.load(f)
    characters = [CharacterInScene.model_validate(character) for character in characters]
else:
    characters = asyncio.run(character_extractor.extract_characters(script=script))
    with open(os.path.join(output_dir, "characters.json"), "w", encoding="utf-8") as f:
        json.dump([character.model_dump() for character in characters], f, ensure_ascii=False, indent=4)


storyboard = asyncio.run(
    storyboard_artist.design_storyboard(
        script=script,
        characters=characters,
        user_requirement=user_requirement,
    )
)
with open(os.path.join(output_dir, "storyboard.json"), "w", encoding="utf-8") as f:
    json.dump([shot.model_dump() for shot in storyboard], f, ensure_ascii=False, indent=4)
