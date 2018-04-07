$(function () {
    //Button used to hide the search criteria and show more results
    var searchHidden = false;
            
    // Makes a new tab in schedule.html, and populates it with course details.
    $('.js-make-tab').on('click', function() {
        /*
          Data flow upon click:
           -do ajax call or other method to update the session context variable
           -have the pre-existing tabs + contents render in normal view
           -render the new tab from javascript
           -render the new tab contents through javascript + django html
        */
        id = $(event.target).attr('course-id');
        dept = $(event.target).attr('course-dept');
        num = $(event.target).attr('course-num');
        url_content = $(event.target).attr('href');
        
        // If the course tab does not already exist, make a new tab for it
        if ( !$("#nav-"+id).length ) {
            // Create the new tab
            
            $('<li class="nav-item" id="nav-'+id+'">\
            <a class="nav-link" id="'+id+'-tab" data-toggle="tab" href="#'+id+'">'+
            dept+' '+num+
            '  <button class="btn btn-danger btn-xs js-del-tab btn-results" course-id="'+id+'">X</button>\
            </a>').appendTo('#scheduleTab');
            
            // Add a new tab content pane including the schedule_tabs_content.html file
            $('<div class="tab-pane" id='+id+'></div>').appendTo('#scheduleTabContent');
            
            // Populate it with the schedule_tabs_content.html file through django
            $('#'+id).html('').load(
                url_content + "?course_pk=" + id
            );
            
        }
      
        // Show the tab
        $('#'+id+'-tab').tab('show');
    
    });
    
    /*
    Adds the delete function to any element currently in the page or
    added dynamically later. deletes the tab and its contents
    */
    $(document).on('click', '.js-del-tab', function () {
        id = $(event.target).attr('course-id');
        if ( $('#nav-'+id).length ) {
            $('#nav-'+id).remove();
            $('#'+id).remove();
        }
    });
    
    /*
    This button adds a course to the schedule
    It uses an ajax request to retrieve the section information, then
    uses the retrieved information to populate the schedule.
    When the server recieves the ajax request, it updates the database
    It also programmatically updates the current courses list
    */
    $(document).on('click', '.js-add', function() {
        id = $(event.target).attr('section-id');
        url_ajax = $(event.target).attr('ajax-url');
        url_html = $(event.target).attr('html-url');        
        
        schedules = $('.js-schedule');
        schedule = ""
        for (i = 0; i < schedules.length; i++) {
            if (schedules[i].checked === true) {
                schedule = schedules[i].name;
            }
        }
        
        // Execute the ajax to get course data from server, and update database
        $.ajax({
            url: url_ajax,
            data: {
                'id': id,
                'schedule': schedule,
            },
            dataType: 'json',
            success: function (data) {
                
                var days = []
                
                for (i = 0; i < data.days.length; i+=2) {
                    day = data.days.charAt(i) + data.days.charAt(i+1);
                    switch(day) {
                        case 'Mo':
                            days.push('01-01-2018 ');
                            break;
                        case 'Tu':
                            days.push('02-01-2018 ');
                            break;
                        case 'We':
                            days.push('03-01-2018 ');
                            break;
                        case 'Th':
                            days.push('04-01-2018 ');
                            break;
                        case 'Fr':
                            days.push('05-01-2018 ');
                            break;
                    }
                }
                
                for (i = 0; i < days.length; i++) {
                    scheduler.addEvent({
                        id: id + "" + i,
                        start_date: days[i] + data.start_time,
                        end_date: days[i] + data.end_time,
                        text: data.title,
                        color: "#157ddf9f",
                        type: schedule,
                        readonly: true
                    });
                }
                
                // Add the course to the current course list
                // If the course listing does not already exist, add a list element for it
                if ( !$("#curr-"+id).length ) {
                    // Create the new list element
                    $('<li class="list-group-item" id="curr-' + id + '"></li>').appendTo('#current-courses');
                    
                    // Populate it with the schedule_current_courses.html file through django
                    $('#curr-'+id).html('').load(
                        url_html + "?course_id=" + id
                    );
                }
                
            }
        });

    });
    
    $(document).on('click', '.js-del', function() {
        id = $(event.target).attr('section-id');
        url = $(event.target).attr('ajax-url');
                
        //Attempt to delete every possible occurrence of the section
        scheduler.deleteEvent(id + "0");
        scheduler.deleteEvent(id + "1");
        scheduler.deleteEvent(id + "2");
        scheduler.deleteEvent(id + "3");
        scheduler.deleteEvent(id + "4");
        
        $.ajax({
            url: url,
            data: {
                'id': id,
            },
            dataType: 'json',
            success: function (data) {
                
                // Remove the listing from the current courses
                if ( $("#curr-"+id).length ) {
                    $('#curr-'+id).remove();
                }
            }
        });
    });
    
    /*
      Button for expanding information
      To use in html, follow this example:
      
      <div class="js-expand-block">
        <button class="js-expand-btn">+</button>
        ...
        <div class="js-expand-info">...</div>
        ...
      </div>
      
      The button and expanded info must be enclosed in a "js-expand-block"
      All content within the "js-expand-info" div (or any other element with that class) will be expandable
      Making the button's text content "+" will make it automatically switch to "-" as necessary.
       For custom response, a new function must be implemented (see the next function for example)
    */
    $('.js-expand-btn').on('click', function() {
        info = $(event.target).closest('.js-expand-block').find('.js-expand-info');
        info.toggle(100);
        if ($(event.target).text() === "+") {
            $(event.target).text("-");
        } else if ($(event.target).text() === "-") {
            $(event.target).text("+");
        }
    });
    
    // This function handles extra behavior for expanding search filters, such as swapping
    // the expand button
    $('#searchToggleBTN').on('click', function () {
        searchHidden ? searchHidden = false : searchHidden = true;
        if (searchHidden) {
            //switch between max/minimize arrows
            expandBtn.style.display = 'block';
            hideBtn.style.display = 'none'; 
        } else {
            //switch between max/minimize arrows
            expandBtn.style.display = 'none';
            hideBtn.style.display = 'block'; 
        }
    });

});