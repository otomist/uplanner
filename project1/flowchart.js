

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
function courseBtn(course){
	btn = "<a href='#' class='button' id = 'Button'>Text</a>";
	btn = btn.replace("Button", course);
	btn = btn.replace("Text", course)
	return btn;
}



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

function addEvent(course){
	var curr = document.getElementById(course);
	curr.addEventListener("mouseenter", function(e) {   
    // highlight the mouseenter target

    	e.target.style.border = "6px solid green";
    	var pre_requ = examples[course][0];
    	console.log(pre_requ);
    	for( var i = 0; i<pre_requ.length; i++ ){
			console.log(pre_requ[i]);
			var pre = document.getElementById(pre_requ[i]);
    		pre.style.border = "6px solid green";
		}

    	
	})
    // reset the color after a short delay
    curr.addEventListener("mouseleave", function(e){
    	e.target.style.border = "5px solid #0a3c59";
    	var pre_requ = examples[course][0];
    	console.log(pre_requ);
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





