import os
import asyncio
import logging
from PIL import Image
from tools.video_generator.veo import VeoVideoGenerator
from tools.video_generator.wan import WanVideoGenerator
from tools.video_generator.doubao_seedance import DoubaoSeedanceVideoGenerator

logging.basicConfig(level=logging.INFO)


# save_prefix = "example_inputs/videos/veo_output"
# api_key = "sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB"
# video_generator = VeoVideoGenerator(
#     api_key=api_key,
# )



# save_prefix = "example_inputs/videos/wan_output"
# video_generator = WanVideoGenerator(
#     api_key="9caa641d699a4223b95b7bccebf597c4",
# )


save_prefix = "example_inputs/videos/doubao_output"
video_generator = DoubaoSeedanceVideoGenerator(
    api_key="sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB",
)


# prompt = "The transformation process from a seed to a big tree. Natural transition, high detail, vibrant colors."
prompt = "镜头切换。第一个镜头为一颗种子在土壤中萌发，慢慢长出嫩芽。第二个镜头为大树的树干逐渐长高，树枝伸展。自然过渡，高细节，色彩鲜艳。"
reference_image_paths = [
    r"example_inputs\images\nanobanana_output\seed.png",
    r"example_inputs\images\nanobanana_output\tree.png"
]


reference_image_paths = [
    r"example_inputs\images\nanobanana_output\seed.png",
    r"example_inputs\images\nanobanana_output\tree.png"
]

video = asyncio.run(
    video_generator.generate_single_video(
        prompt=prompt,
        reference_image_paths=reference_image_paths,
    )
)
# save_path = f"{save_prefix}/ff2v.mp4" if len(reference_image_paths) == 1 else f"{save_prefix}/flf2v.mp4"
# save_path = f"{save_prefix}/seed_to_tree_ff2v.mp4"
save_path = f"{save_prefix}/seed_to_tree_flf2v.mp4"
os.makedirs(save_prefix, exist_ok=True)
video.save(save_path)


import os
import asyncio
import logging
from PIL import Image
from tools.video_generator.veo import VeoVideoGenerator
from tools.video_generator.wan import WanVideoGenerator
from tools.video_generator.doubao_seedance import DoubaoSeedanceVideoGenerator

logging.basicConfig(level=logging.INFO)


save_prefix = "example_inputs/videos/veo_output"
api_key = "sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB"
# video_generator = VeoVideoGenerator(
#     api_key=api_key,
# )



# save_prefix = "example_inputs/videos/wan_output"
# video_generator = WanVideoGenerator(
#     api_key="9caa641d699a4223b95b7bccebf597c4",
# )


save_prefix = "example_inputs/videos/doubao_output"
video_generator = DoubaoSeedanceVideoGenerator(
    api_key="sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB",
)


# prompt = "The transformation process from a seed to a big tree. Natural transition, high detail, vibrant colors."
# prompt = "镜头切换。第一个镜头为一颗种子在土壤中萌发，慢慢长出嫩芽。第二个镜头为大树的树干逐渐长高，树枝伸展。自然过渡，高细节，色彩鲜艳。"
# reference_image_paths = [
#     r"example_inputs\images\nanobanana_output\seed.png",
#     r"example_inputs\images\nanobanana_output\tree.png"
# ]


# reference_image_paths = [
#     r"example_inputs\images\nanobanana_output\seed.png",
#     r"example_inputs\images\nanobanana_output\tree.png"
# ]


# prompt = "镜头切换。第一个镜头为中景镜头，拍摄站着的白色衣服男人与坐着的小女孩和黑色衣服男人的互动场景。第二个镜头为白色衣服男人的过肩视角，与坐着的黑色衣服男人互动，背景是便利店门口。自然过渡，高细节，色彩鲜艳。"
# prompt = "镜头切换。第一个镜头为中景镜头，拍摄站着的黑色衣服男人与坐着的小女孩和白色衣服男人的互动场景。第二个镜头为左侧白色衣服男人的特写镜头，拍摄白色衣服男人面对着镜头说话，背景是便利店门口的货架。自然过渡，高细节，色彩鲜艳。"

# reference_image_paths = [
#     r"example_inputs/images/便利店三人.png",
# ]


# prompt = "镜头自然过渡。第一个镜头为中景镜头，拍摄坐在沙发上的妈妈与趴在沙发后面的小女孩互动的场景。第二个镜头为妈妈的侧面视角，拍摄小女孩和背景中的房间布置。自然过渡，高细节，色彩鲜艳。"
# reference_image_paths = [
#     r"example_inputs\images\妈妈和女儿.png",
# ]


# prompt = "镜头切换。第一个镜头为中景镜头，拍摄站在门口的男人与右下角工位上的女人互动的场景。第二个镜头为女人的近景镜头，拍摄女人面对着镜头，背景是办公室内的其他工位。自然过渡，高细节，色彩鲜艳。"
# reference_image_paths = [
#     r"example_inputs/images/办公室.png",
# ]


# prompt = "两个镜头。第一个镜头为大远景镜头，拍摄一望无际的沙漠景象，画面中央是一名探险者，其身后留着长长的脚印。第二个镜头为中景镜头，拍摄探险者在沙漠中行走的场景，背景是连绵起伏的沙丘。自然过渡，高细节，色彩鲜艳。"

prompt = "两个镜头。第一个镜头为大远景镜头，拍摄一望无际的沙漠景象，画面中央是一名探险者，其身后留着长长的脚印。第二个镜头为特写镜头，拍摄探险者的侧脸，背景是连绵起伏的沙丘。自然过渡，高细节，色彩鲜艳。"
reference_image_paths = [
    r"example_inputs\images\沙漠.png",
]


video = asyncio.run(
    video_generator.generate_single_video(
        prompt=prompt,
        reference_image_paths=reference_image_paths,
    )
)
# save_path = f"{save_prefix}/ff2v.mp4" if len(reference_image_paths) == 1 else f"{save_prefix}/flf2v.mp4"
# save_path = f"{save_prefix}/seed_to_tree_ff2v.mp4"
# save_path = f"{save_prefix}/白色衣服男人_过肩镜头.mp4"
# save_path = f"{save_prefix}/黑色衣服男人_特写镜头.mp4"
# save_path = f"{save_prefix}/妈妈和女儿_侧面镜头.mp4"
# save_path = f"{save_prefix}/办公室_new_viewpoint_1.mp4"
save_path = f"{save_prefix}/沙漠_new_viewpoint_2.mp4"
os.makedirs(save_prefix, exist_ok=True)
video.save(save_path)
