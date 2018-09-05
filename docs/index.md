---
layout: base
---

<div class="alert alert-sigai-semester-description mb-3">
	<h4 class="alert-heading"> Welcome to {{ site.title }}! </h4>
	<p class="mb-0"> {{ site.description }}</p>
</div>

{% comment %} 24*7*60*60 = 604,800 {% endcomment %}
{% assign this_week = site.time | date: "%s" | plus: 604800 %}

{% for post_ in site.posts %}
    {% assign post_date = post_.date | date: "%s" | plus: 0 %}
    {% assign post = post_ %}
    {% if post_date < this_week %} 
        {% break %}
    {% endif %}
{% endfor %}

{% assign semester = post.categories | first %}

<div class="d-lg-flex justify-content-between">
    <h2 class="mb-lg-0 text-center text-lg-left"> The next lecture: </h2>
    <div class="d-flex flex-lg-row flex-column">
        <a class="btn btn-success d-lg-flex d-block ml-lg-2 mt-2 mt-lg-0" href="{{ site.baseurl }}/{{ semester }}/signin"> Check-in for this meeting </a>
        <a class="btn btn-primary d-lg-flex d-block ml-lg-2 mt-2 mt-lg-0" href="{{ site.baseurl }}/{{ semester }}">View semester syllabus</a>
    </div>
</div>

<div class="my-3 p-3 bg-white rounded box-shadow">
    <ul class="list-unstyled">
        {% include syllabus-card.html %}
    </ul>
</div>

