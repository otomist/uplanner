
// examle data for test and implement, will connect to serve later.
// courseNumber: [listOfPreRequirement, courseLevelNum]
// will add more features for more funcitons. 
var examples = {
	"cs121":[[],1],
	"cs187":[["cs121"], 1],
	"cs220":[["cs121","cs187"], 2],
	"cs230":[["cs121","cs187"], 2],
	"cs240":[["cs121","cs187","cs220"], 2],
	"cs250":[["cs121","cs187","cs230"], 2],
	"cs326":[["cs121","cs187","cs240","cs220"],3],
	"cs383":[["cs121","cs187","cs230","cs250"],3],
	"cs446":[["cs121","cs187","cs230","cs250"],4],
	"cs589":[["cs230","cs250","cs383"],5]
};

// create course section for each couser by button
function courseBtn(course){
	btn = ""<button class='button' id = 'Button'><a class='text' href='index.html'>Text</a></a>"";
	// auto replace each button and text with .replace().
	btn = btn.replace("Button", course);
	btn = btn.replace("Text", course)
	return btn;
}


// auto table generator.
// append all course from data to tables. Seperate by class level. 
function makeTable(){
	var table = "";
	var rowEnd = "</tr>";
	var tableDataStart = "<td>";
	var tableDataEnd = "</td>";
	for(var i = 1; i < 6; i++){
		var rowStart = "<tr id = 'levelNUM00'><th>level LEL00+</th>";
		rowStart = rowStart.replace("LEL", i);
		table+=rowStart.replace("NUM", i);
		for(var key in examples){
			var values = examples[key];
			if(values[1] === i){
				table+=(tableDataStart.replace("courseNum", key));
				table+=courseBtn(key);
				table+=tableDataEnd;
			}
		}
		table+=rowEnd;

	}
	document.write("<table>" + table + "</table>");
}
makeTable();


// implement the even function to all course buttons so that when mouse move over one course system will highlight all pre-req.
function addEvent(course){
	var curr = document.getElementById(course);
	curr.addEventListener("mouseenter", function(e) {   
    // highlight the mouseenter target
	// highlight by changing the border color.
    	e.target.style.border = "5px solid red";
    	var pre_requ = examples[course][0];
	// loop for all pre_requ for one course
		// warn: for in loop will not work.
    	for( var i = 0; i<pre_requ.length; i++ ){
			console.log(pre_requ[i]);
			var pre = document.getElementById(pre_requ[i]);
    		pre.style.border = "5px solid red";
		}

    	
	})
    // reset the color after mouse leave
    curr.addEventListener("mouseleave", function(e){
    	e.target.style.border = "5px solid #0a3c59";
    	var pre_requ = examples[course][0];
    	for( var i = 0; i<pre_requ.length; i++ ){
			console.log(pre_requ[i]);
			var pre = document.getElementById(pre_requ[i]);
    		pre.style.border = "5px solid #0a3c59";
		}
    })
}

for(var key in examples){
	addEvent(key);
}





