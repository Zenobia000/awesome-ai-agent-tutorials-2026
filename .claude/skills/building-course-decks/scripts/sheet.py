"""主控者審查用的緊湊總覽（4 欄）：uv run --with pillow python sheet.py <shots 目錄> <前綴> <輸出.png>"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
shots=Path(sys.argv[1]); prefix=sys.argv[2]; out=sys.argv[3]
fs=sorted(shots.glob(f"{prefix}*.png")); W,H,c=640,360,4
r=(len(fs)+c-1)//c; sh=Image.new("RGB",(c*W,r*(H+24)),"white")
for i,f in enumerate(fs):
    x,y=(i%c)*W,(i//c)*(H+24); sh.paste(Image.open(f).convert("RGB").resize((W-6,H-4)),(x,y+24)); ImageDraw.Draw(sh).text((x+6,y+6),f.stem,fill="black")
sh.save(out); print(out,len(fs))
