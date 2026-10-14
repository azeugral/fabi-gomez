"""Monta as páginas da raiz a partir de tools/paginas/*.html (nav, rodapé e lightbox comuns).
Cada página começa com três linhas de cabeçalho:
<!--titulo: ...-->
<!--desc: ...-->
<!--menu: chave do item ativo (ou vazio)-->
Marcadores no corpo: <!--seta--> e <!--anel-->. Troque V para furar o cache de CSS/JS."""
import os, re, glob

V = '2'
AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
BASE = 'https://azeugral.github.io/fabi-gomez/'  # CONFIRMAR: trocar quando houver domínio
ZAP = 'https://wa.me/351938851358'

SETA = '<svg class="i-seta" viewBox="0 0 18 18" aria-hidden="true"><path d="M1 9h15M11 4l5 5-5 5"/></svg>'
# o anel fino que contorna o monograma no logo dela
ANEL = '<svg class="anel" viewBox="0 0 44 44" aria-hidden="true"><circle cx="22" cy="22" r="20.5" fill="none" stroke="currentColor" stroke-width=".8" stroke-dasharray="104 6 2 6 2 6"/><path d="M22 14v16M14 22h16" stroke="currentColor" stroke-width=".8"/></svg>'

MENU = [('procedimentos', './#procedimentos', 'Procedimentos'), ('portfolio', 'portfolio.html', 'Portfólio'),
        ('formacoes', 'formacoes.html', 'Formações'), ('terapias', './#terapias', 'Terapias'), ('sobre', './#sobre', 'Sobre a Fabi')]

HEAD = '''<!doctype html>
<html lang="pt-PT">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{titulo}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#f5efe7">
<link rel="canonical" href="{base}{arq}">
<meta property="og:type" content="website">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{base}og-alma.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Monograma FG de Fabi Gomez ao lado de um retrato dela">
<meta property="og:locale" content="pt_PT">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" href="favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="assets/img/icone-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;1,6..96,400&family=IBM+Plex+Sans:wght@400;500&display=swap">
<link rel="stylesheet" href="assets/css/site.css?v={v}">
{extra_head}</head>
<body>
<a class="sr" href="#conteudo">Saltar para o conteúdo</a>
<div class="progresso" data-prog aria-hidden="true"><i></i></div>
<header class="nav">
  <a class="nav-marca" href="./" aria-label="Fabi Gomez, Alma Beauty, início"><img src="assets/img/mono-ouro-96.webp" srcset="assets/img/mono-ouro-96.webp 1x, assets/img/mono-ouro-192.webp 2x" alt="" width="78" height="96"><span><b>Fabi Gomez</b><small>Alma Beauty</small></span></a>
  <button class="nav-abrir" type="button" aria-expanded="false" aria-controls="menu"><span>Menu</span><i aria-hidden="true"></i></button>
  <nav class="nav-menu" id="menu" aria-label="Principal">
    <ul class="menu">{menu}</ul>
    <a class="btn peq" href="marcar.html"><span>Marcar avaliação</span>{seta}</a>
    <div class="gaveta-extra"><a href="{zap}" target="_blank" rel="noopener">WhatsApp 938 851 358</a><span>Sesimbra, Portugal</span></div>
  </nav>
</header>
<main id="conteudo">
'''

FOOT = '''</main>
<footer class="rodape">
  <div class="wrap">
    <div class="rodape-topo">
      <img src="assets/img/logo-claro-320.webp" srcset="assets/img/logo-claro-320.webp 1x, assets/img/logo-claro-640.webp 2x" alt="Fabianna Gomez, Terapia &amp; Estética" width="320" height="315" loading="lazy">
      <p>Micropigmentação, sobrancelhas, olhar e pele. Formadora na área da beleza em Sesimbra, Portugal.</p>
    </div>
    <div class="colunas">
      <div><h4>Páginas</h4><ul><li><a href="./">Início</a></li><li><a href="./#procedimentos">Procedimentos</a></li><li><a href="portfolio.html">Portfólio</a></li><li><a href="formacoes.html">Formações</a></li><li><a href="marcar.html">Marcar</a></li></ul></div>
      <div><h4>Contacto</h4><ul><li><a href="{zap}" target="_blank" rel="noopener">WhatsApp 938 851 358</a></li><li><a href="tel:+351938851358">Telefone 938 851 358</a></li><li><a href="https://www.instagram.com/fabialmabeauty/" target="_blank" rel="noopener">Instagram @fabialmabeauty</a></li><li><a href="https://www.instagram.com/fabii_terapeuta/" target="_blank" rel="noopener">Terapias @fabii_terapeuta</a></li></ul></div>
      <div><h4>Estúdio</h4><ul><li>Sesimbra, Setúbal</li><li>Morada: <em class="a-preencher">a preencher</em></li><li>Horário: <em class="a-preencher">a preencher</em></li><li>Atendimento só com marcação</li></ul></div>
    </div>
    <div class="base"><span>© <span data-ano>2026</span> Fabi Gomez · Alma Beauty</span><span>Site por <a href="https://lrgz.com.br" target="_blank" rel="noopener">L R G Z</a></span></div>
  </div>
</footer>
{fixo}{extra}<script src="assets/js/site.js?v={v}"></script>
</body>
</html>
'''

LB = '''<div class="lb" role="dialog" aria-modal="true" aria-label="Foto ampliada" aria-hidden="true">
  <div class="lb-topo"><span class="rot" data-cont></span><button type="button" data-fechar>Fechar</button></div>
  <div class="lb-palco"><img alt=""></div>
  <div class="lb-base"><button type="button" data-ant aria-label="Anterior">&larr;</button><span class="rot" data-leg></span><button type="button" data-prox aria-label="Seguinte">&rarr;</button></div>
</div>
'''


def montar(caminho):
    nome = os.path.basename(caminho)
    txt = open(caminho, encoding='utf-8').read()
    meta = dict(re.findall(r'<!--(titulo|desc|menu):\s*(.*?)-->', txt))
    corpo = re.sub(r'^(<!--(titulo|desc|menu):.*?-->\s*)+', '', txt).strip() + '\n'
    corpo = corpo.replace('<!--seta-->', SETA).replace('<!--anel-->', ANEL)
    ativo = meta.get('menu', '').strip()
    menu = ''.join(f'<li><a href="{h}"{" aria-current=\"page\"" if k == ativo else ""}>{t}</a></li>' for k, h, t in MENU)
    usa_obras = 'data-obras' in corpo
    extra_head = ''
    if nome == 'index.html':
        extra_head = '<link rel="preload" as="image" href="assets/img/fabi-retrato-720.webp" imagesrcset="assets/img/fabi-retrato-720.webp 720w, assets/img/fabi-retrato-1200.webp 879w" imagesizes="(max-width:900px) 90vw, 46vw">\n'
    arq = '' if nome == 'index.html' else nome
    html = HEAD.format(titulo=meta['titulo'].strip(), desc=meta['desc'].strip(), base=BASE, arq=arq, v=V, menu=menu, seta=SETA, zap=ZAP, extra_head=extra_head)
    html += corpo
    extra = (LB + f'<script src="assets/js/obras.js?v={V}"></script>\n') if usa_obras else ''
    fixo = '' if nome == 'marcar.html' else '<a class="fixo" href="marcar.html"><img src="assets/img/mono-osso-96.webp" alt="" width="78" height="96"><span>Marcar avaliação</span></a>\n'
    html += FOOT.format(zap=ZAP, extra=extra, v=V, fixo=fixo)
    open(os.path.join(SITE, nome), 'w', encoding='utf-8', newline='\n').write(html)
    print('ok', nome)


if __name__ == '__main__':
    for p in sorted(glob.glob(os.path.join(AQUI, 'paginas', '*.html'))):
        montar(p)
