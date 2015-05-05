var carte;  
var tabMarqueurs = new Array();
var prev_infobulle;
var infowindow = new google.maps.InfoWindow();
var bikesAndStandsAvailable;
function attachContent(marker, data) {	
	google.maps.event.addListener(marker, 'click', function() {
	var aujourdhui = new Date();
	content = data.stationRegion + "<br>"+ data.stationNum + " - " + data.stationName;	
	content += "<br>Vélos disponibles : <span id='availableBikes'></span>";
	content += "<br> Bornes disponibles : <span id='availableStands'></span>/" + data.bornes;
	content += "<form action='/' id='map_form' method='post'>";
	content += "<fieldset>";
    content += "<legend>Faire une prévision</legend>";
    content += "<input type='hidden' name='station' id='stationNum' value=" + data.stationNum + " />";
    content += "<input type='hidden' name='nbBornes' id='nbBornes' value=" + data.borens + " />";
	content += "<label id='date'>Date</label>";
	content += "<select name='day_day' id='day_day'>";
    content += remplirDate(1,31,1, aujourdhui.getDate());
    content += "</select>";
    content += "<select name='day_month' id='day_month'>";
    content += remplirMois((aujourdhui.getMonth()+1));
    content += "</select>";
    content += "<select name='day_year' id='day_year'>";
    content += remplirDate(aujourdhui.getFullYear(),aujourdhui.getFullYear(),1, aujourdhui.getFullYear());
    content += "</select><br>";
    content += "<label type='number' for='hour'>Heure</label>";
    content += "<select name='hour_hour' id='hour_hour'>"
    content += remplirDate(00,23,1, aujourdhui.getHours());
    content += "</select>h";
    content += "<select name='hour_minute' id='hour_minute'>";
    var minutes = aujourdhui.getMinutes();
    content += remplirDate(00,55,5, (minutes-(minutes%5)));
    content += "</select>m<br>";

	content += "</fieldset>";
	content += "<input type='button' name='valider' value='valider' class='btn btn-primary btn-lg btn-block'  onclick=\"prevision('map_form');\">";
	content += "</form>";
	infowindow.setContent(content);
	$.ajax({
		url : "search/lastKnownStatus/"+ data.stationNum,
		type: "GET",
		data:{
			format:'json'
		}
	}).success(function(response){
		document.getElementById('availableBikes').innerHTML = response.bikes;
		document.getElementById('availableStands').innerHTML = response.stands;
	}).fail(function(){
		console.log("fail");
	});
	
	
	console.log(Date());
	
	infowindow.open(marker.get('map'), marker);
	});		
}


function remplirDate(debut, fin, pas, currentDate){
	var content = "";
	for( var cpt = debut; cpt <= fin; cpt += pas){
		content += "<option value=" + cpt;
		if(cpt == currentDate){
			content += " selected";
		}
		content +=  " >" + cpt + "</option>";
	}
	return content;
}
function remplirMois(currentDate){
	var content = "";
	for(var cpt = 1; cpt <= 12; cpt++){
		content += "<option value=" + cpt;
		if(cpt == currentDate){
			content += " selected";
		}
		content +=  " >";
		switch(cpt){
			case 1: content += "Janvier";
				break;
			case 2: content += "Février";
				break;
			case 3: content += "Mars";
				break;
			case 4: content += "Avril";
				break;
			case 5: content += "Mai";
				break;
			case 6: content += "Juin";
				break;
			case 7: content += "Juiller";
				break;
			case 8: content += "Août";
				break;
			case 9: content += "Semptembre";
				break;
			case 10: content += "Octobre";
				break;
			case 11: content += "Novembre";
				break;
			case 12: content += "Decembre";
				break;
		}
		content +=  "</option>";
		
	}
	return content;
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
	console.log(data);
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
	        alert(xhr.status +  " - "  +ajaxOptions + " - " + thrownError);
	        $('#imgWait').hide(); // Hide the loading image
	        $('#fade').css({'filter' : 'alpha(opacity=80)'}).fadeOut(); // Fade out the fade layer 
	        $('body').remove('<div id="fade"></div>'); // Remove the fade layer to bottom of the body tag.
      	}
	});



}
