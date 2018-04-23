$(function () {

    // Makes a new tab in schedule.html, and populates it with course details.
    $('.js-make-tab').on('click', function () {
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
        url_content = $('#meta').attr('make-tab-content-url');
        url_delete = $('#meta').attr('delete-tab-url');

        // If the course tab does not already exist, make a new tab for it
        if (!$("#nav-" + id).length) {
            // Create the new tab
            $('<li class="nav-item" id="nav-' + id + '">\
            <a class="nav-link navTab course-tab" id="'+ id + '-tab" data-toggle="tab" href="#' + id + '">' +
                dept + ' ' + num +
                '  <button class="btn btn-danger btn-xs js-del-tab btn-results" course-id="' + id + '">&times;</button>\
            </a></li>').appendTo('#scheduleTab');
            
            // Add a new tab content pane including the schedule_tabs_content.html file
            $('<div class="tab-pane" id=' + id + '></div>').appendTo('#scheduleTabContent');
            
            // Populate it with the schedule_tabs_content.html file through django
            $('#' + id).html('').load(
                url_content + "?course_pk=" + id
            );
        }

        // Show the tab
        $('#' + id + '-tab').tab('show');

    });

    // Reloads a course tab every time it is visited, in case something has changed
    $(document).on('show.bs.tab', '.course-tab', function () {
        var id = $(event.target).attr('id');
        var url_content = $('#meta').attr('make-tab-content-url');

        if (id) {
            id = id.slice(0, id.length - 4)
            //Populate it with the schedule_tabs_content.html file through django
            $('#' + id).html('').load(
                url_content + "?course_pk=" + id
            );
        }
    });

    /*
    Adds the delete function to any element currently in the page or
    added dynamically later. deletes the tab and its contents
    */
    $(document).on('click', '.js-del-tab', function () {

        var id = $(event.target).attr('course-id');
        var url = $('#meta').attr('delete-tab-url');

        //use ajax to update server session variable
        $.ajax({
            url: url,
            data: {
                'id': id,
            },
            dataType: 'json',
            success: function (data) {
                if ($('#nav-' + id).length) {
                    $('#nav-' + id).remove();
                    $('#' + id).remove();

                    // Show a new tab
                    $('#results-tab').tab('show');
                }
            }
        });

    });

    /*
    This button adds a course to the schedule
    It uses an ajax request to retrieve the section information, then
    uses the retrieved information to populate the schedule.
    When the server recieves the ajax request, it updates the database
    It also programmatically updates the current courses list
    */
    $(document).on('click', '.js-add', function () {
        id = $(event.target).attr('section-id');
        url_ajax = $('#meta').attr('add-section-url');
        url_html = $('#meta').attr('make-current-course-url');

        var schedule = $(".js-schedule:checked").attr('name');

        // Execute the ajax to get course data from server, and update database
        $.ajax({
            url: url_ajax,
            data: {
                'id': id,
            },
            dataType: 'json',
            success: function (data) {
                
                events = data['events']
                
                for (i = 0; i < events.length; i++) {
                    scheduler.parse([events[i]], 'json');
                }
                
                // Add the course to the current course list
                // If the course listing does not already exist, add a list element for it
                if (!$("#curr-" + id).length) {
                    // Create the new list element
                    $('<li class="list-group-item current-course" id="curr-' + id + '"></li>').appendTo('#current-courses');

                    // Populate it with the schedule_current_courses.html file through django
                    $('#curr-' + id).html('').load(
                        url_html + "?course_id=" + id + '&schedule=' + data['schedule_id']
                    );
                }
            }
        });

    });

    /*
     Delete a course from the schedule
    */
    $(document).on('click', '.js-del', function () {
        var id = $(event.target).attr('section-id');
        var url = $('#meta').attr('del-section-url');
        var schedule = $(".js-schedule:checked").attr('name');

        //TODO: adjust for saturday/sunday
        //Attempt to delete every possible occurrence of the section
        // there are many, because each ScheduleCourse can meet on many
        // different days, and each day needs its own id
        // so the ids are just the section id[0-4]
        scheduler.deleteEvent(id + "0" + schedule);
        scheduler.deleteEvent(id + "1" + schedule);
        scheduler.deleteEvent(id + "2" + schedule);
        scheduler.deleteEvent(id + "3" + schedule);
        scheduler.deleteEvent(id + "4" + schedule);

        scheduler.updateView();

        $.ajax({
            url: url,
            data: {
                'id': id,
            },
            dataType: 'json',
            success: function (data) {

                // Remove the listing from the current courses
                if ($("#curr-" + id).length) {
                    $('#curr-' + id).remove();
                }
            }
        });
    });
    
    // function submitting a new schedule form
    // this function is a little complicated. It overrides the
    //  standard django form behavior to prevent page reloading
    //  on form submission; instead, ajax handles communication
    //  with server
    $('#js-submit-schedule-btn').on('submit', function (event) {
        // make an ajax call to django's make_schedule view
        // django gets data from form and validates it
        // returns success or failure:
        // success:
        //  django adds it to database
        //  hide schedule form
        //  display new radiobutton for schedule
        //  update scheduleBuilder.js???
        // failure:
        //  display error
        //  (when does error message go away?)

        event.preventDefault(); //Prevents auto-submission of form through server

        url = $('#meta').attr('make-schedule-url');

        $.ajax({
            url: url,
            data: $(this).serialize(),
            dataType: 'json',
            method: 'POST',
            success: function (data) {
                if (data['status'] === 'SUCCESS') {
                    $('<label class="js-schedule-container">\
                       <input type="radio" class="js-schedule" name="'+ data['title'] + '" schedule-id="' + data['id'] + '"/>' +
                        data['title'] +
                        '</label>'
                    ).appendTo('#filters_wrapper');
                }
            }
        });
    });

    //Delete schedule is in scheduleBuilder.js

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
    $(document).on('click', '.js-expand-btn', function () {
        info = $(event.target).closest('.js-expand-block').find('.js-expand-info');
        info.toggle(100);
        if ($(event.target).text() === "+") {
            $(event.target).text("-");
        } else if ($(event.target).text() === "-") {
            $(event.target).text("+");
        }
    });

    //readmore button code for the course description and course requirements
    var $el, $ps, $up, totalHeight;
    $(document).on('click', '.sidebar-box .button', function () {
        console.log("Readmore was clicked");
        totalHeight = 0;

        $el = $(this);
        $p = $el.parent();
        $up = $p.parent();
        $ps = $up.find("p:not('.read-more')");

        // measure how tall inside should be by adding together heights of all inside paragraphs (except read-more paragraph)
        $ps.each(function () {
            totalHeight += $(this).outerHeight();
        });

        $up
            .css({
                // Set height to prevent instant jumpdown when max height is removed
                "height": $up.height(),
                "max-height": 9999
            })
            .animate({
                "height": totalHeight
            });

        // fade out read-more
        $p.fadeOut();

        // prevent jump-down
        return false;
    });
});