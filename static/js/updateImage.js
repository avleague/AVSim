
function updateImage(){
	var str = ''
	document.getElementById("chart").setAttribute("src", str.concat(document.getElementById("chart").src,"?",new Date().getTime()));
};
//teste();
setInterval(updateImage, 500);