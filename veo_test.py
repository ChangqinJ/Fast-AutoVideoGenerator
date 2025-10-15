from tools.video_generator.veo import VeoVideoGenerator
import asyncio
import os

video_generator = VeoVideoGenerator(
    api_key="sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB",
)


prompt = "美女跳舞镜头"

# reference_image_paths是参考图片的路径列表
# 0 张图片时，使用text to video (t2v)模型
# 1 张图片时，使用first frame to video (ff2v)模型
# 2 张图片时，使用first and last frame to video (flf2v)模型

reference_image_paths = [
    #r"images/first_frame.png"
]

video = asyncio.run(
    video_generator.generate_single_video(
        prompt=prompt,
        reference_image_paths=reference_image_paths,
    )
)
os.makedirs("examples_for_test/video_generator/output/veo", exist_ok=True)
video.save("examples_for_test/video_generator/output/veo/no_frame_to_video.mp4")
