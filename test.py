from application import genVideo

#only one shot! only ont shot! only one shot
script = """
Ultra-realistic cinematic shot under heavy overcast sky, natural diffuse daylight, desaturated cold palette. 
Camera glides slowly forward near the ground through muddy ruins and fallen armor, toward a distant gothic fortress wall fading into fog. 
Smoke drifts, ash falls, subtle motion, oppressive silence, raw post-war atmosphere. 
No fantasy effects, only realism and weight. 
Film look: ARRI Alexa 65, 50mm lens, HDR tone, shallow depth, soft fog, subdued contrast.
"""

package = {'id':1,'task_uuid':"科幻/战锤1",'prompt':script,'width':1920,'height':1080,'output_path':"/home/changqin/movieAgentCache",'movie_agent_pack_id':2}
dbpool = None
if(genVideo(package=package,dbpool=dbpool)[1] == None):
    print("成功生成")
else:
    print("生成失败")