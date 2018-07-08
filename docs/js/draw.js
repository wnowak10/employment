// Functions:

  function draw_lines(data, x, y, xscale_type, yscale_type, color, line_ids){
    // y can be array of y values.
    // line_ids should be an array containing the ids we'll
    // give to each line.

    // Range (extent) of dates (or x values)
    if (xscale_type == 'time'){
		var xscale = d3.scaleTime().range([0, width]);
	    xscale.domain(d3.extent(data, function(d) { return d[x]; }));
    };

    if (yscale_type == 'linear'){
		var yscale = d3.scaleLinear().range([height, 0]);
    };

    if (y.length > 1) {
      // Draw lines on properly scaled y axis
      min = Math.pow(10, 1000) // Big positive number as initial min. 
      max = Math.pow(-10, 1001) // Big negative number as initial max. 
      // Anything greater than this will then become max.
      for (i = 0; i < y.length; i++){
        local_min = d3.min(data, function(d) { return d[y[i]]; })
        if (local_min < min){
          min = local_min;
        }
        local_max = d3.max(data, function(d) { return d[y[i]]; })
        if (local_max > max){
          max = local_max;
        }
      }
      yscale.domain([.75*min, 1.1*max])
    }
    else {  
      yscale.domain([d3.min(data, function(d) { return d[y]; }) - 
      how_far_below_min_for_y_scale*d3.min(data, function(d) { return d[y]; }), 
        d3.max(data, function(d) { return d[y]; })]);
    };

    for (i = 0; i < y.length; i++) { 
      path = svg.append("path")
	      .datum(data)
	      .attr("fill", "none")
	      .attr("id", line_ids[i])
	      .attr("stroke", color[i])
	      .attr("stroke-linejoin", "round")
	      .attr("stroke-linecap", "round")
	      .attr("stroke-width", 2.5)
	      .attr("d", d3.line()
	        .x(function(d) { return xscale(d[x]); })
	        .y(function(d) { return yscale(d[y[i]]); }));

      // Mechanism for animating line path left to right.
      totalLength = path.node().getTotalLength();
      path
      	  .attr("stroke-dasharray", totalLength + " " + totalLength)
          .attr("stroke-dashoffset", totalLength)
          .transition()
          .duration(transitionTime)
          .attr("stroke-dashoffset", 0);
    }

  };

  function split_line(data, x, initial_line_ids, list_of_new_lines, xscale, yscale){
  	// If you want to split one line, you need to make
  	// TWO overlapping lines with different ids. We then 
  	// select each and move it to a new line.

  	// Make these nicer colors!
    colors = ['LightCoral', 'green','red','blue','pink','orange']
    for (i = 0; i < list_of_new_lines.length; i++) { 
      d3.select('#'+initial_line_ids[i])
      .transition()
      .duration(transitionTime)
      .delay(transitionTime)
      .attr("d", d3.line()
            .x(function(d, e, f, g, h, i, j, k) { 
              console.log(f) // Where does d, e, f, come from???
              return xscale(d[x]); })
            .y(function(d) { return yscale(d[list_of_new_lines[i]]); }))
      .attr('stroke', colors[i])
      .attr('id', list_of_new_lines[i]);
    }
  };

  function axes_labels(xAxis, yAxis, x_axis_label, y_axis_label){
  	// Function to label x and y axis.

    // Axes labels:
    // X axis label:
    xAxis.append("text")             
      .attr("transform",
            "translate(" + (width/2) + " ," + 
                           (margin.top + 20) + ")")
      .style("text-anchor", "middle")
      .style('fill','black')
      .text(x_axis_label);
    // Y axis label
    xAxis.append("text").attr("transform", "rotate(-90)")
      .attr("y", -3*margin.top)
      .attr("x",(height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .style('fill','black')
      .text(y_axis_label); 

  };

    // Add initial axes.

  function addInitialAxes(xx, yy, data, x_axis_series, y_axis_series){
  	// This draws axes initially.

    xx.domain(d3.extent(data, function(d) { return d[x_axis_series]; }));
    yy.domain([d3.min(data, function(d) { return d[y_axis_series]; }) - 
      how_far_below_min_for_y_scale*d3.min(data, function(d) { return d[y_axis_series]; }), 
        d3.max(data, function(d) { return d[y_axis_series]; })]);
    // Add the Y Axis initially
    var yAxis = svg.append("g")
      .attr('id', 'unemployment_axis')
      .call(d3.axisLeft().tickFormat(percentFormat).scale(yy));
    // Add the X Axis
    var xAxis = svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .attr('id','xaxis')
      .call(d3.axisBottom(xx).ticks(10).tickFormat(d3.timeFormat("%Y")));
    // Call axes_labels function to add labels.
    axes_labels(xAxis,yAxis,'Date', 'Percent (%)');
  }
  function fade_object(line_id) {
  // Fade out.
  // https://groups.google.com/forum/#!msg/d3-js/nkIpeZ60Sas/RZEIhmrsI0cJ
    d3.select(line_id) //#emp_line
     .style("opacity", 1)
     .transition().duration(transitionTime).style("opacity", 0);
  };
  function replace_axis(data, scale, old_axis_id, new_axis_id, new_series, type){
    if (type == 'y'){
    	if (new_series.length > 1) {
      // If we are fading an old axis and adding multiple new lines,
      // we find the minimum and maximum of all these values and then set the 
      // axis appropriately to fit everything.
        min = Math.pow(10, 1000) // Big positive number as initial min. 
        max = Math.pow(-10, 1001) // Big negative number as initial max.
        for (i = 0; i < new_series.length; i++){
          mi = d3.min(data, function(d) { return d[new_series[i]]; })
          console.log(i, mi)
          ma = d3.max(data, function(d) { return d[new_series[i]]; })
          console.log(i, ma)
          if (mi<min){
            min = mi;
          }
          if (ma>max){
            max = ma;
          }
        }
        console.log(min, max)
        scale.domain([min, max])
      }
      else {
        scale.domain( [d3.min(data, function(d) { return d[new_series]; }) 
                   - how_far_below_min_for_y_scale*d3.min(data, function(d) { return d[new_series]; }), 
                    1.1*d3.max(data, function(d) { return d[new_series]; })]);
      };
      d3.select("body")
      .select('#'+old_axis_id) // change out the old y axis
      .attr("id", new_axis_id) //give a new id tag to the new axis
      .transition()
      .duration(transitionTime)
      .call(d3.axisLeft().tickFormat(percentFormat).scale(scale));
    }
    if (type == 'x'){
    	scale.domain(d3.extent(data, function(d) { return d[new_series]; }));
    	d3.select("body")
	      .select('#'+old_axis_id) // change out the old y axis
	      .attr("id", new_axis_id) //give a new id tag to the new axis
	      .transition()
	      .duration(transitionTime)
	      .call(d3.axisBottom().scale(scale));

    }
  };
  function change_slide_title(new_title){
    d3.select("#title_text")
     .transition()
     .duration(transitionTime/2)
     .style("opacity", 0)
     .transition()
     .text(new_title)
     .duration(transitionTime/2)
     .style("opacity", 1);
  };
  function label_line(data, line_id, yscale, label_id, label, color){
  	// Add text below? a line to serve purpose of 
  	// a legend.

  	// Get the last y value in the array
  	recent_value = data[data.length-1][line_id]
  	svg.append("text")
	    .attr("transform", "translate("+width*.9+","+yscale(recent_value*.95)+")")
	    .attr("dy", ".35em")
	    .attr("text-anchor", "start")
	    .style("fill", color)
	    .attr('id',label_id)
	    .transition()
	    .delay(transitionTime)
	    .text(label);
  }