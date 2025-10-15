from application import genVideo

#only one shot! only ont shot! only one shot
script = """
一位漂亮性感的丰满紫发(亚洲)少妇在跳舞 (全身照)
"""

package = {'id':1,'task_uuid':"test002",'prompt':script,'width':1920,'height':1080,'output_path':"/home/changqin/movieAgentCache",'movie_agent_pack_id':1}
dbpool = None
if(genVideo(package=package,dbpool=dbpool)[1] == None):
    print("成功生成")
else:
    print("生成失败")