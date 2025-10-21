import logging
import requests
import json
from typing import Literal, List
from utils.images2url import images2url
import aiohttp
import asyncio
from tools.video_generator.base import VideoGeneratorOutput,BaseVideoGenerator
# NOT IMPLEMENTED

class JimengVideoGenerator(BaseVideoGenerator):
    def __init__(
        self,
        api_key: str,
        base_url: str = "http://yunwu.ai",
    ):
        self.api_key = api_key
        self.base_url = base_url

    async def generate_single_video(
        self,
        model_name: str = "jimeng-videos",
        prompt: str = "",
        image_paths: List[str] = [],
        duration: int = 5,
    )-> VideoGeneratorOutput:
        logging.info(f"Calling {model_name} to generate video")
        url = self.base_url
        picture_url = images2url(image_paths[0]).get_url()
        print(f"图片地址: {picture_url}")
        payload = {
            #"model_name": model_name,
            "image_url": picture_url,
            "prompt": prompt,
            "aspect_ratio": "9:16",
            "cfg_scale": 0.5,
            "duration": duration,
        }
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(self.base_url+"/jimeng/submit/videos",headers=headers,json=payload) as response:
                        response = await response.json()
                        task_id = response["data"]
            except Exception as e:
                logging.error(f"Error occurred while creating video generation task: {e}")
                logging.info("Retrying in 1 second...")
                await asyncio.sleep(1)
                continue
            break
        
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
            'Content-type': 'application/json',
        }
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.base_url}/jimeng/fetch/{task_id}", headers=headers) as response:
                        payload = await response.json()
                        status = payload["code"]
            except Exception as e:
                logging.error(f"Error occurred while querying video generation task: {e}")
                logging.info("Retrying in 1 second...")
                await asyncio.sleep(1)
                continue
            if status == "completed":
                logging.info(f"Video generation completed successfully")
                video_url = payload["video_url"]
                video = VideoGeneratorOutput(fmt="url", ext="mp4", data=video_url)
                return video
            elif status == "failed":
                logging.error(f"Video generation failed: \n{payload}")
                break
            else:
                logging.info(f"Video generation status: {status}, waiting 1 second...")
                await asyncio.sleep(1)
                continue
