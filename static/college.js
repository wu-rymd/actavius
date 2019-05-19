var width = 480,
height = 250,
radius = Math.min(width, height) / 2 - 10;

var acceptance = .25
var data = [1-acceptance,acceptance]

var grad_data = graduation/100
var grad = [grad_data,1-grad_data]
var arc = d3.arc()  .innerRadius(radius-35)
  .outerRadius(radius)
.outerRadius(radius);

var pie = d3.pie();

var drawPie = function(data,id){
  var svg = d3.select(id).append("svg")
  .datum(data)
  .attr("width", width)
  .attr("height", height)
  .append("g")
  .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

  var arcs = svg.selectAll("g.arc")
  .data(pie)
  .enter().append("g")
  .attr("class", "arc");

  arcs.append("path")
  .attr("fill", function(d, i) {
    if (i == 0) {
      return "#add8e6"
    }
    else{
      return "white"
    }
  })
  .transition()
  .ease(d3.easeBounce)
  .duration(2000)
  .attrTween("d", tweenPie)

  arcs.append("text")
      .style("text-anchor", "middle")
      .style("font-size","30px")
      .text(data[0] * 100 + "%");
}

function tweenPie(b) {
  b.innerRadius = 0;
  var i = d3.interpolate({startAngle: 0, endAngle: 0}, b);
  return function(t) { return arc(i(t)); };
}

drawPie(grad,"#graduation")
