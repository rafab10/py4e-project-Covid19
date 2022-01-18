
let casesJSON = Cases;
let deathsJSON = Deaths;
let vaccineJSON = Vaccines;
let monthsArray = Months;

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
let id = urlParams.get('id')
let m = urlParams.get('m')
let title = ""
let cData = [];

if(m === null){
    m = '2022-01';
}

if(id === null){
    id = "Cases";
    id2 = "cases";
    cData = casesJSON[m]
    title = "New Cases"
}else{
    if(id === "Cases"){
        id2 = "cases";
        cData = casesJSON[m]
        title = "New Cases"
    }else if(id === "Deaths"){
        id2 = "deaths";
        cData = deathsJSON[m]
        title = "New Deaths"
    }else{
        id2 = "vaccines";
        cData = vaccineJSON[m]
        title = "Applied Vaccines"
    }
}

const stateData = [['State',id]]
cData.forEach(element => {
    stateData.push(['US-'+element['code'],element[id2]])
});


google.charts.load('current', {
'packages':['geochart'],
});
google.charts.setOnLoadCallback(drawVisualization);

function drawVisualization() {
var data = google.visualization.arrayToDataTable(stateData);

var options = {};

var geochart = new google.visualization.GeoChart(
document.getElementById('visualization'));
geochart.draw(data, {width: 556, height: 347, region: "US", resolution: "provinces"});
}

function backMonth() {
    let x = monthsArray.findIndex(checkMonth) - 1
    var url = window.location.href.split('?')[0];
    let new_m = monthsArray[x]
    url = url + '?id=' + id + '&m=' + new_m;
    if(x < 0){
        alert('Limit inferior')
    }else{
        window.location.href = url;
    }
}

function nextMonth() {
    let x = monthsArray.findIndex(checkMonth) + 1
    var url = window.location.href.split('?')[0];
    let new_m = monthsArray[x]
    url = url + '?id=' + id + '&m=' + new_m;
    if(x > monthsArray.length - 1){
        alert('Limit superior')
    }else{
        window.location.href = url;
    }
}

function selectOption(value){
    var url = window.location.href.split('?')[0];
    let new_id = value;
    url = url + '?id=' + new_id + '&m=' + m;
    window.location.href = url;
}

function checkMonth(month){
    return month === m;
}