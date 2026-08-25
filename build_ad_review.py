#!/usr/bin/env python3
"""A client-facing review page for the TML ad creative.

Aaron's working folder holds ~86MB of PNGs and MP4s in seven sets. Handing that
to a client as a Dropbox folder means they scroll a file list; handing them this
means they see every ad at the size it will run, grouped by concept, and can
leave a verdict on each one.

What it does:
  * Copies the folder into site/ad-review/media/, re-encoding as it goes —
    images to WebP (long edge 1440, q82) and videos to H.264 at CRF 26 with a
    poster frame. 86MB of source lands around 25MB, which matters because the
    client is likely opening this on a phone.
  * Reads each file's real dimensions and labels it by placement: 1:1 feed,
    4:5 feed, 9:16 story/reel.
  * Writes the page. Approve / Request change / notes per asset, held in the
    browser's own storage, with a "Copy feedback" button that produces plain
    text they can paste into an email. No backend, nothing to sign into — the
    fewer steps between a client and their opinion, the more opinions you get.

Re-running is cheap: an asset is only re-encoded if the source is newer than
what is already there. When the last ads land, drop them in the folder and run
this again.

Usage:  python3 build_ad_review.py [source-folder]
"""
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "site" / "ad-review"
MEDIA = OUT / "media"
SRC = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else Path.home() / "Downloads" / "TML-Ads"

# Folder name -> what the client should see. Anything not listed falls back to a
# tidied version of the folder name, so new folders work without editing this.
SET_LABELS = {
    ".":                        ("Facebook Cover", "Video cover art for the page"),
    "creatives-1":              ("Concept 1 — Offer", "Coupon-led, all three placements"),
    "creatives-2":              ("Concept 2 — Coupon", "Discount-forward variants"),
    "creatives-3":              ("Concept 3 — Before & After", "Same home, new door"),
    "creatives-4":              ("Concept 4 — Trust", "Credential and guarantee led"),
    "creatives-5":              ("Concept 5 — Testimonials", "Real customer proof"),
    "social/campaign-1":        ("Social — Campaign 1", "Vertical social set"),
    "social/campaign-3-knowledge": ("Social — Campaign 3", "Education and knowledge angle"),
}
SET_ORDER = [".", "creatives-1", "creatives-2", "creatives-3", "creatives-4",
             "creatives-5", "social/campaign-1", "social/campaign-3-knowledge"]

MAX_EDGE = 1440
IMG_Q = 82
VID_CRF = 26


def slug(s):
    s = re.sub(r"\.[^.]+$", "", s)
    s = s.replace("×", "x").replace("’", "").replace("'", "")
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or "asset"


def placement(w, h):
    if not w or not h:
        return ""
    r = w / h
    if abs(r - 1) < .05:
        return "1:1 · Feed"
    if abs(r - 0.8) < .05:
        return "4:5 · Feed"
    if abs(r - 0.5625) < .04:
        return "9:16 · Story / Reel"
    if abs(r - 1.7778) < .05:
        return "16:9 · Landscape"
    return f"{w}×{h}"


def newer(src, dst):
    return not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime


def do_image(src, dst):
    from PIL import Image
    with Image.open(src) as im:
        w, h = im.size
        if newer(src, dst):
            im = im.convert("RGB") if im.mode in ("P", "RGBA", "LA") else im
            scale = min(1, MAX_EDGE / max(w, h))
            if scale < 1:
                im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
            im.save(dst, "WEBP", quality=IMG_Q, method=5)
    return w, h


def probe(src):
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
             "stream=width,height", "-of", "json", str(src)],
            capture_output=True, text=True, timeout=60).stdout
        s = json.loads(out)["streams"][0]
        return s["width"], s["height"]
    except Exception:
        return None, None


def do_video(src, dst, poster):
    w, h = probe(src)
    if newer(src, dst):
        scale = f"scale='min({MAX_EDGE},iw)':-2" if w and w > MAX_EDGE else "scale=trunc(iw/2)*2:trunc(ih/2)*2"
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-vf", scale,
             "-c:v", "libx264", "-crf", str(VID_CRF), "-preset", "medium",
             "-pix_fmt", "yuv420p", "-movflags", "+faststart",
             "-c:a", "aac", "-b:a", "128k", str(dst)], check=True, timeout=900)
    if newer(src, poster):
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-ss", "1", "-i", str(dst),
             "-frames:v", "1", "-q:v", "4", str(poster)], check=True, timeout=120)
    return w, h


def collect():
    sets = {}
    for p in sorted(SRC.rglob("*")):
        if not p.is_file() or p.name.startswith("."):
            continue
        if p.suffix.lower() not in (".png", ".jpg", ".jpeg", ".mp4", ".mov", ".webp"):
            continue
        rel = p.parent.relative_to(SRC).as_posix()
        sets.setdefault(rel, []).append(p)
    return sets


def main():
    if not SRC.exists():
        sys.exit(f"source folder not found: {SRC}")
    MEDIA.mkdir(parents=True, exist_ok=True)

    sets, cards, n_img, n_vid = collect(), {}, 0, 0
    for rel, files in sets.items():
        d = MEDIA / (slug(rel) if rel != "." else "cover")
        d.mkdir(parents=True, exist_ok=True)
        items = []
        for f in files:
            base = slug(f.name)
            if f.suffix.lower() in (".mp4", ".mov"):
                dst, poster = d / f"{base}.mp4", d / f"{base}.jpg"
                w, h = do_video(f, dst, poster)
                items.append({"type": "video", "src": f"media/{d.name}/{dst.name}",
                              "poster": f"media/{d.name}/{poster.name}",
                              "name": f.name, "w": w, "h": h,
                              "kb": round(dst.stat().st_size / 1024)})
                n_vid += 1
            else:
                dst = d / f"{base}.webp"
                w, h = do_image(f, dst)
                items.append({"type": "image", "src": f"media/{d.name}/{dst.name}",
                              "name": f.name, "w": w, "h": h,
                              "kb": round(dst.stat().st_size / 1024)})
                n_img += 1
            print(f"  {rel}/{f.name}  ->  {items[-1]['kb']}KB")
        cards[rel] = items

    order = [s for s in SET_ORDER if s in cards] + [s for s in cards if s not in SET_ORDER]
    OUT.joinpath("index.html").write_text(render(order, cards, n_img, n_vid), "utf-8")
    total = sum(i["kb"] for v in cards.values() for i in v)
    print(f"\n{n_img} images + {n_vid} videos across {len(cards)} sets — {total/1024:.1f}MB")
    print(f"page: {OUT/'index.html'}")


def render(order, cards, n_img, n_vid):
    from html import escape
    blocks, nav, idx = [], [], 0
    for rel in order:
        label, sub = SET_LABELS.get(rel, (rel.replace("-", " ").replace("/", " · ").title(), ""))
        anchor = slug(rel) if rel != "." else "cover"
        nav.append(f'<a href="#{anchor}">{escape(label)}</a>')
        tiles = []
        for it in cards[rel]:
            idx += 1
            aid = f"a{idx}"
            place = placement(it["w"], it["h"])
            ratio = f'{it["w"]}/{it["h"]}' if it["w"] and it["h"] else "1/1"
            if it["type"] == "video":
                media = (f'<video src="{it["src"]}" poster="{it["poster"]}" controls '
                         f'preload="none" playsinline style="aspect-ratio:{ratio}"></video>')
            else:
                media = (f'<button class="shot" data-full="{it["src"]}" '
                         f'aria-label="View {escape(it["name"])} full size">'
                         f'<img src="{it["src"]}" alt="{escape(it["name"])}" loading="lazy" '
                         f'decoding="async" style="aspect-ratio:{ratio}"></button>')
            tiles.append(f"""<figure class="card" data-id="{aid}">
 <div class="media">{media}</div>
 <figcaption>
  <div class="meta"><span class="place">{escape(place)}</span>
   <span class="size">{it["kb"]}KB</span></div>
  <div class="fname" title="{escape(it["name"])}">{escape(it["name"])}</div>
  <div class="verdict" role="group" aria-label="Verdict for {escape(it['name'])}">
   <button class="v ok" data-v="approved">Approve</button>
   <button class="v no" data-v="changes">Request change</button>
  </div>
  <textarea class="note" rows="2" placeholder="Notes (optional)"></textarea>
 </figcaption>
</figure>""")
        blocks.append(f'<section id="{anchor}"><h2>{escape(label)}</h2>'
                      f'<p class="sub">{escape(sub)} · {len(cards[rel])} asset'
                      f'{"s" if len(cards[rel])!=1 else ""}</p>'
                      f'<div class="grid">{"".join(tiles)}</div></section>')

    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Ad Creative Review — TML Garage Door Services</title>
<style>
*{{box-sizing:border-box}}
:root{{--ink:#1b1e19;--mute:#6d7563;--line:#e2e6d8;--bg:#f7f8f4;--card:#fff;
 --green:#587735;--red:#b3462f;--radius:14px}}
html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:var(--bg);color:var(--ink);
 font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif}}
header{{background:var(--card);border-bottom:1px solid var(--line);
 padding:26px 20px 0;position:sticky;top:0;z-index:20}}
.hwrap{{max-width:1280px;margin:0 auto}}
h1{{font-size:23px;margin:0 0 4px;letter-spacing:-.01em}}
.lede{{color:var(--mute);font-size:14.5px;margin:0 0 14px}}
nav{{display:flex;gap:6px;overflow-x:auto;padding-bottom:2px;scrollbar-width:thin}}
nav a{{flex:0 0 auto;font-size:13px;padding:8px 13px;border-radius:99px;color:var(--mute);
 text-decoration:none;border:1px solid var(--line);white-space:nowrap}}
nav a:hover{{color:var(--ink);border-color:var(--mute)}}
.bar{{display:flex;flex-wrap:wrap;gap:10px;align-items:center;padding:12px 0 14px;
 border-top:1px solid var(--line);margin-top:12px}}
.count{{font-size:13.5px;color:var(--mute);margin-right:auto}}
.count b{{color:var(--ink)}}
button.act{{font:inherit;font-size:13.5px;font-weight:600;padding:9px 15px;border-radius:9px;
 border:1px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer}}
button.act.primary{{background:var(--green);border-color:var(--green);color:#fff}}
button.act:hover{{border-color:var(--mute)}}
main{{max-width:1280px;margin:0 auto;padding:30px 20px 90px}}
section{{margin-bottom:46px;scroll-margin-top:190px}}
h2{{font-size:19px;margin:0 0 3px}}
.sub{{color:var(--mute);font-size:14px;margin:0 0 18px}}
.grid{{display:grid;gap:20px;grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}}
.card{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
 overflow:hidden;display:flex;flex-direction:column}}
.card[data-state=approved]{{border-color:var(--green);box-shadow:0 0 0 1px var(--green)}}
.card[data-state=changes]{{border-color:var(--red);box-shadow:0 0 0 1px var(--red)}}
.media{{background:#eceee6;display:grid;place-items:center}}
.media img,.media video{{display:block;width:100%;height:auto;object-fit:contain;
 max-height:70vh}}
.shot{{display:block;padding:0;border:0;background:none;cursor:zoom-in;width:100%}}
figcaption{{padding:13px 14px 15px;display:flex;flex-direction:column;gap:9px}}
.meta{{display:flex;justify-content:space-between;gap:8px;font-size:12.5px;color:var(--mute)}}
.place{{font-weight:600;color:var(--ink)}}
.fname{{font-size:12px;color:var(--mute);overflow:hidden;text-overflow:ellipsis;
 white-space:nowrap}}
.verdict{{display:flex;gap:7px}}
.v{{flex:1;font:inherit;font-size:13px;font-weight:600;padding:8px 6px;border-radius:8px;
 border:1px solid var(--line);background:var(--card);color:var(--mute);cursor:pointer}}
.v:hover{{border-color:var(--mute);color:var(--ink)}}
.v.ok[aria-pressed=true]{{background:var(--green);border-color:var(--green);color:#fff}}
.v.no[aria-pressed=true]{{background:var(--red);border-color:var(--red);color:#fff}}
.note{{font:inherit;font-size:13px;padding:8px 10px;border:1px solid var(--line);
 border-radius:8px;resize:vertical;background:#fcfdfb;color:var(--ink);width:100%}}
.note:focus{{outline:2px solid var(--green);outline-offset:1px}}
dialog{{border:0;padding:0;background:none;max-width:96vw;max-height:96vh}}
dialog::backdrop{{background:rgba(12,14,10,.88)}}
dialog img{{display:block;max-width:96vw;max-height:96vh;width:auto;height:auto;
 border-radius:8px}}
.close{{position:fixed;top:16px;right:18px;font:inherit;font-size:15px;padding:8px 14px;
 border-radius:8px;border:0;background:#fff;cursor:pointer}}
.toast{{position:fixed;left:50%;bottom:26px;transform:translateX(-50%) translateY(20px);
 background:var(--ink);color:#fff;padding:11px 18px;border-radius:10px;font-size:14px;
 opacity:0;transition:.2s;pointer-events:none;z-index:60}}
.toast.on{{opacity:1;transform:translateX(-50%)}}
@media(max-width:600px){{
 header{{padding:18px 15px 0;position:static}}
 main{{padding:22px 15px 70px}}
 .grid{{grid-template-columns:1fr;gap:16px}}
 h1{{font-size:20px}}
}}
@media(prefers-reduced-motion:reduce){{.toast{{transition:none}}}}
</style>
</head><body>
<header><div class="hwrap">
 <h1>Ad creative review — TML Garage Door Services</h1>
 <p class="lede">Every ad below is a draft. Mark each one Approve or Request change,
  add a note where it helps, then press Copy feedback and send it back.
  Your marks save in this browser, so you can stop and come back.</p>
 <nav>{"".join(nav)}</nav>
 <div class="bar">
  <div class="count"><b id="done">0</b> of <b>{n_img + n_vid}</b> reviewed
   · {n_img} images, {n_vid} videos · updated {date.today():%d %b %Y}</div>
  <button class="act" id="clear">Clear marks</button>
  <button class="act primary" id="copy">Copy feedback</button>
 </div>
</div></header>
<main>{"".join(blocks)}</main>
<dialog id="lb"><button class="close" id="lbx">Close</button><img alt=""></dialog>
<div class="toast" id="toast"></div>
<script>
(function(){{
 var KEY='tml-ad-review-v1';
 var state={{}};
 try{{state=JSON.parse(localStorage.getItem(KEY))||{{}}}}catch(e){{}}

 function save(){{try{{localStorage.setItem(KEY,JSON.stringify(state))}}catch(e){{}}}}
 function toast(m){{var t=document.getElementById('toast');t.textContent=m;
  t.classList.add('on');setTimeout(function(){{t.classList.remove('on')}},1900);}}
 function tally(){{
  var n=0;for(var k in state){{if(state[k]&&state[k].v)n++;}}
  document.getElementById('done').textContent=n;
 }}

 document.querySelectorAll('.card').forEach(function(card){{
  var id=card.dataset.id, s=state[id]||{{}};
  var note=card.querySelector('.note');
  if(s.v){{card.dataset.state=s.v;}}
  if(s.n){{note.value=s.n;}}
  card.querySelectorAll('.v').forEach(function(b){{
   b.setAttribute('aria-pressed', String(s.v===b.dataset.v));
   b.addEventListener('click',function(){{
    var cur=(state[id]||{{}}).v;
    var next=cur===b.dataset.v?null:b.dataset.v;
    state[id]=Object.assign({{}},state[id],{{v:next}});
    if(next){{card.dataset.state=next;}}else{{delete card.dataset.state;}}
    card.querySelectorAll('.v').forEach(function(x){{
     x.setAttribute('aria-pressed',String(next===x.dataset.v));}});
    save();tally();
   }});
  }});
  note.addEventListener('input',function(){{
   state[id]=Object.assign({{}},state[id],{{n:note.value}});save();
  }});
 }});
 tally();

 // full-size viewer
 var lb=document.getElementById('lb'), lbImg=lb.querySelector('img');
 document.querySelectorAll('.shot').forEach(function(b){{
  b.addEventListener('click',function(){{
   lbImg.src=b.dataset.full;lbImg.alt=b.querySelector('img').alt;lb.showModal();
  }});
 }});
 document.getElementById('lbx').addEventListener('click',function(){{lb.close()}});
 lb.addEventListener('click',function(e){{if(e.target===lb)lb.close()}});
 lb.addEventListener('close',function(){{lbImg.removeAttribute('src')}});

 document.getElementById('clear').addEventListener('click',function(){{
  if(!confirm('Clear every mark and note on this page?'))return;
  state={{}};save();
  document.querySelectorAll('.card').forEach(function(c){{
   delete c.dataset.state;c.querySelector('.note').value='';
   c.querySelectorAll('.v').forEach(function(x){{x.setAttribute('aria-pressed','false')}});
  }});
  tally();toast('Marks cleared');
 }});

 document.getElementById('copy').addEventListener('click',function(){{
  var out=['TML ad creative review — '+new Date().toLocaleDateString(),''];
  document.querySelectorAll('section').forEach(function(sec){{
   var lines=[];
   sec.querySelectorAll('.card').forEach(function(c){{
    var s=state[c.dataset.id]||{{}};
    if(!s.v&&!(s.n||'').trim())return;
    var mark=s.v==='approved'?'APPROVED':(s.v==='changes'?'NEEDS CHANGE':'note');
    var l='  ['+mark+'] '+c.querySelector('.fname').textContent;
    if((s.n||'').trim())l+='\\n      '+s.n.trim().replace(/\\n/g,'\\n      ');
    lines.push(l);
   }});
   if(lines.length){{out.push(sec.querySelector('h2').textContent);
    out.push(lines.join('\\n'));out.push('');}}
  }});
  if(out.length<3){{toast('Nothing marked yet');return;}}
  var txt=out.join('\\n');
  function fallback(){{
   var ta=document.createElement('textarea');ta.value=txt;document.body.appendChild(ta);
   ta.select();try{{document.execCommand('copy')}}catch(e){{}}ta.remove();
   toast('Feedback copied');
  }}
  if(navigator.clipboard&&navigator.clipboard.writeText){{
   navigator.clipboard.writeText(txt).then(function(){{toast('Feedback copied')}},fallback);
  }}else{{fallback();}}
 }});
}})();
</script>
</body></html>"""


if __name__ == "__main__":
    main()
