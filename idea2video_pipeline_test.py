from pipelines.idea2video_pipeline import Idea2VideoPipeline
from langchain.chat_models import init_chat_model
from tools.image_generator.doubao_seedream import DoubaoSeedreamImageGenerator
from tools.image_generator.gemini import GeminiImageGenerator
from tools.video_generator.veo import VeoVideoGenerator
import asyncio




idea = "有一个很常见的电信骗术，具体是：你好，我是秦始皇，其实我并没有死，我在西安有100吨黄金，我现在需要2000元人民币解冻我在西安的黄金，你微信，支付宝转给我都可以。账号就是我的手机号码！转过来后，我明天直接带部队复活，让你统领三军！简化就是：我，秦始皇，打钱！\n根据这个创意，生成一个短剧故事，故事中秦始皇真的穿越到现代，并且真的用上面的话术和别人交流，发生了一些有趣的故事。"
user_requirement = "搞笑短剧风格，只要一个场景就行，总共不要超过10句对话，面向短剧用户"
style = "真实电影风格"
working_dir = r".working_dir/我是秦始皇_v50"


# idea = "如果有一天，你发现你是一个机器人，你会怎么办？"
# user_requirement = "科幻小说风格，一个场景就行，总共不要超过10句对话，不要超过15个镜头，面向短剧用户"
# style = "真实电影风格"
# working_dir = r".working_dir/我是机器人"


chat_model = init_chat_model(
    model="gemini-pro-latest",
    api_key="sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB",
    base_url=r"https://yunwu.ai/v1",
    model_provider="openai",
)


image_generator = GeminiImageGenerator(
    api_key="sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB",
    base_url="https://yunwu.ai",
    api_version="v1beta",
    model="gemini-2.5-flash-image-preview",
)

# image_generator = DoubaoSeedreamImageGenerator(
#     api_key="sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB",
# )

video_generator = VeoVideoGenerator(
    api_key="sk-RsgJVQohu9e1HBMgdYsy9mQFKs3ue4fZXL2iGMjiiupiViQB",
)

pipeline = Idea2ScriptPipeline(
    chat_model=chat_model,
    image_generator=image_generator,
    video_generator=video_generator,
    working_dir=working_dir,
)

asyncio.run(
    pipeline(idea=idea, user_requirement=user_requirement, style=style)
)
