var width = 480,
height = 250,
radius = Math.min(width, height) / 2 - 10;

var accept = acceptance.toFixed(2);
var acc_rate = [accept,1-accept];

var grad_data = graduation/100;
var grad = [grad_data,1-grad_data];

var act_data = act/36;
var act_rate = [act_data]


var sat_data = sat/1600
var sat_rate = [sat_data]

document.getElementById('search').onclick = function() {
    window.open('http://google.com/search?q='+name);
};

document.getElementById("avgSAT").innerHTML = "The average SAT score is " + sat + " out of 1600";
document.getElementById("avgACT").innerHTML = "The average ACT score is " + Math.round(act) + " out of 36";

var q = name;
document.getElementById('search').onclick = function() {
    window.open('http://google.com/search?q='+q);
};

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
        return "#add8e6"
        // return "#32CD32"
      }
      else{
        // return "#888888"
        return "#C0C0C0"
      }
    })
    .transition()
    .duration(2000)
    .attrTween("d", trans1)

  arcs.append("text")
    .style("text-anchor", "middle")
    .style("font-size","30px")
    .text(data[0] * 100 + "%");
}

var trans1 = function(b) {
  b.innerRadius = 0;
  var i = d3.interpolate({startAngle: 0, endAngle: 0}, b);
  return function(t) { return arc(i(t)); };
}

drawPie(grad,"#graduation");
drawPie(acc_rate,"#acceptance");

var scoreBar = function(data,id){
  svg = d3.select(id)
    .append("svg")
    .attr("width", "90%")
    .attr("height", "40%")
    .attr("viewBox", "0 0 500 200")
    .attr("transform", "translate(" + 0 + "," + height / 4 + ")");

  bar = svg.selectAll("g")
    .data(data)
    .enter()
    .append("g");

  bar.append("rect")
    .attr("height", 75)
    .attr("width", 0)
    .attr("fill","#C0C0C0")
    .transition()
    .duration(1500)
    .attr("width", 500);

  bar.append("rect")
    .attr("height", 76)
    .attr("width", 0)
    .attr("fill","#add8e6")
    .transition()
    .duration(1500)
    .attr("width", data[0] * 500);
}

scoreBar(act_rate,"#act");
scoreBar(sat_rate,"#sat");
