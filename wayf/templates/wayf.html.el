{% extends "base.html" %}
{% load i18n %}
{% block header %}Επιλογή οικείου φορέα{% endblock %}
{% block content %}
<p>Σε αυτή τη σελίδα μπορείτε να καθορίσετε έναν προεπιλεγμένο Οικείο Φορέα που μπορεί να σας πιστοποιήσει για πρόσβαση σε υπηρεσίες της Ομοσπονδίας AAI του ΕΔΕΤ. Η ρύθμιση θα αποθηκευτεί στο συγκεκριμένο web browser και θα έχει ως αποτέλεσμα να μεταφέρεστε αυτόματα στο σύστημα ταυτοποίησης του ιδρύματός σας όταν προσπελαύνετε AAI-πόρους.</p>
<form method="post" action="/wayf/set">
	<select name="user_idp">
	{% for category, insts in  idplist %}
		<optgroup label="{{ category }}">
		{% for inst in insts %}
			<option value="{{ inst.id }}">{{ inst.name }}</option>
		{% endfor %}
		</optgroup>
	{% endfor %}
	</select>
	<input type="submit" value="{% trans "Save Selection" %}" />
</form>
{% endblock %}
