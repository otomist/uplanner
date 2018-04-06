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
            '  <button class="btn btn-danger btn-xs js-del-tab btn-results" list-class="js-tab-'+id+'">x</button>\
            </a>').appendTo('#scheduleTab');
            
            
            /*
            $('<li class="nav-item" id="nav-'+id+'">\
            <a class="nav-link" id="'+id+'-tab" data-toggle="tab" href="#'+id+'">'+
            dept+' '+num+
            '</a>').appendTo('#scheduleTab');
            */
            
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