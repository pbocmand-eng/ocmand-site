"""Build a click-through preview of the whole site, outside the repository, to publish as a Claude Artifact
so Preston can look through every page before anything goes live.

Usage:  python3 _source/make_preview.py [output folder]      (default: <temp>/ocmand-preview)

Then publish with the Artifact tool:  file_path = <folder>/index.html,  root = <folder>,
files = the JSON map this script prints. In the preview the forms and analytics are switched off.
"""
import os, sys, re, json, glob, shutil, subprocess, tempfile
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
out=os.path.abspath(sys.argv[1]) if len(sys.argv)>1 else os.path.join(tempfile.gettempdir(),'ocmand-preview')
if out.startswith(ROOT): raise SystemExit('Pick a folder outside the repository so the preview is never published.')
shutil.rmtree(out,ignore_errors=True); os.makedirs(out)
subprocess.run([sys.executable,os.path.join(HERE,'build.py')],env={**os.environ,'PREVIEW':'1','OUT':out},check=True)
for f in ('sitemap.xml','robots.txt','_redirects'):
    p=os.path.join(out,f)
    if os.path.exists(p): os.remove(p)
skip={'og.jpg','apple-touch-icon.png'}
for ext in ('css','js','woff2','jpg','png'):
    for f in glob.glob(os.path.join(ROOT,'*.'+ext)):
        if os.path.basename(f) not in skip: shutil.copy(f,out)
# the logo is one SVG file referenced from every page; inline it so the preview does not depend on a cross-file <use>
sprite=re.sub(r'<\?xml[^>]*\?>','',open(os.path.join(ROOT,'logo.svg')).read())
sprite=sprite.replace('<svg ','<svg style="position:absolute;width:0;height:0;overflow:hidden" aria-hidden="true" ',1)
for f in glob.glob(os.path.join(out,'*.html')):
    h=open(f).read().replace('href="logo.svg#','href="#').replace('<a class="skip"',sprite+'<a class="skip"',1)
    open(f,'w').write(h)
files={f:f for f in sorted(os.listdir(out)) if f!='index.html'}
print('preview folder:',out)
print('files map:',json.dumps(files))
