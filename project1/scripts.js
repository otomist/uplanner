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
        document.getElementById("b1").textContent = 
            (document.getElementById("b1").textContent === "+") ? "-" : "+";
    });
    //Button for adding to scheduler
    document.getElementById("add1").onclick = function () {
        scheduler.addEvent({
            id:1,
            start_date: "01-01-2018 13:00",
            end_date:   "01-01-2018 13:50",
            text:       "CS121",
            readonly:   true
        });
        scheduler.addEvent({
            id:2,
            start_date: "03-01-2018 13:00",
            end_date:   "03-01-2018 13:50",
            text:       "CS121",
            readonly:   true
        });
        scheduler.addEvent({
            id:3,
            start_date: "05-01-2018 13:00",
            end_date:   "05-01-2018 13:50",
            text:       "CS121",
            readonly:   true
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
        document.getElementById("b2").textContent = 
            (document.getElementById("b2").textContent === "+") ? "-" : "+";
    });
    //Button for adding to scheduler
    document.getElementById("add2").onclick = function () {
        scheduler.addEvent({
            id:4,
            start_date: "02-01-2018 10:00",
            end_date:   "02-01-2018 11:15",
            text:       "CS121",
            readonly:   true
        });
        scheduler.addEvent({
            id:5,
            start_date: "04-01-2018 10:00",
            end_date:   "04-01-2018 11:15",
            text:       "CS121",
            readonly:   true
        });
    };
    //button for deleting from scheduler
    document.getElementById("del2").onclick = function () {
        scheduler.deleteEvent(4);
        scheduler.deleteEvent(5);
    };

    $('#b3').on('click', function () {
        $('.r3').toggle(1000);
        document.getElementById("b3").textContent = 
            (document.getElementById("b3").textContent === "+") ? "-" : "+";
    });
    //Button for adding to scheduler
    document.getElementById("add3").onclick = function () {
        scheduler.addEvent({
            id:6,
            start_date: "01-01-2018 09:00",
            end_date:   "01-01-2018 09:50",
            text:       "CS187",
            readonly:   true
        });
        scheduler.addEvent({
            id:7,
            start_date: "03-01-2018 09:00",
            end_date:   "03-01-2018 09:50",
            text:       "CS187",
            readonly:   true
        });
        scheduler.addEvent({
            id:8,
            start_date: "05-01-2018 09:00",
            end_date:   "05-01-2018 09:50",
            text:       "CS187",
            readonly:   true
        });
    };
    //button for deleting from scheduler
    document.getElementById("del3").onclick = function () {
        scheduler.deleteEvent(6);
        scheduler.deleteEvent(7);
        scheduler.deleteEvent(8);
    };

    $('#b4').on('click', function () {
        $('.r4').toggle(1000);
        document.getElementById("b4").textContent = 
            (document.getElementById("b4").textContent === "+") ? "-" : "+";
    });
    //Button for adding to scheduler
    document.getElementById("add4").onclick = function () {
        scheduler.addEvent({
            id:9,
            start_date: "02-01-2018 13:00",
            end_date:   "02-01-2018 14:15",
            text:       "CS187",
            readonly:   true
        });
        scheduler.addEvent({
            id:10,
            start_date: "04-01-2018 13:00",
            end_date:   "04-01-2018 14:15",
            text:       "CS187",
            readonly:   true
        });
    };
    //button for deleting from scheduler
    document.getElementById("del4").onclick = function () {
        scheduler.deleteEvent(9);
        scheduler.deleteEvent(10);
    };
    
});