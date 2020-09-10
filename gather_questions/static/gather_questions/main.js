const ENTER = 13; 
const SPACE = 32

function isKeyPressedToSubmit (e, submitKeys) {
  return submitKeys.includes(e.keyCode); 
}; 

function patternCondition (rgExp) {
  return function (el) {
    if (el) {
      return rgExp.test(el.innerText); 
    }; 
    return false; 
  }; 
}; 

function onKeyUp (keys) {
  return function (event) {
    
    if (isKeyPressedToSubmit(event, keys)) {
      button.click(); 
    };
    return true; 
  };
};


let input = document.getElementById("qinput"); 

input.addEventListener("keyup", onKeyUp([ENTER])); 

document.getElementById("submit") 
  .addEventListener("keyup", onKeyUp([ENTER, SPACE])); 

window.onload = function(e) {
  let el = document.getElementsByClassName("num-display")[0]; 
  
  let hasNumberDisplay = patternCondition(/\d+$/); 

  if (hasNumberDisplay(el)) {
    input.focus();     
  }; 
}; 

