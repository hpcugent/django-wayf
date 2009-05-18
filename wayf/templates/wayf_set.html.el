{% extends "base.html" %}
{% load i18n %}
{% block header %}{% trans "Select your home institution" %}{% endblock %}
{% block content %}
<p>
Η προεπιλογή ενός Οικείου Φορέα έχει ως αποτέλεσμα ότι δε χρειάζεται πλέον να επιλέγετε τον Οικείο Φορέα σας όταν προσπελαύνετε AAI-πόρους με το συγκεκριμένο web browser.
</p>
<p>
Η καθορισμένη προεπιλογή είναι:
</p>
<div align="center">
<h4>{{ currentidp }}</h4>
<form method="post">
	<input type="hidden" name="clear" value="true" />
	<input type="submit" value="{% trans "Clear" %}" />
</form>
</div>
{% endblock %}
