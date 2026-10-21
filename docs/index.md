---
layout: default
title: Graduate Research Journey
---

<div class="eyebrow">GRADUATE RESEARCH JOURNEY</div>

<section class="hero">
  <div>
    <span class="pill">{{ site.student.degree | escape }}</span>
    <h1>{{ site.student.name | escape }}</h1>
    <p class="lead">{{ site.student.summary | escape }}</p>
    <div class="metadata">
      <span><strong>Affiliation:</strong> {{ site.student.lab | escape }} · NTUT</span>
      <span><strong>Joined:</strong> {{ site.student.joined | escape }}</span>
      <span><strong>Research interests:</strong> {{ site.student.interests | escape }}</span>
    </div>
    <a class="primary-link" href="{{ '/meetings/' | relative_url }}">Browse regular meetings <span aria-hidden="true">&#8594;</span></a>
  </div>
  <div class="hero-graphic" aria-hidden="true"><div class="orb one"></div><div class="orb two"></div><div class="orb three"></div><span class="hero-monogram">{{ site.student.name | slice: 0 | upcase }}</span></div>
</section>

<section class="content-section" aria-labelledby="journey-title">
  <div class="section-title">
    <div>
      <span class="eyebrow">ACADEMIC DEVELOPMENT</span>
      <h2 id="journey-title">My Research Journey</h2>
    </div>
    <p>Four broad stages guide my master's study. They can evolve as my research progresses.</p>
  </div>
  <div class="timeline">
    <article class="stage"><span class="stage-no">01</span><div><div class="stage-period">Semester 1</div><h3>Building foundations</h3><p>Python, statistical learning, literature review, and reproducible analysis.</p></div></article>
    <article class="stage"><span class="stage-no">02</span><div><div class="stage-period">Semester 2</div><h3>Defining a research problem</h3><p>Research questions, baseline models, and initial experiments.</p></div></article>
    <article class="stage"><span class="stage-no">03</span><div><div class="stage-period">Semester 3</div><h3>Developing and validating methods</h3><p>Method improvement, evaluation, and research communication.</p></div></article>
    <article class="stage"><span class="stage-no">04</span><div><div class="stage-period">Semester 4</div><h3>Thesis and research outputs</h3><p>Thesis writing, defense, and future research directions.</p></div></article>
  </div>
</section>

<section class="cta-card" aria-labelledby="meetings-title">
  <div><span class="eyebrow">ONGOING RESEARCH</span><h2 id="meetings-title">Regular Meetings</h2><p>Brief research check-ins submitted before each supervision meeting. Each date opens a password-protected meeting record derived from a private <code>.rst</code> file.</p></div>
  <a class="secondary-link" href="{{ '/meetings/' | relative_url }}">View meeting records &#8594;</a>
</section>
