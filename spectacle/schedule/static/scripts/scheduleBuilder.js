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
    function update_page(url) {
        var schedule = $(".js-schedule:checked").attr('schedule-id');
                
        // Reload the current courses
        $('#current-courses').html('').load(
            url + '?schedule=' + schedule
        );
        
        // If the currently open tab is a course detail tab, reload it
        var active_tab = $('.course-tab').find("a.active");
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
    
    function change_schedule(url, schedule_name) {
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
        var url = $(event.target).attr('courses-url');
        var schedule_url = $(event.target).attr('schedule-url');
        
        change_schedule(url, $(event.target).attr('name'));
        
        $.ajax({
            url: schedule_url,
            data: {'schedule_title': $(".js-schedule:checked").attr('name')},
            dataType: 'json',
            success: function (data) {
                update_page(url);
            }
        });
        
    });
    
    //TODO: consider positioning of this function
    //It needs direct access to change_schedule, which needs access to
    // filters. But it is strange that it is separated
    // Delete a schedule
    $('.js-del-schedule').on('click', function () {
        var schedule = $(".js-schedule:checked");
        var url = $(event.target).attr('url');
        var courses_url = schedule.attr('courses-url');
        
        if ($('.js-schedule').length === 1) {
            //TODO: give error message to user
            console.log("cannot delete last schedule");
            return
        }
        
        var new_schedule = $(".js-schedule")[0].name;
        
        schedule.closest('.js-schedule-container').remove();
        $(".js-schedule")[0].checked = true;
        
        change_schedule(courses_url, $(".js-schedule")[0].name);
                
        //make ajax call to delete schedule from database
        $.ajax({
            url: url,
            data: {
                'schedule':schedule.attr('name'),
                'new_schedule': new_schedule,
            },
            dataType: 'json',
            success: function (data) {
                schedule = schedule.attr('name');
                
                for (var i = 0; i < data['course_ids'].length; i++) {
                    id = data['course_ids'][i]
                    scheduler.deleteEvent(id + "0" + schedule);
                    scheduler.deleteEvent(id + "1" + schedule);
                    scheduler.deleteEvent(id + "2" + schedule);
                    scheduler.deleteEvent(id + "3" + schedule);
                    scheduler.deleteEvent(id + "4" + schedule);
                }
                
                scheduler.updateView();
                update_page(courses_url);
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
        url: 'ajax/schedule',       //TODO: probably shouldn't be hardcoded
        data: {},
        dataType: 'json',
        success: function (data) {
            var count = data['count'];
            var courses = data['courses'];
            var schedule = data['active_schedule'];
            var url = data['url'];
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
            
            change_schedule(url, schedule);
            update_page(url);
        }
    });
}
