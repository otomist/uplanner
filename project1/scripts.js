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
    //Button for maximize/minimize result info
    $('#b1').on('click', function () {
        $('.r1').toggle(1000);
    });
    //button for adding to scheduler
    document.getElementById("add1").onclick = function () {
        scheduler.addEvent({
            id:1,
            start_date: "01-01-2018 13:00",
            end_date:   "01-01-2018 13:50",
            text:       "CS121"
        });
        scheduler.addEvent({
            id:2,
            start_date: "03-01-2018 13:00",
            end_date:   "03-01-2018 13:50",
            text:       "CS121"
        });
        scheduler.addEvent({
            id:3,
            start_date: "05-01-2018 13:00",
            end_date:   "05-01-2018 13:50",
            text:       "CS121"
        });
    };
    //button for deleting from scheduler
    document.getElementById("del1").onclick = function () {
        scheduler.deleteEvent(1);
        scheduler.deleteEvent(2);
        scheduler.deleteEvent(3);
    };

    $('#b2').on('click', function () {
        $('.r2').toggle(1000);
    });
    $('#b3').on('click', function () {
        $('.r3').toggle(1000);
    });
    $('#b4').on('click', function () {
        $('.r4').toggle(1000);
    });
    

});