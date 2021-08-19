'use strict'

//variables for part 4
var selected_cause_hazard = '';
var selected_effect_hazard = '';
var cause_hazards = ['cause_earthquakes', 'cause_storms', 'cause_landslides', 'cause_space', 'cause_volcanoes', 'cause_waves'];
var effect_hazards = ['effect_earthquakes', 'effect_storms', 'effect_landslides', 'effect_space', 'effect_volcanoes', 'effect_waves'];

//Drag and Drop

function allowDrop(ev) {
    ev.preventDefault();
  }
  
  function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
  }
  
  function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    ev.target.appendChild(document.getElementById(data));
  }

//For debugging
//document.getElementById('log').innerHTML += hazard_type;




//Page 4 click
function select_cause_hazard(hazard_type) {
  if (hazard_type == selected_cause_hazard) {
    document.getElementById(hazard_type).style.border = '';
  }
  else {
    selected_cause_hazard = hazard_type;
    for (let i = 0; i < cause_hazards.length; i++) {
      if (hazard_type == cause_hazards[i]){
        document.getElementById(cause_hazards[i]).style.border = '3px solid skyblue';
      }
      else {
        document.getElementById(cause_hazards[i]).style.border = '';
      }
    }
  }
}

function select_effect_hazard(hazard_type) {
  if (hazard_type == selected_effect_hazard) {
    document.getElementById(hazard_type).style.border = '';
  }
  else {
    selected_effect_hazard = hazard_type;
    for (let i = 0; i < effect_hazards.length; i++) {
      if (hazard_type == effect_hazards[i]){
        document.getElementById(effect_hazards[i]).style.border = '3px solid skyblue';
      }
      else {
        document.getElementById(effect_hazards[i]).style.border = '';
      }
    }
  }
  drawConnector(selected_cause_hazard, selected_effect_hazard);
}

// Draw arrows part 4

function get_y_coordinates(element) {
  var container_height = 400;
  var item_height = container_height/13;

  var index = cause_hazards.indexOf(element);

  if (index == -1) {
    index = effect_hazards.indexOf(element);
  }

  var y = 1.5*item_height + 2*index*item_height;

  return y;
};

function drawConnector(left, right) {
  var arrow = document.getElementById("arrow_line");
	
  var y_left = get_y_coordinates(left);
  var y_right = get_y_coordinates(right);
  arrow.setAttribute("y1", y_left);
  arrow.setAttribute("y2", y_right);
}

drawConnector("cause_storms", "effect_waves");


// Draw and erase arrow buttons

function draw_arrow() {
  var current_arrow = document.getElementById("arrow");
  var new_arrow = current_arrow.cloneNode(true);
  new_arrow.id = "drawn_arrow";
  //new_arrow.arrow_head.style.stroke = "#797979";
  //new_arrow.arrow_line.style.fill = "#797979";
  //new_arrow.arrow_line.y1 = 0;
  //new_arrow.arrow_line.y2 = 100;
  document.getElementById("drawn_arrows").appendChild(new_arrow);
}

function erase_arrow() {
  
}

function highlight_arrow() {
  var arrow_line = document.getElementById("arrow_line");
  var arrow_head = document.getElementById("arrow_head");
  if (arrow_line.style.stroke == "red") {
    arrow_line.setAttribute("style", "stroke: black;");
    arrow_head.setAttribute("style", "fill: black;");
  }
  else {
    arrow_line.setAttribute("style", "stroke: red;");
    arrow_head.setAttribute("style", "fill: red;");
  }
  
}

//Pagination

var bulletClasses = {
  elements: {
    container: ".pindicator",
    bullet: ".bullet",
  },
  helpers: {
    past: "past",
    current: "current",
    next: "next",
    future: "future",
  }
};

var bulletEls;
document.addEventListener("DOMContentLoaded", initBullets);

function initBullets() {
  bulletEls = Array.prototype.slice.call(
    document.body.querySelectorAll(bulletClasses.elements.bullet)
  );
  bulletEls.forEach(function(el) {
    el.addEventListener("mousedown", function(event) {
      gotoPage(bulletEls.indexOf(this) + 1);
    });
    el.addEventListener("touchstart", function(event) {
      event.preventDefault();
      gotoPage(bulletEls.indexOf(this) + 1);
    });
  });
}

function gotoPage(pageNum) {
  bulletEls.forEach(function(e) {
    e.classList.remove.apply(e.classList,
      Object.keys(bulletClasses.helpers).map(function(e){
        return bulletClasses.helpers[e];
      })
    )
  });
  bulletEls[pageNum - 1].classList.add(bulletClasses.helpers.current);
  if(pageNum > 1) {
    for(var i = 0; i < pageNum; i++) {
      bulletEls[i].classList.add(bulletClasses.helpers.past);
    }
  }
  if(pageNum < bulletEls.length) {
    bulletEls[pageNum].classList.add(bulletClasses.helpers.next);
    for(var i = bulletEls.length - 1; i >= pageNum; i--) {
      bulletEls[i].classList.add(bulletClasses.helpers.future);
    }
  }
  update_page(pageNum)
}

//Update the page so it only shows the relevant elements
function update_page(current_page) {
  // Set elements hidden first so that sections that belong to multiple pages are displayed
  if (current_page == 1) {
    var other_pages = document.querySelectorAll('.page2, .page3, .page4, .page5, .page6');
    var page1 = document.querySelectorAll('.page1');
    update_visibility(other_pages, page1);
  }
  else if (current_page == 2) {
    var other_pages = document.querySelectorAll('.page1, .page3, .page4, .page5, .page6');
    var page2 = document.querySelectorAll('.page2');
    update_visibility(other_pages, page2);
  }
  else if (current_page == 3) {
    var other_pages = document.querySelectorAll('.page1, .page2, .page4, .page5, .page6');
    var page3 = document.querySelectorAll('.page3');
    update_visibility(other_pages, page3);
  }
  else if (current_page == 4) {
    var other_pages = document.querySelectorAll('.page1, .page2, .page3, .page5, .page6');
    var page4 = document.querySelectorAll('.page4');
    update_visibility(other_pages, page4);
  }
  else if (current_page == 5) {
    var other_pages = document.querySelectorAll('.page1, .page2, .page3, .page4, .page6');
    var page5 = document.querySelectorAll('.page5');
    update_visibility(other_pages, page5);
  }
  else if (current_page == 6) {
    var other_pages = document.querySelectorAll('.page1, .page2, .page3, .page4, .page5');
    var page6 = document.querySelectorAll('.page6');
    update_visibility(other_pages, page6);
  }
}

function update_visibility(other_pages, current_page) {
    for (let i = 0; i < other_pages.length; i++) {
      other_pages[i].style.display = 'none';
    }
    for (let i = 0; i < current_page.length; i++) {
      current_page[i].style.display = 'block';
    }
}

//initialize the page
window.onload = update_page(1)