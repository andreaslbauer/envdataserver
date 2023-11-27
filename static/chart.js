

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
  var margin = {top: 10, right: 10, bottom: 50, left: 40},
      width = elementRect.width - margin.left - margin.right,
      height = 220 - margin.top - margin.bottom;

  // append the svg object to the body of the page
  var svg = d3.select('#' + tag)
    .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")")
      .on("pointerenter pointermove", pointermoved)
      .on("pointerleave", pointerleft)
      .on("touchstart", event => event.preventDefault());

      // Add X axis --> it is a date format
      var xscale = d3.scaleTime()
        .domain(d3.extent(data, function(d) { return d.TimeStamp; }))
        .range([ 0, width ]);
      svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(xscale));

      // Add Y axis
      var yscale = d3.scaleLinear()
        .domain([d3.min(data, function(d) { return +d.Value; }), d3.max(data, function(d) { return +d.Value; })])
        .range([ height, 0 ]);

      svg.append("g")
        .call(d3.axisLeft(yscale))
        .call(g => g.selectAll(".tick line").clone()
          .attr("x2", width)
          .attr("stroke-opacity", 0.1));

      // Add the line
      svg.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 1.5)
        .attr("d", d3.line()
          .x(function(d) { return xscale(d.TimeStamp) })
          .y(function(d) { return yscale(d.Value) })
          )

    // Create the tooltip container.
  const tooltip = svg.append("g");

  // Add the event listeners that show or hide the tooltip.
  const bisect = d3.bisector(d => d.TimeStamp).center;
  function pointermoved(event) {
    const [x, y] = d3.pointer(event);
    const i = bisect(data, xscale.invert(d3.pointer(event)[0]));
    tooltip.style("display", null);
    tooltip.attr("transform", `translate(${xscale(data[i].TimeStamp)},${yscale(data[i].Value)})`);

    const path = tooltip.selectAll("path")
      .data([,])
      .join("path")
        .attr("fill", "white")
        .attr("stroke", "black");

  function formatDate(date) {
    return date.toLocaleString("en", {
      day: "numeric",
      month: "numeric",
      hour: "numeric",
      minute: "numeric"
    });
  }

    const text = tooltip.selectAll("text")
      .data([,])
      .join("text")
      .call(text => text
        .selectAll("tspan")
        .data([formatDate(data[i].TimeStamp), data[i].Value])
        .join("tspan")
          .attr("x", 0)
          .attr("y", (_, i) => `${i * 1.1}em`)
          .attr("font-weight", (_, i) => i ? null : "bold")
          .text(d => d));

    size(text, path);
  }

  function pointerleft() {
    tooltip.style("display", "none");
  }

  // Wraps the text with a callout path of the correct size, as measured in the page.
  function size(text, path) {
    const {x, y, width: w, height: h} = text.node().getBBox();
    text.attr("transform", `translate(${-w / 2},${15 - y})`);
    path.attr("d", `M${-w / 2 - 10},5H-5l5,-5l5,5H${w / 2 + 10}v${h + 20}h-${w + 20}z`);
  }

}
