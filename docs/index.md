---
layout: base
---

<div class="alert alert-sigai-semester-description mb-3">
	<h4 class="alert-heading"> Welcome to {{ site.title }}! </h4>
	<p class="mb-0"> {{ site.description }}</p>
</div>

{% assign today = site.time | date: "%s" | plus: 0 %}

{% for post_ in site.posts %}
    {% assign post_date = post_.date | date: "%s" | plus: 0 %}
    {% assign post = post_ %}
    {% if post_date < today %} 
        {% break %}
    {% endif %}
{% endfor %}

{% assign semester = post.categories | first %}

<div class="d-lg-flex justify-content-between">
    <h2 class="mb-lg-0 text-center text-lg-left"> The next lecture: </h2>
    <a class="btn btn-primary d-lg-flex d-block" href="{{ site.baseurl }}/{{ semester }}">View semester syllabus</a>
</div>

<div class="my-3 p-3 bg-white rounded box-shadow">
    <ul class="list-unstyled">
        {% include syllabus-card.html %}
    </ul>
</div>

