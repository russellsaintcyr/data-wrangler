<html>
	<head>
		<title>Collections - MongoDB Browser</title>
	</head>
	<body bgcolor="white">
		<h3>First 10 documents in collection {{collname}}</h3>
		[{{count}} documents total]
		<br><a href="/db/{{dbname}}">Show collections for {{dbname}}</a>
		<br><a href="/">Show databases</a>
		<p>
		<div class="name">
		<table border=2>
			<tr>
		%for key in keys:
				<th>{{key}}</th>
		%end
			</tr>
		%for coll in collection:
			<tr>
			%for key in coll.keys():
				<td>{{coll[key]}}</td>
			%end
			</tr>
		%end
		</table>
		</div>
	</body>
</html>

