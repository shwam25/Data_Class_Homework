// from data.js
var tableData = data;

// YOUR CODE HERE!
var dataUFO = data;

// SECTION 1: 'body'
var bodyUFO = d3.select('body');


// SECTION 2: 'table'- id='#ufo-table'
var tableUFO = bodyUFO.select('#ufo-table');
// Getting reference to the UFO table tbody
var tbodyUFO = tableUFO.select('tbody');


// SECTION 3: 'filter form'- id='#filter-form'
var filterUFO = bodyUFO.select('#filter-form');
// DateTime filter id='#datetime'
var filterDatetime = filterUFO.select("#datetime");
// City filter id='#city'
var filterCity = filterUFO.select("#city");
// State filter id='#state'
var filterState = filterUFO.select("#state");
// Country filter id='#country'
var filterCountry = filterUFO.select("#country");
// Shape filter id='#shape'
var filterShape = filterUFO.select("#shape");



// SECTION 4: 'button'- id='#filter-btn'
var filterButton = filterUFO.select("#filter-btn");
// Reset Button id='#reset-btn'
var resetButton = filterUFO.select("#reset-btn");


// Render Table
var renderTable = (tableData, tbodyTable) => {
    tableData.forEach((record) => {
       var row = tbodyTable.append("tr");
        Object.entries(record).forEach(([key, value]) => {
            var cell = row.append("td");
            cell.text(value);
        });
    });
};



function resetTable() {
    tbodyUFO.html("");
    renderTable(dataUFO, tbodyUFO);
};


// Button Click Event
function runFilters() {
    d3.event.preventDefault();
    tbodyUFO.html("");


    // Process `filterDatetime`
    var inputDateTime = filterDatetime.property("value").trim();
    console.log(inputDateTime);

    // Process `filterCity`
    var inputCity = filterCity.property("value").toLowerCase().trim();
    console.log(inputCity);

    // Process `filterState`
    var inputState = filterState.property("value").toLowerCase().trim();
    console.log(inputState);

    // Process `filterCountry`
    var inputCountry = filterCountry.property("value").toLowerCase().trim();
    console.log(inputCountry);

    // Process `filterShape`
    var inputShape = filterShape.property("value").toLowerCase().trim();
    console.log(inputShape);

    // Initialize the filtered UFO to dataUFO
    var FilteredUFO = dataUFO;


    //Process all the filters 
    if (inputDateTime != "") { FilteredUFO = FilteredUFO.filter(UFO => UFO.datetime === inputDateTime) };
    if (inputCity != "") { FilteredUFO = FilteredUFO.filter(UFO => UFO.city === inputCity) };
    if (inputState != "") { FilteredUFO = FilteredUFO.filter(UFO => UFO.state === inputState) };
    if (inputCountry != "") { FilteredUFO = FilteredUFO.filter(UFO => UFO.country === inputCountry) };
    if (inputShape != "") { FilteredUFO = FilteredUFO.filter(UFO => UFO.shape === inputShape) };



    // Render the table with filter search. For no records returned, display message: 'No Results found!'
    if (FilteredUFO.length !== 0) { renderTable(FilteredUFO, tbodyUFO) } else { tbodyUFO.append("tr").append("td").text("No results found!") };
};


// Event handlers
// 1. Body OnLoad Event
bodyUFO.on("onLoad", resetTable);

// 2. Button Click Event
filterButton.on("click", runFilters);

// 3. Form Submit Event
filterUFO.on("submit", runFilters);

// 4. Button Click Event
resetButton.on("click", resetTable);



// On page load event - Render the table with data and display
resetTable();