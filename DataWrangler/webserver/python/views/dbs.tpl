<html>
	<head>
		<title>MongoDB Browser</title>
	</head>
	<body bgcolor="white">
		<h3>Databases:</h3>
		<div class="name">
		%for db in databases:
			<li><a href="db/{{db}}">{{db}}</a>
		%end
		</div>
	</body>
</html>

