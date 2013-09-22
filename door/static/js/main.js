// load the window data
$(document).ready(function() {
    window.dailyGraphData = null;
    $.ajax("./daily_summary").done(function( data ) {
        window.dailyGraphData = ensureJson(data);
        displayDailyGraph();
    });
    $.ajax("./daily_total_summary").done(function( data ) {
        window.dailyTotalGraphData = ensureJson(data);
        displayDailyTotalGraph();
    });
    $.ajax("./weekly_summary").done(function( data ) {
        window.weeklyGraphData = ensureJson(data);
        displayWeeklyGraph();
    });
    $.ajax("./weekly_total_summary").done(function( data ) {
        window.weeklyTotalGraphData = ensureJson(data);
        displayWeeklyTotalGraph();
    });
});

///// Helper functions

function ensureJson(d) {
    if (typeof(d) == 'string')
        d = JSON.parse(d);
    return d;
}

function makeTip() {
    return d3.tip()
             .attr('class', 'd3-tip')
             .offset([-10, 0])
             .html(function(d) {
                return "<div class='time'>" + d[0] + "</div> <div class='val'>" + d[1] + " opens </div>";
             });
}

function makeXYAxis(data, width, height) {
    var ret = {}
    ret['x'] = d3.scale.ordinal().rangeRoundBands([0, width], .1);
    ret['y'] = d3.scale.linear().range([height, 0]);
    ret['xAxis'] = d3.svg.axis().scale(ret['x']).orient("bottom");
    ret['yAxis'] = d3.svg.axis().scale(ret['y']).orient("left");
    return ret
}

function setDomain(x, y, data) {
    // set a domain on the x and y scales based on data
    x.domain(data.map(function(d) {return d[0]}));
    y.domain([0, d3.max( data.map(function(d) {return d[1]}) )]);
}

function makeSVG(selector, width, height, margin) {
    return d3.select(selector).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
}

function drawAxes(svg, xAxis, yAxis, height, yLabel) {
    // add the x axis
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
        .selectAll("text")
          .remove();
    
    // add the y axis
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text(yLabel);
}

function drawBars(svg, data, tip, width, height, x, y) {
    // add the bars
    svg.selectAll(".bar")
        .data(data)
      .enter().append("rect")
        .attr("class", "bar")
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide)
        .attr("x", function(d) { return x(d[0]) })
        .attr("width", x.rangeBand())
        .attr("y", height)
        .attr("height", 0)
        .transition().delay(function (d,i) {return i*100}).duration(200)
            .attr("height", function(d) {return height - y(d[1])-1})
            .attr("y", function(d) { return y(d[1]) });
}

///// Main plotting functions

function displayDailyGraph() {
    drawBar("#daily-graph-holder", window.dailyGraphData);
}

function displayDailyTotalGraph() {
    drawBar("#daily-total-graph-holder", window.dailyTotalGraphData);
}

function displayWeeklyGraph() {
    drawBar("#weekly-graph-holder", window.weeklyGraphData);
}

function displayWeeklyTotalGraph() {
    drawBar("#weekly-total-graph-holder", window.weeklyTotalGraphData);
}

function drawBar(selector, data) {
    var tip = makeTip();

    var margin = {top: 20, right: 20, bottom: 50, left: 30};
    var width  = 600 - margin.left - margin.right;
    var height = 300 - margin.top - margin.bottom;
    
    var axes = makeXYAxis(data, width, height);
    var x = axes['x'],
        y = axes['y'],
        xAxis = axes['xAxis'],
        yAxis = axes['yAxis'];
    setDomain(x, y, data);
    var svg = makeSVG(selector, width, height, margin);
    svg.call(tip)
    
    drawAxes(svg, xAxis, yAxis, height, "Opens");
    drawBars(svg, data, tip, width, height, x, y);
}
