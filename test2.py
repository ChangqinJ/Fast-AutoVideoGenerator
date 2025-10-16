from pipelines.script2video_pipeline import Script2VideoPipeline
from langchain.chat_models import init_chat_model
from tools.image_generator.doubao_seedream import DoubaoSeedreamImageGenerator
from tools.image_generator.gemini import GeminiImageGenerator
from tools.video_generator.veo import VeoVideoGenerator
from tools.video_generator.doubao_seedance import DoubaoSeedanceVideoGenerator
import asyncio

from pipelines.script2video_pipeline import Script2VideoPipeline
from langchain.chat_models import init_chat_model
from tools.image_generator.doubao_seedream import DoubaoSeedreamImageGenerator
from tools.image_generator.gemini import GeminiImageGenerator
from tools.video_generator.veo import VeoVideoGenerator
from tools.video_generator.doubao_seedance import DoubaoSeedanceVideoGenerator
import asyncio
import logging

#相机速度变化:[0-2]45度/秒,[3-3.5]360度/秒,[3.5-5.5]45度/秒,[5.5-6]360度/秒,[6-8]45度/秒,[8-8.5]360度/秒,[8.5-10]45度/秒,强调:整个过程镜头速度变化应该是:慢-很快-慢-很快-慢-很快-慢-很快
script = \
"""
only 1 shot!only 1 shot! only 1 shot!!!
Ultra-realistic cinematic shot 
The same lone soldier in damaged blue-and-gold armor walks carefully down a stone staircase into the dim interior of a gothic fortress, illuminated by fading overcast light from above. 
Camera follows from behind at shoulder level, steady and slow. 
Dust floats in the air, water drips down the walls, faint sparks glimmer in the darkness ahead. 
The soldier pauses briefly, looking into the dark corridor, fog swirling around his feet. 
HDR tone, photorealism, handheld realism, desaturated cold palette, subdued silence, cinematic weight.
"""
user_requirement = "真实电影风格，不要超过10句对话，面向短剧用户,一定要保持人物一致性,一定要保持人物一致性"

style = "真实电影风格"

working_dir = r".working_dir/科幻/战锤3"

chat_model = init_chat_model(
    model="claude-sonnet-4-5-20250929",  # claude-sonnet-4-5-20250929
    api_key="sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB",
    base_url=r"https://yunwu.ai/v1",
    model_provider="openai",
)


# image_generator = GeminiImageGenerator(
#     api_key="sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB",
#     base_url="https://yunwu.ai",
#     api_version="v1beta",
#     model="gemini-2.5-flash-image-preview",
# )

image_generator = DoubaoSeedreamImageGenerator(
    api_key="sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB",
)

# video_generator = VeoVideoGenerator(
#     api_key="sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB",
# )

video_generator = VeoVideoGenerator(
    api_key="sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB",
)

pipeline = Script2VideoPipeline(
    chat_model=chat_model,
    image_generator=image_generator,
    video_generator=video_generator,
    working_dir=working_dir,
)

asyncio.run(
    pipeline(
        script=script,
        user_requirement=user_requirement,
        style=style,
    )
)




