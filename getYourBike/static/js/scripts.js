var carte;  
var tabMarqueurs = new Array();
var prev_infobulle;
var infowindow = new google.maps.InfoWindow();

function attachContent(marker, data) {	
	google.maps.event.addListener(marker, 'click', function() {
	var content = data.stationName;
	content += data.stationRegion + "<br>"+ data.stationNum + " - " + data.stationName;			; 
	content += "<br><div><div class='modal-content'><div class='modal-header'><h3> Faire une prévision</h3></div><div class='modal-body'><form action=\"{% url 'search.views.home' %}\" method='post' class='form col-xs-6 center-block'><div class='form-group'><label id='jour'>Jour</label><input type='time' id='jour'/><button class='btn btn-primary btn-sm '>Valider</button></div></form></div><div class='modal-footer'>	</div></div></div>";
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
