function init() {
    scheduler.config.xml_date = "%Y-%m-%d %H:%i";
    scheduler.config.first_hour = 6;
    scheduler.config.last_hour = 20;
    scheduler.config.limit_time_select = true;

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
    var filters = {
        calendar1: true,
        calendar2: false,
        calendar3: false
    };

    var filter_inputs = document.getElementById("filters_wrapper").getElementsByTagName("input");
    for (var i=0; i<filter_inputs.length; i++) {
        var filter_input = filter_inputs[i];

        // set initial input value based on filters settings
        filter_input.checked = filters[filter_input.name];

        // attach event handler to update filters object and refresh view (so filters will be applied)
        filter_input.onchange = function() {
            var filter_inputs_radio = document.getElementById("filters_wrapper").getElementsByTagName("input");
            for(var j=0; j<filter_inputs_radio.length; j++) {
                if(filter_inputs_radio[j] !== this){
                    filter_inputs_radio[j].checked = false;
                }
                filters[filter_inputs_radio[j].name] = !!filter_inputs_radio[j].checked;
                console.log(filter_inputs_radio[j].name+" is shown?: "+ filters[filter_inputs_radio[j].name]);
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

    scheduler.init('scheduler_here', new Date(2018, 0, 1), "workweek");

    scheduler.parse([
        { start_date: "2018-01-01 12:00", end_date: "2018-01-01 19:00", text:"Calendar1 some course", type: "calendar1" },
        { start_date: "2018-01-05 14:00", end_date: "2018-01-05 16:00", text:"Calendar1 some course 2", type: "calendar1" },
        { start_date: "2018-01-02 16:30", end_date: "2018-01-02 18:00", text:"Calendar2 some other course", type: "calendar2" },
        { start_date: "2018-01-03 18:30", end_date: "2018-01-03 20:00", text:"Calendar3 a different course", type: "calendar3" }
    ],"json");
}
