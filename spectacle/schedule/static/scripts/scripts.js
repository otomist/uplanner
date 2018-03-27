
// Button for minimize/maximize using id passed from html
function expand(id) {
    $('.r' + id).toggle(1000);
    document.getElementById("b" + id).textContent = 
        (document.getElementById("b" + id).textContent === "+") ? "-" : "+";
}

function view_tab(id, url_content, dept, num) {
    
    /*
      Data flow upon click:
       -do ajax call or other method to update the session context variable
       -have the pre-existing tabs + contents render in normal view
       -render the new tab from javascript
       -render the new tab contents through javascript + django html
    */
    
    $('<li class="nav-item"><a class="nav-link" id="'+id+'-tab" data-toggle="tab" href="#'+id+'">'+dept+' '+num+'</a>').appendTo('#scheduleTab');
    
    // Add a new tab content pane including the schedule_tabs_content.html file
    $('<div class="tab-pane" id='+id+'></div>').appendTo('#scheduleTabContent');
    
    // Populate the schedule_tabs_content.html file through django
    $('#'+id).html('').load(
        url_content + "?course_pk=" + id
    );
    
}

function add(id) {
    //Temporary if statement until integration with django backend:
    if (id === 1) {
        scheduler.addEvent({
            id: 1,
            start_date: "01-01-2018 13:00",
            end_date: "01-01-2018 13:50",
            text: "CS121",
            color: "rgb(0, 153, 255)",
            readonly: true
        });
        scheduler.addEvent({
            id: 2,
            start_date: "03-01-2018 13:00",
            end_date: "03-01-2018 13:50",
            text: "CS121",
            color: "rgb(0, 153, 255)",
            readonly: true
        });
        scheduler.addEvent({
            id: 3,
            start_date: "05-01-2018 13:00",
            end_date: "05-01-2018 13:50",
            text: "CS121",
            color: "rgb(0, 153, 255)",
            readonly: true
        });
    } else {
        scheduler.addEvent({
            id: 4,
            start_date: "02-01-2018 10:00",
            end_date: "02-01-2018 11:15",
            text: "CS121",
            color: "rgb(0, 153, 255)",
            readonly: true
        });
        scheduler.addEvent({
            id: 5,
            start_date: "04-01-2018 10:00",
            end_date: "04-01-2018 11:15",
            text: "CS121",
            color: "rgb(0, 153, 255)",
            readonly: true
        });
    }
}

function del(id) {
    if (id === 1) {
        scheduler.deleteEvent(1);
        scheduler.deleteEvent(2);
        scheduler.deleteEvent(3);
    } else {
        scheduler.deleteEvent(4);
        scheduler.deleteEvent(5);
        scheduler.deleteEvent(6);
    }
}

$(function () {
    //Button used to hide the search criteria and show more results
    var searchHidden = false;
    $('#searchToggleBTN').on('click', function () {
        searchHidden ? searchHidden = false : searchHidden = true;
        $('.search-toggle').toggle(1000);
        var resPanel = document.querySelector('.fixed-panel');
        if (searchHidden) {
            resPanel.style.minHeight = '40rem';
            resPanel.style.maxHeight = '40rem';
        } else {
            resPanel.style.minHeight = '25rem';
            resPanel.style.maxHeight = '25rem';
        }
    });
    //Button for adding to scheduler
    /*
    document.getElementById("add1").onclick = function () {
        scheduler.addEvent({
            id: 1,
            start_date: "01-01-2018 13:00",
            end_date: "01-01-2018 13:50",
            text: "CS121",
            color: "rgb(0, 153, 255)",
            readonly: true
        });
        scheduler.addEvent({
            id: 2,
            start_date: "03-01-2018 13:00",
            end_date: "03-01-2018 13:50",
            text: "CS121",
            color: "rgb(0, 153, 255)",
            readonly: true
        });
        scheduler.addEvent({
            id: 3,
            start_date: "05-01-2018 13:00",
            end_date: "05-01-2018 13:50",
            text: "CS121",
            color: "rgb(0, 153, 255)",
            readonly: true
        });
    };
    //Button for deleting from scheduler
    document.getElementById("del1").onclick = function () {
        scheduler.deleteEvent(1);
        scheduler.deleteEvent(2);
        scheduler.deleteEvent(3);
    };
    //Button for adding to scheduler
    document.getElementById("add2").onclick = function () {
        scheduler.addEvent({
            id: 4,
            start_date: "02-01-2018 10:00",
            end_date: "02-01-2018 11:15",
            text: "CS121",
            color: "rgb(0, 153, 255)",
            readonly: true
        });
        scheduler.addEvent({
            id: 5,
            start_date: "04-01-2018 10:00",
            end_date: "04-01-2018 11:15",
            text: "CS121",
            color: "rgb(0, 153, 255)",
            readonly: true
        });
    };
    //Button for deleting from scheduler
    document.getElementById("del2").onclick = function () {
        scheduler.deleteEvent(4);
        scheduler.deleteEvent(5);
    };
    
    //Button for adding to scheduler
    document.getElementById("add3").onclick = function () {
        scheduler.addEvent({
            id: 6,
            start_date: "01-01-2018 09:00",
            end_date: "01-01-2018 09:50",
            text: "CS187",
            color: "rgb(0, 153, 255)",
            readonly: true
        });
        scheduler.addEvent({
            id: 7,
            start_date: "03-01-2018 09:00",
            end_date: "03-01-2018 09:50",
            text: "CS187",
            color: "rgb(0, 153, 255)",
            readonly: true
        });
        scheduler.addEvent({
            id: 8,
            start_date: "05-01-2018 09:00",
            end_date: "05-01-2018 09:50",
            text: "CS187",
            color: "rgb(0, 153, 255)",
            readonly: true
        });
    };
    //Button for deleting from scheduler
    document.getElementById("del3").onclick = function () {
        scheduler.deleteEvent(6);
        scheduler.deleteEvent(7);
        scheduler.deleteEvent(8);
    };

    //Button for adding to scheduler
    document.getElementById("add4").onclick = function () {
        scheduler.addEvent({
            id: 9,
            start_date: "02-01-2018 13:00",
            end_date: "02-01-2018 14:15",
            text: "CS187",
            color: "rgb(0, 153, 255)",
            readonly: true
        });
        scheduler.addEvent({
            id: 10,
            start_date: "04-01-2018 13:00",
            end_date: "04-01-2018 14:15",
            text: "CS187",
            color: "rgb(0, 153, 255)",
            readonly: true
        });
    };
    //button for deleting from scheduler
    document.getElementById("del4").onclick = function () {
        scheduler.deleteEvent(9);
        scheduler.deleteEvent(10);
    };
    */
});