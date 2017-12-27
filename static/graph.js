$('#cy').css({
  "width": window.innerWidth * .75,
  "height": window.innerHeight * .75
});
removed = null 
var cy = cytoscape({
  container: document.getElementById('cy'),
  elements: [],
  layout: {
    name: 'random'
  },
  // so we can see the ids
  style: [
    { selector: 'node',
      style: {
        'content': 'data(id)',
       'width': '1vw',
        'height': '1vh',
        'font-size': '0.5vmin',
        'overlay-opacity': 0
         }},
    
    { selector: 'edge',
    	style: {
    		'width': 0.01,
    		'overlay-opacity': 0,
    		'content': 'data(percent)',
    		'font-size': '0.3vmin'
    	}}]});


var options = {
  name: 'cose',
  ready: function(){},
  stop: function(){},
  animate: true,
  animationEasing: undefined,
  animationDuration: undefined,
  // A function that determines whether the node should be animated
  // All nodes animated by default on animate enabled
  // Non-animated nodes are positioned immediately when the layout starts
  animateFilter: function ( node, i ){ return true; },
  animationThreshold: 250,
  refresh: 20,
  fit: true,
  padding: 30,
  boundingBox: undefined,
  // Excludes the label when calculating node bounding boxes for the layout algorithm
  nodeDimensionsIncludeLabels: false,
  // Randomize the initial positions of the nodes (true) or use existing positions (false)
  randomize: true,
  componentSpacing: 1,
  // Node repulsion (non overlapping) multiplier
  nodeRepulsion: function( node ){ return 2; },
  nodeOverlap: 1000,
  idealEdgeLength: function( edge ){ return Math.log(edge._private.data.weight); },
  edgeElasticity: function( edge ){ return 500; },
  // Nesting factor (multiplier) to compute ideal edge length for nested edges
  nestingFactor: 2.2,
  gravity: 1,
  numIter: 1000,
  // Initial temperature (maximum node displacement)
  initialTemp: 1000,
  // Cooling factor (how the temperature is reduced between consecutive iterations
  coolingFactor: 0.99,
  // Lower temperature threshold (below this point the layout will end)
  minTemp: 1.0,
  // Pass a reference to weaver to use threads for calculations
  weaver: false
};

var nodes = graphdata.nodes.forEach(function(node) {
	cy.add({ group: "nodes", data: { id: node.id}})
	});
var edges = graphdata.links.forEach(function(link) {
	cy.add({ group: "edges", 
            data: { source: link.source, target: link.target, 
                    weight: link.weight, percent: Math.round(link.weight*100).toString() + "%"}})
	});



cy.nodes().bind("click", function() {
  //console.log(this._private.data.id)
  window.location.href = 'http://www.uniprot.org/uniprot/'+this._private.data.id
})

buildGraph(0)

cy.layout(options).run();



function buildGraph(weight) {
	if (removed != null) {
		removed.restore()
	}
	removed = cy.remove("edge[weight < " + weight + "]");
  cy.layout(options).run();
}
