$(function() {
    //button used to hide the search criteria
    $('#searchToggleBTN').on('click', function() {
        $('.search-toggle').toggle(1000);
    });
    $('.btn-results').on('click', function() {
        $('.result-details').toggle(1000);
    });


});