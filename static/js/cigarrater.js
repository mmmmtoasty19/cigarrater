
    $.fn.stars = function() {
        return $(this).each(function() {

            var rating = $(this).data("rating");

            var numStars = $(this).data("numStars");

            var fullStar = new Array(Math.floor(rating + 1)).join('<i class="fas fa-star"></i>');

            var halfStar = ((rating%1) !== 0) ? '<i class="fa fa-star-half"></i>': '';

            var noStar = new Array(Math.floor(numStars + 1 - rating)).join('<i class="far fa-star"></i>');

            $(this).html(fullStar + halfStar + noStar);

        });
    }

    $('.stars').stars();



    var rangeSlider = function() {
        var slider = $(".cigar_rating_range"),
          range = $(".cigar_rating__range"),
          value = $(".cigar_rating__value");
      
        slider.each(function() {
          value.each(function() {
            var value = $(this)
              .prev()
              .attr("value");
            $(this).html(value);
          });
      
          range.on("input", function() {
            $(this)
              .next(value)
              .html(this.value);
          });
        });
      };
      
      rangeSlider();
      

// Code for clicking through tabs in search menu (currently only have cigar and brand)
function openSearchTab(evt, tabName) {
    var i, tabcontent;

    // Hide all search tabs by default
    tabcontent = document.getElementsByClassName("search_tab_content")
    for (i = 0; i < tabcontent.length; i++){
      tabcontent[i].style.display = "none";
    }

    // Get all elements with class="searchtabs" and remove the class "active"
    tablinks = document.getElementsByClassName("searchtabs");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Opens tab for currently click link
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
};




// opens cigar tab by default

$(document).ready(function () { 
  document.getElementById("defaultOpen").click();
 });




//Get sort type on search page
// form is autosubmited on change.
// need to work on setting default select option to equal page arguments 

$(document).ready(function () {
  $("select.cigar_sort_options").change(function () {
    var sort_type = $(this).val();
    $("#sort").attr('value', sort_type);
    $("#search_form").submit();
    });
  });


// Testing 4sqaure instead of google
  $(document).ready(function () {
      $('#test_search').click(function () {
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function (position) {  
          var pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          };
          var pos_param = $.param(pos);
          var searchReq = $.get("/sendRequest?" + pos_param);
          searchReq.done(function (data) {
            for (var key in data) {
              if (data.hasOwnProperty(key)) {
                  $('#rating_location').append( "<option value=" + key + ">" + data[key] + "</option>");
              }
          }
            });
          });    
        } else {
          alert("Browser doesn't support geolocation");
        }  
        });
      });



// Testing Geolocation for Google Places API  
// current function passing users lat and lng to flask backend and returns the values.
// took about 2 seconds to return results this way
// $(document).ready(function () {
//   $('#test_search').click(function () {
//     if (navigator.geolocation) {
//       navigator.geolocation.getCurrentPosition(function (position) {  
//       var pos = {
//         lat: position.coords.latitude,
//         lng: position.coords.longitude
//       };
//       var pos_param = $.param(pos);
//       var searchReq = $.get("/sendRequest?" + pos_param);
//       searchReq.done(function (data) {
//           for (i = 0; i < data.length; i++) {
//             $('#rating_location').append( "<option value=" + data[i]+ ">" + data[i] + "</option>")
//           };
//         });
//       });    
//     } else {
//       alert("Browser doesn't support geolocation");
//     }  
//     });
//   });

// var map
// var service 
// var infowindow

// $(document).ready(function () {
//     $('#test_search').click(function () {
//       if (navigator.geolocation) {
//         navigator.geolocation.getCurrentPosition(function (position) {  
//         var pos = {
//           lat: position.coords.latitude,
//           lng: position.coords.longitude
//         };

//         var center = new google.maps.LatLng(pos['lat'],pos['lng']);
//         infowindow = new google.maps.InfoWindow();
//         map = new google.maps.Map(document.getElementById('map'), {
//           center: center,
//           zoom : 11
//         });

//         var request = {
//           location : center,
//           radius : 16000,
//           query : 'cigar'
//         };
//         service = new google.maps.places.PlacesService(map);
//         service.textSearch(request,callback);
       
//     });
//   };
//     });

//     function callback(results, status) {
//         if (status == google.maps.places.PlacesServiceStatus.OK) {
//           for (var i = 0; i < results.length; i++) {
//             var place = results[i];
//             createMarker(results[i]);
//         }
//     };
//   };

//   function createMarker(place) {
//     var placeLoc = place.geometry.location;
//     var marker = new google.maps.Marker({
//       map: map,
//       position: place.geometry.location
//     });
//     google.maps.event.addListener(marker, 'click', function() {
//       infowindow.setContent(place.name);
//       infowindow.open(map, this);
//     });
//   };

  

// });






