// @TODO: YOUR CODE HERE!

// The code for the chart is wrapped inside a function that automatically resizes the chart
function makeResponsive() {
 
  // if the SVG area isn't empty when the browser loads, remove it and replace it with a resized version of the chart
  var svgArea = d3.select("body").select("svg");

   // clear svg is not empty
  if (!svgArea.empty()) { svgArea.remove(); }

 // SVG wrapper dimensions are determined by the current width and height of the browser window
  var svgWidth = window.innerWidth * 0.8;
  var svgHeight = svgWidth * 0.7;

  var circleR = svgWidth * 0.012;
  var textScale = parseInt(svgWidth * 0.009);

  var margin = { top: 20, right: 40, bottom: 100, left: 100 };

  var width = svgWidth - margin.left - margin.right;
  var height = svgHeight - margin.top - margin.bottom;

 // Create an SVG wrapper, append an SVG group that will hold our scatter chart, and shift the latter by left and top margins
  var svg = d3
    .select("#scatter")
    .append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight);

 // Append an SVG group
  var chartGroup = svg.append("g")
    .classed("chart", true)
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

  // Initial Params
  let chosenXAxis = 'poverty';
  let chosenYAxis = 'healthcare';


  // function used for updating x-scale var upon click on axis label
  function xScale(data, chosenXAxis) {
    // create scales
    var xLinearScale = d3.scaleLinear()
      .domain([d3.min(data, d => d[chosenXAxis]) * 0.8,
      d3.max(data, d => d[chosenXAxis]) * 1.2])
      .range([0, width]);

    return xLinearScale;
  }

  // function used for updating y-scale var upon click on axis label
  function yScale(stateData, chosenYAxis) {
     // create scales
    let yLinearScale = d3.scaleLinear()
      .domain([d3.min(stateData, d => d[chosenYAxis]) * 0.8,
      d3.max(stateData, d => d[chosenYAxis]) * 1.2])
      .range([height, 0]);

    return yLinearScale;
  } 

  // function used for updating xAxis var upon click on axis label
  function renderXAxis(newXScale, xAxis) {
    var bottomAxis = d3.axisBottom(newXScale);

    xAxis.transition()
      .duration(1000)
      .call(bottomAxis);

    return xAxis;
  } 

  //function used for updating yAxis variable upon click on axis label
  function renderYAxis(newYScale, yAxis) {
    var leftAxis = d3.axisLeft(newYScale);

    yAxis.transition()
      .duration(2000)
      .call(leftAxis);

    return yAxis;
  } 


  // function used for updating circles group with a transition to new circles

  function renderCircles(circlesGroup, newXScale, chosenXAxis, newYScale, chosenYAxis) {
   circlesGroup.transition()
      .duration(2000)
      .attr('cx', data => newXScale(data[chosenXAxis]))
      .attr('cy', data => newYScale(data[chosenYAxis]));

    return circlesGroup;
  } 
  //function for updating State labels as the Axes change
  function renderText(textGroup, newXScale, chosenXAxis, newYScale, chosenYAxis) {
  

    textGroup.transition()
      .duration(2000)
      .attr('x', d => newXScale(d[chosenXAxis]))
      .attr('y', d => newYScale(d[chosenYAxis]));

    return textGroup;

  } 

  // Custom function to format a number to currency
  const formatUSD = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0
  }); 


  //function to style x-axis values based on different variables(poverty,age,income) for tooltips
  function styleX(value, chosenXAxis) {
    if (chosenXAxis === "poverty") { return `${value}%`; }
    else if (chosenXAxis === "age") { return `${value} yrs`; }
    else { return `${formatUSD.format(value)}`; }
  } 

  // function used for updating circles group with new tooltip
  function updateToolTip(chosenXAxis, chosenYAxis, circlesGroup) {
    var xLabel, yLabel;

    // X label
    if (chosenXAxis === "poverty") { xLabel = "Poverty(%):"; }
    else if (chosenXAxis === "age") { xLabel = "Age (Median):"; }
    else { xLabel = "Income (Median):"; }

    // Y label
    if (chosenYAxis === "healthcare") { yLabel = "Lacks Healthcare(%):"; }
    else if (chosenYAxis === "smokes") { yLabel = "Smokes(%):"; }
    else { yLabel = "Obese (%):"; }

    // Define tooltip
    var toolTip = d3.tip()
      .attr("class", "d3-tip")
      .offset([80, -60])
      .html(d => (`${d.state}<br>${xLabel} ${styleX(d[chosenXAxis],
        chosenXAxis)}<br>${yLabel} ${d[chosenYAxis]}%`)
      );

    // Set the tooltip
    circlesGroup.call(toolTip);

    // Event listners for mouseover and mouseout
    circlesGroup.on("mouseover", toolTip.show)
      .on("mouseout", toolTip.hide);

    return circlesGroup;

  } 

  // Retrieve data from the CSV file and execute everything below
  d3.csv("assets/data/data.csv").then(function (stateData, err) {
    if (err) throw err;

    // Parse Data 
    stateData.forEach(function (data) {
      data.poverty = +data.poverty;
      data.healthcare = +data.healthcare;
      data.income = +data.income;
      data.age = +data.age;
      data.obesity = +data.obesity;
      data.smokes = +data.smokes;
    });

    // Linear scales
    var xLinearScale = xScale(stateData, chosenXAxis);
    var yLinearScale = yScale(stateData, chosenYAxis);

    // Axis functions
    var bottomAxis = d3.axisBottom(xLinearScale);
    var leftAxis = d3.axisLeft(yLinearScale);

    // Append x axis
    var xAxis = chartGroup.append("g")
      .classed("aText", true)
      .attr("transform", `translate(0, ${height})`)
      .call(bottomAxis);

    // Append y axis 
    var yAxis = chartGroup.append('g')
      .classed('aText', true)
      .call(leftAxis);

    // Append initial circles
    var circlesGroup = chartGroup.selectAll("circle")
      .data(stateData)
      .enter()
      .append("circle")
      .classed("stateCircle", true)
      .attr("cx", d => xLinearScale(d[chosenXAxis]))
      .attr("cy", d => yLinearScale(d[chosenYAxis]))
      .attr("r", circleR)
      .attr("opacity", ".5");

    //Append initial text (abbr)
    var textGroup = chartGroup.selectAll(".stateText")
      .data(stateData)
      .enter()
      .append("text")
      .classed("stateText", true)
      .attr("x", d => xLinearScale(d[chosenXAxis]))
      .attr("y", d => yLinearScale(d[chosenYAxis]))
      .attr('dy', 3)
      .attr("font-size", textScale + "px")
      .text(d => d.abbr);

    // Create group for all three x-axis labels
    var xLabelsGroup = chartGroup.append("g")
      .attr("font-size", textScale * 2 + "px")
      .attr("transform", `translate(${width / 2}, ${height + 20})`);

    var povertyLabel = xLabelsGroup.append("text")
      .attr("x", 0)
      .attr("y", 20)
      .attr("value", "poverty") 
      .classed("active", true)
      .classed("aText", true)
      .text("In Poverty (%)");

    var ageLabel = xLabelsGroup.append("text")
      .attr("x", 0)
      .attr("y", 40)
      .attr("value", "age") 
      .classed("inactive", true)
      .classed("aText", true)
      .text("Age (Median)");

    var incomeLabel = xLabelsGroup.append("text")
      .attr("x", 0)
      .attr("y", 60)
      .attr("value", "income") 
      .classed("inactive", true)
      .classed("aText", true)
      .text("Household Income (Median)");

    // Append y-axis
    var yLabelsGroup = chartGroup.append("g")
      .attr("font-size", textScale * 2 + "px")
      .attr("transform", `translate(${0 - margin.left / 4}, ${height / 20})`);

    var healthcareLabel = yLabelsGroup.append("text")
      .attr("x", (0 - (height / 2)))
      .attr("y", (0 - (margin.left * 1 / 4)) + textScale)
      .attr("dy", "1em")
      .attr("transform", "rotate(-90)")
      .classed("active", true)
      .classed("aText", true)
      .attr("value", "healthcare")
      .text("Lacks Healthcare (%)");

    var smokesLabel = yLabelsGroup.append("text")
      .attr("x", (0 - (height / 2)))
      .attr("y", (0 - (margin.left * 2 / 4)) + textScale)
      .attr("dy", "1em")
      .attr("transform", "rotate(-90)")
      .classed("inactive", true)
      .classed("aText", true)
      .attr("value", "smokes")
      .text("Smokes (%)");

    var obeseLabel = yLabelsGroup.append("text")
      .attr("x", (0 - (height / 2)))
      .attr("y", (0 - (margin.left * 3 / 4)) + textScale)
      .attr("dy", "1em")
      .attr("transform", "rotate(-90)")
      .classed("inactive", true)
      .classed("aText", true)
      .attr("value", "obesity")
      .text("Obese (%)");

    // updateToolTip function above csv import
    var circlesGroup = updateToolTip(chosenXAxis, chosenYAxis, circlesGroup);

    // x axis labels event listener
    xLabelsGroup.selectAll("text")
      .on("click", function () {
        var value = d3.select(this).attr("value");
        if (value !== chosenXAxis) {

          // replaces chosenXAxis with value
          chosenXAxis = value;
          console.log(chosenXAxis);

          // functions call below have been defined above csv import
          // updates x scale for new data
          xLinearScale = xScale(stateData, chosenXAxis);

          // updates x axis with transition
          xAxis = renderXAxis(xLinearScale, xAxis);

          // updates circles with new x values
          circlesGroup = renderCircles(circlesGroup, xLinearScale, chosenXAxis, yLinearScale, chosenYAxis);

          // Update the circle text
          textGroup = renderText(textGroup, xLinearScale, chosenXAxis, yLinearScale, chosenYAxis);

          // updates tooltips with new information
          circlesGroup = updateToolTip(chosenXAxis, chosenYAxis, circlesGroup);

          // changes classes to change bold text
          if (chosenXAxis === "poverty") {
            povertyLabel
              .classed("active", true)
              .classed("inactive", false);
            ageLabel
              .classed("active", false)
              .classed("inactive", true);
            incomeLabel
              .classed("active", false)
              .classed("inactive", true);
          }
          else if (chosenXAxis === "age") {
            povertyLabel
              .classed("active", false)
              .classed("inactive", true);
            ageLabel
              .classed("active", true)
              .classed("inactive", false);
            incomeLabel
              .classed("active", false)
              .classed("inactive", true);
          }
          else {
            povertyLabel
              .classed("active", false)
              .classed("inactive", true);
            ageLabel
              .classed("active", false)
              .classed("inactive", true);
            incomeLabel
              .classed("active", true)
              .classed("inactive", false);
          }
        }
      });

    // y-axis labels event listener
    yLabelsGroup.selectAll("text")
      .on("click", function () {
       var value = d3.select(this).attr("value");

        if (value !== chosenYAxis) {

          // replaces chosenXAxis with value
          chosenYAxis = value;

          console.log(value);
          console.log(chosenYAxis);


          // functions call below have been defined above csv import
          // updates y scale for new data
          yLinearScale = yScale(stateData, chosenYAxis);

          // updates x axis with transition
          yAxis = renderYAxis(yLinearScale, yAxis);

          // updates circles with new y values
          circlesGroup = renderCircles(circlesGroup, xLinearScale, chosenXAxis, yLinearScale, chosenYAxis);

          //Update the circle text
          textGroup = renderText(textGroup, xLinearScale, chosenXAxis, yLinearScale, chosenYAxis);

          // updates tooltips with new information
          circlesGroup = updateToolTip(chosenXAxis, chosenYAxis, circlesGroup);

          // changes classes to change bold text
          if (chosenYAxis === "healthcare") {
            healthcareLabel
              .classed("active", true)
              .classed("inactive", false);
            smokesLabel
              .classed("active", false)
              .classed("inactive", true);
            obeseLabel
              .classed("active", false)
              .classed("inactive", true);
          }
          else if (chosenYAxis === "smokes") {
            healthcareLabel
              .classed("active", false)
              .classed("inactive", true);
            smokesLabel
              .classed("active", true)
              .classed("inactive", false);
            obeseLabel
              .classed("active", false)
              .classed("inactive", true);
          }
          else {
            healthcareLabel
              .classed("active", false)
              .classed("inactive", true);
            smokesLabel
              .classed("active", false)
              .classed("inactive", true);
            obeseLabel
              .classed("active", true)
              .classed("inactive", false);
          }
        }
      });

  }).catch(function (error) {
    console.log(error);
  }); 

} 

// When the browser loads, makeResponsive() is called
makeResponsive();

// When the browser window is resized, makeResponsive() is called
d3.select(window).on("resize", makeResponsive);
