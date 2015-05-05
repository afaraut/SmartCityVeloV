var carte;  
var tabMarqueurs = new Array();
var prev_infobulle;
var infowindow = new google.maps.InfoWindow();

function attachContent(marker, data) {	
	google.maps.event.addListener(marker, 'click', function() {
	var content = data.stationName;
	content += data.stationRegion + "<br>"+ data.stationNum + " - " + data.stationName;	
	content += "<br>Vélos disponibles : "; // + data.availableBike
	content += "<br> Bornes disponibles : "; //+ data.availableStands
	content += "<hr>";
	content += "<form action=\"{% url 'search.views.home' %}\" method='post'>";
	content += "<fieldset>";
    content += "<legend>Faire une prévision</legend>";
	content += "<label id='date'>Date</label>";
	content += "<input type='number' id='date' min=1 max=31 value=1 style='width:40px;height:20px;'/>";
	content += "<input type='number' id='date' min=1 max=12  value=5 style='width:40px;height:20px;'/>";
	content += "<input type='number' id='date' min=2015 max= 2015 value=2015 style='width:60px;height:20px;'/><br>";
	content += "<label id='heure'>Heure</label>";
	content += "<input type='text' id='hour' style='width:30px;height:20px;'>h<input type='text' id='hour' style='width:30px;height:20px;'>m"
	content += "<br><button class='btn btn-primary btn-sm '>Valider</button></form>";
	content += "</fieldset>";
	content += "</form>";
	
	infowindow.setContent(content);
	infowindow.open(marker.get('map'), marker);
	});		
}

function theposition(){

			var pos;
			if (navigator.geolocation)
			{
			  navigator.geolocation.getCurrentPosition(function(position)
			  {
				var center = new google.maps.LatLng(position.coords.latitude, position.coords.longitude)
				carte.setCenter(center);
				var marker = new google.maps.Marker({
				position: new google.maps.LatLng(position.coords.latitude,position.coords.longitude),//coordonnée de la position du clic sur la carte 
				map: carte
				});
			  });
			}
}


function initialiser() {
var latlng = new google.maps.LatLng(45.750000,  4.850000);

var image = {
	url : "static/velo2.png",
	size: new google.maps.Size(32, 32)
}

var image = {
	url : "static/velo2.png",
	size: new google.maps.Size(32, 32)
}


//objet contenant des propriétés avec des identificateurs prédéfinis dans Google Maps permettant
//de définir des options d'affichage de notre carte
var options = {
	center: latlng,
	zoom: 15,
	mapTypeId: google.maps.MapTypeId.ROADMAP
};
carte = new google.maps.Map(document.getElementById("map-canvas"), options); 
	$.ajax({
		type: "POST",
		url: "/search/stations",
		traditional: true,
		success: function(data) {
			 for(var key in data){
				var marker = new google.maps.Marker({
				position: new google.maps.LatLng(data[key].stationLat, data[key].stationLong),//coordonnée de la position du clic sur la carte 
				title: data[key].stationRegion + " - " + data[key].stationNum + " - " + data[key].stationName,
				icon: image,
				
				map: carte//la carte sur laquelle le marqueur doit être affiché
				});		
				attachContent(marker, data[key]);
				tabMarqueurs.push(marker); 
			}
			theposition();
		}
	});

}

 function getDataFromForm(Form) {
    var data="";
    var key=0;
    for (key=1;key<Form.elements.length;key++) {      
        data+=escape(Form.elements[key].name)+"="+escape(Form.elements[key].value)+"&";
    }
    return data.substr(0, data.length-1);
}


function prevision(idFormulaire){
	formulaire = document.getElementById(idFormulaire);
	data = getDataFromForm(formulaire);
	$('#imgWait').show(); // Show the loading image
    $('body').append('<div id="fade"></div>'); // Add the fade layer to bottom of the body tag.
    $('#fade').css({'filter' : 'alpha(opacity=80)'}).fadeIn(); // Fade in the fade layer 
	$.ajax({
		type:'POST',
		url: "/search/search",
		traditional: true,
		data:data,

		success: function(data){
			document.getElementById('reponse').innerHTML ="<hr>Vélos disponibles : " +  data[0] + "<br> Bornes disponibles : " + data[1];
			$('#imgWait').hide(); // Hide the loading image
        	$('#fade').css({'filter' : 'alpha(opacity=80)'}).fadeOut(); // Fade out the fade layer 
        	$('body').remove('<div id="fade"></div>'); // Remove the fade layer to bottom of the body tag.
		},
		error: function (xhr, ajaxOptions, thrownError) {
	        alert(xhr +  " - "  +ajaxOptions + " - " + thrownError);
	        $('#imgWait').hide(); // Hide the loading image
	        $('#fade').css({'filter' : 'alpha(opacity=80)'}).fadeOut(); // Fade out the fade layer 
	        $('body').remove('<div id="fade"></div>'); // Remove the fade layer to bottom of the body tag.
      	}
	});



}
