var width = 480,
height = 250,
radius = Math.min(width, height) / 2 - 10;

var accept = acceptance.toFixed(2)
var acc_rate = [accept,1-accept]

var grad_data = graduation/100
var grad = [grad_data,1-grad_data]
var arc = d3.arc().innerRadius(radius-35)
  .outerRadius(radius)
.outerRadius(radius);

var pie = d3.pie();

var drawPie = function(data,id){
  var svg = d3.select(id).append("svg")
  .datum(data)
  .attr("width", "100%")
  .attr("height", "100%")
  .attr("viewBox", "0 0 480 250")
  .append("g")
  .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

  var arcs = svg.selectAll("g.arc")
  .data(pie)
  .enter().append("g")
  .attr("class", "arc");

  arcs.append("path")
  .attr("fill", function(d, i) {
    if (i == 0) {
      // return "#add8e6"
      return "#32CD32	"
    }
    else{
      return "#888888"
    }
  })
  .transition()
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
drawPie(acc_rate,"#acceptance")
