

function getGraphDataByLabel(data, label) {
    var length = data.length;
    var chartdata = [];
    for (var i = 0; i < length; i++) {
       item = data[i]
       var datapoint = {
                TimeStamp: new Date(Date.parse(item['datetime'])),
                Value: item[label]
       };
       chartdata.push(datapoint);
    }

    return chartdata;
};

function drawChart(tag, data) {
  var elementRect = document.getElementById(tag).getBoundingClientRect();

  // set the dimensions and margins of the graph
  var margin = {top: 10, right: 30, bottom: 30, left: 30},
      width = elementRect.width - margin.left - margin.right,
      height = 180 - margin.top - margin.bottom;

  // append the svg object to the body of the page
  var svg = d3.select('#' + tag)
    .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

      // Add X axis --> it is a date format
      var xaxis = d3.scaleTime()
        .domain(d3.extent(data, function(d) { return d.TimeStamp; }))
        .range([ 0, width ]);
      svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(xaxis));

      // Add Y axis
      var yaxis = d3.scaleLinear()
        .domain([d3.min(data, function(d) { return +d.Value; }), d3.max(data, function(d) { return +d.Value; })])
        .range([ height, 0 ]);

      svg.append("g")
        .call(d3.axisLeft(yaxis));

      // Add the line
      svg.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 1.5)
        .attr("d", d3.line()
          .x(function(d) { return xaxis(d.TimeStamp) })
          .y(function(d) { return yaxis(d.Value) })
          )

svg.selectAll("line.horizontalGrid").data(yaxis.ticks(4)).enter()
    .append("line")
        .attr(
        {
            "class":"horizontalGrid",
            "x1" : margin.right,
            "x2" : width,
            "y1" : function(d){ return yaxis(d);},
            "y2" : function(d){ return yaxis(d);},
            "fill" : "none",
            "shape-rendering" : "crispEdges",
            "stroke" : "black",
            "stroke-width" : "1px"
        });

}

drawChart('tempchart1', getGraphDataByLabel(data, 'temp1'));
drawChart('tempchart2', getGraphDataByLabel(data, 'temp2'));
drawChart('tempchart3', getGraphDataByLabel(data, 'temp3'));
drawChart('tempchart4', getGraphDataByLabel(data, 'temp4'));
drawChart('humidity', getGraphDataByLabel(data, 'humidity'));
drawChart('pressure', getGraphDataByLabel(data, 'pressure'));
drawChart('moisture', getGraphDataByLabel(data, 'moisture'));
drawChart('light', getGraphDataByLabel(data, 'light'));