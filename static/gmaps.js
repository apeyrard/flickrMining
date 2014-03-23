console.log('import')

function initialize() {
    var mapOptions = 
    {
        center: new google.maps.LatLng(45.76, 4.83),
        zoom: 14
    };
    map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
}

function addMarker(position) {
    var marker = new google.maps.Marker({
        map: map,
        draggable: false,
        position: position
    });
}

function addCluster(cluster) {
    color = Math.floor(Math.random() * 256.0 * 256.0 * 256.0);
    color = '#' + color.toString(16);

    var clusterOptions = {
        strokeColor: color,
        strokeOpacity: 0.7,
        strokeWeight: 2,
        fillColor: color,
        fillOpacity: 0.2,
        map: map,
        center: new google.maps.LatLng(cluster.latitude, cluster.longitude),
        radius: cluster.radius 
    };
    
    var circle = new google.maps.Circle(clusterOptions);
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
