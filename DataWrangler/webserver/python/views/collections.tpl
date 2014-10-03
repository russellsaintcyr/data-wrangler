<html>
	<head>
		<title>Collections in {{dbname}} - MongoDB Browser</title>
	</head>
	<body bgcolor="white">
		<h3>Collections in database {{dbname}}:</h3>
		<a href="/">Show all databases</a>
		<p>
		<div class="name">
		%for coll in collections:
			<li><a href="{{dbname}}/{{coll}}">{{coll}}</a>
		%end
		</div>
	</body>
</html>

