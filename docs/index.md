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
  <div class="hero-graphic">
    {% if site.student.photo %}
      <img class="hero-photo" src="{{ site.student.photo | relative_url }}" alt="{{ site.student.name | escape }}">
    {% else %}
      <div class="orb one" aria-hidden="true"></div><div class="orb two" aria-hidden="true"></div><div class="orb three" aria-hidden="true"></div>
      <span class="hero-monogram" aria-hidden="true">{{ site.student.name | slice: 0 | upcase }}</span>
    {% endif %}
  </div>
</section>

<section class="content-section" aria-labelledby="journey-title">
  <div class="section-title">
    <div>
      <span class="eyebrow">ACADEMIC DEVELOPMENT</span>
      <h2 id="journey-title">My Research Journey</h2>
    </div>
    <p>Four broad stages guide my master's study.</p>
  </div>
  <div class="timeline">
    {% assign semesters = site.semesters | sort: "order" %}
    {% for stage in semesters %}
    <article class="stage">
      <span class="stage-no">{% if stage.order < 10 %}0{{ stage.order }}{% else %}{{ stage.order }}{% endif %}</span>
      <div class="stage-body">
        <div class="stage-period">{{ stage.period | default: "Semester" | escape }}</div>
        <h3>{{ stage.title | escape }}</h3>
        <p>{{ stage.description | default: stage.summary | escape }}</p>
        {% if stage.image %}
        <figure class="stage-figure">
          <img src="{{ stage.image | relative_url }}" alt="{{ stage.title | escape }}" loading="lazy">
          {% if stage.caption %}
          <figcaption>{{ stage.caption | escape }}</figcaption>
          {% endif %}
        </figure>
        {% endif %}
      </div>
    </article>
    {% endfor %}
  </div>
</section>

<section class="content-section" aria-labelledby="showcase-title">
  <div class="section-title">
    <div>
      <span class="eyebrow">SHOWCASE</span>
      <h2 id="showcase-title">Research Showcase</h2>
    </div>
    <p>Featured research projects, tools, and publications.</p>
  </div>

  <div class="showcase-grid">
    {% assign showcases = site.showcases | sort: "order" %}
    {% for item in showcases %}
    <article class="showcase-card">
      {% if item.image %}
      <img class="showcase-img" src="{{ item.image | relative_url }}" alt="{{ item.title | escape }}" loading="lazy">
      {% endif %}
      <div class="showcase-content">
        {% if item.tags and item.tags.size > 0 %}
        <div class="showcase-tags">
          {% for tag in item.tags %}
          <span class="showcase-tag">{{ tag | escape }}</span>
          {% endfor %}
        </div>
        {% endif %}
        <h3>{{ item.title | escape }}</h3>
        <p>{{ item.summary | default: item.description | escape }}</p>
        <div class="showcase-links">
          {% if item.links and item.links.size > 0 %}
            {% for link in item.links %}
            <a href="{{ link.url }}" target="_blank" rel="noopener">{{ link.label | escape }} &rarr;</a>
            {% endfor %}
          {% endif %}
          {% if item.content and item.content.size > 20 %}
            <a href="{{ item.url | relative_url }}">Read Details &rarr;</a>
          {% endif %}
        </div>
      </div>
    </article>
    {% endfor %}
  </div>
</section>
