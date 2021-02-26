// TOP SCRIPT TAG
function parse_query_string(query) {
  var vars = query.split("&");
  var query_string = {};
  for (var i = 0; i < vars.length; i++) {
    var pair = vars[i].split("=");
    var key = decodeURIComponent(pair[0]);
    var value = decodeURIComponent(pair[1]);
    // If first entry with this name
    if (typeof query_string[key] === "undefined") {
      query_string[key] = decodeURIComponent(value);
      // If second entry with this name
    } else if (typeof query_string[key] === "string") {
      var arr = [query_string[key], decodeURIComponent(value)];
      query_string[key] = arr;
      // If third or later entry with this name
    } else {
      query_string[key].push(decodeURIComponent(value));
    }
  }
  return query_string;
}
var query = window.location.search.substring(1);
var qs = parse_query_string(query);
//Default country to map upon start
if(Object.keys(qs).length === 1){
  qs.ADM = "ADM0"
  qs.ISO = "AFG"
}
//console.log(qs.ADM)
//console.log(qs.ISO)
function initComparisons() {
  var x, i;
  /*find all elements with an "overlay" class:*/
  x = document.getElementsByClassName("img-comp-overlay");
  //console.log(x);
  for (i = 0; i < x.length; i++) {
    /*once for each "overlay" element:
    pass the "overlay" element as a parameter when executing the compareImages function:*/
    compareImages(x[i]);
    //console.log(x[i]);
  }
  function compareImages(img) {
    var slider, img, clicked = 0, w, h;
    /*get the width and height of the img element*/
    w = img.offsetWidth;
    //console.log('width: '+ w);
    h = img.offsetHeight;
    //console.log('height: '+ h);
    /*set the width of the img element to 50%:*/
    img.style.width = (w / 2) + "px";
    /*create slider:*/
    slider = document.createElement("div");
    slider.setAttribute("class", "img-comp-slider");
    /*insert slider*/
    img.parentElement.insertBefore(slider, img);
    //console.log("slider height before: "+ slider.offsetHeight);
    //console.log("slider width before: "+ slider.offsetWidth);
    /*position the slider in the middle:*/
    slider.style.top = (h / 2) - (slider.offsetHeight / 2) + "px";
    slider.style.left = (w / 2) - (slider.offsetWidth / 2) + "px";
    /*execute a function when the mouse button is pressed:*/
    slider.addEventListener("mousedown", slideReady);
    /*and another function when the mouse button is released:*/
    window.addEventListener("mouseup", slideFinish);
    /*or touched (for touch screens:*/
    slider.addEventListener("touchstart", slideReady);
    /*and released (for touch screens:*/
    window.addEventListener("touchend", slideFinish);
    function slideReady(e) {
      /*prevent any other actions that may occur when moving over the image:*/
      e.preventDefault();
      /*the slider is now clicked and ready to move:*/
      clicked = 1;
      /*execute a function when the slider is moved:*/
      window.addEventListener("mousemove", slideMove);
      window.addEventListener("touchmove", slideMove);
    }
    function slideFinish() {
      /*the slider is no longer clicked:*/
      clicked = 0;
    }
    function slideMove(e) {
      var pos;
      /*if the slider is no longer clicked, exit this function:*/
      if (clicked == 0) return false;
      /*get the cursor's x position:*/
      pos = getCursorPos(e)
      /*prevent the slider from being positioned outside the image:*/
      if (pos < 0) pos = 0;
      if (pos > w) pos = w;
      /*execute a function that will resize the overlay image according to the cursor:*/
      slide(pos);
    }
    function getCursorPos(e) {
      var a, x = 0;
      e = e || window.event;
      /*get the x positions of the image:*/
      a = img.getBoundingClientRect();
      /*calculate the cursor's x coordinate, relative to the image:*/
      x = e.pageX - a.left;
      /*consider any page scrolling:*/
      x = x - window.pageXOffset;
      return x;
    }
    function slide(x) {
      /*resize the image:*/
      img.style.width = x + "px";
      /*position the slider:*/
      slider.style.left = img.offsetWidth - (slider.offsetWidth / 2) + "px";
    }
  }
}

// BOTTOM SCRIPT TAG
var mymap1 = L.map('map1').setView([0, 0], 1);
var mymap2 = L.map('map2').setView([0, 0], 1);

//retrieve key for selected map in drop down menu
selectedTile = $("#Maps").val();

//dictionar for various maps and their tile map url
var dict = {
"Stamen WaterColor" : ['https://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.png', 
'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://creativecommons.org/licenses/by-sa/3.0">CC BY SA</a>.'],

"OpenStreet Map" : ['https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', 
'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>'],

"Stamen Toner" : ['http://tile.stamen.com/toner/{z}/{x}/{y}.png', 
'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.'],

"Stamen Terrain": ['http://tile.stamen.com/terrain/{z}/{x}/{y}.jpg',
'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.'], 

"OSM Black and White": ['http://tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png', 
'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>'], 


"Esri Imagery": ['https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', 
'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'],

"Esri Streets": ['https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
'Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012'],

"Esri Topo": ['https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', 
'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community'], 

"Carto Positron": ['https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png', 
'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>']
};
      

var tileUrl = dict[selectedTile][0];
var tile_attribution = dict[selectedTile][1];

//right map
//GeoBoundaries
var tiles1 = L.tileLayer(tileUrl, {attribution: tile_attribution}).addTo(mymap1);
var zoomOptions = {
  position: 'topright'
};
var zoom = L.control.zoom(zoomOptions);   // Creating zoom control
zoom.addTo(mymap1);   // Adding zoom control to the map

//left map 
//Natural Earth
var tiles2 = L.tileLayer(tileUrl, {attribution: tile_attribution}).addTo(mymap2);

/*Execute a function that will execute an image compare function for each element with the img-comp-overlay class:*/
initComparisons();
$.getJSON("https://www.geoboundaries.org/data/geoBoundaries-3_0_0/"+qs.ISO+"/"+ qs.ADM+"/geoBoundaries-3_0_0-"+qs.ISO+"-"+qs.ADM+".geojson",function(data){
  // add GeoJSON layer to the map once the file is loaded
  var datalayer = L.geoJson(data).addTo(mymap1);
  //Zoom to layer
  mymap1.fitBounds(datalayer.getBounds());
});

$.getJSON("naturalEarthGeoJson/"
        +qs.ISO+"/"+qs.ADM+"/"+"naturalEarth"+qs.ISO+".geojson",
        function(data){
  // add GeoJSON layer to the map once the file is loaded
  var datalayer = L.geoJson(data).addTo(mymap2);
  //Zoom to layer
  mymap2.fitBounds(datalayer.getBounds());
});

// L.Map.Sync.js library
mymap1.sync(mymap2);
mymap2.sync(mymap1);

const arr = [null, null];

//fix
$(document).ready(function(){
var adm;
var iso;
var selectedTile;
$('select[name="ISO"]').change(function(){
    iso = "ISO="+$("#ISO").val();
    adm = "ADM="+$("#ADM").val();
    selectedTile = $("#Maps").val();

});

$('select[name="ADM"]').change(function(){
    adm = "ADM="+$("#ADM").val();
    iso = "ISO="+$("#ISO").val();
    selectedTile = $("#Maps").val(); 
});

$('select[name="MapTiles"]').change(function(){
  adm = "ADM="+$("#ADM").val();
  iso = "ISO="+$("#ISO").val();
  selectedTile = $("#Maps").val();

});


document.getElementById("ADM").value=qs.ADM;
$("#compare").click(function(){
    // replace url in address bar
    const stateObj = { id: 'geo' };
    window.history.replaceState(stateObj, '', "?"+adm+"&"+iso); 
    location.reload();
});
});

