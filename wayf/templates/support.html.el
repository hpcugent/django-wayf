{% extends "base.html" %}
{% load i18n %}
{% block header %}{% trans "User support" %}{% endblock %}
{% block content %}
{% spaceless %}
Παρουσιάστηκε πρόβλημα κατά τη χρήση της Υποδομής Ταυτοποίησης και Εξουσιοδότησης του ΕΔΕΤ. Παρακαλούμε επικοινωνήστε με τον οικείο φορέα σας{% if not idpname %}.{% else %},{% endif %}
{% if idpname %}
<strong>{{ idpname }}</strong>
{% endif %}
{% if idp.contact.email or idp.contact.telephone %}
, με έναν από τους παρακάτω τρόπους:
{% endif %}
{% endspaceless %}
<ul>

{% if idp.contact.email %}
	<li>email: <a href="mailto:{{ idp.contact.email }}?subject={% trans "Shibboleth Authentication Issue" %}">{{ idp.contact.email }}</a></li>
{% endif %}
{% if idp.contact.telephone %}
	<li>{% trans "Telephone" %}: {{ idp.contact.telephone }}</li>
{% endif %}

</ul>
{% endblock %}
