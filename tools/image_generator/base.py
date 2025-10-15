import base64
import os
import logging
import asyncio
from abc import abstractmethod
from typing import List, Literal, Optional, Union
from PIL import Image

from utils.image import download_image

from interfaces.image_output import ImageOutput


class BaseImageGenerator:

    async def generate_single_image(
        self,
        prompt: str,
        reference_image_paths: List[str] = [],
        size: Optional[str] = None,
    ) -> ImageOutput:
        """
        prompt: str
            The text prompt to generate the image.

        reference_image_paths: List[str]
            List of paths to reference images. If provided, the model will use these images as references for generation. If empty, the model will generate an image based solely on the text prompt.

        size: Optional[str]
            The desired size of the generated image. For example, 1280x720 (width x height).
        
        """
        pass

    async def generate_multiple_images_from_one_prompt(
        self,
        prompt: str,
        reference_image_paths: List[str],
        num_images: int,
        **kwargs,
    ) -> List[ImageOutput]:
        tasks = [
            self.generate_single_image(prompt, reference_image_paths, **kwargs)
            for _ in range(num_images)
        ]
        output_images = await asyncio.gather(*tasks)
        return output_images

    async def generate_multiple_images_from_multiple_prompts(
        self,
        prompts: List[List[str]],
        reference_image_paths: List[List[str]],
        num_images_per_prompt: int = 1,
        **kwargs,
    ) -> List[List[ImageOutput]]:
        tasks = [
            self.generate_multiple_images_from_one_prompt(
                prompt,
                ref_image,
                num_images=num_images_per_prompt,
                **kwargs
            )
            for prompt, ref_image in zip(prompts, reference_image_paths)
        ]
        output_images = await asyncio.gather(*tasks)
        return output_images
