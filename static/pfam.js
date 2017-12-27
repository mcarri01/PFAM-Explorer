class DataPoint {
  constructor(family, connectedComp, size, color) {
    this.family = family
    this.cc = connectedComp
    this.size = size
    this.color = color
  }
  getX() {
    return this.cc
  }
  getY() {
    return this.size
  }
  getFamily() {
    return this.family
  }
  getColor() {
    return this.color
  }
  getThreshold() {
    return this.threshold
  }
}

function initData(data, threshold, colors) {
  let dataList = []
  let colorList = []
  for (let i = 0; i < data.length; i++) {
    for (let j = 0; j < threshold.length; j++) {
      dataList.push(new DataPoint(data[i].family, data[i].connected_components[threshold[j]], data[i].familysize, colors[j]))
    }
  }
  return dataList
}

function handleMouseOver(d, i) {
  d3.select(this).attr({
    fill: "orange"
  })
  var div = d3.select(".tooltip")
  div.transition()
    .duration(200)
    .style("opacity", .9);
  div.html(d.getFamily() + "<br/>" +
           "CCPS: " + d.getX() + "<br/>" +
           "Size: " + d.getY() + "<br/>")
    .style("left", (d3.event.pageX) + "px")
    .style("top", (d3.event.pageY - 28) + "px");
}

function handleMouseOut(d, i) {
  d3.select(this).attr({
    fill: d.getColor()
  })
  var div = d3.select(".tooltip")
  div.transition()
    .duration(500)
    .style("opacity", 0);

}