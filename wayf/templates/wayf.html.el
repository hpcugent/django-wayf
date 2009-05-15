{% extends "base.html" %}
{% load i18n %}
{% block header %}Επιλογή οικείου φορέα{% endblock %}
{% block content %}
<p>Σε αυτή τη σελίδα μπορείτε να καθορίσετε έναν προεπιλεγμένο Οικείο Φορέα που μπορεί να σας πιστοποιήσει για πρόσβαση σε υπηρεσίες της Ομοσπονδίας AAI του ΕΔΕΤ. Η ρύθμιση θα αποθηκευτεί στο συγκεκριμένο web browser και θα έχει ως αποτέλεσμα να μεταφέρεστε αυτόματα στο σύστημα ταυτοποίησης του ιδρύματός σας όταν προσπελαύνετε AAI-πόρους.</p>
<div id="idpform">
<form method="post" action="/wayf/set">
	<select name="user_idp">
	{% include "idp_dropdown.html" %}
	</select>
	<input type="submit" value="{% trans "Confirm" %}" /><br />
	{% if request.GET %}
	<script type="text/javascript">
	function toggleRadios(){
		var state;
		state = ! document.forms[0].save.checked;
		document.getElementById('permsave').disabled = state;
		document.getElementById('sesssave').disabled = state;
	}
	</script>
	<div id="userprefs">
	<input type="hidden" name="queryString" value="{{ request.GET.urlencode }}" />	<input type="checkbox" name="save" value="1" onclick="toggleRadios();"/>Αποθήκευση της προτίμησης:</input>
	<input type="radio" id="sesssave" name="savetype" value="session" disabled="true" checked="true" />Μέχρι να κλείσω το browser</input>
	<input type="radio" id="permsave" name="savetype" value="perm" disabled="true" />Μόνιμα</input><br />
	</div>
	{% else %}
	<input type="hidden" name="save" value="true" />
	<input type="hidden" name="savetype" value="perm" />
	{% endif %}
</form>
</div>
{% endblock %}
