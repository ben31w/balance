console.log("This script loaded");
// initialize dateLabel's text when this script loads
dateLabel = document.getElementById("date-label");
let today = new Date();
dateLabel.innerHTML = today;


function decDate() {
    let date = new Date(dateLabel.innerHTML);
    let newDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() - 1);
    dateLabel.innerHTML = newDate;
}


function incDate() {
    let date = new Date(dateLabel.innerHTML);
    let newDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() + 1);
    dateLabel.innerHTML = newDate;
}

