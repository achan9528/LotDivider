
const expandRow = (e) =>{
    let b = e.target;
    let siblingElements = b.parentElement.parentElement.children;
    let tableLotHeader;
    let tableLots = [];
    console.log(siblingElements)
    for (let i =0; i<siblingElements.length; i++){
        if (siblingElements[i].className == "tableLotHeader"){
            tableLotHeader = siblingElements[i]; // find tableLotHeader 
        }
        // find the tableLots and add them to the relevant array
        if (siblingElements[i].className == "tableLot"){
            tableLots.push(siblingElements[i]);
        }
    }
    if (tableLotHeader.style.display === "block"){
        tableLots.forEach(item => {
            item.style.display ="none";
        })
    } else{
        tableLots.forEach(item => {
            item.style.display ="block";
        })
    }
}
document.querySelectorAll('.rowExpandButton').forEach(item => {
    item.addEventListener("click", expandRow);
})