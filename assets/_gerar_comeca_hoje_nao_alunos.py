#!/usr/bin/env python3
# Arte "COMEÇA HOJE!" da live dos NÃO ALUNOS (ter 10/11/2026) — header do template do disparo É HOJE.
# Pedido do Fábio 10/11: trocar a foto dos fones (era da live dos alunos, com Play Passei na oferta) pela foto de braços
# cruzados com a camisa "10/11" (recorte PNG que ele mandou → assets/fabio-1011-bracos.png).
# Layout = o da arte dos alunos (comeca-hoje-alunos.jpg): logo + "COMEÇA HOJE!" à esquerda, Fábio à direita,
# faixa escura embaixo com filetes e "10 DE NOVEMBRO · 20H BRASÍLIA / AO VIVO E GRATUITO".
# Uso: python3 _gerar_comeca_hoje_nao_alunos.py  →  comeca-hoje-nao-alunos.jpg (1080×1080)
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
AQUI = os.path.dirname(os.path.abspath(__file__))
FOTO = os.path.join(AQUI, "fabio-1011-bracos.png")
LOGO = os.path.join(AQUI, "logo-black-revolucao.png")
BG = os.path.join(AQUI, "hero-bg.jpg")
FONTE = os.path.join(AQUI, "fonts", "figtree-latin.woff2")
OUT = os.path.join(AQUI, "comeca-hoje-nao-alunos.jpg")
W = 1080

def fonte(peso, tam):
    f = ImageFont.truetype(FONTE, tam); f.set_variation_by_name(peso); return f

def texto(d, x, y_caps, s, f, track, cor):
    asc = f.getbbox("H")[1]
    for ch in s:
        d.text((x, y_caps - asc), ch, font=f, fill=cor)
        x += f.getlength(ch) + track
    return x

# 1) fundo: base quase preta + textura metálica do site bem escura + brilho azul atrás do Fábio
img = Image.new("RGB", (W, W), (4, 7, 10))
bg = Image.open(BG).convert("RGB")
s = W / bg.height
bg = bg.resize((round(bg.width * s), W)).crop((0, 0, W, W))
bg = ImageEnhance.Brightness(bg).enhance(0.35)
img = Image.blend(img, bg, 0.75)
glow = Image.new("L", (W, W), 0)
ImageDraw.Draw(glow).ellipse((380, 20, 1180, 820), fill=150)
glow = glow.filter(ImageFilter.GaussianBlur(170))
img = Image.composite(Image.new("RGB", (W, W), (18, 120, 140)), img, glow)

# 2) Fábio à direita (recorte com transparência), cabeça perto do topo, cortado embaixo
foto = Image.open(FOTO).convert("RGBA")
sc = 0.54
foto = foto.resize((round(foto.width * sc), round(foto.height * sc)), Image.LANCZOS)
img.paste(foto, (W - foto.width, 34), foto)

# 3) escurece a esquerda (leitura do texto) e o pé da arte (faixa do rodapé)
d = ImageDraw.Draw(img)
esq = Image.new("L", (W, W), 0)
de = ImageDraw.Draw(esq)
for x in range(0, 560):
    de.line([(x, 0), (x, W)], fill=round(150 * (1 - x / 560) ** 1.4))
img = Image.composite(Image.new("RGB", (W, W), (2, 4, 6)), img, esq)
pe = Image.new("L", (W, W), 0)
dp = ImageDraw.Draw(pe)
for y in range(780, W):
    dp.line([(0, y), (W, y)], fill=min(250, round(250 * ((y - 780) / 170) ** 1.2)))
img = Image.composite(Image.new("RGB", (W, W), (1, 2, 3)), img, pe)

# 4) filetes horizontais do rodapé (iguais aos da arte dos alunos)
d = ImageDraw.Draw(img, "RGBA")
for y in (851, 882, 913):
    d.line([(0, y), (W, y)], fill=(120, 170, 185, 38), width=1)

# 5) logo + COMEÇA HOJE! (com sombra suave)
logo = Image.open(LOGO).convert("RGBA")
lw = 290
logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
img.paste(logo, (82, 300), logo)

camada = Image.new("RGBA", (W, W), (0, 0, 0, 0))
dc = ImageDraw.Draw(camada)
texto(dc, 88, 556, "COMEÇA", fonte(b"Regular", 98), 0, (255, 255, 255, 255))
texto(dc, 84, 680, "HOJE!", fonte(b"Bold", 140), -2, (255, 255, 255, 255))
sombra = camada.split()[3].filter(ImageFilter.GaussianBlur(14))
img = Image.composite(Image.new("RGB", (W, W), (0, 0, 0)), img, sombra.point(lambda v: round(v * 0.55)))
img.paste(camada, (0, 0), camada)

# 6) rodapé
d = ImageDraw.Draw(img)
texto(d, 92, 929, "10 DE NOVEMBRO · 20H BRASÍLIA", fonte(b"Bold", 29), 6.2, (255, 255, 255))
texto(d, 93, 969, "AO VIVO E GRATUITO", fonte(b"Regular", 29), 7.4, (255, 255, 255))
img.save(OUT, quality=92)
print(OUT)
