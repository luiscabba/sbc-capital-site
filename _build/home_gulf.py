"""Gulf photos on the live Home (index.html). Safe to re-run.
Swaps the three photos for the generated Gulf images:
  How it works   stone cubes -> container port at night   (trade coming in)
  The mark       stone slab  -> limestone civic building, one cobalt window   (the institution)
  Closing band   gateways    -> Gulf skyline at dawn   (where you are headed)
On phones the photos stay hidden (option A, see _build/home_phone.py).
Run from the repo root after _build/home_phone.py: python3 _build/home_gulf.py
"""
import re

s = open('index.html', encoding='utf-8').read()

PORT, CIVIC, SKY = '/assets/img/gulf/gulf-port-night.webp', '/assets/img/gulf/gulf-civic-dusk.webp', '/assets/img/gulf/gulf-skyline-dawn.webp'

s = re.sub(r'<img src="/assets/img/585baed4eca919820a1c25863c794e77.webp" alt="[^"]*" style="([^"]*?)object-position: 60% center;',
           r'<img src="%s" alt="A Gulf container port at night, cranes over a docked ship" style="\1object-position: 28%% center;' % PORT, s)
s = re.sub(r'<img src="/assets/img/4d27b8120b3c93094094b2023236d91c.webp" alt="[^"]*" style="([^"]*?)object-position: 82% 45%;',
           r'<img src="%s" alt="A limestone civic building at dusk, one window lit cobalt" style="\1object-position: 74%% center;' % CIVIC, s)
s = s.replace('src="/assets/img/c7357b0450070dc44d66d1c10bd82874.webp" alt="" loading="lazy" style="width:100%;height:100%;object-fit:cover;object-position:70% 50%;',
              'src="%s" alt="" loading="lazy" style="width:100%%;height:100%%;object-fit:cover;object-position:62%% 60%%;' % SKY)
assert s.count(PORT) == 2 and s.count(CIVIC) == 2 and s.count(SKY) == 2, (s.count(PORT), s.count(CIVIC), s.count(SKY))  # re-run safe: already swapped counts the same

open('index.html', 'w', encoding='utf-8').write(s)
print('ok')
