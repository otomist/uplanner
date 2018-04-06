/*
A file to contain the add and del functions for the schedule.
This avoids double-binding of other functions, such as the expand/hide functions
*/


$(function () {
    
    /*
    This button adds a course to the schedule
    It uses an ajax request to retrieve the section information, then
    uses the retrieved information to populate the schedule.
    When the server recieves the ajax request, it updates the database
    It also programmatically updates the current courses list
    */
    $('.js-add').on('click', function() {
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
    
    $('.js-del').on('click', function() {
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
});