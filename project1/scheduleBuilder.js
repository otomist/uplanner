function init() {
    scheduler.config.xml_date = "%Y-%m-%d %H:%i";
    scheduler.init('scheduler_here', new Date(2018, 0, 1), "week");

    //used to make events read_only if they have that attribute.
    function block_readonly(id){
        if (!id) return true;
        return !this.getEvent(id).readonly;
    }
    scheduler.attachEvent("onBeforeDrag",block_readonly)
    scheduler.attachEvent("onClick",block_readonly)
}
