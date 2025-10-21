import logging
from typing import List, Optional
from PIL import Image
import asyncio
import aiohttp
import requests
from tools.video_generator.base import VideoGeneratorOutput, BaseVideoGenerator
from utils.image import image_path_to_b64
from utils.images2url import images2url

class SoraVideoGenerator(BaseVideoGenerator):
    def __init__(
        
        self,
        api_key: str,
        model: str = "sora-2",
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://yunwu.ai"
    async def generate_single_video(
        self, 
        prompt: str, 
        reference_image_paths: str,     
    )-> VideoGeneratorOutput:
        model = self.model
        logging.info(f"Calling {model} to generate video...")
        picture_url = images2url(LOCAL_FOLDER=reference_image_paths[0]).get_url()
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "images": [picture_url],
            "model": model,
            "orientation": "portrait",
            "prompt": prompt,
            "size": "large",
            "duration":15
        }
        # body = {
        #         "images": [
        #             "https://filesystem.site/cdn/20250612/VfgB5ubjInVt8sG6rzMppxnu7gEfde.png",
        #             "https://filesystem.site/cdn/20250612/998IGmUiM2koBGZM3UnZeImbPBNIUL.png"
        #         ],
        #         "model": "sora-2",
        #         "orientation": "portrait",
        #         "prompt": "make animate",
        #         "size": "large",
        #         "duration":10
        # }
        
        url = f"https://yunwu.ai/v1/video/create"
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(url,headers=headers,json=payload) as response:
                        response = await response.json()
                        task_id = response["id"]
                        print(f"图片地址:{picture_url}")
            except Exception as e:
                logging.error(f"Error occurred while creating video generation task--: {e}")
                logging.info("Retrying in 1 second...")
                await asyncio.sleep(1)
                continue
            break

        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
            'Content-type': 'application/json'
        }
        url = f"https://yunwu.ai/volc//v1/video/query?id={task_id}"
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.base_url}/v1/video/query?id={task_id}",headers=headers) as response:
                        payload = await response.json()
                        status = payload["status"]
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


        