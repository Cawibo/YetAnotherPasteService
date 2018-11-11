<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/pastes">
	<html>
		<head>
			<title>YAPS</title>
			<link rel="stylesheet" type="text/css" href="css/style.css"/>
			<meta name="author" content="Caroline Borg"/>
		</head>
		<body>
			<form action="/upload" method="post">

				name: <input type="text" name="name"/><br/>
				type: <input type="text" name="type"/><br/>
				content: <input type="text" name="content"/><br/>
				<input type="submit" value="paste!"/>

			</form>
			
			<ul>
				<xsl:apply-templates select="paste" /> 
			</ul>

			<iframe src="/update" name="hidden_iframe_upload" class="hide"></iframe>
		</body>
	</html>

</xsl:template> 

<xsl:template match="paste">
	<xsl:variable name="name" select="name"/>
	<xsl:variable name="content" select="content"/>
	<xsl:variable name="id" select="id"/>

	<li>
		<form id="update_form" action="/update" method="post" target="hidden_iframe_upload">
			<input type="hidden" name="id" value="{id}"/>
			<input type="text" name="name" value="{name}"/><xsl:value-of select="type"/><br/>
			<textarea form="update_form" name="content"><xsl:value-of select="content"/></textarea><br/>
			<input type="submit" value="paste!"/>
		</form>
	</li>

</xsl:template>


</xsl:stylesheet>