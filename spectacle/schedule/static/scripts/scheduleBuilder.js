function init() {
    scheduler.config.xml_date = "%Y-%m-%d %H:%i";
    scheduler.config.first_hour = 6;
    scheduler.config.last_hour = 20;
    scheduler.config.limit_time_select = true;
    scheduler.config.time_step = 5;

    //used to make events read_only if they have that attribute.
    function block_readonly(id) {
        if (!id) return true;
        return !this.getEvent(id).readonly;
    }
    scheduler.attachEvent("onBeforeDrag", block_readonly)
    scheduler.attachEvent("onClick", block_readonly)
    
    //Work week
    scheduler.attachEvent("onTemplatesReady",function(){
        scheduler.date.workweek_start = scheduler.date.week_start;
        scheduler.templates.workweek_date = scheduler.templates.week_date;
        scheduler.templates.workweek_scale_date = scheduler.templates.week_scale_date;
        scheduler.date.add_workweek=function(date,inc){ return scheduler.date.add(date,inc*7,"day"); }
        scheduler.date.get_workweek_end=function(date){ return scheduler.date.add(date,5,"day"); }
    });
    
    //Title for the week Schedule
    scheduler.templates.week_date = function(){
        return "Class Schedule"; 
    };
    //Change the date in each Day-column (Not the best way to code it)
    scheduler.templates.week_scale_date = function(date){
        var day = scheduler.date.date_to_str(scheduler.config.day_date)(date).substring(0,3);
        if(day === "Tue") day += "sday";
        else if(day === "Wed") day += "nesday";
        else if(day === "Thu") day += "rsday";
        else day += "day";
        return day;
    };

    // Start Calendar swapping code
    scheduler.locale.labels.section_type = "Type";

    // default values for filters
    var filters = {};
    
    var filter_inputs = document.getElementById("filters_wrapper").getElementsByTagName("input");
    
    for (var i=0; i<filter_inputs.length; i++) {
        var filter_input = filter_inputs[i];
        
        // set initial input value based on filters settings
        filters[filter_input.name] = false;
        filter_input.checked = false;
    }
    
    // Call this after changing schedule and database has been updated
    // It updates the page; reloads current courses, and reloads the active course tab
    function update_page() {
        var url = $('#meta').attr('make-current-courses-url');
                
        // Reload the current courses
        $('#current-courses').html('').load(
            url
        );
        
        // If the currently open tab is a course detail tab, reload it
        var active_tab = $('.course-tab.active');
        var id = active_tab.attr('id');
        if (id) {
            id = id.slice(0, id.length-4);
            var url_content = $('#meta').attr('make-tab-content-url');
            //Populate it with the schedule_tabs_content.html file through django
            $('#'+id).html('').load(
                url_content + "?course_pk=" + id
            );
        }
    }
    
    //function for submitting a new user event
    //it is an ajax call that submits a form to the server. see the
    // submit schedule for explanation if necessary
    $('#js-submit-user-event-btn').on('submit', function(event) {
        event.preventDefault();
        url = $('#meta').attr('make-user-event-url');
        
        $.ajax({
            url: url,
            data: $(this).serialize(),
            dataType: 'json',
            method: 'POST',
            success: function (data) {
                //success: add the new event to the schedule
                if (data['status'] === 'SUCCESS') {
                    $('#event-modal').modal('hide');
                    events = data['events']
                    
                    for (i = 0; i < events.length; i++) {
                        scheduler.parse([events[i]], 'json');
                    }
                    
                    scheduler.updateView();
                    update_page();
                }
            }
        });
    });
    
    function change_schedule(schedule_name) {
        var filter_inputs_radio = document.getElementById("filters_wrapper").getElementsByTagName("input");
        for(var j=0; j<filter_inputs_radio.length; j++) {
            
            if (filter_inputs_radio[j].name !== schedule_name) {
                filter_inputs_radio[j].checked = false;
            }
            filters[filter_inputs_radio[j].name] = !!filter_inputs_radio[j].checked;
        }
                
        scheduler.updateView();
    }
    
    // function for toggling radio buttons and updating display
    // to change between user schedules
    $(document).on('change', '.js-schedule', function () {
        var schedule_url = $('#meta').attr('change-schedule-url');
        
        change_schedule($(event.target).attr('name'));
        
        $.ajax({
            url: schedule_url,
            data: {'schedule_title': $(".js-schedule:checked").attr('name')},
            dataType: 'json',
            success: function (data) {
                update_page();
            }
        });
        
    });
    
    //TODO: consider positioning of this function
    //It needs direct access to change_schedule, which needs access to
    // filters. But it is strange that it is separated
    // Delete a schedule
    $('.js-del-schedule').on('click', function () {
        var schedule = $(".js-schedule:checked");
        var url = $('#meta').attr('del-schedule-url');
                
        if ($('.js-schedule').length === 1) {
            //TODO: give error message to user
            console.log("cannot delete last schedule");
            return
        }
        
        //var new_schedule = $(".js-schedule")[0].name;
        
        //make ajax call to delete schedule from database
        $.ajax({
            url: url,
            data: {},
            dataType: 'json',
            success: function (data) {
                schedule_title = schedule.attr('name');
                
                for (var i = 0; i < data['course_ids'].length; i++) {
                    id = data['course_ids'][i]
                    scheduler.deleteEvent(id + "0" + schedule_title);
                    scheduler.deleteEvent(id + "1" + schedule_title);
                    scheduler.deleteEvent(id + "2" + schedule_title);
                    scheduler.deleteEvent(id + "3" + schedule_title);
                    scheduler.deleteEvent(id + "4" + schedule_title);
                }
                
                schedule.closest('.js-schedule-container').remove();
                new_schedule = data['new_schedule_title']
                
                $(".js-schedule")[0].checked = true;
        
                change_schedule(new_schedule);
                
                scheduler.updateView();
                update_page();
            }
        });
    });

    // logic for workweek view
    scheduler.filter_workweek = function(id, event) {
        // display event only if its type is set to true in filters obj
        // or it was not defined yet - for newly created event
        if (filters[event.type] || event.type==scheduler.undefined) {
            console.log(event.type)
            return true;
        }
        // default, do not display event
        return false;
    };
    // End Calendar swapping code

    //Mouse highlighting code
	scheduler.attachEvent("onTemplatesReady", function() {
		var highlight_step = 60; // we are going to highlight 30 minutes timespan

		var highlight_html = "";
		var hours = scheduler.config.last_hour - scheduler.config.first_hour; // e.g. 24-8=16
		var times = hours*60/highlight_step; // number of highlighted section we should add
		var height = scheduler.config.hour_size_px*(highlight_step/60);
		for (var i=0; i<times; i++) {
			highlight_html += "<div class='highlighted_timespan' style='height: "+height+"px;'></div>"
		}
		scheduler.addMarkedTimespan({
			days: "fullweek",
			zones: "fullday",
			html: highlight_html
		});
	});
    
    //We can compare event_id's with the events that have been rendered on the scheduler and if they match
        //what we are looking for we can change the style of those events.
    function startHighlight(course_id) {
        var schedule_title = $(".js-schedule:checked").attr('name');
        for (var day=0; day < 5; day++) {
            for(var i=0; i<scheduler._rendered.length; i++) {
                if(scheduler._rendered[i].getAttribute('event_id') === course_id + '' + day + schedule_title) {
                    var schedule_event = scheduler._rendered[i];
                    schedule_event.style.backgroundColor = "black";
                    schedule_event.style.borderRadius = "6px";
                }
            }
        }
    }
    
    function stopHighlight(course_id) {
        var schedule_title = $(".js-schedule:checked").attr('name');
        for (var day=0; day < 5; day++) {
            for(var i=0; i<scheduler._rendered.length; i++) {
                if(scheduler._rendered[i].getAttribute('event_id') === course_id + '' + day + schedule_title) {                    
                    var schedule_event = scheduler._rendered[i];
                    schedule_event.style.backgroundColor = "transparent";
                    schedule_event.style.borderRadius = "0";
                }
            }
        }
    }
    
    //Highlight hovered course
    $(document).on('mouseover', '.current-course', function () {
        var event_target = $(event.target).closest('.current-course');
        var course_id = event_target.attr('id');
        var course_id = course_id.slice(5);
        startHighlight(course_id);
    });
    
    //Highlight hovered course
    $(document).on('mouseout', '.current-course', function () {
        var event_target = $(event.target).closest('.current-course');
        var course_id = event_target.attr('id');
        var course_id = course_id.slice(5);
        stopHighlight(course_id);
    });
    
    //Highlight conflicting courses
    $(document).on('mouseover', '.js-add', function () {
        var course_id = $(event.target).attr('conflict-id');
        startHighlight(course_id);
    });
    
    //Highlight conflicting courses
    $(document).on('mouseout', '.js-add', function () {
        var course_id = $(event.target).attr('conflict-id');
        stopHighlight(course_id);
    });
    
    //Highlight course to be removed
    $(document).on('mouseover', '.js-del', function () {
        var course_id = $(event.target).attr('section-id');
        startHighlight(course_id);
    });
    
    //Highlight course to be removed
    $(document).on('mouseout', '.js-del', function () {
        var course_id = $(event.target).attr('section-id');
        stopHighlight(course_id);
    });
    
    
    //On hover highlight courses
    scheduler.templates.event_class=function(start, end, event){
        var css = "";
        if(event.id == scheduler.getState().select_id){
            css += " selected";
        }
        return css; // default return
    }
    

    scheduler.init('scheduler_here', new Date(2018, 0, 1), "workweek");
    
    var searchHidden = false;
    function toggleSearch() {
        searchHidden ? searchHidden = false : searchHidden = true;
        if (searchHidden) {
            //switch between max/minimize arrows
            expandBtn.style.display = 'block';
            hideBtn.style.display = 'none';

            //change the size of results to larger when search filters hidden
            $('.fixed-panel').css('min-height', '42rem');
            $('.fixed-panel').css('max-height', '42rem'); 
        } else {
            //switch between max/minimize arrows
            expandBtn.style.display = 'none';
            hideBtn.style.display = 'block';

            //change the size of results to smaller when search filters shown
            $('.fixed-panel').css('min-height', '28rem');
            $('.fixed-panel').css('max-height', '28rem');
        }
        $.ajax({
            url: $('#meta').attr('update-session-url'),
            data: {'filters_expanded': !searchHidden,},
            dataType: 'json',
            success: function (data) {
                
            }
        });
    }
    
    // This function handles extra behavior for expanding search filters, such as swapping
    // the expand button
    $('#searchToggleBTN').on('click', function () {
        toggleSearch();
    });
    
    /*
    Add all previously stored classes to the schedule
    Processed as an ajax json request for convenience.
    */
    
    
    $.ajax({
        url: $('#meta').attr('schedule-courses-url'),
        data: {},
        dataType: 'json',
        success: function (data) {
            var count = data['count'];
            var courses = data['courses'];
            var schedule = data['active_schedule'];
            var filters_expanded = data['filters_expanded'];
            
            //I don't know why this gets converted to a string...
            if (filters_expanded === 'false') {
                toggleSearch();
            }
            
            for (i = 0; i < count; i++) {
                scheduler.parse([courses[i]], 'json');
            }
            
            $('.js-schedule:checked').prop('checked', false);
            $('.js-schedule[name="' + schedule + '"]').prop('checked', true);
            
            change_schedule(schedule);
            update_page();
        }
    });
}
