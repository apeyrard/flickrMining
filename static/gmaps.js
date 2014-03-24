console.log('import');
var cur_infowindow = null;

function initialize() {
    var mapOptions = 
    {
        center: new google.maps.LatLng(45.76, 4.83),
        zoom: 14
    };
    map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
}


function addCluster(cluster) {
    color = Math.floor(Math.random() * 256.0 * 256.0 * 256.0);
    color = '#' + color.toString(16);
    var center = new google.maps.LatLng(cluster.latitude, cluster.longitude);

    var clusterOptions = {
        strokeColor: color,
        strokeOpacity: 0.7,
        strokeWeight: 2,
        fillColor: color,
        fillOpacity: 0.2,
        map: map,
        center: center,
        radius: cluster.radius 
    };
    var circle = new google.maps.Circle(clusterOptions);
    circle.markers = new Array();
    
    $.each(cluster._cluster__listMarker, function(i, data){
        position = new google.maps.LatLng(data[0], data[1]);

        var marker = new google.maps.Marker({
            map: map,
            visible: false,
            draggable: false,
            position: position
        });

        circle.markers[i] = marker;
    });
    
    var infowindow = new google.maps.InfoWindow({
            content: circle.markers.length.toString(),
            position: center
    });

    google.maps.event.addListener(circle, 'click', function()  {
        if(cur_infowindow){
            cur_infowindow.close();
        }
        cur_infowindow = infowindow;
        infowindow.open(map);
        $.each(circle.markers, function(i, marker) {
            marker.setVisible(!marker.getVisible());
        });
    });
}

function initData() {
    var data = $.getJSON("http://127.0.0.1:5000/data", function(data) {
        console.log( "loading data" );
        $.each(data, function(i, cluster) {
            addCluster(cluster);
        });

})
  .done(function() {
          console.log( "markers loaded" );
            })
  .fail(function() {
          console.log( "error" );
            })
  .always(function() {
          console.log( "complete" );
            });
}
