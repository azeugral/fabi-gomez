# Fabi Gomez · Alma Beauty

Site de apresentação da Fabiana "Fabi" Gomez ([@fabialmabeauty](https://www.instagram.com/fabialmabeauty/)), especialista em sobrancelhas e micropigmentação e formadora em Sesimbra, Portugal. Texto em PT-PT.

Prévia: https://azeugral.github.io/fabi-gomez/ (com `noindex` até haver domínio).

## Identidade (v1, 14/10/2026)

- **Logo:** é o oficial, em ouro texturizado, que ela enviou em 15/10/2026 como PNG transparente (`../_ref/logo-oficial.webp`). O `tools/processar.py` gera o logo completo (anel + monograma) e o monograma sozinho, separado como o maior componente conectado.
- **Favicon:** o monograma em ouro, sem fundo. O ícone da Apple (180 px) leva fundo marfim, porque o iOS pinta de preto o que fica transparente.
- **Cores:** marfim `#f5efe7`, linho `#ece3d6`, cacau `#231813` e ouro `#a8813a` (claro `#d9bf86`). O ouro é o do monograma e o cacau é o 🤎 que ela usa nas legendas.
- **Fontes:** Bodoni Moda nos títulos (didone, como o monograma) e IBM Plex Sans no texto.
- **Movimento:** curva `cubic-bezier(.16,.84,.32,1)` em tudo:
  - a foto do hero entra com recorte de baixo para cima e o selo FG roda até assentar;
  - as imagens das secções revelam-se com recorte;
  - os acordeões abrem com altura animada e a gaveta do menu desce como cortina;
  - o filtro do portfólio troca as fotos com fade;
  - o lightbox aceita deslizar o dedo.
  
  Não há faixas animadas nem avaliações inventadas. Tudo respeita `prefers-reduced-motion`.
- **Botões:** retos, com um varrimento de ouro da esquerda para a direita e a seta a avançar. O hover só existe em dispositivos com rato.

## Estrutura

| Arquivo | O que é |
|---|---|
| `index.html` | Hero, sobre, procedimentos (acordeão por grupo), como funciona, portfólio recente, formações, terapias, palcos e congressos, perguntas frequentes e contacto com mapa |
| `portfolio.html` | 34 trabalhos com filtro Sobrancelhas, Lábios, Olhar, Pele e correção (`?cat=brows`, `labios`, `olhar` ou `pele`) e lightbox |
| `formacoes.html` | Os dois caminhos do site Canva dela ("Quero viver da beleza" e "Sou da beleza e quero faturar mais"), quatro cursos, o que está incluído e como se inscrever |
| `marcar.html` | Monta a mensagem e abre o WhatsApp `351938851358`. Aceita `?tipo=procedimento`, `formacao` ou `terapia`, e `?servico=` com o nome exato da opção |
| `assets/js/site.js` | `CONFIG` (WhatsApp e Instagram) e o comportamento do site |
| `assets/js/obras.js` | Gerado. Não editar à mão |

## Fluxo

```bash
python tools/processar.py      # ../_ref/ig -> logo, favicons, og-alma.jpg, assets/img, assets/obras e obras.js
python tools/montar_paginas.py # tools/paginas/*.html -> páginas da raiz (V = cache)
```

Os originais são os 263 posts mais recentes do Instagram dela (até 14/10/2026), em `../_ref/ig`. As legendas estão em `../_ref/legendas.txt` e as folhas de contacto em `../_ref/contato`.

## Origem dos dados

- **Do Instagram:**
  - bio, telefone 938 851 358 (arte da foto 256) e o perfil de terapias @fabii_terapeuta;
  - procedimentos e protocolos: Alquimia do Glow, Reativa Brows, Rímel Effect, Hidra Lips, neutralização labial, remoção com laser e microagulhamento, Peeling Hollywood e unhas com lima manual;
  - formações: Alma Essence Brows (Arte & Essência Brows), com certificado SIGO;
  - eventos e história pessoal.
- **Do site Canva da bio** (fabigomes88.my.canva.site), que estava incompleto, com botões sem destino: as secções Mentoria de Transformação Pessoal, Mesa Quântica, "Quero viver da beleza" e "Sou da beleza e quero faturar mais". Foram reorganizadas em Terapias (início) e Formações. O WhatsApp do Canva (`wa.me/message/TVNVHDIPCWH7O1`) foi trocado pelo número direto, porque o número permite mensagem pré-preenchida.

## CONFIRMAR

Os itens pendentes aparecem no site como "✦ a preencher", com sublinhado tracejado. O texto genérico também está listado aqui.

- [ ] **Morada e horário do estúdio** em Sesimbra (rodapé e contacto). O mapa mostra só "Sesimbra".
- [ ] **Valores** de cada procedimento. Ela fez um reajuste em janeiro de 2026. Se preferir não mostrar, apagar a linha "Valor".
- [ ] **Durações e retoques** dos procedimentos (2h30, 30 a 45 dias, etc.). São valores de referência do setor.
- [ ] **Retoque incluído no valor?** (pergunta frequente).
- [ ] **Perguntas frequentes:** as respostas são genéricas, a validar por ela, sobretudo as contraindicações.
- [ ] **Formações:**
  - datas das próximas turmas, carga horária e valores;
  - se há kit incluído;
  - formas de pagamento: MB Way e transferência em prestações saíram de uma legenda de evento.
  - Os dois dias da Alma Essence vêm da turma de 24 e 25/09. Os três dias e os dois meses do curso de unhas vêm do post da aluna Andréia.
- [ ] **Peeling Hollywood:** ela tem a formação (legenda de 2025). Confirmar se está a oferecer.
- [ ] **Palcos:**
  - o Seminário PMU Portugal (Porto, 18 e 19/10/2026) passa a evento passado depois dessa data;
  - o Eurochampions de Roma 2027 está como "presença confirmada".
- [ ] **Nome:** ela assina "Fabi Gomez", "Fabianna Gomez" no logo e "Fabiana Gomes" nos eventos. O site usa **Fabi Gomez** e a marca **Alma Beauty**.
- [ ] **Domínio:** quando houver, trocar `BASE` em `tools/montar_paginas.py`, tirar o `noindex` e trocar o `robots.txt`.

Site por [L R G Z](https://lrgz.com.br).
