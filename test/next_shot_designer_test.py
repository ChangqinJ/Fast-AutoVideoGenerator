import os
from agents.next_shot_designer import NextShotsDesigner
from agents.character_extractor import CharacterExtractor
import asyncio
import json
from components.character import CharacterInScene
from components.shot import ShotDescription

from utils.timer import Timer

import logging
logging.basicConfig(level=logging.INFO)

version = "version_1"

script_path = r"examples_for_test\next_shot_designer\input\0-套路.txt"
working_dir = r"examples_for_test\next_shot_designer\output\0-套路"

# script_path = r"examples_for_test\next_shot_designer\input\3-无间道.txt"
# working_dir = r"examples_for_test\next_shot_designer\output\3-无间道"

# script_path = r"examples_for_test\next_shot_designer\input\4-今天抽华子.txt"
# working_dir = r"examples_for_test\next_shot_designer\output\4-今天抽华子"


script = open(script_path, "r", encoding="utf-8").read()
os.makedirs(working_dir, exist_ok=True)


character_extractor = CharacterExtractor(
    api_key="sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB",
    base_url=r"https://yunwu.ai/v1",
    chat_model="gpt-5-2025-08-07",
)

next_shot_designer = NextShotsDesigner(
    api_key="sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB",
    base_url=r"https://yunwu.ai/v1",
    chat_model="gpt-5-2025-08-07",
)

if os.path.exists(os.path.join(working_dir, "characters.json")):
    with open(os.path.join(working_dir, "characters.json"), "r", encoding="utf-8") as f:
        characters = json.load(f)
    characters = [CharacterInScene.model_validate(character) for character in characters]
else:
    characters = asyncio.run(character_extractor(script=script))
    with open(os.path.join(working_dir, "characters.json"), "w", encoding="utf-8") as f:
        json.dump([character.model_dump() for character in characters], f, ensure_ascii=False, indent=4)

shot_descriptions = []
if os.path.exists(os.path.join(working_dir, f"shot_descriptions_{version}.json")):
    with open(os.path.join(working_dir, f"shot_descriptions_{version}.json"), "r", encoding="utf-8") as f:
        shot_descriptions = json.load(f)
    shot_descriptions = [ShotDescription.model_validate(shot) for shot in shot_descriptions]


while True:
    with Timer() as timer:
        next_shot_descs = asyncio.run(
            next_shot_designer.design_next_shots(
                script=script,
                characters=characters,
                previous_shot_descriptions=shot_descriptions,
                max_num_shots=5,
                design_retry_timeout=300,
                decompose_retry_timeout=300,
            )
        )
        shot_descriptions.extend(next_shot_descs)
        with open(os.path.join(working_dir, f"shot_descriptions_{version}.json"), "w", encoding="utf-8") as f:
            json.dump([shot.model_dump() for shot in shot_descriptions], f, ensure_ascii=False, indent=4)

    if shot_descriptions[-1].is_last:
        break





