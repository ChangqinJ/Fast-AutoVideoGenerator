import os
from agents.camera_image_generator import CameraImageGenerator
from langchain.chat_models import init_chat_model
import asyncio
import json
from interfaces import Camera, ShotBriefDescription


camera_path = r"examples_for_test\camera_image_generator\input\0-套路\cameras_version_1.json"
shot_brief_description_path = r"examples_for_test\camera_image_generator\input\0-套路\shot_brief_descriptions_version_1.json"


chat_model = init_chat_model(
    api_key="sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB",
    base_url="https://yunwu.ai/v1",
    model="gpt-5-2025-08-07",
    model_provider="openai",
)

camera_image_generator = CameraImageGenerator(
    chat_model=chat_model,
    image_generator=None,
    video_generator=None,
)

with open(camera_path, "r", encoding="utf-8") as f:
    cameras = json.load(f)
    cameras = [Camera.model_validate(camera) for camera in cameras]

with open(shot_brief_description_path, "r", encoding="utf-8") as f:
    shot_brief_descriptions = json.load(f)
    shot_brief_descriptions = [ShotBriefDescription.model_validate(shot) for shot in shot_brief_descriptions]

cameras = asyncio.run(
    camera_image_generator.construct_camera_tree(cameras=cameras, shot_descs=shot_brief_descriptions)
)

save_path = r"examples_for_test\camera_image_generator\output\0-套路\camera_tree_version_1.json"
os.makedirs(os.path.dirname(save_path), exist_ok=True)
with open(save_path, "w", encoding="utf-8") as f:
    json.dump([camera.model_dump() for camera in cameras], f, ensure_ascii=False, indent=4)
