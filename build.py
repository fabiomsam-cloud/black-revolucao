#!/usr/bin/env python3
"""Gera v1/index.html, v2/index.html, obrigado/index.html e index.html (raiz) a partir de um template único.
Rodar: python3 build.py   (a chave anon é lida do gerador-paginas/public/index.html, nunca fica no repositório fonte)"""
import re, pathlib, html, json

ROOT = pathlib.Path(__file__).resolve().parent
GERADOR = ROOT.parent.parent / "gerador-paginas" / "public" / "index.html"
ANON = re.search(r'const ANON = "([^"]+)"', GERADOR.read_text()).group(1)

PIXEL = "429553154418122"
SLUG = "black-revolucao-nao-alunos"
GRUPO = "https://sndflw.com/i/D3dZyygkzj3LQgQ73IHP"
TITLE = "Black · A Revolução do Estudo — 10 de novembro, 20h, ao vivo"
DESC = "No dia 10 de novembro, ao vivo, a preparação para concurso que cabe na rotina de quem trabalha, cuida da família e tem pouco tempo. E a maior Black Friday da história do Sou Concurseiro."

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
<link rel="preload" href="../assets/fonts/saira-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../assets/fonts/figtree-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../assets/hero-bg-m.webp" as="image" type="image/webp" media="(max-width:959px)" fetchpriority="high">
<link rel="preload" href="../assets/hero-bg.webp" as="image" type="image/webp" media="(min-width:960px)" fetchpriority="high">
<link rel="stylesheet" href="../assets/black.css?v={v}">
<script>window.BLACK_CFG={{anon:"{anon}",slug:"{slug}",pixel:"{pixel}",versao:"{versao}",grupo:"{grupo}",obrigado:"{obrigado}",live:"{live}",utm:{utm},gads:{gads}}};</script>
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

ESCOLARIDADE = """<div class="field"><label for="f-esc">Escolaridade</label>
    <select id="f-esc" name="escolaridade" class="placeholder" required>
      <option value="" disabled selected>Qual a sua escolaridade?</option>
      <option value="fundamental">Ensino Fundamental</option>
      <option value="medio">Ensino Médio</option>
      <option value="superior_cursando">Superior Cursando</option>
      <option value="superior_completo">Superior Completo</option>
      <option value="pos">Pós-graduação</option>
    </select><div class="msg">Selecione a sua escolaridade.</div></div>"""

ARROW = '<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

def form_card(cta, sem_escolaridade=False, titulo="Garanta o seu lugar na live", nota="Cadastro gratuito · Link no grupo do WhatsApp"):   # 18/10: página de ALUNOS não pergunta escolaridade
    arrow = ARROW
    return f"""
<form class="form-card rv" id="form" novalidate style="--d:.35s">
  <p class="form-title">{titulo}</p>
  <div class="field"><label for="f-tel">WhatsApp com DDD</label><input id="f-tel" name="telefone" type="tel" inputmode="numeric" autocomplete="tel-national" placeholder="(00) 00000-0000" required><div class="msg">Confira o WhatsApp: DDD + número com 9 dígitos.</div></div>
  <div class="field"><label for="f-email">E-mail</label><input id="f-email" name="email" type="email" autocomplete="email" placeholder="Seu melhor e-mail" required><div class="msg">Digite um e-mail válido.</div></div>
  {"" if sem_escolaridade else ESCOLARIDADE}
  <button class="btn block" type="submit"><span>{cta}</span>{arrow}</button>
  <div class="form-error" role="alert"></div>
  <p class="form-note">{nota}</p>
  <p class="form-note">Com Fábio Silva · Sou Concurseiro</p>
</form>
"""

def hero(c):
    cal = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="16" rx="3"/><path d="M8 3v4M16 3v4M3 10h18"/></svg>'
    return f"""
<section class="hero{(' hero--' + c['fx']) if c.get('fx') else ''}{' hero--ref' if c.get('topo_ref') else ''}" aria-labelledby="h1">
  <div class="hero-bg" aria-hidden="true"></div>{('<canvas class="' + c['fx'] + '" aria-hidden="true"></canvas>') if c.get('fx') else ''}
  <div class="wrap">
    <div class="hero-copy">
      <div class="brand-row rv" style="--d:0s">
        <div class="brand"><img src="../assets/logo-black-revolucao.webp" width="480" height="188" alt="Black · A Revolução do Estudo"></div>
        <div class="date-pill">{cal}<span class="d1">{c.get('data', '10 de novembro · 20h')}</span><span class="d2 live">Ao vivo · Brasília</span></div>
      </div>
      <h1 id="h1" class="rv" style="--d:.1s">{c['h1']}</h1>
      <p class="sub rv" style="--d:.18s">{c['sub']}</p>
      <div class="hero-form-slot">{c["topo_cta"] if c.get("topo_cta") else form_card("Quero participar", c.get("sem_escolaridade"))}</div>
    </div>
    <div class="hero-photo rv{' hero-video' if c.get('hero_video') else ''}" aria-hidden="true" style="--d:.05s">
      <img src="../assets/fabio-cerebro-860.webp" srcset="../assets/fabio-cerebro-440.webp 440w, ../assets/fabio-cerebro-860.webp 860w" sizes="{c.get('foto_sizes', '(max-width:959px) 210px, 700px')}" width="860" height="1091" alt="" loading="eager" fetchpriority="high">{('<video muted loop playsinline preload="none" width="540" height="780" data-webm="../assets/' + c['hero_video'] + '.webm" data-mp4="../assets/' + c['hero_video'] + '.mp4"></video>') if c.get('hero_video') else ''}
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
  <article class="card img rv"><div class="pic"><img src="../assets/cena-transito.webp" width="900" height="1117" loading="lazy" decoding="async" alt="Mulher no ônibus, a caminho do trabalho, estudando pelo fone"></div><span class="num">01</span><h3>Mais horas de estudo sem tirar nenhuma do seu dia</h3><p>Você estuda e revisa no trânsito, na academia e nas tarefas de casa. O tempo que hoje se perde vira matéria revisada.</p></article>
  <article class="card img rv" style="transition-delay:.08s"><div class="pic"><img src="../assets/cena-louca.webp" width="900" height="1117" loading="lazy" decoding="async" alt="Homem lavando a louça à noite enquanto ouve uma aula"></div><span class="num">02</span><h3>Direção para o seu concurso</h3><p>Você sabe o que estudar hoje, o que mais pesa na sua prova e o que pode ficar para depois. Acaba o cronograma impossível.</p></article>
  <article class="card img rv" style="transition-delay:.16s"><div class="pic"><img src="../assets/cena-noite.webp" width="900" height="1117" loading="lazy" decoding="async" alt="Mãe estudando na cozinha às dez da noite, com o filho dormindo no quarto ao lado"></div><span class="num">03</span><h3>Constância nas semanas difíceis</h3><p>Você estuda ao lado de gente no mesmo caminho e tem quem te puxe de volta quando a rotina aperta.</p></article>
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
        <figure><img src="../assets/cena-noite.webp" width="900" height="1117" loading="lazy" decoding="async" alt=""><figcaption>Dez da noite</figcaption></figure>
        <figure><img src="../assets/cena-transito.webp" width="900" height="1117" loading="lazy" decoding="async" alt=""><figcaption>No trajeto</figcaption></figure>
        <figure><img src="../assets/cena-louca.webp" width="900" height="1117" loading="lazy" decoding="async" alt=""><figcaption>Em casa</figcaption></figure>
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
    <div class="bio-photo rv"><img src="../assets/fabio-bracos-cruzados.webp" width="966" height="1200" loading="lazy" decoding="async" alt="Fábio Silva, delegado, professor e mentor do Sou Concurseiro"><div class="tag">Quem vai te mostrar o caminho<b>Fábio Silva</b></div></div>
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


def encontro():
    """Seções da revisão 'não alunos' (07/10): rotina · o que vamos conversar · professor · como participar · dúvidas · final."""
    return """
<div class="encontro">
<section class="velha"><div class="wrap"><div class="velha-grid"><div class="velha-pic"><img src="../assets/velha-livros-560.webp" srcset="../assets/velha-livros-360.webp 360w, ../assets/velha-livros-560.webp 560w" sizes="(max-width:959px) 60vw, 440px" width="560" height="700" loading="lazy" decoding="async" alt="A Velha Forma de Estudar, personagem dos vídeos da Black, segurando uma pilha de livros velhos"><div class="tag">Essa velha é quem mais te atrapalha<b>A Velha Forma de Estudar</b></div></div><div><p class="eyebrow">Conheça a inimiga</p><h2>A <span class="metal">Velha Forma de Estudar</span>.</h2><p class="section-copy">É ela que aparece nos nossos vídeos. Mora na cabeça de quase todo concurseiro e tem um conselho pronto para cada dia de estudo. Todos errados — e é por causa deles que tanta gente boa estuda muito e não passa.</p><ul class="velha-regras"><li><b>Grifa tudo de amarelo</b><p>“Se a página inteira ficou amarela, você estudou.”</p></li><li><b>Só assiste a aula</b><p>“Dá o play, senta… e espera o nome no Diário Oficial.”</p></li><li><b>Copia tudo</b><p>“Estudo de verdade é copiar a aula palavra por palavra. Faltou uma vírgula? Copia de novo.”</p></li><li><b>Espera as horas livres</b><p>“Só estuda quando sobrar tempo. Meia hora por dia? Não serve.”</p></li><li><b>Questão fica pra depois</b><p>“Primeiro a teoria inteira. Errar questão antes da prova é perda de tempo.”</p></li><li><b>Quanto mais material, melhor</b><p>“Apostila, PDF, curso… de todo professor. Não deu tempo de ler? Compra mais.”</p></li><li><b>Estuda só o que gosta</b><p>“O importante é estudar feliz. Matéria difícil? Pula — a banca nunca cobra.”</p></li><li><b>Celular é pra fofocar</b><p>“Estudar é livro e apostila. Aplicativo? Plataforma? Coisa de preguiçoso.”</p></li></ul><p class="velha-fecho">No dia <b>10 de novembro</b>, ao vivo, o Professor Fábio mostra o jeito de estudar que aposenta a velha: feito para quem trabalha, cuida da família e estuda com o tempo que tem.</p><a class="text-cta" href="#form" data-goto-form>Quero ver a nova forma de estudar <span aria-hidden="true">↗</span></a></div></div><div class="velha-fotos"><figure><img src="../assets/velha-mesa-400.webp" width="400" height="300" loading="lazy" decoding="async" alt="A velha com a mesa coberta de livros e uma lupa"><figcaption>“Quanto mais material, melhor.”</figcaption></figure><figure><img src="../assets/velha-relogio-400.webp" width="400" height="300" loading="lazy" decoding="async" alt="A velha mostrando um relógio de bolso"><figcaption>“Só estuda quando sobrar tempo.”</figcaption></figure></div></div></section>
<section class="routine"><div class="wrap"><p class="eyebrow">A vida não espera</p><div class="section-heading"><h2>Você quer começar.<br>Mas por onde?</h2><p>Talvez a vontade de mudar já esteja aí. O que falta é encontrar um jeito de estudar no meio da vida que você tem hoje.</p></div><div class="three-cards"><article><div class="pic"><img src="../assets/s2-trabalho-640.webp" srcset="../assets/s2-trabalho-400.webp 400w, ../assets/s2-trabalho-640.webp 640w" sizes="(max-width:959px) 100vw, 400px" width="640" height="480" loading="lazy" decoding="async" alt="Mulher cansada à mesa depois do trabalho, tentando estudar"></div><span>01 / TRABALHO</span><h3>O dia termina.<br>A energia também.</h3><p>Depois do expediente e do deslocamento, estudar parece mais uma tarefa impossível de encaixar.</p></article><article><div class="pic"><img src="../assets/s2-familia-640.webp" srcset="../assets/s2-familia-400.webp 400w, ../assets/s2-familia-640.webp 640w" sizes="(max-width:959px) 100vw, 400px" width="640" height="480" loading="lazy" decoding="async" alt="Família em casa, com o estudo precisando conviver com a rotina"></div><span>02 / FAMÍLIA</span><h3>Há pessoas que<br>contam com você.</h3><p>A casa, os filhos e as responsabilidades continuam. O estudo precisa conviver com tudo isso.</p></article><article><div class="pic"><img src="../assets/s2-direcao-640.webp" srcset="../assets/s2-direcao-400.webp 400w, ../assets/s2-direcao-640.webp 640w" sizes="(max-width:959px) 100vw, 400px" width="640" height="480" loading="lazy" decoding="async" alt="Pilha de materiais e dúvida sobre por onde começar"></div><span>03 / DIREÇÃO</span><h3>Muito conteúdo.<br>Pouca clareza.</h3><p>Entre tantas matérias e conselhos, fica difícil saber o que fazer primeiro — e o que pode esperar.</p></article></div></div></section>
<section class="value"><div class="wrap reveal-grid"><div><p class="eyebrow">O que vamos conversar</p><h2>Um começo com direção.<br><span class="blue">Uma rotina possível.</span></h2><p class="section-copy">O encontro é um convite para organizar seus próximos passos na preparação para concursos, mesmo que você esteja começando agora.</p><a class="text-cta" href="#form" data-goto-form>Quero dar o primeiro passo <span aria-hidden="true">↗</span></a></div><ol class="steps steps-pic"><li><div><b>Entender por onde começar</b>Como olhar para o seu momento e definir os primeiros passos da preparação.</div><img src="../assets/s3-comecar-320.webp" srcset="../assets/s3-comecar-200.webp 200w, ../assets/s3-comecar-320.webp 320w" sizes="96px" width="320" height="320" loading="lazy" decoding="async" alt=""></li><li><div><b>Escolher suas prioridades</b>O que considerar para estudar com mais direção, sem tentar abraçar tudo de uma vez.</div><img src="../assets/s3-prioridades-320.webp" srcset="../assets/s3-prioridades-200.webp 200w, ../assets/s3-prioridades-320.webp 320w" sizes="96px" width="320" height="320" loading="lazy" decoding="async" alt=""></li><li><div><b>Encontrar espaço na rotina</b>Como pensar em um plano possível para quem trabalha e cuida da família.</div><img src="../assets/s3-rotina-320.webp" srcset="../assets/s3-rotina-200.webp 200w, ../assets/s3-rotina-320.webp 320w" sizes="96px" width="320" height="320" loading="lazy" decoding="async" alt=""></li></ol></div></section>
<section class="authority"><div class="wrap bio"><div class="bio-photo"><img src="../assets/fabio-bracos-cruzados.webp" width="966" height="1200" loading="lazy" decoding="async" alt="Fábio Silva, delegado e professor"><div class="tag">Seu professor neste encontro<b>Fábio Silva</b></div></div><div><p class="eyebrow">Quem vai estar com você</p><h2>Fábio Silva</h2><ul class="roles"><li>Delegado</li><li>Professor</li></ul><p>Fábio Silva é delegado e professor do Sou Concurseiro. Neste encontro, vai conversar com você sobre os primeiros passos e as escolhas que fazem parte da preparação para concursos.</p><p>Você não precisa chegar com tudo resolvido. Traga suas dúvidas e a vontade de começar.</p></div></div></section>
<section class="depoimentos"><div class="wrap"><p class="eyebrow">Quem já passou por aqui</p><div class="section-heading"><h2>Histórias de quem estudou<br>com o Sou Concurseiro.</h2><p>Mensagens e comentários de alunos que chegaram à aprovação estudando com a gente — do jeito que eles mesmos escreveram.</p></div><div class="depo-grid"><img src="../assets/dep-1-560.webp" width="560" height="820" loading="lazy" decoding="async" alt="Depoimento de aluno do Sou Concurseiro"><img src="../assets/dep-9-560.webp" width="560" height="364" loading="lazy" decoding="async" alt="Depoimento de aluno do Sou Concurseiro"><img src="../assets/dep-2-560.webp" width="560" height="197" loading="lazy" decoding="async" alt="Depoimento de aluno do Sou Concurseiro"><img src="../assets/dep-10-560.webp" width="560" height="160" loading="lazy" decoding="async" alt="Depoimento de aluno do Sou Concurseiro"><img src="../assets/dep-5-560.webp" width="560" height="110" loading="lazy" decoding="async" alt="Depoimento de aluno do Sou Concurseiro"><img src="../assets/dep-11-560.webp" width="560" height="162" loading="lazy" decoding="async" alt="Depoimento de aluno do Sou Concurseiro"><img src="../assets/dep-7-316.webp" width="316" height="198" loading="lazy" decoding="async" alt="Depoimento de aluno do Sou Concurseiro"><img src="../assets/dep-8-506.webp" width="506" height="107" loading="lazy" decoding="async" alt="Depoimento de aluno do Sou Concurseiro"></div></div></section>
<section class="participate"><div class="wrap"><p class="eyebrow">Do cadastro ao encontro</p><h2>É simples participar.</h2><ol class="journey journey-pic"><li><img src="../assets/s5-cadastro-600.webp" srcset="../assets/s5-cadastro-400.webp 400w, ../assets/s5-cadastro-600.webp 600w" sizes="(max-width:959px) 100vw, 380px" width="600" height="400" loading="lazy" decoding="async" alt="Formulário de cadastro"><b>Faça seu cadastro</b><p>Preencha WhatsApp, e-mail e escolaridade no formulário desta página.</p></li><li><img src="../assets/s5-grupo-600.webp" srcset="../assets/s5-grupo-400.webp 400w, ../assets/s5-grupo-600.webp 600w" sizes="(max-width:959px) 100vw, 380px" width="600" height="400" loading="lazy" decoding="async" alt="Grupo do WhatsApp"><b>Entre no grupo</b><p>Use o convite da página de confirmação para entrar no grupo do WhatsApp e receber o link.</p></li><li><img src="../assets/s5-aovivo-600.webp" srcset="../assets/s5-aovivo-400.webp 400w, ../assets/s5-aovivo-600.webp 600w" sizes="(max-width:959px) 100vw, 380px" width="600" height="400" loading="lazy" decoding="async" alt="Live ao vivo"><b>Participe ao vivo</b><p>10 de novembro de 2026, às 20h de Brasília (19h de Manaus).</p></li></ol><div class="offer-note"><strong>Um encontro gratuito, com uma oferta ao final.</strong><p>Durante a live, também será apresentada uma oferta de preparação do Sou Concurseiro. Você pode participar do encontro sem compromisso de compra.</p></div></div></section>
<section class="faq"><div class="wrap faq-grid"><div><p class="eyebrow">Antes de se inscrever</p><h2>Suas dúvidas,<br>respondidas.</h2></div><div>
<details><summary>O encontro é on-line e gratuito?</summary><p>Sim. Você participa on-line e o cadastro para o encontro é gratuito.</p></details>
<details><summary>Serve para quem está começando do zero?</summary><p>Sim. Vamos conversar sobre primeiros passos, prioridades e como pensar em uma rotina de estudos possível.</p></details>
<details><summary>Preciso ser aluno do Sou Concurseiro?</summary><p>Não. Este convite é para você que ainda não é aluno e quer conhecer a preparação.</p></details>
<details><summary>Qual é a data e o horário?</summary><p>10 de novembro de 2026, às 20h no horário de Brasília e às 19h no horário de Manaus.</p></details>
<details><summary>Como vou receber o acesso?</summary><p>Após o cadastro, entre no grupo do WhatsApp pelo convite da página de confirmação. O link do encontro será compartilhado no grupo.</p></details>
<details><summary>Haverá uma oferta na live?</summary><p>Sim. Além do conteúdo do encontro, será apresentada uma oferta do Sou Concurseiro. Os detalhes serão revelados na live, e a compra é opcional.</p></details>
</div></div></section>
<section class="final"><div class="wrap"><p class="eyebrow">Seu próximo passo pode começar aqui</p><h2>Sua vida continua.<br><span class="blue">Sua preparação pode começar.</span></h2><p>10/11/2026 · 20h Brasília · 19h Manaus<br>On-line, gratuito e ao vivo com Fábio Silva.</p><a class="btn" href="#form" data-goto-form>Quero participar do encontro <span aria-hidden="true">↗</span></a><p class="note">Cadastre-se e receba o convite para o grupo do WhatsApp.</p></div></section>
</div>
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

# 03/11 (Fábio): v6 = página EXPLICATIVA do Cérebro (Dominei) — o lead entra sabendo o que é a revolução. Topo da v2b com botão no lugar do
# formulário; formulário só no fim, depois de: velha forma · 4 passos com telas reais (geradas do app com dados de demonstração, sem conta de aluno) ·
# VSL do Cérebro (Vturb, carrega só perto da tela) · como entra · para quem é · professor · dúvidas. Mesmo slug/grupo/pixel/régua.
# Até CZ_TETO (fim do T1 da régua do Cérebro) a página promete o acesso grátis pelo WhatsApp; depois, só a live ([data-cz-ate] / [data-cz-depois]).
CZ_TETO = "2026-11-09T23:00:00Z"
CZ_PLAYER = "6ae8f6ceb850e26f93ec6966"
CZ_CONTA = "98f98845-02a5-4e75-a39a-bbafedfa3212"

def cz_tela(nome, alt):
    return (f'<div class="cz-tela"><img src="../assets/cz-{nome}-560.webp" srcset="../assets/cz-{nome}-360.webp 360w, ../assets/cz-{nome}-560.webp 560w" '
            f'sizes="(max-width:959px) 260px, 300px" loading="lazy" decoding="async" alt="{alt}"></div>')

def cerebro_secoes():
    passos = [
        ("edital", "Escolha o seu edital", "O Cérebro é montado para a prova que você vai fazer: PRF, TJ-AM, Polícia Federal, Polícia Civil e Polícia Militar do Amazonas, INSS, ManausPrev, SES-AM, SEDUC-AM, SEDUC-PA e SEMED Manaus.",
         "Tela do Cérebro: escolha do concurso, com a PRF selecionada"),
        ("cerebro", "Faça o diagnóstico e veja o seu cérebro acender", "Um teste de até 20 questões do seu edital. Cada assunto vira um ponto: <b class=\"cz-v\">verde</b> é o que você domina, <b class=\"cz-a\">amarelo</b> está em desenvolvimento, <b class=\"cz-r\">vermelho</b> precisa de atenção.",
         "Tela do Cérebro: mapa do edital da PRF aceso em verde, amarelo e vermelho"),
        ("hoje", "Receba a sua sessão do dia", "Todo dia ele mostra a sua prioridade: o assunto que mais pesa na prova cruzado com o que falta em você, mais as revisões na hora certa. Um botão e você começa.",
         "Tela do Cérebro: prioridade de hoje com os assuntos e o botão para começar"),
        ("material", "Guarde o seu material", "Resumo, foto das anotações, mapa mental, PDF: tudo fica no <b>Meu Material</b>, organizado por disciplina e assunto do edital, e aceso no seu cérebro.",
         "Tela do Cérebro: Meu Material com resumos, fotos e PDFs organizados"),
    ]
    lis = "".join(f'<li class="cz-passo rv"><div class="cz-txt"><span class="cz-n">0{i + 1}</span><h3>{t}</h3><p>{p}</p></div>{cz_tela(n, alt)}</li>'
                  for i, (n, t, p, alt) in enumerate(passos))
    dores = [("O que você já domina", "Você termina um assunto e não sabe se ele ficou ou se vai sumir até a prova."),
             ("O que mais cai", "O edital tem centenas de temas e todos parecem urgentes. Sem saber o peso de cada um, o tempo vai para o lugar errado."),
             ("O que revisar, e quando", "Revisar tudo é impossível. Não revisar é esquecer. Falta alguém dizendo o que voltar a ver hoje.")]
    cards = "".join(f'<article class="card txt rv" style="transition-delay:{i * .08:.2f}s"><span class="num">0{i + 1}</span>{BARS}<h3>{a}</h3><p>{b}</p></article>' for i, (a, b) in enumerate(dores))
    sim = ["Você vai fazer concurso e quer saber exatamente o que estudar.", "Você tem pouco tempo e quer usar cada minuto no que mais pesa na prova.",
           "Você topa estudar um pouco todo dia, pelo celular ou pelo computador.", "Você quer testar de verdade nesta semana, com o seu edital."]
    nao = ["Você procura um atalho para passar sem estudar.", "Você quer só assistir aula, sem responder questão.", "Você não pretende abrir a plataforma antes da live."]
    faq = [("É de graça mesmo?", '<span data-cz-ate>Sim. O cadastro é gratuito e o Cérebro fica liberado para você até terça, 10 de novembro, às 8h de Manaus. Não pedimos cartão.</span><span data-cz-depois hidden>O cadastro é gratuito. O acesso grátis ao Cérebro desta semana já foi encerrado; na live o Professor Fábio mostra como continuar.</span>'),
           ("Preciso instalar alguma coisa?", "Não. O Cérebro abre no navegador do celular ou do computador. Você cria a sua conta pelo link pessoal que chega no seu WhatsApp."),
           ("O meu concurso está lá?", "Hoje são 20 editais: PRF, Polícia Federal (agente e administrativo), Polícia Civil e Polícia Militar do Amazonas, TJ-AM, INSS, ManausPrev, SES-AM, SEDUC-AM, SEDUC-PA e SEMED Manaus. Se o seu não estiver na lista, você pode pedir o seu dentro do Cérebro."),
           ("Preciso ser aluno do Sou Concurseiro?", "Não. Esta semana é para você que ainda não é aluno conhecer a nova forma de estudar."),
           ("O que acontece no dia 10?", "Às 8h de Manaus o acesso grátis termina e o seu progresso fica guardado. Às 20h de Brasília (19h de Manaus), ao vivo no YouTube, o Professor Fábio mostra como continuar estudando com o Cérebro e revela a condição de Black Friday."),
           ("Vai ter oferta na live?", "Sim. Na live será apresentada uma oferta do Sou Concurseiro. A participação é gratuita e a compra é opcional.")]
    det = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq)
    return f"""
<div class="cz">
<section class="glow-top" id="como-era">
  <div class="wrap center">
    <p class="eyebrow rv">A velha forma de estudar</p>
    <h2 class="rv">Você estuda. Mas sabe o que vai <span class="blue">lembrar no dia da prova</span>?</h2>
    <div class="cz-dores">{cards}</div>
    <p class="lead rv" style="margin:36px auto 0">Antes era quase impossível enxergar isso sozinho. Agora, com inteligência artificial, dá. <b>Essa é a Revolução do Estudo.</b></p>
  </div>
</section>
<section id="como">
  <div class="wrap">
    <div class="center">
      <p class="eyebrow rv">O Cérebro por dentro</p>
      <h2 class="rv">Quatro passos. Todo dia você sabe <span class="blue">onde está e o que falta</span>.</h2>
      <p class="lead rv">O nome oficial da plataforma é <b>Dominei</b>. A gente chama de Cérebro porque é isso que ela monta: o mapa da sua cabeça para o seu edital.</p>
    </div>
    <ol class="cz-passos">{lis}</ol>
  </div>
</section>
<section class="cz-vsl">
  <div class="wrap center">
    <p class="eyebrow rv">Veja funcionando</p>
    <h2 class="rv">O Professor Fábio abre o Cérebro e mostra <span class="blue">cada tela</span>.</h2>
    <div class="cz-player rv"><vturb-smartplayer id="vid-{CZ_PLAYER}" style="display:block;margin:0 auto;width:100%;max-width:360px"><div class="vturb-player-placeholder" style="position:relative;width:100%;padding:177.77777777777777% 0 0;z-index:0;background-color:#000"></div></vturb-smartplayer></div>
    <p class="cta-row"><a class="btn" href="#form" data-goto-form><span data-cz-ate>Quero usar o Cérebro de graça</span><span data-cz-depois hidden>Quero participar da live</span></a></p>
  </div>
</section>
<section>
  <div class="wrap center">
    <p class="eyebrow rv">Como você entra</p>
    <h2 class="rv">Do cadastro ao seu <span class="blue">cérebro aceso</span>.</h2>
    <ol class="cz-jornada">
      <li class="rv"><span class="cz-n">01</span><b>Faça o cadastro</b><p>WhatsApp, e-mail e escolaridade, no fim desta página.</p></li>
      <li class="rv"><span class="cz-n">02</span><b>Entre no grupo</b><p>A página seguinte leva você ao grupo do WhatsApp da Revolução. É por lá que saem os avisos e o link da live.</p></li>
      <li class="rv" data-cz-ate><span class="cz-n">03</span><b>Receba o seu acesso</b><p>No seu WhatsApp chega o link pessoal para criar a sua conta no Cérebro. Use de graça até terça, 10/11, às 8h de Manaus.</p></li>
      <li class="rv"><span class="cz-n" data-cz-ate>04</span><span class="cz-n" data-cz-depois hidden>03</span><b>Venha para a live</b><p>Terça, 10 de novembro, às 20h de Brasília (19h de Manaus), no YouTube. O Professor Fábio abre o Cérebro ao vivo e revela a condição de Black Friday.</p></li>
    </ol>
  </div>
</section>
<section class="glow-top">
  <div class="wrap">
    <div class="center"><p class="eyebrow rv">Antes de se cadastrar</p><h2 class="rv">Essa semana é para você?</h2></div>
    <div class="cz-filtro">
      <div class="cz-sim rv"><h3>É para você se</h3><ul>{"".join(f"<li>{t}</li>" for t in sim)}</ul></div>
      <div class="cz-nao rv"><h3>Não é para você se</h3><ul>{"".join(f"<li>{t}</li>" for t in nao)}</ul></div>
    </div>
  </div>
</section>
<section>
  <div class="wrap bio">
    <div class="bio-photo rv"><img src="../assets/fabio-bracos-cruzados.webp" width="966" height="1200" loading="lazy" decoding="async" alt="Fábio Silva, delegado, professor e mentor do Sou Concurseiro"><div class="tag">Quem construiu o Cérebro<b>Fábio Silva</b></div></div>
    <div>
      <p class="eyebrow rv">Quem está com você</p>
      <h2 class="rv">Delegado, professor e mentor do Sou Concurseiro.</h2>
      <ul class="roles rv"><li>Polícias</li><li>Tribunais</li><li>Saúde</li><li>Educação</li></ul>
      <p class="rv">Fábio Silva prepara alunos para concursos de polícia, tribunais, saúde e educação. Viu muita gente boa estudar no escuro e desistir sem saber se estava perto ou longe da aprovação.</p>
      <p class="rv">O Cérebro é a resposta que ele construiu para isso: uma forma de estudar em que você enxerga, todo dia, o que já domina e o que falta para a sua prova.</p>
    </div>
  </div>
</section>
<section class="final cz-final" id="cadastro">
  <div class="wrap center">
    <p class="eyebrow rv">Seu cadastro</p>
    <h2 class="rv"><span data-cz-ate>Cadastre-se e <span class="blue">acenda o seu cérebro</span>.</span><span data-cz-depois hidden>Garanta o seu lugar na <span class="blue">live de 10/11</span>.</span></h2>
    <p class="cz-final-sub rv"><span data-cz-ate>Gratuito. O acesso ao Cérebro chega no seu WhatsApp e vale até terça, 10/11, às 8h de Manaus.</span><span data-cz-depois hidden>Gratuito. O link da live sai no grupo do WhatsApp.</span></p>
    {form_card("Quero participar", titulo="Seu lugar na Revolução do Estudo", nota="Cadastro gratuito · Acesso e link da live pelo WhatsApp")}
  </div>
</section>
<section class="cz-faq">
  <div class="wrap">
    <div class="center"><p class="eyebrow rv">Dúvidas</p><h2 class="rv">Antes de entrar.</h2></div>
    <div class="cz-det">{det}</div>
    <p class="cta-row"><a class="btn" href="#form" data-goto-form>Quero participar</a></p>
  </div>
</section>
</div>
<script>(function(){{var fim=Date.parse("{CZ_TETO}");if(Date.now()<fim)return;
document.querySelectorAll("[data-cz-ate]").forEach(function(e){{e.hidden=true}});document.querySelectorAll("[data-cz-depois]").forEach(function(e){{e.hidden=false}})}})();
(function(){{var p=document.querySelector(".cz-player");if(!p)return;var ok=false,go=function(){{if(ok)return;ok=true;var s=document.createElement("script");
s.src="https://scripts.converteai.net/{CZ_CONTA}/players/{CZ_PLAYER}/v4/player.js";s.async=true;document.head.appendChild(s)}};
if("IntersectionObserver" in window){{var io=new IntersectionObserver(function(es){{if(es[0].isIntersecting){{go();io.disconnect()}}}},{{rootMargin:"900px 0px"}});io.observe(p)}}else go();
window.addEventListener("load",function(){{setTimeout(go,6000)}})}})();</script>
"""

CZ_TOPO = ('<div class="cz-topo rv" style="--d:.3s"><a class="btn block" href="#como">Ver como o Cérebro funciona</a>'
           '<a class="cz-ja" href="#form" data-goto-form>Já quero o meu acesso <span aria-hidden="true">↓</span></a>'
           '<p class="form-note">Cadastro gratuito no fim da página · Com Fábio Silva · Sou Concurseiro</p></div>')

CZ_CSS = """
.sub [data-cz-depois][hidden],.sub [data-cz-ate][hidden]{display:none}
.cz-topo{max-width:560px}.cz-topo .btn.block{font-size:16px}
.cz-ja{display:block;text-align:center;margin:14px 0 0;color:#1cc6e6;font-weight:600;font-size:15px;text-decoration:underline;text-underline-offset:3px}
.cz section{padding:84px 0;border-top:1px solid var(--line)}
.cz h3{font-family:var(--font-d);font-weight:800;font-size:clamp(20px,2vw,26px);line-height:1.15;margin:0 0 10px}
.cz [hidden]{display:none!important}
.cz-dores{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:30px;text-align:left}
.cz-dores .card{grid-column:auto;min-height:0;justify-content:flex-start}.cz-dores .card .bars{margin-bottom:18px}
.cz-passos{list-style:none;margin:40px 0 0;padding:0;display:grid;gap:56px}
.cz-passo{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:48px;align-items:center;max-width:900px;margin:0 auto;width:100%}
.cz-passo:nth-child(even) .cz-txt{order:2}
.cz-txt p{color:var(--ink-2);font-size:clamp(16.5px,1.35vw,19px);margin:0}
.cz-n{display:inline-block;font-family:var(--font-d);font-weight:800;font-size:14px;letter-spacing:.14em;color:#1cc6e6;margin:0 0 10px}
.cz-v{color:#2fe08d}.cz-a{color:#ffc93c}.cz-r{color:#ff5d6c}
.cz-tela{border-radius:28px;overflow:hidden;border:1px solid var(--line-2);background:#05070a;box-shadow:0 30px 70px rgba(0,0,0,.55),0 0 50px rgba(0,155,190,.16);max-width:300px;margin:0 auto}
.cz-tela img{display:block;width:100%;height:auto}
.cz-player{max-width:360px;margin:30px auto 0;border-radius:18px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.55),0 0 60px rgba(0,155,190,.18)}
.cz-jornada{list-style:none;padding:0;margin:34px auto 0;max-width:980px;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;text-align:left}
.cz-jornada li{background:linear-gradient(180deg,var(--card-2),var(--card));border:1px solid var(--line);border-radius:var(--r);padding:22px 20px}
.cz-jornada li[hidden]{display:none}
.cz-jornada b{display:block;font-family:var(--font-d);font-size:19px;margin:0 0 8px}
.cz-jornada p{margin:0;color:var(--ink-2);font-size:15.5px}
.cz-filtro{display:grid;grid-template-columns:1fr 1fr;gap:16px;max-width:900px;margin:30px auto 0}
.cz-filtro>div{border-radius:var(--r);padding:24px 22px;border:1px solid var(--line);background:var(--card)}
.cz-sim{border-color:rgba(47,224,141,.35)!important;background:linear-gradient(180deg,rgba(47,224,141,.07),var(--card))!important}
.cz-filtro ul{list-style:none;margin:0;padding:0;display:grid;gap:12px}
.cz-filtro li{position:relative;padding-left:30px;color:var(--ink-2);font-size:16px;line-height:1.4}
.cz-filtro li::before{position:absolute;left:0;top:0;font-weight:800}
.cz-sim li::before{content:"✓";color:#2fe08d}.cz-nao li::before{content:"✕";color:#ff5d6c}
.cz-final .form-card{margin:26px auto 0}
.cz-final-sub{color:var(--ink-2);font-size:17px;max-width:46ch;margin:0 auto}
.cz-det{max-width:760px;margin:26px auto 0}
.cz-det details{border:1px solid var(--line);border-radius:14px;background:var(--card);margin:0 0 10px;padding:0 20px}
.cz-det summary{cursor:pointer;list-style:none;padding:18px 26px 18px 0;font-weight:700;font-size:16.5px;position:relative}
.cz-det summary::-webkit-details-marker{display:none}
.cz-det summary::after{content:"+";position:absolute;right:0;top:14px;font-size:22px;color:#1cc6e6}
.cz-det details[open] summary::after{content:"–"}
.cz-det p{margin:0 0 18px;color:var(--ink-2)}
@media (max-width:959px){
  /* 03/11 (Fábio, print do iPhone): primeira dobra com fontes maiores */
  h1{font-size:27px;line-height:1.14;margin:6px 0 10px}
  .sub{font-size:17px;line-height:1.38;margin:0 0 18px}
  .cz-topo .btn.block{font-size:18px;padding:22px 18px}
  .cz-ja{font-size:17.5px;margin-top:18px}
  .cz-topo .form-note{font-size:14px}
  .cz-topo{margin:0 0 36px}
  .cz section{padding:56px 0}
  .cz-dores{grid-template-columns:1fr}
  .cz-passos{gap:44px}
  .cz-passo{grid-template-columns:1fr;gap:20px;text-align:center}
  .cz-passo:nth-child(even) .cz-txt{order:0}
  .cz-tela{max-width:260px;border-radius:24px}
  .cz-jornada{grid-template-columns:1fr}
  .cz-filtro{grid-template-columns:1fr}
  .cz-final .form-card{text-align:left}
}
@media (max-width:374px){h1{font-size:25px}.sub{font-size:16px}.cz-topo .btn.block{font-size:16.5px}}
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
COPY["v3"] = dict(COPY["v2"], fx="synapse")  # v3 = v2 + rede de sinapses (21st.dev · Interactive Synapse Network, portada)
COPY["v4"] = dict(COPY["v2"], fx="aether")   # v4 = v2 + éter de partículas (21st.dev · Aether Flow Hero, portado)
COPY["v5"] = dict(COPY["v3"], encontro=True)  # v5 = hero da v3 (sinapses) + seções da revisão "não alunos" (Codex 07/10)

# 18/10 (Fábio): /bio = cópia da v5 p/ o link da bio dos perfis do Instagram. Sem UTM na URL, o cadastro ganha
# utm_source=instagram_bio (o Data Core classifica como instagram_organico) e utm_content=bio (versão).
COPY["bio"] = dict(COPY["v5"], utm={"utm_source": "instagram_bio", "utm_medium": "organico", "utm_campaign": "black-revolucao-bio"},
                   hero_video="fabio-cerebro-loop")   # 18/10: animação do Higgsfield em loop mudo (150 KB), foto como capa; só depois do load
COPY["alunos"] = dict(COPY["v4"],   # 18/10 (Fábio): "replicando a v4" p/ ALUNOS — live terça 27/10 20h, grupo dos alunos, só WhatsApp + e-mail
    h1='A Revolução do Estudo chega <span class="metal">primeiro</span> para quem já é aluno.',
    sub="Terça, 27 de outubro, às 20h de Brasília, o Professor Fábio mostra ao vivo, só para alunos, a nova forma de estudar para concursos. O link da live sai no grupo dos alunos.",
    slug="black-revolucao-alunos", grupo="https://sndflw.com/i/4OSYf8OR5Ac5eJh0UGBk", data="27 de outubro · 20h", live="2026-10-27T20:00:00-03:00",
    obrigado="../obrigado-alunos/", sem_escolaridade=True,
    title="Black · A Revolução do Estudo — 27 de outubro, 20h, ao vivo, só para alunos",
    desc="Terça, 27 de outubro, às 20h, ao vivo e só para quem já é aluno: a nova forma de estudar para concursos. O link sai no grupo dos alunos.")
# 21/10 (Fábio): v2 SEM contador e com o topo do celular no padrão da página da Escola da Bel (lp.escoladabel.com/bffv1126-cap-mads-v1):
# contador em pílula por cima da foto, foto grande centralizada, logo + pílula de data sobre a foto, título e subtítulo centralizados
# com destaque. Formulário igual, sem caixinha de LGPD. CSS só da v2, embutido na própria página (assets/v2-topo.css).
# Definido aqui, depois das derivadas, para v3/v4/v5/bio/alunos NÃO herdarem.
COPY["v2"] = dict(COPY["v2"], topo_ref=True, sem_contador=True, foto_sizes="(max-width:959px) 270px, 700px",
    data='10 de novembro<span class="sep"> · </span><span class="hr">20h</span>',   # 21/10: no celular quebra em linhas (logo e data ao lado da cabeça); no desktop lê igual
    sub='No dia 10 de novembro, irei revelar ao vivo a preparação que faz o estudo caber na rotina de quem trabalha, cuida da família e tem pouco tempo. <strong class="hl">Você passa a estudar nos momentos que hoje perde, sabe todo dia o que precisa estudar para a sua prova e não se prepara mais sozinho.</strong>')
# 21/10 (Fábio): v2b, v2c e v2d = cópias da v2 (mesmo topo, sem contador, mesmo formulário, mesmo slug/grupo/pixel/régua)
# trocando só título e subtítulo — teste de copy. A versão vai no cadastro (answers.versao = v2b/v2c/v2d) p/ comparar no painel.
COPY["v2b"] = dict(COPY["v2"],
    h1='Você não precisa ter uma vida diferente para passar em um concurso. Precisa de uma <span class="metal">forma diferente de estudar</span>.',
    sub="Descubra no dia 10 de novembro como construir uma preparação que funciona mesmo para quem trabalha o dia inteiro, cuida da família e tem pouco tempo disponível.")
COPY["v2c"] = dict(COPY["v2"],
    h1='O problema não é que você tem pouco tempo para estudar. É que ensinaram você a estudar <span class="metal">como se tivesse o dia inteiro livre</span>.',
    sub="Dia 10 de novembro, descubra uma nova forma de preparação que combina planejamento, música, tecnologia e acompanhamento para fazer seus estudos caberem na sua rotina.",
    css_extra="@media (max-width:959px){h1{font-size:21.5px}}@media (max-width:374px){h1{font-size:20.5px}}")   # título mais longo: 4 linhas no celular
COPY["v2d"] = dict(COPY["v2"],
    h1='E se você pudesse estudar para concurso até nos momentos em que hoje <span class="metal">acredita não ter tempo</span>?',
    sub="Uma nova forma de estudar está chegando. No dia 10 de novembro, descubra como transformar momentos esquecidos da sua rotina em oportunidades de aprendizagem, com música, inteligência artificial e uma comunidade ao seu lado.",
    css_extra="@media (max-width:959px){h1{font-size:22px}}@media (max-width:374px){h1{font-size:21px}}")
# 21/10 (Fábio): TESTE DA V4 — o link /v4 das campanhas fica igual; quem abre cai por sorteio (20% cada) em v4, v2, v2b, v2c ou v5.
# Script inline no topo do <head> da v4 (antes de qualquer CSS): sorteio fixo por visitante (30 dias), leva UTMs/fbclid/gclid e marca ?ab=v4
# p/ o cadastro gravar answers.teste = "v4" e a visita entrar no bloco "Teste da v4" do painel. Só a v4 recebe o script.
# 28/10 (Fábio): fase 2 do teste — só v2b e v2c, 50% cada (fase 1, 21–28/10: v4, v2, v2b, v2c, v5 a 20%). Quem tinha sorteio antigo
# (v4/v2/v5) é sorteado de novo entre as duas; a própria página (S) só "fica" se estiver na lista.
COPY["v4"] = dict(COPY["v4"], rodizio=("v2b", "v2c"))
# 03/11 (Fábio): fase 3 do teste — v2b × v6 (explicativa do Cérebro), 50% cada. Quem tinha v2c é sorteado de novo entre as duas.
COPY["v4"] = dict(COPY["v4"], rodizio=("v2b", "v6"))
COPY["v6"] = dict(COPY["v2b"], cerebro=True, topo_cta=CZ_TOPO,
    h1='A Revolução do Estudo é estudar com um <span class="metal">Cérebro</span> do seu lado.',
    sub='Uma plataforma que mostra o que você já domina do seu edital, o que estudar hoje e o que revisar. '
        '<strong class="hl" data-cz-ate>Faça o cadastro e use o Cérebro de graça até a live de 10 de novembro.</strong>'
        '<strong class="hl" data-cz-depois hidden>No dia 10 de novembro, ao vivo, o Professor Fábio abre o Cérebro e mostra como estudar com ele.</strong>',
    css_extra=CZ_CSS,
    title="A Revolução do Estudo · o Cérebro — de graça até a live de 10 de novembro",
    desc="Conheça o Cérebro: a plataforma que mostra o que você já domina do seu edital, o que estudar hoje e o que revisar. Use de graça até a live de 10 de novembro, 20h.")
RODIZIO = """<script>(function(){try{var A=%s,S=%s,K="black_ab_v4",v=null,s=null;
try{s=JSON.parse(localStorage.getItem(K)||"null")}catch(e){}
if(s&&A.indexOf(s.v)>-1&&Date.now()-s.ts<2592e6)v=s.v;
if(!v){v=A[Math.floor(Math.random()*A.length)];try{localStorage.setItem(K,JSON.stringify({v:v,ts:Date.now()}))}catch(e){}}
window.BLACK_AB="v4";
if(v!==S){window.BLACK_REDIRECT=true;var q=new URLSearchParams(location.search);q.set("ab","v4");location.replace("../"+v+"/?"+q.toString()+location.hash)}
}catch(e){}})();</script>
"""
OBRIGADO_ALUNOS = dict(slug="black-revolucao-alunos", grupo="https://sndflw.com/i/4OSYf8OR5Ac5eJh0UGBk", live="2026-10-27T20:00:00-03:00", versao="obrigado-alunos",
    dia="27/10", data_longa="27 de outubro", data_curta="27 de outubro · 20h (Brasília)", dates="20261027T230000Z/20261028T010000Z",
    quem="o grupo dos alunos no WhatsApp", avisos="os avisos do encontro", auto=4)   # 23/10 (Fábio): também vai sozinha p/ o grupo dos alunos em 4 s
LIVE = "2026-11-10T20:00:00-03:00"
V = "35"
# 18/10 (Fábio): Google Ads (conta 182-909-5948) — Lead superior R$ 30 / médio R$ 10, só nas páginas de NÃO alunos
GADS = {"id": "AW-646244794", "sup": "AW-646244794/ulgwCP2W0KEdELrTk7QC", "med": "AW-646244794/lH70CICX0KEdELrTk7QC"}
OG = "https://revolucaodoestudo.com.br/assets/og.jpg"

def page(versao):
    c = COPY[versao]
    out = HEAD.format(title=c.get("title", TITLE), desc=c.get("desc", DESC), og=OG, v=V, anon=ANON, slug=c.get("slug", SLUG), pixel=PIXEL,
                      versao=versao, grupo=c.get("grupo", GRUPO), obrigado=c.get("obrigado", "../obrigado/"), live=c.get("live", LIVE),
                      utm=json.dumps(c.get("utm") or {}), gads=json.dumps(GADS) if c.get("slug", SLUG) == SLUG else "null")
    # so_dobra1: página só com a primeira dobra (pedido do Fábio 07/10 para a v2)
    if c.get("cerebro"): corpo = hero(c) + cerebro_secoes()
    elif c.get("encontro"): corpo = hero(c) + encontro()
    else: corpo = hero(c) if c.get("so_dobra1") else hero(c) + c["dobra2"]() + band() + bio() + final()
    extra = f'<script src="../assets/{c["fx"]}.js?v={V}" defer></script>\n' if c.get("fx") else ""
    if c.get("rodizio"):
        out = out.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n' + RODIZIO % (json.dumps(list(c["rodizio"])), json.dumps(versao)), 1)
    if c.get("topo_ref"):
        out = out.replace("</head>", "<style>" + (ROOT / "assets" / "v2-topo.css").read_text(encoding="utf-8") + c.get("css_extra", "") + "</style>\n</head>", 1)
    # 21/10: v2 sem contador (pedido do Fábio)
    out += ("" if c.get("sem_contador") else topbar()) + "<main>" + corpo + "</main>" + FOOT.format(v=V).replace("</body>", extra + "</body>")
    return out

# 23/10 (Fábio, pedido da equipe): /obrigado/ (NÃO alunos) leva ao grupo sozinha depois de `auto` segundos — o botão continua, e o clique
# antecipa. O Lead do pixel/CAPI e a conversão do Google já dispararam na página de cadastro, antes de chegar aqui; nada muda neles.
# /obrigado-alunos/ idem (auto=4) desde 23/10, a pedido do Fábio.
OBRIGADO_PADRAO = dict(slug=SLUG, grupo=GRUPO, live=None, versao="obrigado", dia="10/11", data_longa="10 de novembro", data_curta="10 de novembro · 20h (Brasília)",
                       dates="20261110T230000Z/20261111T010000Z", quem="o grupo oficial do WhatsApp", avisos="os avisos da Black", auto=4)
def obrigado(o=None):
    o = dict(OBRIGADO_PADRAO, **(o or {}))
    out = HEAD.format(title="Falta um passo: entre no grupo · Black · A Revolução do Estudo", desc=f"Entre no grupo do WhatsApp para receber o link da live de {o['data_longa']}.", og=OG, v=V, anon=ANON, slug=o["slug"], pixel=PIXEL, versao=o["versao"], grupo=o["grupo"], obrigado="./", live=o["live"] or LIVE, utm="{}", gads="null")
    GRUPO_ = o["grupo"]
    auto_msg = ('\n    <p class="small" data-auto-msg>Em <b>%d</b> segundos você vai direto para o grupo. Se preferir, toque no botão.</p>' % o["auto"]) if o.get("auto") else ""
    cal = ("https://calendar.google.com/calendar/render?action=TEMPLATE&text=" + "Black+%C2%B7+A+Revolu%C3%A7%C3%A3o+do+Estudo+%28ao+vivo%29" +
           f"&dates={o['dates']}&details=Live+da+Black+A+Revolu%C3%A7%C3%A3o+do+Estudo.+O+link+sai+no+grupo+do+WhatsApp.&ctz=America/Sao_Paulo")
    out += f"""
<main class="thanks"{(' data-auto="%d"' % o['auto']) if o.get('auto') else ''}>
  <div class="thanks-bg" aria-hidden="true"></div>
  <div class="thanks-card">
    <div class="brand"><img src="../assets/logo-black-revolucao.webp" width="480" height="188" alt="Black · A Revolução do Estudo"></div>
    <h1>Sucesso! Só falta <span class="blue">1 passo</span> para garantir o seu lugar…</h1>
    <div class="bar" role="progressbar" aria-valuenow="84" aria-valuemin="0" aria-valuemax="100"><i></i><b>0%</b></div>
    <p>Clique no botão abaixo e entre n{o['quem']}. É por lá que você recebe <b>o link da live do dia {o['dia']}</b>, o lembrete na hora certa e {o['avisos']}. Sem ele, você pode perder a condição especial.</p>
    <a class="btn" data-grupo href="{GRUPO_}" rel="noopener">Entrar no grupo agora</a>{auto_msg}
    <p class="small">O grupo é silencioso: você só recebe as mensagens enviadas pela minha equipe.</p>
    <div class="date"><span>Salve a data</span><b>{o['data_curta']}</b><a href="{cal}" target="_blank" rel="noopener">Adicionar à agenda</a></div>
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

for v in ("v1", "v2", "v2b", "v2c", "v2d", "v3", "v4", "v5", "v6", "bio", "alunos"):
    d = ROOT / v; d.mkdir(exist_ok=True); (d / "index.html").write_text(page(v), encoding="utf-8")
(ROOT / "obrigado").mkdir(exist_ok=True); (ROOT / "obrigado" / "index.html").write_text(obrigado(), encoding="utf-8")
(ROOT / "obrigado-alunos").mkdir(exist_ok=True); (ROOT / "obrigado-alunos" / "index.html").write_text(obrigado(OBRIGADO_ALUNOS), encoding="utf-8")
(ROOT / "index.html").write_text(ROOT_INDEX, encoding="utf-8")
(ROOT / ".nojekyll").write_text("")
print("ok: v1–v6/, v2b–v2d/, bio/, alunos/, obrigado/, obrigado-alunos/, index.html")
