console.log('import')

function initialize() {
    console.log('1')
    var mapOptions = 
    {
        center: new google.maps.LatLng(45.76, 4.83),
        zoom: 14
    };
    map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
}

function addMarker(position) {
    console.log('2');
    var marker = new google.maps.Marker({
        map: map,
        draggable: false,
        position: position
    });
}

function initData() {
    console.log('2');
    var markers = $.getJSON("http://127.0.0.1:5000/markers", function() {
      console.log( "success" );
})
  .done(function() {
          console.log( "second success" );
            })
  .fail(function() {
          console.log( "error" );
            })
  .always(function() {
          console.log( "complete" );
            });
}
