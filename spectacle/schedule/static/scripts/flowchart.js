
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



// examle data for test and implement, will connect to serve later.
// courseNumber: [listOfPreRequirement, courseLevelNum]
// will add more features for more funcitons. 
// examples with format courseNum: [listOfPre(0), levelNumber(1), Selected(2), linked(3), credits(4), required(5), root(6)]
// var examples = {
// 	"cs121":[[],1, 0, 0,4,1,0],
// 	"cs187":[["cs121"], 1,0,0,4,1,0],
// 	"cs220":[["cs121","cs187"], 2,0,0,4,1,0],
// 	"cs230":[["cs121","cs187"], 2,0,0,4,1,0],
// 	"cs240":[["cs121","cs187","cs220"], 2,0,0,4,1,0],
// 	"cs250":[["cs121","cs187","cs230"], 2,0,0,4,1,0],
// 	"cs326":[["cs121","cs187","cs240","cs220"],3,0,0,3,0,0],
// 	"cs383":[["cs121","cs187","cs230","cs250"],3,0,0,3,0,0],
// 	"cs446":[["cs121","cs187","cs230","cs250"],4,0,0,3,0,0],
// 	"cs589":[["cs230","cs250","cs383"],5,0,0,3,0,0]
// };

// create course section for each couser by button
function courseBtn(course){
	btn = "<button class='button' id = 'Button'>TextREQURIED</br>coursetitle</br>CREDITS credits</button>";
	// auto replace each button and text with .replace().
	if(examples[course][5] === 1){
		btn = btn.replace("REQURIED", "*");
	}
	else{
		btn = btn.replace("REQURIED", "");
	}
	btn = btn.replace("Button", course);
	btn = btn.replace("CREDITS", examples[course][4]);
	title_1 = course.replace("cs", "COMPSCI-");
	btn = btn.replace("Text", title_1);
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
				courseInfo_1 = tableDataStart.replace("courseNum", key);
				table+=courseInfo_1;
				table+=courseBtn(key);
				table+=tableDataEnd;
			}
		}
		table+=rowEnd;

	}
	document.write("<table>" + table + "</table>");
}
makeTable();
function highlight(e){
	e.style.border = "7px solid #881c1c";
}
function unhighlight(e){
	e.style.border = "5px solid #0a3c59";
}

// implement the even function to all course buttons so that when mouse move over one course system will highlight all pre-req.
function addMoveOverEvent(course){
	var curr = document.getElementById(course);
	curr.addEventListener("mouseenter", function(e) {   
		if(examples[course][2] != 1){
	    // highlight the mouseenter target
		// highlight by changing the border color.
	    	highlight(e.target);
	    	var pre_requ = examples[course][0];
		// loop for all pre_requ for one course
			// warn: for in loop will not work.
	    	for( var i = 0; i<pre_requ.length; i++ ){
				var pre = document.getElementById(pre_requ[i]);
	    		highlight(pre);
			}
		}
    	
	})
    // reset the color after mouse leave
    curr.addEventListener("mouseleave", function(e){
    	if(examples[course][2] != 1){
	    	unhighlight(e.target);
	    	var pre_requ = examples[course][0];
	    	for( var i = 0; i<pre_requ.length; i++ ){
	    		if(examples[pre_requ[i]][2] != 1){
					var pre = document.getElementById(pre_requ[i]);
	    			unhighlight(pre);
	    		}
			}
		}
    })
}

function deleteLink(course){
	if (examples[course][6] === 1){
		var pre_requ = examples[course][0];
		for(var i = 0; i < pre_requ.length; i++){
			examples[pre_requ[i]][3]-=1;
		}
		examples[course][6] = 0;
	}


}

function addLink(course){
	var pre_requ = examples[course][0];
	for(var i = 0; i< pre_requ.length; i++){
		examples[pre_requ[i]][3]+=1;
	}
}

function addDoubleClickerEvent(course){
	var curr = document.getElementById(course);
	curr.addEventListener("dblclick", function(e){
		window.open("courseModel.html");
	})
}
function addOnClikerEvent(course){

	var curr = document.getElementById(course);
	curr.addEventListener("click", function(e){
		if(examples[course][2] === 0){
			examples[course][2] = 1;
			highlight(e.target);
			var pre_requ = examples[course][0];
			addLink(course);
			examples[course][6] = 1;
	    	for( var i = 0; i<pre_requ.length; i++ ){
	    		// selected. 
	    		examples[pre_requ[i]][2] = 1;
	    		// linked to course
				var pre = document.getElementById(pre_requ[i]);
	    		highlight(pre);
			}
			totalCredits();
		}
		else{
			
			if(examples[course][3] === 0){
				examples[course][2] = 0;
				unhighlight(e.target);
				deleteLink(course);
				totalCredits();
			}
			else{
				alert('You have to take this course according to your plan.');
			}

		}
	})
}


function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {

    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

for(var key in examples){
	addMoveOverEvent(key);
	addOnClikerEvent(key);
	addDoubleClickerEvent(key);
}

function totalCredits(){
	credits = 0
	for(var key in examples){
		var courseInfo = examples[key];
		credits += courseInfo[2]*courseInfo[4];
	}
	var element = document.getElementById("credits");
	element.innerHTML = "Total Credits: " + credits;
}





