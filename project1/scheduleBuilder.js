function init() {
    scheduler.config.xml_date = "%Y-%m-%d %H:%i";
    scheduler.config.first_hour = 6;
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

    scheduler.init('scheduler_here', new Date(2018, 0, 1), "workweek");
}
