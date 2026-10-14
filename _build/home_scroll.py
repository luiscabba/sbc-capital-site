"""Ship the scroll redesign to the live Home (index.html):
How it works C2 (the stack builds while the section is locked), the card-only mark section (rises, turns over, locked),
and the closing band image wipe (locked). GSAP + ScrollTrigger are self-hosted in assets/vendor/.
It runs the prototype chain (proto_scroll -> proto_how_c -> proto_card) on the current index.html and writes the result back.
Run once, from the repo root, on a Home that has not had it yet (after home_stack, home_phone, home_gulf):
  python3 _build/home_scroll.py
"""
import shutil, subprocess
s = open('index.html', encoding='utf-8').read()
assert '<section class="sec" aria-label="How it works"' in s and 'class="sec mk"' not in s, 'index.html already has the scroll redesign'
subprocess.run(['python3', '_build/proto_card.py'], check=True)
shutil.copyfile('_build/proto/card.html', 'index.html')
print('index.html updated')
