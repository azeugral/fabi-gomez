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
    """Logo oficial dela (../_ref/logo-oficial.webp, PNG transparente enviado em 15/10/2026): anel + monograma FG em ouro texturizado.
    O monograma sozinho sai do maior componente conectado, para não levar letras do anel."""
    import numpy as np
    from scipy import ndimage
    src = Image.open(os.path.join(os.path.dirname(SITE), '_ref', 'logo-oficial.webp')).convert('RGBA')
    arr = np.array(src)
    arr[..., 3][arr[..., 3] < 8] = 0  # resto de recorte quase invisível
    src = Image.fromarray(arr)
    src = src.crop(src.getchannel('A').getbbox())
    for nome in ('logo-ouro', 'logo-claro'):
        src.save(os.path.join(IMG, nome + '.png'))
        for s in (160, 320, 640):
            src.resize((s, round(src.height * s / src.width)), Image.LANCZOS).save(os.path.join(IMG, f'{nome}-{s}.webp'), 'WEBP', quality=92, method=6)
    a = np.array(src.getchannel('A'))
    lab, n = ndimage.label(a > 40)
    tam = ndimage.sum(np.ones_like(a), lab, range(1, n + 1))
    maior = int(np.argmax(tam)) + 1
    masc = ndimage.binary_dilation(lab == maior, iterations=4)
    m = np.array(src)
    m[..., 3] = np.where(masc, m[..., 3], 0)
    mono = Image.fromarray(m)
    mono = mono.crop(mono.getchannel('A').getbbox())
    alfa = mono.getchannel('A')
    for nome, im in (('mono-ouro', mono), ('mono-osso', Image.merge('RGBA', [Image.new('L', mono.size, c) for c in OSSO] + [alfa]))):
        for s in (96, 192):
            im.resize((round(mono.width * s / mono.height), s), Image.LANCZOS).save(os.path.join(IMG, f'{nome}-{s}.webp'), 'WEBP', quality=92, method=6)
    print('logo', src.size, 'mono', mono.size)
    return mono


def icones(mono):
    """Favicon sem fundo: monograma em ouro centrado num quadrado transparente.
    O apple-touch-icon leva fundo marfim, porque o iOS pinta de preto o que for transparente."""
    def quadrado(S, margem, fundo=None):
        q = Image.new('RGBA', (S, S), fundo or (0, 0, 0, 0))
        h = round(S * (1 - 2 * margem))
        m = mono.resize((round(mono.width * h / mono.height), h), Image.LANCZOS)
        q.alpha_composite(m, ((S - m.width) // 2, (S - m.height) // 2))
        return q
    quadrado(512, .06).save(os.path.join(IMG, 'icone-512.png'))
    quadrado(180, .14, (245, 239, 231, 255)).save(os.path.join(IMG, 'icone-180.png'))
    quadrado(32, .02).save(os.path.join(SITE, 'favicon-32.png'))
    grande = quadrado(256, .02)
    grande.save(os.path.join(SITE, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])


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
