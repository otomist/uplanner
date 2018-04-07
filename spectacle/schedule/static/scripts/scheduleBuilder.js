function init() {
    scheduler.config.xml_date = "%Y-%m-%d %H:%i";
    scheduler.config.first_hour = 6;
    scheduler.config.last_hour = 20;
    scheduler.config.limit_time_select = true;
    scheduler.config.time_step = 60;

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
        if (i === 0) {
            filters[filter_input.name] = true;
        }
        filter_input.checked = filters[filter_input.name];
        

        // attach event handler to update filters object and refresh view (so filters will be applied)
        filter_input.onchange = function() {
            var filter_inputs_radio = document.getElementById("filters_wrapper").getElementsByTagName("input");
            for(var j=0; j<filter_inputs_radio.length; j++) {
                if(filter_inputs_radio[j] !== this) {
                    filter_inputs_radio[j].checked = false;
                }
                filters[filter_inputs_radio[j].name] = !!filter_inputs_radio[j].checked;
            }
            scheduler.updateView();
        }
    }

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

    /*
    Add all previously stored classes to the schedule
    Processed as an ajax json request for convenience.
    */
    $.ajax({
        url: 'ajax/schedule',
        data: {},
        dataType: 'json',
        success: function (data) {            
            count = data['count'];
            courses = data['courses'];
            
            for (i = 0; i < count; i++) {
                scheduler.parse([courses[i]], 'json');
            }
        }
    });
}
