﻿
<h1>DJCRM Project</h1>

<p>The DJCRM project is a simple Customer Relationship Management (CRM) system built using the Django web framework.</p>

<h2>Setting up environment</h2>

<ol>
	<li>Create a virtual environment and activate it:</li>
	<ul>
		<li><code>python -m venv env</code></li>
		<li><code>source env/bin/activate  # On Unix-based systems</code></li>
		<li><code>env\Scripts\activate  # On Windows</code></li>
	</ul>
	<br>
	<li>Install the required packages using pip:</li>
	<ul>
		<li><code>pip install -r requirements.txt</code></li>
	</ul>
	<br>
	<li>Set up the database by running the following commands:</li>
	<ul>
		<li><code>python manage.py makemigrations</code></li>
		<li><code>python manage.py migrate</code></li>
	</ul>
	<br>
	<li>Create a superuser account:</li>
	<ul>
		<li><code>python manage.py createsuperuser</code></li>
	</ul>
	<br>
	<li>Run the development server:</li>
	<ul>
		<li><code>python manage.py runserver</code></li>
	</ul>
	<br>
	<li>Access the DJCRM application by navigating to <a href="http://127.0.0.1:8000/admin/">http://127.0.0.1:8000/admin/</a> in your web browser.</li>
</ol>
