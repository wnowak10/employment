/////////////////////////////////////////////
// Helper functions for onclick update.
/////////////////////////////////////////////
function filterbyCounty(x, currentCounty, currentState){
  return x.filter(function(d) { return d.County === currentCounty & d.State === currentState; });
};

function getDistribution(data){
  var proportions = []
  var countyPopulation = data[0]["Estimate; Total:"]
  // Populate the income distribution list `proportions`
  for(var i=0; i<distribution_breakdowns.length; i++){
    proportions.push( data[0][distribution_breakdowns[i]]  / countyPopulation);
  }
  return proportions
};
// https://www.investopedia.com/financial-edge/0912/which-income-class-are-you.aspx
function low_Middle_High_class(proportions){
  /// Take what proportion of citizens in each bin as defined by CB
  /// Then just bin into low or high with 35K and 100K as cutoffs.
  newData = []
  low = 0
  for(var i=0; i<7;i++){
    low += proportions[i]
  }
  newData.push(low)
  medium = 0
  for(var i=7; i<13;i++){
    medium += proportions[i]
  }
  newData.push(medium)
  high = 0
  for(var i=12; i<16;i++){
    high += proportions[i]
  }
  newData.push(high)
  return newData;

};
var barSpacing = 100;
var barWidth = 20;
function bar_location(d,i, numclicks){
  bar_loc = barWidth+ (i*barSpacing)+barWidth*(numclicks);
  return bar_loc;
};

function spread(i){
  // Spread a sequence (say, of x values), out.
  return i*barSpacing+barWidth;
};

classes = ["Low", "Middle", "High"]
function get_CLASS_bar_x_positions(){
  var barXvalues = [];
  for(var i=0; i<classes.length; i++){
    barXvalues.push(spread(i));
  }
  return barXvalues;
};

var y_axisLength = (height / 2); //*.85;
function getYscale(proportions){
  var maxValue = d3.max(proportions, function(d) { return +d;} ); // get max value of our dataset
  // http://duspviz.mit.edu/d3-workshop/intro-to-d3/
  yScale = d3.scaleLinear()
    .domain([0, 1])
    .range([y_axisLength, 0]);
  return [yScale, maxValue];
}
function getXscale(barXvalues){
   return xScale = d3.scaleOrdinal()
      .domain(classes)
      .range(barXvalues);
}

function drawAxes(yScale, xScale){
      var axez = chart2.append("g");
        axez
        .attr("transform", "translate(0,-"+y_axisLength+")") // How far to shift down so ?
        .attr("id", "axes")
        .call(d3.axisLeft(yScale));

      // Add x scale
      chart2.append("g")
        .attr("transform", "translate(0,0)")
        .call(d3.axisBottom(xScale))
        .selectAll("text")
        .attr("y", 0)
        .attr("x", 9)
        .attr("dy", ".35em")
        .attr("transform", "translate(0,10)")
        .attr("id", "axes")
        .style("text-anchor", "start");
};