<!DOCTYPE html>
<html lang="en">
<head>
    <title>Fabulous Price Finder</title>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">

    <link href="/static/bootstrap.min.css" rel="stylesheet" media="screen">
    <link href="/static/bootstrap-responsive.css" rel="stylesheet">
    <link href="/static/bootstrap.css" rel="stylesheet">

    <style type="text/css">
	body {
        padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
	
      }
	
	/* Custom container */
      .container-narrow {
        margin: 0 auto;
        max-width: 900px;
	border-style: solid;
	border-color: transparent;
	background-color: #D8D8D8;
	z-index: 9;
	height : 100%;
	-moz-border-radius: 15px;
	border-radius: 15px;
	
      }
      .container-narrow > hr {
        margin: 30px 0;
      }

	.sidebar-nav {
        padding: 20px 0;
      }

      @media (max-width: 980px) {
        /* Enable use of floated navbar text */
        .navbar-text.pull-right {
          float: none;
          padding-left: 5px;
          padding-right: 5px;
        }
	
	 #myModal .modal-body {
  max-height: 600px;
   }

   #myModal {
  width: 700px; /* SET THE WIDTH OF THE MODAL */
}
	
  </style>



<style type="text/css" id="holderjs-style">.holderjs-fluid {font-size:16px;font-weight:bold;text-align:center;font-family:sans-serif;margin:0}</style>
</head>

<body>

  <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          
          <a class="brand pull-left" href="/"><em>Fabulous Price Finder </em><small>v2.0</small></a>
	  
          <div class="nav-collapse collapse">

          </div><!--/.nav-collapse -->
        </div>
      </div>
  </div>  <!-- end of div for nav bar-->

  <div id="error"></div>

  <div class="container">
  <div class="hero-unit">
  
  <h2>Items to Watch:</h2>
  <h4>Record count: {{totinf}}</h4>
  <div style="background-color:white">
  	<table class="table table-hover">
  	<tr>
  	<td>Name</td><td>Url</td><td>Price field id</td><td>Current Price</td><td> </td>
  	</tr>
		%include
  	</table>
  </div>
  	<br>
  <div style="text-align:center">
  	<!-- </form> -->
  	
  	<!-- unable to get Delete All to work with cloudant, so temporarily removing this feature
  	<p style="text-align:center">
  		<form action="/clearall" method="post">
  		<input type="submit" value="Delete All Records" class="btn btn-danger">
  		</form>
	</p> -->
	 
  </div>
  
  </div> <!-- end of the hero-unit-->
  </div> <!-- end of the container-->


</body>
</html>
