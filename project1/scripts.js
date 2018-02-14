$(function () {
    //button used to hide the search criteria and show more results
    var searchHidden=false;
    $('#searchToggleBTN').on('click', function () {
        searchHidden ? searchHidden=false : searchHidden=true;
        $('.search-toggle').toggle(1000);
        var resPanel = document.querySelector('.fixed-panel');
        if(searchHidden){
            resPanel.style.minHeight='40rem';
            resPanel.style.maxHeight='40rem';
        }else{
            resPanel.style.minHeight='25rem';
            resPanel.style.maxHeight='25rem';
        }
    });


    $('.b1').on('click', function () {
        $('.r1').toggle(1000);
    });
    $('.b2').on('click', function () {
        $('.r2').toggle(1000);
    });
    $('.b3').on('click', function () {
        $('.r3').toggle(1000);
    });
    $('.b4').on('click', function () {
        $('.r4').toggle(1000);
    });
    $('.b5').on('click', function () {
        $('.r5').toggle(1000);
    });
    $('.b6').on('click', function () {
        $('.r6').toggle(1000);
    });
    $('.b7').on('click', function () {
        $('.r7').toggle(1000);
    });
    $('.b8').on('click', function () {
        $('.r8').toggle(1000);
    });
    $('.b9').on('click', function () {
        $('.r9').toggle(1000);
    });
    $('.b10').on('click', function () {
        $('.r10').toggle(1000);
    });
    $('.b11').on('click', function () {
        $('.r11').toggle(1000);
    });
    $('.b12').on('click', function () {
        $('.r12').toggle(1000);
    });
    $('.b13').on('click', function () {
        $('.r13').toggle(1000);
    });
    $('.b14').on('click', function () {
        $('.r14').toggle(1000);
    });



});