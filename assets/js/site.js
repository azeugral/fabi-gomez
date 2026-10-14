/* Fabi Gomez · Alma Beauty */
var CONFIG = {
  whatsapp: '351938851358',
  instagram: 'https://www.instagram.com/fabialmabeauty/'
};

(function () {
  var doc = document.documentElement;
  doc.classList.add('js');
  var semMov = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ano */
  document.querySelectorAll('[data-ano]').forEach(function (e) { e.textContent = new Date().getFullYear(); });

  /* hero: entrada depois de a foto carregar */
  var hero = document.querySelector('.hero');
  if (hero) {
    var img = hero.querySelector('figure img');
    var ir = function () { requestAnimationFrame(function () { hero.classList.add('pronto'); }); };
    if (!img || img.complete) ir(); else { img.addEventListener('load', ir); img.addEventListener('error', ir); setTimeout(ir, 1400); }
  }

  /* nav: fundo ao rolar, esconde a descer, mostra a subir */
  var nav = document.querySelector('.nav');
  var prog = document.querySelector('[data-prog] i');
  var fixo = document.querySelector('.fixo');
  var ultimo = 0, pedido = false;
  function rolar() {
    pedido = false;
    var y = window.scrollY;
    var max = doc.scrollHeight - window.innerHeight;
    if (nav) {
      nav.classList.toggle('solida', y > 24);
      if (!document.body.classList.contains('nav-aberta')) nav.classList.toggle('oculta', y > 420 && y > ultimo + 2);
      if (y < ultimo - 2) nav.classList.remove('oculta');
    }
    if (prog) prog.style.transform = 'scaleX(' + (max > 0 ? Math.min(y / max, 1) : 0) + ')';
    if (fixo) fixo.classList.toggle('ver', y > window.innerHeight * .7 && (max - y) > 260);
    ultimo = y;
  }
  window.addEventListener('scroll', function () { if (!pedido) { pedido = true; requestAnimationFrame(rolar); } }, { passive: true });
  rolar();

  /* gaveta */
  var abrir = document.querySelector('.nav-abrir');
  if (abrir) {
    var fechar = function () { document.body.classList.remove('nav-aberta'); abrir.setAttribute('aria-expanded', 'false'); abrir.querySelector('span').textContent = 'Menu'; };
    abrir.addEventListener('click', function () {
      var a = !document.body.classList.contains('nav-aberta');
      document.body.classList.toggle('nav-aberta', a);
      abrir.setAttribute('aria-expanded', a);
      abrir.querySelector('span').textContent = a ? 'Fechar' : 'Menu';
      nav.classList.remove('oculta');
    });
    document.querySelectorAll('.nav-menu a').forEach(function (a) { a.addEventListener('click', fechar); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') fechar(); });
    window.addEventListener('resize', function () { if (window.innerWidth > 1060) fechar(); });
  }

  /* revelações */
  var alvos = document.querySelectorAll('[data-r]');
  if ('IntersectionObserver' in window && !semMov) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('visto'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: .08 });
    alvos.forEach(function (el) {
      var d = el.getAttribute('data-d');
      if (d) el.style.transitionDelay = (d * .09) + 's';
      io.observe(el);
    });
  } else alvos.forEach(function (el) { el.classList.add('visto'); });

  /* acordeões com altura animada */
  document.querySelectorAll('details.item, details.pergunta').forEach(function (d) {
    var s = d.querySelector('summary'), c = d.querySelector('.item-corpo');
    if (!s || !c) return;
    s.addEventListener('click', function (e) {
      if (semMov) return;
      e.preventDefault();
      if (d.dataset.anim) return;
      d.dataset.anim = 1;
      if (!d.open) {
        d.open = true;
        var h = c.scrollHeight;
        c.animate([{ height: '0px', opacity: 0 }, { height: h + 'px', opacity: 1 }], { duration: 520, easing: 'cubic-bezier(.16,.84,.32,1)' }).onfinish = function () { delete d.dataset.anim; };
      } else {
        var h2 = c.scrollHeight;
        c.animate([{ height: h2 + 'px', opacity: 1 }, { height: '0px', opacity: 0 }], { duration: 400, easing: 'cubic-bezier(.65,0,.35,1)' }).onfinish = function () { d.open = false; delete d.dataset.anim; };
      }
    });
  });

  /* trabalhos */
  var OB = window.OBRAS || [];
  function fig(o, i) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'obra';
    b.dataset.i = i;
    b.dataset.c = o.c;
    b.dataset.leg = o.l;
    b.setAttribute('aria-label', 'Ampliar: ' + o.l);
    b.innerHTML = '<img src="assets/obras/' + o.f + '-640.webp" alt="' + o.l + '" width="640" height="' + Math.round(640 * o.h / o.w) + '" loading="lazy" decoding="async">';
    return b;
  }
  var grade = document.querySelector('[data-obras]');
  var lista = [];
  if (grade && OB.length) {
    var lim = parseInt(grade.getAttribute('data-obras'), 10) || OB.length;
    var lim2 = OB.slice(0, lim);
    lim2.forEach(function (o, i) { grade.appendChild(fig(o, i)); });
    lista = lim2;

    var filtro = document.querySelector('.filtro');
    if (filtro) {
      var aplicar = function (cat, primeira) {
        filtro.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.cat === cat); });
        var vis = [];
        var els = grade.querySelectorAll('.obra');
        var trocar = function () {
          els.forEach(function (el) {
            var ok = cat === 'todos' || el.dataset.c === cat;
            el.hidden = !ok;
            el.classList.remove('sai', 'entra');
            if (ok) { vis.push(OB[+el.dataset.i]); if (!primeira) { el.style.animationDelay = Math.min(vis.length, 12) * 40 + 'ms'; el.classList.add('entra'); } }
          });
          lista = vis;
        };
        if (primeira || semMov) trocar();
        else { els.forEach(function (el) { if (!el.hidden) el.classList.add('sai'); }); setTimeout(trocar, 280); }
        var url = new URL(location.href);
        if (cat === 'todos') url.searchParams.delete('cat'); else url.searchParams.set('cat', cat);
        if (!primeira) history.replaceState(null, '', url);
      };
      filtro.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) aplicar(b.dataset.cat); });
      var ini = new URLSearchParams(location.search).get('cat');
      aplicar(filtro.querySelector('[data-cat="' + ini + '"]') ? ini : 'todos', true);
    }
  }

  /* lightbox */
  var lb = document.querySelector('.lb');
  if (lb && grade) {
    var lim3 = lb.querySelector('.lb-palco img'), atual = 0, foco = null;
    var leg = lb.querySelector('[data-leg]'), cont = lb.querySelector('[data-cont]');
    var mostrar = function (i) {
      if (!lista.length) return;
      atual = (i + lista.length) % lista.length;
      var o = lista[atual];
      lim3.classList.remove('ok');
      var n = new Image();
      n.onload = function () { lim3.src = n.src; lim3.alt = o.l; requestAnimationFrame(function () { lim3.classList.add('ok'); }); };
      n.src = 'assets/obras/' + o.f + '-1200.webp';
      leg.textContent = o.l;
      cont.textContent = (atual + 1) + ' / ' + lista.length;
    };
    var abrirLb = function (o) {
      foco = document.activeElement;
      mostrar(lista.indexOf(o));
      lb.classList.add('aberto');
      lb.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      lb.querySelector('[data-fechar]').focus();
    };
    var fecharLb = function () {
      lb.classList.remove('aberto');
      lb.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      if (foco) foco.focus();
    };
    grade.addEventListener('click', function (e) { var b = e.target.closest('.obra'); if (b) abrirLb(OB[+b.dataset.i]); });
    lb.querySelector('[data-fechar]').addEventListener('click', fecharLb);
    lb.querySelector('[data-ant]').addEventListener('click', function () { mostrar(atual - 1); });
    lb.querySelector('[data-prox]').addEventListener('click', function () { mostrar(atual + 1); });
    lb.querySelector('.lb-palco').addEventListener('click', function (e) { if (e.target === e.currentTarget) fecharLb(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('aberto')) return;
      if (e.key === 'Escape') fecharLb();
      if (e.key === 'ArrowLeft') mostrar(atual - 1);
      if (e.key === 'ArrowRight') mostrar(atual + 1);
    });
    var x0 = null;
    lb.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 48) mostrar(atual + (dx < 0 ? 1 : -1));
      x0 = null;
    });
  }

  /* marcar: monta a mensagem e abre o WhatsApp */
  var form = document.querySelector('[data-marcar]');
  if (form) {
    var prev = form.querySelector('[data-previa]');
    var sel = form.querySelector('[name="servico"]');
    var grupos = { procedimento: 'proc', formacao: 'form', terapia: 'ter' };
    var filtrarServicos = function () {
      var t = (form.querySelector('[name="tipo"]:checked') || {}).value || 'procedimento';
      var primeiro = null;
      sel.querySelectorAll('optgroup').forEach(function (g) {
        var ok = g.dataset.g === grupos[t];
        g.hidden = !ok;
        g.disabled = !ok;
        if (ok && !primeiro) primeiro = g.querySelector('option');
      });
      var at = sel.options[sel.selectedIndex];
      if (!at || at.parentNode.disabled) sel.value = primeiro ? primeiro.value : '';
    };
    var texto = function () {
      var f = new FormData(form);
      var t = { procedimento: 'marcar uma avaliação/procedimento', formacao: 'saber mais sobre uma formação', terapia: 'marcar uma sessão de terapia' }[f.get('tipo')] || 'marcar';
      var l = ['Olá, Fabi! Vim pelo site e gostaria de ' + t + '.', '', '• Serviço: ' + (f.get('servico') || '-')];
      if (f.get('nome')) l.push('• Nome: ' + f.get('nome'));
      if (f.get('quando')) l.push('• Preferência: ' + f.get('quando'));
      if (f.get('antes') && f.get('antes') !== 'Não') l.push('• Já tenho micropigmentação: ' + f.get('antes'));
      if (f.get('msg')) { l.push('', f.get('msg')); }
      return l.join('\n');
    };
    var atualizar = function () { prev.textContent = texto(); };
    form.addEventListener('change', function (e) { if (e.target.name === 'tipo') filtrarServicos(); atualizar(); });
    form.addEventListener('input', atualizar);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      window.open('https://wa.me/' + CONFIG.whatsapp + '?text=' + encodeURIComponent(texto()), '_blank', 'noopener');
    });
    var q = new URLSearchParams(location.search);
    var tp = q.get('tipo');
    if (tp && form.querySelector('[name="tipo"][value="' + tp + '"]')) form.querySelector('[name="tipo"][value="' + tp + '"]').checked = true;
    filtrarServicos();
    var sv = q.get('servico');
    if (sv) { var op = Array.prototype.find.call(sel.options, function (o) { return o.value === sv && !o.parentNode.disabled; }); if (op) sel.value = sv; }
    atualizar();
  }
})();
