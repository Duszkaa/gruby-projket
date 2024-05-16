const data2 = new Date();
let miesiacInt = data2.getMonth();
let rokInt = data2.getMonth();
function daysInMonth(rokInt, miesiacInt) {
    return new Date(rokInt, miesiacInt + 1, 0).getDate();
}
let kalendarz = document.getElementById('kalendarz');
let tbl = document.createElement('table');
let daysCount = daysInMonth(rokInt, miesiacInt);
let row = tbl.insertRow();

for(let i = 1; i <= daysCount; i++){
    let cell = row.insertCell();
    cell.appendChild(document.createTextNode(i));

    if (i % 7 === 0) {
        row = tbl.insertRow();
    }
}

kalendarz.appendChild(tbl);