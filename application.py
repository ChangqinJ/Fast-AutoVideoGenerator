from pipelines.script2video_pipeline import Script2VideoPipeline
from pipelines.idea2video_pipeline import Idea2VideoPipeline
from langchain.chat_models import init_chat_model
from tools.image_generator.doubao_seedream import DoubaoSeedreamImageGenerator
from tools.image_generator.gemini import GeminiImageGenerator
from tools.video_generator.veo import VeoVideoGenerator
from tools.video_generator.doubao_seedance import DoubaoSeedanceVideoGenerator
import shutil
import asyncio
import logging
import os
import cv2
def genVideo(package,dbpool):
    try:
        logging.basicConfig(level=logging.WARNING)
        prompt = package["prompt"]
        task_uuid = package["task_uuid"]
        width = package["width"]
        height = package["height"]
        id = package["id"]
        os.makedirs(f".working_dir/{task_uuid}", exist_ok=True)
        output_path = package["output_path"]+f"/{task_uuid}"
        os.makedirs(output_path, exist_ok=True)
        with open(f".working_dir/{task_uuid}/prompt.txt", "w", encoding="utf-8") as f:
            f.write(prompt)

        with open(f".working_dir/{task_uuid}/prompt.txt", "r", encoding="utf-8") as f:
            prompt_d = f.read()
        pack_id=package["movie_agent_pack_id"]
        try:
            Pipeline(pack_id=pack_id,prompt=prompt_d,task_uuid=task_uuid,output_path=output_path)
        except Exception as e:
            logging.error(f"发生异常: {e}")
            return (id, str(e))
        return (id,None)
    except Exception as e:
        logging.error(f"发生异常： {e}")
        return (id, str(e))


def Pipeline(pack_id,prompt,task_uuid,output_path):
    if(pack_id == 1):
        video_generator = VeoVideoGenerator(
            api_key="sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB",
        )
        reference_image_paths = [
            #r"images/first_frame.png"
        ]
        
        video = asyncio.run(
            video_generator.generate_single_video(
                prompt=prompt,
                reference_image_paths=reference_image_paths,
            )
        )
        os.makedirs(f".working_dir/{task_uuid}/", exist_ok=True)
        video.save(f".working_dir/{task_uuid}/final_video.mp4")
        cap = cv2.VideoCapture(f".working_dir/{task_uuid}/final_video.mp4")
        try:
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(f"{output_path}/0_first_frame.png",frame)
                print("☑️ 封面已保存")
            else:
                print(" 封面保存失败")
        except Exception as e:
            logging.error(f"发生异常： {e}")

        #cover_path = f".working_dir/{task_uuid}/first_frame.mp4"
        user_output_path = os.path.join(output_path,"final_video.mp4")
        shutil.copy2(f".working_dir/{task_uuid}/final_video.mp4",user_output_path)
        #shutil.copy2(cover_path,output_path)
        print(f"☑️ Copy created in project root: {user_output_path}")
    elif(pack_id >= 2):
        user_requirement = "真实电影风格，不要超过10句对话,一定要要保持人物一致性，只要1个scene,参考生成的图片,面向短剧用户,the number of shots should not over 5!the number of shots should not over 5!the number of shots should not over 5!"
        style = "真实电影风格"
        if(len(prompt) > 30):
            print("Using Script to video")
            chat_model = init_chat_model(
                model="claude-sonnet-4-5-20250929",  # claude-sonnet-4-5-20250929
                api_key="sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB",
                base_url=r"https://yunwu.ai/v1",
                model_provider="openai",
            )
            image_generator = DoubaoSeedreamImageGenerator(
                api_key="sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB",
            )
            video_generator = VeoVideoGenerator(
                api_key="sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB",
            )
            pipeline = Script2VideoPipeline(
                chat_model=chat_model,
                image_generator=image_generator,
                video_generator=video_generator,
                working_dir=f".working_dir/{task_uuid}",
            )
            asyncio.run(
                pipeline(
                    script=prompt,
                    user_requirement=user_requirement,
                    style=style,
                )
            )
            user_output_path = os.path.join(output_path,"final_video.mp4")
            cover_path = f".working_dir/{task_uuid}/shots/0/first_frame.png"
            shutil.copy2(f".working_dir/{task_uuid}/final_video.mp4",user_output_path)
            shutil.copy2(cover_path,output_path)
            print(f"☑️ Copy created in project root: {user_output_path}")
        else:
            print("Using Idea to video")
            chat_model = init_chat_model(
                model="claude-sonnet-4-5-20250929",
                api_key="sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB",
                base_url=r"https://yunwu.ai/v1",
                model_provider="openai",
            )


            image_generator = DoubaoSeedreamImageGenerator(
                api_key="sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB",
                # base_url="https://yunwu.ai",
                # api_version="v1beta",
                # model="gemini-2.5-flash-image-preview",
            )
            video_generator = VeoVideoGenerator(
                api_key="sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB",
            )
            pipeline = Idea2VideoPipeline(
                chat_model=chat_model,
                image_generator=image_generator,
                video_generator=video_generator,
                working_dir=f".working_dir/{task_uuid}",
            )
            asyncio.run(
                pipeline(idea=prompt, user_requirement=user_requirement, style=style)
            )

            user_output_path = os.path.join(output_path,"final_video.mp4")
            cover_path = f".working_dir/{task_uuid}/scene_0/shots/0/first_frame.png"
            shutil.copy2(f".working_dir/{task_uuid}/final_video.mp4",user_output_path)
            shutil.copy2(cover_path,output_path)
            print(f"☑️ Copy created in project root: {user_output_path}")
