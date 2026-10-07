#!/usr/bin/env python3
"""Gera v1/index.html, v2/index.html, obrigado/index.html e index.html (raiz) a partir de um template único.
Rodar: python3 build.py   (a chave anon é lida do gerador-paginas/public/index.html, nunca fica no repositório fonte)"""
import re, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parent
GERADOR = ROOT.parent.parent / "gerador-paginas" / "public" / "index.html"
ANON = re.search(r'const ANON = "([^"]+)"', GERADOR.read_text()).group(1)

PIXEL = "429553154418122"
SLUG = "black-revolucao-nao-alunos"
GRUPO = "https://sndflw.com/i/D3dZyygkzj3LQgQ73IHP"
TITLE = "Black · A Revolução do Estudo — 10 de novembro, 20h, ao vivo"
DESC = "No dia 10 de novembro, ao vivo, a preparação para concurso que cabe na rotina de quem trabalha, cuida da família e tem pouco tempo. E a maior Black Friday da história do Sou Concurseiro."
FONTS = "https://fonts.googleapis.com/css2?family=Saira:wght@500;600;700;800&family=Figtree:wght@400;500;600;700&display=swap"

HEAD = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:image" content="{og}">
<meta name="theme-color" content="#050607">
<link rel="icon" href="../assets/logo-e.png" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{fonts}">
<link rel="stylesheet" href="../assets/black.css?v={v}">
<script>window.BLACK_CFG={{anon:"{anon}",slug:"{slug}",pixel:"{pixel}",versao:"{versao}",grupo:"{grupo}",obrigado:"../obrigado/"}};</script>
</head>
<body>
"""

BARS = '<span class="bars" aria-hidden="true"><i></i><i></i><i></i></span>'

def topbar():
    return f"""
<header class="topbar">
  <div class="wrap">
    <div class="cd" aria-label="Contagem regressiva para a live de 10 de novembro às 20h">
      <span class="cd-label">A condição será liberada em:</span>
      <div class="cd-units">
        <span class="cd-unit"><b data-cd="d">--</b><span>dias</span></span>
        <span class="cd-unit"><b data-cd="h">--</b><span>horas</span></span>
        <span class="cd-unit"><b data-cd="m">--</b><span>minutos</span></span>
        <span class="cd-unit"><b data-cd="s">--</b><span>segundos</span></span>
      </div>
    </div>
    <a class="btn" href="#form" data-goto-form>Quero participar</a>
  </div>
</header>
"""

def form_card(cta):
    arrow = '<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
    return f"""
<form class="form-card rv" id="form" novalidate style="--d:.35s">
  <p class="form-title">Garanta o seu lugar na live</p>
  <div class="field"><label for="f-tel">WhatsApp com DDD</label><input id="f-tel" name="telefone" type="tel" inputmode="numeric" autocomplete="tel-national" placeholder="(00) 00000-0000" required><div class="msg">Confira o WhatsApp: DDD + número com 9 dígitos.</div></div>
  <div class="field"><label for="f-email">E-mail</label><input id="f-email" name="email" type="email" autocomplete="email" placeholder="Seu melhor e-mail" required><div class="msg">Digite um e-mail válido.</div></div>
  <div class="field"><label for="f-esc">Escolaridade</label>
    <select id="f-esc" name="escolaridade" class="placeholder" required>
      <option value="" disabled selected>Qual a sua escolaridade?</option>
      <option value="fundamental">Ensino Fundamental</option>
      <option value="medio">Ensino Médio</option>
      <option value="superior_cursando">Superior Cursando</option>
      <option value="superior_completo">Superior Completo</option>
      <option value="pos">Pós-graduação</option>
    </select><div class="msg">Selecione a sua escolaridade.</div></div>
  <button class="btn block" type="submit"><span>{cta}</span>{arrow}</button>
  <div class="form-error" role="alert"></div>
  <p class="form-note">Cadastro gratuito · Link no grupo do WhatsApp</p>
  <p class="form-note">Com Fábio Silva · Sou Concurseiro</p>
</form>
"""

def hero(c):
    cal = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="16" rx="3"/><path d="M8 3v4M16 3v4M3 10h18"/></svg>'
    return f"""
<section class="hero{' hero--synapse' if c.get('synapse') else ''}" aria-labelledby="h1">
  <div class="hero-bg" aria-hidden="true"></div>{'<canvas class="synapse" aria-hidden="true"></canvas>' if c.get('synapse') else ''}
  <div class="wrap">
    <div class="hero-copy">
      <div class="brand-row rv" style="--d:0s">
        <div class="brand"><img src="../assets/logo-black-revolucao.png" alt="Black · A Revolução do Estudo"></div>
        <div class="date-pill">{cal}<span class="d1">10 de novembro · 20h</span><span class="d2 live">Ao vivo · Brasília</span></div>
      </div>
      <h1 id="h1" class="rv" style="--d:.1s">{c['h1']}</h1>
      <p class="sub rv" style="--d:.18s">{c['sub']}</p>
      <div class="hero-form-slot">{form_card("Quero participar")}</div>
    </div>
    <div class="hero-photo rv" aria-hidden="true" style="--d:.05s">
      <img src="../assets/fabio-camisa-1011.png" alt="" loading="eager" fetchpriority="high">
    </div>
  </div>
</section>
"""

def who():
    items = [
        "Você trabalha e tem pouco tempo para estudar.",
        "Você nunca estudou para concurso e não sabe por onde começar.",
        "Você já começou, parou, e quer voltar sem recomeçar do zero.",
        "Você acha que já passou da idade.",
    ]
    lis = "".join(f"<li>{BARS}<span>{t}</span></li>" for t in items)
    return f"""
<div class="who rv">
  <div><p class="eyebrow">Para quem é</p><h3>Se uma frase aqui é a sua, a live de 10/11 foi feita para você.</h3><p>Não precisa ter estudado antes. Precisa só da vida que você já tem.</p></div>
  <ul>{lis}</ul>
</div>
<p class="cta-row"><a class="btn" href="#form" data-goto-form>Quero garantir meu lugar</a></p>
"""

def dobra2_v2():
    cards = f"""
<div class="bento">
  <article class="card img rv"><div class="pic"><img src="../assets/cena-transito.jpg" alt="Mulher no ônibus, a caminho do trabalho, estudando pelo fone"></div><span class="num">01</span><h3>Mais horas de estudo sem tirar nenhuma do seu dia</h3><p>Você estuda e revisa no trânsito, na academia e nas tarefas de casa. O tempo que hoje se perde vira matéria revisada.</p></article>
  <article class="card img rv" style="transition-delay:.08s"><div class="pic"><img src="../assets/cena-louca.jpg" alt="Homem lavando a louça à noite enquanto ouve uma aula"></div><span class="num">02</span><h3>Direção para o seu concurso</h3><p>Você sabe o que estudar hoje, o que mais pesa na sua prova e o que pode ficar para depois. Acaba o cronograma impossível.</p></article>
  <article class="card img rv" style="transition-delay:.16s"><div class="pic"><img src="../assets/cena-noite.jpg" alt="Mãe estudando na cozinha às dez da noite, com o filho dormindo no quarto ao lado"></div><span class="num">03</span><h3>Constância nas semanas difíceis</h3><p>Você estuda ao lado de gente no mesmo caminho e tem quem te puxe de volta quando a rotina aperta.</p></article>
  <article class="card txt rv"><span class="num">04</span>{BARS}<h3>Clareza do que você já domina</h3><p>Você enxerga onde está forte e onde precisa reforçar antes da prova, e para de estudar no escuro.</p></article>
  <article class="card txt rv" style="transition-delay:.08s"><span class="num">05</span>{BARS}<h3>Um começo guiado</h3><p>Nos primeiros 30 dias você recebe o passo a passo para montar a sua rotina, mesmo que nunca tenha estudado para concurso.</p></article>
</div>
<p class="lead rv" style="margin:40px auto 0"><b>Tempo, direção e constância</b> são o que separa quem quer passar de quem passa. Na live você vê como ter os três, e a condição de Black Friday para começar.</p>
"""
    return f"""
<section class="glow-top">
  <div class="wrap center">
    <div class="center">
      <p class="eyebrow rv">O que você vai conhecer no dia 10</p>
      <h2 class="rv">Quem passa em concurso é quem estuda todo dia, por meses. O que você vai conhecer no dia 10 foi feito para isso acontecer <span class="blue">na vida que você tem</span>.</h2>
      <p class="lead rv">A preparação que te ensinaram exige horas livres que você não tem. Por isso você começa, para, e a aprovação fica para o próximo edital. Com a Revolução do Estudo, você tem:</p>
    </div>
    {cards}
    {who()}
  </div>
</section>
"""

def dobra2_v1():
    steps = [
        ("Por que tanta gente começa a estudar e para", "e por que isso não é falta de disciplina."),
        ("O que impede mais de 25 mil concurseiros", "de passarem nas provas de concurso."),
        ("O novo jeito de estudar", "que cabe na rotina de quem trabalha o dia inteiro."),
        ("A condição de Black Friday", "que o Sou Concurseiro nunca tinha feito."),
    ]
    lis = "".join(f'<li class="rv" style="transition-delay:{i*.07:.2f}s"><b>{a}</b>{b}</li>' for i, (a, b) in enumerate(steps))
    return f"""
<section class="glow-top">
  <div class="wrap center">
    <p class="eyebrow rv">A ideia por trás da Black</p>
    <h2 class="rv">Ninguém deveria ter que <span class="blue">parar a vida</span> para mudar de vida.</h2>
    <p class="lead rv">A preparação para o concurso que te ensinaram foi feita para quem tem horas livres todo dia. Você não tem, e não vai passar a ter. <b>No dia 10 de novembro você vai ver:</b></p>
    <div class="reveal-grid">
      <ol class="steps">{lis}</ol>
      <div class="mosaic rv" aria-hidden="true">
        <figure><img src="../assets/cena-noite.jpg" alt=""><figcaption>Dez da noite</figcaption></figure>
        <figure><img src="../assets/cena-transito.jpg" alt=""><figcaption>No trajeto</figcaption></figure>
        <figure><img src="../assets/cena-louca.jpg" alt=""><figcaption>Em casa</figcaption></figure>
      </div>
    </div>
    {who()}
  </div>
</section>
"""

def band():
    return f"""
<section class="band" aria-label="A condição de Black Friday">
  <div class="wrap">
    <div class="band-in">
    <div class="band-grid">
      <div>
        <p class="eyebrow rv">A condição</p>
        <h2 class="rv">A maior condição de Black Friday da história do Sou Concurseiro será liberada <span class="blue">ao vivo</span>, só para quem estiver na live.</h2>
        <p class="rv">Eu nunca fiz nada parecido. Não vai ter aviso por e-mail nem repescagem: quem está no grupo recebe o link antes e entra primeiro.</p>
      </div>
      <div class="lock rv"><span>Abre em</span><span class="date">10/11<small>20h · Brasília</small></span></div>
    </div>
    </div>
  </div>
</section>
"""

def bio():
    return f"""
<section>
  <div class="wrap bio">
    <div class="bio-photo rv"><img src="../assets/fabio-bracos-cruzados.jpg" alt="Fábio Silva, delegado, professor e mentor do Sou Concurseiro"><div class="tag">Quem vai te mostrar o caminho<b>Fábio Silva</b></div></div>
    <div>
      <p class="eyebrow rv">Quem vai te mostrar o caminho</p>
      <h2 class="rv">Delegado, professor e mentor do Sou Concurseiro.</h2>
      <ul class="roles rv"><li>Polícias</li><li>Tribunais</li><li>Saúde</li><li>Educação</li></ul>
      <p class="rv">Fábio Silva prepara alunos para concursos de polícia, tribunais, saúde e educação. Viu de perto gente boa desistir no meio do caminho, não por falta de capacidade, mas por falta de tempo, de direção e de alguém do lado.</p>
      <p class="rv">A Revolução do Estudo é a resposta que ele passou meses construindo para essas três coisas: uma preparação que anda junto com a vida de quem trabalha, cuida da família e estuda com o tempo que tem.</p>
      <p class="rv" style="margin-top:26px"><a class="btn" href="#form" data-goto-form>Quero garantir meu lugar</a></p>
    </div>
  </div>
</section>
"""

def final():
    return f"""
<section class="final">
  <div class="wrap">
    <p class="eyebrow rv">10 de novembro · 20h · ao vivo</p>
    <h2 class="rv">O caminho para a sua aprovação, <span class="blue">sem parar a sua vida</span>.</h2>
    <p class="rv"><a class="btn" href="#form" data-goto-form>Quero participar da Black</a></p>
    <p class="note rv">Cadastro gratuito. O link da live sai primeiro no grupo do WhatsApp.</p>
  </div>
</section>
"""

FOOT = """
<footer>
  <div class="wrap">
    <p>Seus dados são usados apenas para enviar informações sobre a Black A Revolução do Estudo.</p>
    <p>© 2026 Sou Concurseiro e Vou Passar · Todos os direitos reservados.</p>
  </div>
</footer>
<script src="../assets/black.js?v={v}"></script>
</body>
</html>
"""

COPY = {
    "v1": {
        "h1": 'A <span class="metal">tríade</span> que vai te ajudar na sua aprovação no concurso público de uma vez por todas!',
        "sub": "No dia 10 de novembro vou liberar um novo jeito de se preparar para concursos, feito para quem trabalha, cuida da família e estuda com o tempo que tem. E abrir a maior Black Friday da história do Sou Concurseiro.",
        "dobra2": dobra2_v1,
    },
    "v2": {
        "h1": 'O caminho para ver o seu nome na <span class="metal">lista de aprovados</span>, sem parar a sua vida para estudar.',
        "sub": "No dia 10 de novembro, irei revelar ao vivo a preparação que faz o estudo caber na rotina de quem trabalha, cuida da família e tem pouco tempo. Você passa a estudar nos momentos que hoje perde, sabe todo dia o que precisa estudar para a sua prova e não se prepara mais sozinho. Nessa live vamos abrir a maior Black Friday da história do Sou Concurseiro.",
        "dobra2": dobra2_v2,
        "so_dobra1": True,
    },
}
COPY["v3"] = dict(COPY["v2"], synapse=True)  # v3 = v2 + rede de sinapses (21st.dev, portada) atrás do hero

V = "14"
OG = "https://revolucaodoestudo.com.br/assets/og.jpg"

def page(versao):
    c = COPY[versao]
    out = HEAD.format(title=TITLE, desc=DESC, og=OG, fonts=FONTS, v=V, anon=ANON, slug=SLUG, pixel=PIXEL, versao=versao, grupo=GRUPO)
    # so_dobra1: página só com a primeira dobra (pedido do Fábio 07/10 para a v2)
    corpo = hero(c) if c.get("so_dobra1") else hero(c) + c["dobra2"]() + band() + bio() + final()
    extra = f'<script src="../assets/synapse.js?v={V}" defer></script>\n' if c.get("synapse") else ""
    out += topbar() + "<main>" + corpo + "</main>" + FOOT.format(v=V).replace("</body>", extra + "</body>")
    return out

def obrigado():
    out = HEAD.format(title="Falta um passo: entre no grupo · Black · A Revolução do Estudo", desc="Entre no grupo do WhatsApp para receber o link da live de 10 de novembro.", og=OG, fonts=FONTS, v=V, anon=ANON, slug=SLUG, pixel=PIXEL, versao="obrigado", grupo=GRUPO)
    cal = ("https://calendar.google.com/calendar/render?action=TEMPLATE&text=" + "Black+%C2%B7+A+Revolu%C3%A7%C3%A3o+do+Estudo+%28ao+vivo%29" +
           "&dates=20261110T230000Z/20261111T010000Z&details=Live+da+Black+A+Revolu%C3%A7%C3%A3o+do+Estudo.+O+link+sai+no+grupo+do+WhatsApp.&ctz=America/Sao_Paulo")
    out += f"""
<main class="thanks">
  <div class="thanks-bg" aria-hidden="true"></div>
  <div class="thanks-card">
    <div class="brand"><img src="../assets/logo-black-revolucao.png" alt="Black · A Revolução do Estudo"></div>
    <h1>Sucesso! Só falta <span class="blue">1 passo</span> para garantir o seu lugar…</h1>
    <div class="bar" role="progressbar" aria-valuenow="84" aria-valuemin="0" aria-valuemax="100"><i></i><b>0%</b></div>
    <p>Clique no botão abaixo e entre no grupo oficial do WhatsApp. É por lá que você recebe <b>o link da live do dia 10/11</b>, o lembrete na hora certa e os avisos da Black. Sem ele, você pode perder a condição especial.</p>
    <a class="btn" data-grupo href="{GRUPO}" rel="noopener">Entrar no grupo agora</a>
    <p class="small">O grupo é silencioso: você só recebe as mensagens enviadas pela minha equipe.</p>
    <div class="date"><span>Salve a data</span><b>10 de novembro · 20h (Brasília)</b><a href="{cal}" target="_blank" rel="noopener">Adicionar à agenda</a></div>
  </div>
</main>
<script src="../assets/black.js?v={V}"></script>
</body>
</html>
"""
    return out

ROOT_INDEX = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Black · A Revolução do Estudo</title>
<meta http-equiv="refresh" content="0; url=v2/"><link rel="canonical" href="v2/"><script>location.replace("v2/" + location.search + location.hash);</script></head>
<body style="background:#050607;color:#ccc;font-family:sans-serif;padding:40px;text-align:center"><a href="v2/" style="color:#00b7df">Entrar na página</a></body></html>
"""

for v in ("v1", "v2", "v3"):
    d = ROOT / v; d.mkdir(exist_ok=True); (d / "index.html").write_text(page(v), encoding="utf-8")
(ROOT / "obrigado").mkdir(exist_ok=True); (ROOT / "obrigado" / "index.html").write_text(obrigado(), encoding="utf-8")
(ROOT / "index.html").write_text(ROOT_INDEX, encoding="utf-8")
(ROOT / ".nojekyll").write_text("")
print("ok: v1/, v2/, obrigado/, index.html")
