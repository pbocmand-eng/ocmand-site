"""Generates the Ocmand logo files from the real mark's measurements (stepped "OCC" in bold Times).
The logo is final - run this only if Preston asks for a logo change.
Needs fontTools and the Liberation Serif fonts (a metric match for Times New Roman).
Writes logo.svg and favicon.svg to the repository root and the brand files to _source/logo/brand/.
Then run:  node _source/logo/png.js   to refresh apple-touch-icon.png and the brand PNGs.
"""
import os, re
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(os.path.dirname(HERE)); BRAND=os.path.join(HERE,'brand')
def trim(s): return re.sub(r'(-?\d+\.\d)\d+',r'\1',s)   # one decimal place keeps the files small
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
B=TTFont('/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf')
R=TTFont('/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf')
def glyph(font,ch,scale,x,y):
    gs=font.getGlyphSet(); name=font.getBestCmap()[ord(ch)]
    pen=SVGPathPen(gs); tp=TransformPen(pen,(scale,0,0,-scale,x,y)); gs[name].draw(tp)
    return pen.getCommands(), gs[name].width*scale
def bounds(font,ch):
    gs=font.getGlyphSet(); name=font.getBestCmap()[ord(ch)]; bp=BoundsPen(gs); gs[name].draw(bp); return bp.bounds
def text(font,s,size,x,y,track=0):
    sc=size/font['head'].unitsPerEm; d=[]; cx=x
    for ch in s:
        if ch==' ': cx+=font.getGlyphSet()['space'].width*sc+track; continue
        p,w=glyph(font,ch,sc,cx,y); d.append(p); cx+=w+track
    return ' '.join(d), cx-track-x
# --- stepped mark: cap height H, step dx=.80H dy=.92H (measured from the real logo)
def mark(H,x0,y0):
    sc=H/ (bounds(B,'O')[3]-bounds(B,'O')[1]); d=[]
    for i,ch in enumerate('OCC'):
        b=bounds(B,ch); x=x0+i*0.80*H - b[0]*sc; y=y0+i*0.92*H + b[3]*sc
        d.append(glyph(B,ch,sc,x,y)[0])
    wlast=(bounds(B,'C')[2]-bounds(B,'C')[0])*sc
    return ' '.join(d), 2*0.80*H+wlast, 2*0.92*H+H
H=100
md,mw,mh=mark(H,0,0)
# horizontal lockup: mark + two text lines
tx=mw+34
l1,w1=text(B,'OCMAND CONSTRUCTION CO., LLC',92,tx,158,track=2)
# fit line 2 to line-1 width with tracking
s2='GENERAL CONTRACTOR'; base,_w=text(R,s2,50,0,0,0)
tr=(w1*0.62-_w)/(len(s2)-1)
l2,w2=text(R,s2,50,tx+2,232,track=tr)
LW=tx+w1
# stacked lockup (apparel): mark centered over text
sl1,sw1=text(B,'OCMAND CONSTRUCTION CO., LLC',46,0,0,track=1.2)
SW=max(sw1,mw)+0
smd,_,_=mark(H,(SW-mw)/2,0)
sl1,_=text(B,'OCMAND CONSTRUCTION CO., LLC',46,(SW-sw1)/2,mh+70,track=1.2)
b2,bw=text(R,s2,28,0,0,0); tr2=(sw1*0.72-bw)/(len(s2)-1)
sl2,sw2=text(R,s2,28,0,0,track=tr2)
sl2,_=text(R,s2,28,(SW-sw2)/2,mh+116,track=tr2)
SH=mh+126
sprite=f'''<svg xmlns="http://www.w3.org/2000/svg">
<symbol id="mark" viewBox="0 0 {mw:.1f} {mh:.1f}"><path d="{md}"/></symbol>
<symbol id="lockup" viewBox="0 0 {LW:.1f} {mh:.1f}"><path d="{md}"/><path d="{l1}"/><path d="{l2}"/></symbol>
<symbol id="stacked" viewBox="0 0 {SW:.1f} {SH:.1f}"><path d="{smd}"/><path d="{sl1}"/><path d="{sl2}"/></symbol>
</svg>'''
open(os.path.join(ROOT,'logo.svg'),'w').write(trim(sprite))
NAVY='#0c2148'
def standalone(vb,paths,fill,bg=None,pad=0):
    x,y,w,h=vb
    r=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}">{r}<g fill="{fill}">'+''.join(f'<path d="{p}"/>' for p in paths)+'</g></svg>'
p=60
open(os.path.join(BRAND,'brand-stacked-navy.svg'),'w').write(standalone((-p,-p,SW+2*p,SH+2*p),[smd,sl1,sl2],NAVY))
open(os.path.join(BRAND,'brand-stacked-white-on-navy.svg'),'w').write(standalone((-p,-p,SW+2*p,SH+2*p),[smd,sl1,sl2],'#fff',NAVY))
open(os.path.join(BRAND,'brand-horizontal-navy.svg'),'w').write(standalone((-30,-30,LW+60,mh+60),[md,l1,l2],NAVY))
# favicon: mark white on navy square
S=max(mw,mh)+90
open(os.path.join(ROOT,'favicon.svg'),'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S:.0f} {S:.0f}"><rect width="{S:.0f}" height="{S:.0f}" fill="{NAVY}"/><g fill="#fff" transform="translate({(S-mw)/2:.1f} {(S-mh)/2:.1f})"><path d="{md}"/></g></svg>')
# square social/GBP logo
Q=SW+240
open(os.path.join(BRAND,'brand-square-white-on-navy.svg'),'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Q:.0f} {Q:.0f}"><rect width="{Q:.0f}" height="{Q:.0f}" fill="{NAVY}"/><g fill="#fff" transform="translate(120 {(Q-SH)/2:.1f})"><path d="{smd}"/><path d="{sl1}"/><path d="{sl2}"/></g></svg>')
print('mark',mw,mh,'lockup',LW,'stacked',SW,SH)
