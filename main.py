import asyncio
import  logging
from main_thread import main_thread_cfg_init
from application import genVideo

try:
    mth = main_thread_cfg_init(
        genVideo,
        "movie_agent_config.json"
    )
    mth.run()
except Exception as e:
    logging.error(f"异常: {e}")