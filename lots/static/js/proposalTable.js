
const expandRow = (e) => {
    // find the button and use it to find the totalRow element
    let totalRow = e.target.parentElement.parentElement;
    // change the styles of the next rows until you reach the next
    // button
    let nextSibling = totalRow.nextElementSibling;
    while (nextSibling.className === 'tableLotHeader' ||
        nextSibling.className === 'tableLot') {
            console.log(nextSibling.className)
        if (nextSibling.style.display === "table-row") {
            nextSibling.style.display = "none";
        } else {
            nextSibling.style.display = "table-row";
        }
        nextSibling = nextSibling.nextElementSibling;
    }
}

document.querySelectorAll('.rowExpandButton').forEach(item => {
    item.addEventListener("click", expandRow);
})