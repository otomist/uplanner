
// examle data for test and implement, will connect to serve later.
// courseNumber: [listOfPreRequirement, courseLevelNum]
// will add more features for more funcitons.


//this is a temp work around until I implement the transfer with ajax
var course_list = {}
var parsed = JSON.parse(v.innerText);
for(p in parsed)
{
	Object.assign(course_list, parsed[p]);
	console.log("p:",parsed[p])
	//course_list.push(parsed[p]);
};
//end of temp

//for debugging:
// console.log("EXMAPLES:", course_list)
// var e = {
// 	"cs121":[[],1],
// 	"cs187":[["cs121"], 1],
// 	"cs220":[["cs121","cs187"], 2],
// 	"cs230":[["cs121","cs187"], 2],
// 	"cs240":[["cs121","cs187","cs220"], 2],
// 	"cs250":[["cs121","cs187","cs230"], 2],
// 	"cs326":[["cs121","cs187","cs240","cs220"],3],
// 	"cs383":[["cs121","cs187","cs230","cs250"],3],
// 	"cs446":[["cs121","cs187","cs230","cs250"],4],
// 	"cs589":[["cs230","cs250","cs383"],5]
// };
//course_list = e;
//console.log("E: ", e);

// create course section for each couser by button
function courseBtn(course_number){
	console.log("course: ", course_number);
	btn = "<button class='button' id = 'Button'><a class='text' href='index.html'>Text</a><p>coursetitle</p></a>";
	// auto replace each button and text with .replace().
	btn = btn.replace("Button", course_number);
	btn = btn.replace("Text", course_number);
	btn = btn.replace("coursetitle", course_list[course_number][2]);
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
		for(var key in course_list){
			var values = course_list[key];
			//console.log("values: ", values);
			if(Number(key[0]) === i){
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
function addEvent(course_number){
	var curr = document.getElementById(course_number);
	curr.addEventListener("mouseenter", function(e) {   
    // highlight the mouseenter target
	// highlight by changing the border color.
    	e.target.style.border = "7px solid #881c1c";
    	var pre_requ = course_list[course_number][0];
    	console.log("pres: ", pre_requ);
	// loop for all pre_requ for one course
		// warn: for in loop will not work.
    	for( var i = 0; i<pre_requ.length; i++ ){
			console.log(pre_requ[i]);
			//extract the number from the pre req string 
			var req_number = pre_requ[i].replace( /^\D+/g, '');
			var pre = document.getElementById(req_number);
    		pre.style.border = "7px solid #881c1c";
		}

    	
	})
    // reset the color after mouse leave
    curr.addEventListener("mouseleave", function(e){
    	//the effect used when leaving
    	e.target.style.border = "5px solid #0a3c59";
    	var pre_requ = course_list[course_number][0];
    	for( var i = 0; i<pre_requ.length; i++ ){
			//console.log(pre_requ[i]);
			//extract the number from the pre req string 
			var req_number = pre_requ[i].replace( /^\D+/g, '');
			var pre = document.getElementById(req_number);
    		pre.style.border = "5px solid #0a3c59";
		}
    })
}

//console.log("course_list size: ", Object.keys(course_list).length)
//iterate over the lists of courses and add events to the table elements 
for(var key in course_list){
	addEvent(key);
}





