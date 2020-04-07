from PIL import Image, ImageDraw
import glob
import re

frames = []
images = [i for i in glob.glob("/home/antonio/Repos/iono2/animations/*.png")]
images.sort(key=lambda var:[int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)]) 
for image in images:

    print(image,"\n")
    new_frame = Image.open(image)
    frames.append(new_frame)
    
frames[0].save('/home/antonio/Repos/iono2/tec.gif', format='GIF', append_images=frames[:], save_all=True, duration=500, Loop=2)