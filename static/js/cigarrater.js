
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