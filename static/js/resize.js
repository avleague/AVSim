// CÓDIGO BASEADO DE https://stackoverflow.com/questions/12194469/best-way-to-do-a-split-pane-in-html

// This function is used for dragging and moving
function dragElement( element, direction, handler ){
	// Two variables for tracking positions of the cursor
	const drag = { x : 0, y : 0 };
	const delta = { x : 0, y : 0 };
	/* If present, the handler is where you move the DIV from
	   otherwise, move the DIV from anywhere inside the DIV */
	handler ? ( handler.onmousedown = dragMouseDown ): ( element.onmousedown = dragMouseDown );
  
	// A function that will be called whenever the down event of the mouse is raised
	function dragMouseDown( e ){
	  drag.x = e.clientX;
	  drag.y = e.clientY;
	  document.onmousemove = onMouseMove;
	  document.onmouseup = () => { document.onmousemove = document.onmouseup = null; }
	}
  
	// A function that will be called whenever the up event of the mouse is raised
	function onMouseMove( e ){
	  const currentX = e.clientX;
	  const currentY = e.clientY;
  
	  delta.x = currentX - drag.x;
	  delta.y = currentY - drag.y;
  
	  const offsetLeft = element.offsetLeft;
	  const offsetTop = element.offsetTop;
  
	  var first = document.getElementById("left-page");
	  var right = document.getElementById("right-page");
		var second = document.getElementById("right-page-top");
		var third = document.getElementById("right-page-bottom");
	  
	  let firstWidth = first.offsetWidth;
	  let rightWidth = right.offsetWidth;
		let secondHeight = second.offsetHeight;
		let thirdHeight = third.offsetHeight;
	  
	  if (direction === "H" ) {
		  element.style.left = offsetLeft + delta.x + "px";
		  firstWidth += delta.x;
		  rightWidth -= delta.x;
	  }
	  
		if (direction === "V" ) {
		  element.style.top = offsetTop + delta.y + "px";
		  secondHeight += delta.y;
		  thirdHeight -= delta.y;
	  }
	  
	  drag.x = currentX;
	  drag.y = currentY;
	  
	  first.style.width = firstWidth + "px";
	  right.style.width = rightWidth + "px";
	  
		second.style.height = secondHeight + "px";
	  third.style.height = thirdHeight + "px";
	}
  }
  
  dragElement( document.getElementById("separator-col"), "H" );
  dragElement( document.getElementById("separator-row"), "V" );