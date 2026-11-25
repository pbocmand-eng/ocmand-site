"""Prepare a project photo for the site.

Usage:  python3 _source/add_photo.py <photo file> <number>
Writes project-NN.jpg (1600 px wide) and project-NN-800.jpg to the repository root, turned the right way up
and with all camera data removed (phone photos carry the GPS location of the job site).
Then add the project to the P list in build.py.
"""
import os, sys
from PIL import Image, ImageOps
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src,n=sys.argv[1],int(sys.argv[2])
im=ImageOps.exif_transpose(Image.open(src)).convert('RGB')
if im.width<1200: print(f'WARNING: only {im.width} px wide - it will look soft at full size; ask for the original if there is one.')
def save(w,name):
    w=min(w,im.width); h=round(im.height*w/im.width)
    out=Image.new('RGB',(w,h)); out.paste(im.resize((w,h),Image.LANCZOS))      # new image = no EXIF carried over
    out.save(os.path.join(ROOT,name),quality=82,optimize=True,progressive=True); return w,h
w,h=save(1600,f'project-{n:02d}.jpg'); save(800,f'project-{n:02d}-800.jpg')
print(f'wrote project-{n:02d}.jpg ({w}x{h}) and project-{n:02d}-800.jpg')
if (w,h)!=(1600,1200): print(f'Not 1600x1200 - add  {n}:({w},{h})  to DIM near the top of build.py so the page reserves the right space.')
