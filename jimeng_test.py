import asyncio
import os
from tools.video_generator.jimeng import JimengVideoGenerator

video_generator = JimengVideoGenerator(
    api_key="sk-LucGBvaJWURh7Cd6vmJJMNyCXI6wJqlmKhTHeH2HAWneZmk4",
)

prompt = """
Ultra‑realistic cinematic realism in HDR tone, ARRI Alexa 65 look, 50 mm lens. 
main character:
the man(Theo Kaal) stand in front of the camera who holds a long sword
Frame 1 – Establishing Shot
A vast battlefield stretches beneath a storm‑tinted dusk sky. The camera is positioned at mid‑height, centered on Theo Kaal standing solitary amid scorched earth and drifting ash. His right hand holds a long sword that emits a faint silver‑white glow, the tip angled precisely downward.
Faint gusts lift loose dust around his boots and tug gently at his tattered cloak. In the far distance, along the broken ridgeline, rows of enemy soldiers stand rigid and silent, their armor reflecting the dying light. Low thunder murmurs behind layers of cloud, and small embers swirl through the air.
Frame 2 – Preparation Shot
A tight close‑up focuses on Theo Kaal’s right arm and the sword’s hilt. His forearm muscles tighten; veins stand out slightly beneath the skin. The white radiance along the blade grows brighter, vibrating softly.
He exhales once, lowering his center of gravity. Behind him, the wind intensifies, bending his cloak outward. The distant enemy ranks remain motionless, some soldiers shifting their footing uneasily as the ground hums with restrained power.
Frame 3 – Sword Impact Shot
Theo Kaal steadies himself, shoulder locked, and presses the sword vertically downward with one deliberate motion. The camera captures the impact at ground level: the blade penetrates roughly 30 centimeters into dry earth.
Soil fragments and small stones leap upward, illuminated by streaks of white‑gold light. Within a split second, a ring‑shaped shockwave bursts outward—an expanding halo of dust and energy racing toward the horizon. The echo resounds like struck metal.
Frame 4 – Cracks and Flames Shot
Cracks split outward from the insertion point, spreading in intricate patterns across the entire plain. Each fissure glows from within, then erupts with molten gold‑red fire that surges along the ground.
The wave of flame advances toward the enemy line, leaving twisting heat distortion in its wake. As it reaches the foremost soldiers, their armor glows white, then their bodies crumble into glowing ash, scattering upward like dust caught in sunlight.
The flames roll and sway, 40 to 60 centimeters high, covering the earth like a moving sea of fire.
Frame 5 – Camera Pullback Shot
The camera begins a slow dolly‑out, drifting slightly to the right while maintaining Theo Kaal at the center of frame(back to camera). The battlefield now burns endlessly—a vast ocean of red and gold fire.
The enemy formation collapses completely; lines vanish in drifting gray smoke and settling ash. Heat distortion shimmers between the layers of flame. Theo Kaal stands motionless, cloak whipping upward with each burst of air.
For a brief moment, the whole scene glows under an amber light from the burning ground, and the only movement is the silent dance of the fire surrounding him.
"""
    
path_i = [r"科幻/战锤8-redo/images/first_frame.png",r".working_dir/科幻/战锤8-redo/shots/0/first_frame.png",r"科幻/战锤8-redo/images/"]

reference_image_paths = [
    path_i[2]
]

video = asyncio.run(
    video_generator.generate_single_video(
        prompt=prompt,
        image_paths=reference_image_paths,
    )
)
path_v = [r"科幻/战锤8-redo/",r".working_dir/科幻/战锤8-redo/"]
os.makedirs(path_v[0], exist_ok=True)
video.save(path_v[0]+"final_video_jm.mp4")