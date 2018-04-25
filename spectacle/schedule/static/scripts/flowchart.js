
// examle data for test and implement, will connect to serve later.
// courseNumber: [listOfPreRequirement, courseLevelNum]
// will add more features for more funcitons.


//this is a temp work around until I implement the transfer with ajax
var course_list = {}
var parsed = JSON.parse(v.innerText);
for(p in parsed)
{
	Object.assign(course_list, parsed[p]);
	//console.log("p:",co[p])
	//console.log(course_list)
	//course_list.push(parsed[p]);
};

var examples = course_list

//this is temp for testing to trim down results
// for(var key in examples){
// 	examples = examples[key]
// }

// examples with format courseNum: [(D)listOfPre(0), (D)levelNumber(1), Selected(2), linked(3), (D)credits(4), (D)required(5), root(6)]

//end of temp

// examle data for test and implement, will connect to serve later.
// courseNumber: [listOfPreRequirement, courseLevelNum]
// will add more features for more funcitons. 
// Note: (D) means things should be loaded from server. 
// Selected, Linked, root shouble be initialized to 0.
// examples with format courseNum: [(D)listOfPre(0), 
//(D)levelNumber(1), Selected(2), linked(3), 
//(D)credits(4), (D)required(5), root(6), title(7), department(8)]

// var examples = {
// 	"cs121":[[],1,0,0,4,1,0],
// 	"cs187":[["cs121"], 1,0,0,4,1,0],
// 	"cs220":[["cs121","cs187"], 2,0,0,4,1,0],
// 	"cs230":[["cs121","cs187"], 2,0,0,4,1,0],
// 	"cs240":[["cs121","cs187","cs220"], 2,0,0,4,1,0],
// 	"cs250":[["cs121","cs187","cs230"], 2,0,0,4,1,0],
// 	"cs326":[["cs121","cs187","cs240","cs220"],2,0,0,3,0,0],
// 	"cs383":[["cs121","cs187","cs230","cs250"],2,0,0,3,0,0],
// 	"cs446":[["cs121","cs187","cs230","cs250"],2,0,0,3,0,0],
// 	"cs589":[["cs230","cs250","cs383"],2,0,0,3,0,0]
// };

// create course section for each couser by button
for(key in examples){
	for(a in examples[key]){
		if(examples[key][a] === "1"){
			examples[key][a] = 1;
		}
		if(examples[key][a] === "0"){
			examples[key][a] = 0;
		}
	}
}
function courseBtn(course){
	btn = "<button class='button' id = 'Button'>TextREQURIED</br>CREDITS credits</button>";
	// auto replace each button and text with .replace().
	//console.log('course: ', course)
	if(examples[course][5] === 1){
		btn = btn.replace("REQURIED", "*");
	}
	else{
		btn = btn.replace("REQURIED", "");
	}
	btn = btn.replace("Button", course);
	btn = btn.replace("CREDITS", examples[course][4]);
	title_1 = course.replace("title", examples[course][8] + "-");
	btn = btn.replace("Text", title_1);
	return btn;
}


// auto table generator.
// append all course from data to tables. Seperate by class level. 
function makeTable(){
	console.log(1);
	var table = "";
	var rowEnd = "</tr>";
	var tableDataStart = "<td>";
	var tableDataEnd = "</td>";
	for(var i = 1; i < 9; i++){
		console.log(row_num);
		var rowStart = "<tr id = 'levelNUM00' ><th>LEVEL LEL00+</th>";
		rowStart = rowStart.replace("LEL", i);
		table+=rowStart.replace("NUM", i);
		var row_num = 1;
		for(var key in examples){
			//console.log('examples[key]: ',examples[key], key)
			var values = examples[key];
			if(Number(values[1]) === i){
				if(row_num === 0){
					table+="<tr>"
					table+=tableDataStart;
					table+=tableDataEnd;
					table+=tableDataStart;
					table+=courseBtn(key);
					table+=tableDataEnd;
					row_num+=2;
				}
				else if(row_num === 8){
					table+=tableDataStart;
					table+=courseBtn(key);
					table+=tableDataEnd;
					table+=rowEnd;
					row_num = 0;
				}
				//courseInfo_1 = tableDataStart.replace("courseNum", key);
				else{
					table+=tableDataStart;
					table+=courseBtn(key);
					table+=tableDataEnd;
					row_num+=1;
				}
			}
		}
		table+=rowEnd;

	}
	document.write("<table>" + table + "</table>");
}
function highlight(e){
	e.style.border = "4px solid #a92323";
}
function unhighlight(e){
	e.style.border = "3px solid #65a9d7";
}

// implement the even function to all course buttons so that when mouse move over one course system will highlight all pre-req.
function addMoveOverEvent(course){
	var curr = document.getElementById(course);
	//console.log(course, curr)
	if(curr === null){
		console.log("course: ", course, " is null")
	}

	curr.addEventListener("mouseenter", function(e) {   
		if(Number(examples[course][2]) != 1){
	    // highlight the mouseenter target
		// highlight by changing the border color.
	    	highlight(e.target);
	    	var pre_requ = examples[course][0];
		// loop for all pre_requ for one course
			// warn: for in loop will not work.
	    	for( var i = 0; i<pre_requ.length; i++ ){
				var pre = document.getElementById('title' + pre_requ[i]);
				if(pre != null)
				{
					highlight(pre);	
				}
			}
		}
    	
	})
    // reset the color after mouse leave
    curr.addEventListener("mouseleave", function(e){
    	if(Number(examples[course][2]) != 1){
	    	unhighlight(e.target);
	    	var pre_requ = examples[course][0];
	    	///console.log("pres: ", pre_requ)
	    	for( var i = 0; i<pre_requ.length; i++ ){
	    		if(examples[ ('title' + pre_requ[i]) ] != null && examples[ ('title' + pre_requ[i]) ][2] != 1){
	    			//console.log(examples[('title' + pre_requ[i])])
					var pre = document.getElementById('title' + pre_requ[i]);
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
			examples[('title' + pre_requ[i])][3]-=1;
		}
		examples[course][6] = 0;
	}


}

function addLink(course){
	var pre_requ = examples[course][0];
	for(var i = 0; i< pre_requ.length; i++){
		examples[('title' + pre_requ[i])][3]+=1;
	}
}

function addDoubleClickerEvent(course){
	var curr = document.getElementById(course);
	// if(curr == null){return}//this is to stop errors but must be changed in future
	curr.addEventListener("dblclick", function(e){
		window.open("courseModel.html");
	})
}
function addOnClikerEvent(course){
	var curr = document.getElementById(course);
	// if(curr === null){return}//this is to stop errors but must be changed in future
	curr.addEventListener("click", function(e){
		if(examples[course][2] === 0){
			examples[course][2] = 1;
			highlight(e.target);
			var pre_requ = examples[course][0];
			addLink(course);
			examples[course][6] = 1;
	    	for( var i = 0; i<pre_requ.length; i++ ){
	    		// selected. 
	    		examples['title' + pre_requ[i]][2] = 1;
	    		// linked to course
				var pre = document.getElementById('title' + pre_requ[i]);
	    		highlight(pre);
			}
			totalCredits();
		}
		else{
			
			if(Number(examples[course][3]) === 0){
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



for(var key in examples){
	addMoveOverEvent(key);
	addOnClikerEvent(key);
	addDoubleClickerEvent(key);
}

function totalCredits(){
	credits = 0
	for(var key in examples){
		var courseInfo = examples[key];
		if(examples[4] != null){
			credits += Number(courseInfo[2])*Number(courseInfo[4][1]);
		}
	}
	var element = document.getElementById("credits");
	element.innerHTML = "Total Credits: " + credits;
}
function drawTable(){
	makeTable();
	console.log(examples)
	for(var key in examples){
		//console.log('key:',key)
		addMoveOverEvent(key);
		addOnClikerEvent(key);
		addDoubleClickerEvent(key);
	}
	
}





