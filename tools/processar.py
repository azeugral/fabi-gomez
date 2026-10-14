"""Gera as imagens do site a partir de ../_ref/ig (fotos do Instagram dela, 14/10/2026).
- logo FG (monograma + anel) recortado da foto 097 e convertido para fundo transparente
- portfólio em assets/obras (640 e 1200 px) + assets/js/obras.js
- fotos de apoio em assets/img, favicons e og-alma.jpg
Uso: python tools/processar.py"""
import os, json
from PIL import Image, ImageFilter, ImageOps

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
IG = os.path.join(os.path.dirname(SITE), '_ref', 'ig')
IMG = os.path.join(SITE, 'assets', 'img')
OBRAS = os.path.join(SITE, 'assets', 'obras')
OURO = (176, 136, 62)
OSSO = (245, 239, 231)

# id do post -> (categoria, legenda curta)
PORTFOLIO = [
    (65, 'brows', 'Micropigmentação de sobrancelhas, fio a fio'),
    (52, 'brows', 'Sobrancelhas cicatrizadas, efeito natural'),
    (133, 'brows', 'Design com micropigmentação'),
    (167, 'brows', 'Sobrancelhas estruturadas'),
    (25, 'labios', 'Micropigmentação labial, cobertura total'),
    (145, 'olhar', 'Lifting de pestanas'),
    (151, 'brows', 'Resultado suave em pele madura'),
    (172, 'labios', 'Lábios com cor e contorno'),
    (18, 'brows', 'Lifting de pestanas e design com tintura'),
    (9, 'brows', 'Design de sobrancelhas com henna'),
    (161, 'olhar', 'Extensão de pestanas e sobrancelhas'),
    (90, 'brows', 'Antes e depois, sobrancelhas'),
    (142, 'labios', 'Hidra Lips'),
    (122, 'olhar', 'Rímel Effect, técnica autoral'),
    (39, 'brows', 'Shadow brows'),
    (95, 'brows', 'Antes e depois, pele madura'),
    (33, 'pele', 'Alquimia do Glow, antes e depois'),
    (143, 'labios', 'Lábios logo após o procedimento'),
    (168, 'brows', 'Preenchimento de falhas'),
    (210, 'olhar', 'Lifting de pestanas, detalhe'),
    (173, 'brows', 'Microblading'),
    (5, 'labios', 'Neutralização labial'),
    (162, 'brows', 'Visagismo aplicado ao design'),
    (233, 'olhar', 'Rímel Effect'),
    (241, 'brows', 'Design de sobrancelhas'),
    (55, 'pele', 'Remoção de micropigmentação a laser'),
    (213, 'olhar', 'Extensão de pestanas'),
    (252, 'brows', 'Design de sobrancelhas'),
    (222, 'brows', 'Traços finos com pigmento orgânico'),
    (10, 'pele', 'A pele da Fabi, Alquimia do Glow'),
    (112, 'brows', 'Cicatrizado'),
    (174, 'pele', 'Unhas em gel, manutenção com lima manual'),
    (58, 'labios', 'Micropigmentação labial'),
    (11, 'pele', 'Remoção: laser e microagulhamento'),
]

# fotos de apoio: nome -> (id, recorte relativo (x0,y0,x1,y1) ou None, larguras)
APOIO = {
    'fabi-retrato': (0, (.112, .152, .925, .643), (720, 1200)),
    'fabi-pb': (26, None, (640, 1000)),
    'fabi-sala': (28, (0, .32, 1, 1), (640, 1000)),
    'fabi-jurada': (66, None, (640, 1000)),
    'formacao-certificado': (38, None, (640, 1000)),
    'formacao-certificado-2': (165, None, (640, 1000)),
    'formacao-pratica': (239, None, (640, 1000)),
    'mesa-quantica': (139, (0, .40, 1, 1), (640, 1000)),
    'estudio': (62, (0, 0, 1, .78), (640, 1000)),
    'fabi-estudio': (104, None, (640, 1000)),
    'fabi-palco': (48, None, (640, 1000)),
}


def abrir(i):
    return Image.open(os.path.join(IG, f'{i:03d}.jpg')).convert('RGB')


def salvar(im, pasta, nome, larguras, q=80):
    for w in larguras:
        c = im.copy()
        if c.width > w:
            c = c.resize((w, round(c.height * w / c.width)), Image.LANCZOS)
        c.save(os.path.join(pasta, f'{nome}-{w}.webp'), 'WEBP', quality=q, method=6)


def logo():
    """Anel + monograma FG. Fundo é um cinza-claro em degradê: o alfa vem da falta de azul em relação ao fundo."""
    src = abrir(97).crop((455, 285, 865, 670))
    src = src.resize((src.width * 3, src.height * 3), Image.LANCZOS)
    w, h = src.size
    px = src.load()
    a = Image.new('L', (w, h))
    pa = a.load()
    for y in range(h):
        bg = sum(px[x, y][2] for x in (2, 3, 4, w - 3, w - 4)) / 5
        for x in range(w):
            r, g, b = px[x, y]
            v = (bg - b) / max(bg - 70, 1)
            pa[x, y] = max(0, min(255, int((v - .06) * 1.25 * 255)))
    a = a.filter(ImageFilter.GaussianBlur(.6))
    box = a.point(lambda v: 255 if v > 40 else 0).getbbox()
    a = a.crop(box)
    pad = 12
    full = Image.new('L', (a.width + pad * 2, a.height + pad * 2))
    full.paste(a, (pad, pad))
    for nome, cor in (('logo-ouro', OURO), ('logo-osso', OSSO), ('logo-claro', (217, 191, 134))):
        im = Image.new('RGBA', full.size, cor + (0,))
        im.putalpha(full)
        im.save(os.path.join(IMG, nome + '.png'))
        for s in (160, 320, 640):
            c = im.resize((s, round(full.height * s / full.width)), Image.LANCZOS)
            c.save(os.path.join(IMG, f'{nome}-{s}.webp'), 'WEBP', quality=90, method=6)
    # monograma sozinho (miolo do anel) para favicon
    W, H = full.size
    m = full.crop((int(W * .22), int(H * .17), int(W * .78), int(H * .83)))
    mb = m.point(lambda v: 255 if v > 60 else 0).getbbox()
    m = m.crop(mb)
    for nome, cor in (('mono-ouro', OURO), ('mono-osso', OSSO)):
        im = Image.new('RGBA', m.size, cor + (0,))
        im.putalpha(m)
        for s in (96, 192):
            im.resize((round(m.width * s / m.height), s), Image.LANCZOS).save(os.path.join(IMG, f'{nome}-{s}.webp'), 'WEBP', quality=92, method=6)
    print('mono', m.size)
    return m


def icones(mono):
    S = 512
    fundo = Image.new('RGBA', (S, S), (35, 24, 19, 255))
    s = int(S * .62)
    m = mono.resize((round(mono.width * s / mono.height), s), Image.LANCZOS)
    cor = Image.new('RGBA', m.size, (217, 191, 134, 0))
    cor.putalpha(m)
    fundo.alpha_composite(cor, ((S - m.width) // 2, (S - m.height) // 2))
    fundo.save(os.path.join(IMG, 'icone-512.png'))
    fundo.resize((180, 180), Image.LANCZOS).save(os.path.join(IMG, 'icone-180.png'))
    fundo.resize((32, 32), Image.LANCZOS).save(os.path.join(SITE, 'favicon-32.png'))
    fundo.save(os.path.join(SITE, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])


def og():
    W, H = 1200, 630
    tela = Image.new('RGB', (W, H), (35, 24, 19))
    ret = abrir(0).crop((0, 160, 1080, 860))
    ret = ImageOps.fit(ret, (560, H), centering=(.45, .3))
    tela.paste(ret, (W - 560, 0))
    lg = Image.open(os.path.join(IMG, 'logo-claro.png'))
    lg = lg.resize((330, round(lg.height * 330 / lg.width)), Image.LANCZOS)
    tela.paste(lg, ((W - 560 - 330) // 2, (H - lg.height) // 2), lg)
    tela.save(os.path.join(SITE, 'og-alma.jpg'), quality=86)


def portfolio():
    dados = []
    for i, cat, leg in PORTFOLIO:
        im = abrir(i)
        nome = f'ab-{i:03d}'
        salvar(im, OBRAS, nome, (640, 1200), 78)
        dados.append({'f': nome, 'c': cat, 'l': leg, 'w': im.width, 'h': im.height})
    with open(os.path.join(SITE, 'assets', 'js', 'obras.js'), 'w', encoding='utf-8') as f:
        f.write('/* gerado por tools/processar.py: não editar à mão */\nwindow.OBRAS = ' + json.dumps(dados, ensure_ascii=False) + ';\n')


def apoio():
    for nome, (i, rec, larg) in APOIO.items():
        im = abrir(i)
        if rec:
            W, H = im.size
            im = im.crop((int(rec[0] * W), int(rec[1] * H), int(rec[2] * W), int(rec[3] * H)))
        salvar(im, IMG, nome, larg, 80)
        print(nome, im.size)


if __name__ == '__main__':
    for p in (IMG, OBRAS):
        os.makedirs(p, exist_ok=True)
    mono = logo()
    icones(mono)
    og()
    portfolio()
    apoio()
    print('ok')
