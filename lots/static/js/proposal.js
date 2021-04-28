
const expandRow = (e) => {
    // find the button and use it to find the totalRow element
    let totalRow = e.target.parentElement.parentElement;
    // change the styles of the next rows until you reach the next
    // button
    let sibling = totalRow.nextElementSibling;
    while (sibling.className.search("tableLotHeader") > -1 ||
    sibling.className.search("tableLot") > -1) {
            
            // find the classNames and see if it is collapsed.
            // switch if you find the class
            // if collapsed, switch class, else don't do anything
            if (sibling.className.search(/collapsed/i) > -1) {
                sibling.className = sibling.className.replace(/collapsed/i, "expanded");
            } else {
                sibling.className = sibling.className.replace(/expanded/i, "collapsed");
            }
            sibling = sibling.nextElementSibling;
    }
}

// add eventListener to the expandRow buttons to expand on click
document.querySelectorAll('.rowExpandButton').forEach(item => {
    item.addEventListener("click", expandRow);
})