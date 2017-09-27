/* 
Airton Bordin Junior
airtonbjunior@gmail.com


GRASP

Metaheuristics - Federal University of Goias (UFG)
UFG master's program 
*/

TABU_LIST_SIZE = 5;
TABU_LIST = [];
BEST_KNOW_SOLUTION = null;
MAX_ITERATIONS = 5;
MAX_ITERATIONS_NO_IMPROVE = 50;

INITIAL_SOLUTION = {} // only for log and comparsion
ACTUAL_SOLUTION  = {}

BAG_CAPACITY = 180; /* GRASP feasible limit */
ITENS_QUANTITY = itens.length;

/* GRASP parameters */
VALUE_PER_WEIGHT = []  /* parameter used to calc the "fitness" of an item is value/weight (LC) */
SCHEMA = [] /* hight quality schema */
LRC = []
GRASP_INITIAL_SOLUTION = []
ALPHA = 0.6
LIMIT_VALUE = 0

/* Preprocess the schema with the best(s) "chromossome(s)" */
function preProcessingSchema() {
	var value = 0;
	var bestValue = 0;

	for (var i = 0; i < ITENS_QUANTITY; i++) {
		value = parseFloat(parseFloat(itens[i].value) / parseFloat(itens[i].weight));
		
		if (value > bestValue) { bestValue = value; }
		
		VALUE_PER_WEIGHT.push(value);
	}

	/* Separated for didact reasons */
	for (var i = 0; i< ITENS_QUANTITY; i++) {
		SCHEMA.push(0)
	}

	for (var i = 0; i< ITENS_QUANTITY; i++) {
		if(VALUE_PER_WEIGHT[i] == bestValue) {
			SCHEMA[i] = 1;
			if (weightSolution(SCHEMA) > BAG_CAPACITY) {
				SCHEMA[i] = 0;
			}
		}
	}

	console.log("Value per weight below (LC)");
	console.log(VALUE_PER_WEIGHT);
	console.log("SCHEMA below");
	console.log(SCHEMA);
	console.log("Solution evaluation: " + evaluateSolution(SCHEMA));
}

/* Create the initial solution */
function createInitialSolution() {
	var solution = SCHEMA;
	var randomIndex = 0;

	LIMIT_VALUE = getMaxValue(VALUE_PER_WEIGHT) - ALPHA * (getMaxValue(VALUE_PER_WEIGHT) - getMinValue(VALUE_PER_WEIGHT));
	for (var i = 0; i < ITENS_QUANTITY; i++) {
		if(VALUE_PER_WEIGHT[i] >= LIMIT_VALUE && SCHEMA[i] == 0) { /* if already has on the schema, don't consider */
			LRC.push(i) /* store the index of the values */
		}
	}

	for (var i = 0; i < LRC.length; i++) {
		randomIndex = getRandomInt(0, LRC.length-1);

		solution[LRC[randomIndex]] = 1;
		
		if (weightSolution(solution) > BAG_CAPACITY) {
			solution[LRC[randomIndex]] = 0;
			break;
		}
	}

	GRASP_INITIAL_SOLUTION = solution;

	console.log("LIMIT_VALUE: " + LIMIT_VALUE);
	console.log("LRC below (indexes): Values > LIMIT_VALUE");
	console.log(LRC);
	console.log("The initial solution below");
	console.log(GRASP_INITIAL_SOLUTION);
	console.log("Initial solution weight: " + weightSolution(GRASP_INITIAL_SOLUTION));
	console.log("Initial solution evaluation: " + evaluateSolution(GRASP_INITIAL_SOLUTION));
}

/* Choose a start solution. Default: randomly */
function initializeSolution() {
	console.log("[LOG] [Initializing the solution]")
	console.log("[PARAM] [TABU_LIST_SIZE]: " + TABU_LIST_SIZE)
	console.log("[PARAM] [MAX_ITERATIONS]: " + MAX_ITERATIONS)
	console.log("[PARAM] [BAG_CAPACITY]: " + BAG_CAPACITY)

	var initialSolution = []
	/* For has much better performance than forEach */
	for(var i = 0; i < ITENS_QUANTITY; i++) {
		initialSolution.push(Math.round(Math.random()));
	}
	
	//INITIAL_SOLUTION.solution = initialSolution;
	INITIAL_SOLUTION.solution = GRASP_INITIAL_SOLUTION;
	INITIAL_SOLUTION.weight = -99999; // improve this inicialization
	INITIAL_SOLUTION.value  = -99999;
	INITIAL_SOLUTION.result = -99999;
	
	ACTUAL_SOLUTION    = INITIAL_SOLUTION;
	BEST_KNOW_SOLUTION = ACTUAL_SOLUTION;
	
	console.log("[START RANDOMIZED INITIAL SOLUTION {DEPRECATED IN GRASP}]: " + INITIAL_SOLUTION.solution)
}

/* Value of the solution */
function valueSolution(solution) {
	var sum = 0;
	for (var i = 0; i < solution.length; i++) {
		if(solution[i] == 1) {
			sum += parseInt(itens[i].value);
		}
	}
	return sum;
}

/* Weight of the solution */
function weightSolution(solution) {
	var sum = 0;
	for (var i = 0; i < solution.length; i++) {
		if(solution[i] == 1) {
			sum += parseInt(itens[i].weight);
		}
	}
	return sum;
}

/* Evaluate the solution */
function evaluateSolution(solution) {
	var weight = weightSolution(solution)
	var value  = valueSolution(solution)

	/* if the items can put in the bag, return the value */
	if (weight < BAG_CAPACITY) {
		return value;
	} 
	else {
		return BAG_CAPACITY - weight;
	}
}

/* Get the neighbors of a solution */
function getNeighbors(actual_solution) {
	console.log("[LOG][FUNCTION getNeighbors] [Get neighbors of solution] [" + actual_solution.solution + "]")

	var neighbors = []
	var neighbor  = {}
	var solution  = actual_solution.solution.join().split(",")
	
	for (var i = 0; i < solution.length; i++) {
		if (solution[i] == "0") { solution[i] = "1" } else { solution[i] = "0" }
		
		neighbor.solution = solution;
		neighbor.value  = valueSolution(solution)
		neighbor.weight = weightSolution(solution)
		neighbor.result = evaluateSolution(solution)

		neighbors.push(neighbor)

		/* restart variables */
		solution = actual_solution.solution.join().split(",")
		neighbor = {}
	}
	return neighbors;
}

/* Get the best neighbor of the actual solution */
function getBestNeighbor(actual_solution) {
	var neighbors = getNeighbors(actual_solution)
	var bestNeighbor = neighbors[0];

	var sortedNeighbors = neighbors;
	sortedNeighbors.sort(function(a, b) { 
    	return b.result - a.result;
	});

	for (var i = 0; i < sortedNeighbors.length; i++) {
		if(containsSolution(sortedNeighbors[i], TABU_LIST)) {
			console.log("[LOG][Solution already in Tabu List on " + i + " position]");
		}
		else {
			return sortedNeighbors[i];
		}
	}

	console.log("Sorted Neighbors")
	console.log(sortedNeighbors)

	return bestNeighbor;
}

/* Move to the next solution on the search space */
function moveNextSolution(actual_solution) {
	console.log("[LOG][FUNCTION moveNextSolution][Moving to the next solution]")
	if(TABU_LIST.length < TABU_LIST_SIZE) {
		TABU_LIST.unshift(actual_solution);
	}
	else {
		var removed = TABU_LIST.pop(); // Remove the older value
		console.log("[LOG][Removed the older value from TABU_LIST][" + removed.solution + "]")
		TABU_LIST.unshift(actual_solution)
	}

	var bestNeighbor = getBestNeighbor(actual_solution);
	
	ACTUAL_SOLUTION = bestNeighbor;
	if (ACTUAL_SOLUTION.result > BEST_KNOW_SOLUTION.result) {
		BEST_KNOW_SOLUTION = ACTUAL_SOLUTION;
	}
	console.log("The actual soluction now is: [" + ACTUAL_SOLUTION.solution + "] with weight " + ACTUAL_SOLUTION.weight + ", value " + ACTUAL_SOLUTION.value + " and evaluate result of " + ACTUAL_SOLUTION.result);
}

function sortNeighbors(neighbors_list) {
	var sorted_neighbors;
	neighbors_list.sort(function(a, b) { 
    	sorted_neighbors = b.result - a.result;
	})
	return sorted_neighbors;
}

/* TEST THIS FUNCTION */
function containsSolution(obj, list) {
    for (var i = 0; i < list.length; i++) {
        console.log("[LOG][Function containsSolution] Compare the obj [" + obj.solution + "] with the TABU_LIST [" + list[i].solution + "]")
        
		if(JSON.stringify(list[i].solution) === JSON.stringify(obj.solution)) {
			return true;
		}
    }
    return false;
}

function getMaxValue(arr) {
	return Math.max.apply(null, arr);
}

function getMinValue(arr) {
	return Math.min.apply(null, arr);
}

/* [1] */
function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

/* Initialize the UI with the user params */
intializeUI();

function start() {
	/* GRASP */
	preProcessingSchema();
	createInitialSolution();
	/* GRASP */
	
	/* LOCAL SEARCH - TABU SEARCH*/
	initializeSolution();
	
	/* Main loop. Encapsulate this on start function */
	for (var i = 0; i < MAX_ITERATIONS; i++) {
		console.log("[Starting iteration " + parseInt(i+1) + "]")
		moveNextSolution(ACTUAL_SOLUTION)
		console.log("Tabu List size: " + TABU_LIST.length)
		console.log("Tabu List: " + TABU_LIST)
		//console.log(TABU_LIST)
	}

	/* Restart the default screen */
	document.getElementById("loading-icon").className += " hide-load";
	document.getElementById("btn-start").innerHTML = "Start";
	/* Restart the default screen */

	document.getElementById("result").innerHTML = "Best Know Solution: [" + BEST_KNOW_SOLUTION.solution + "] <br/> Weight: " + BEST_KNOW_SOLUTION.weight + "<br/>Value: " + BEST_KNOW_SOLUTION.value + "<br/>Result: " + BEST_KNOW_SOLUTION.result;

	console.log("[RESULT] [BEST KNOW SOLUTION]: [" + BEST_KNOW_SOLUTION.solution + "] with weight " + BEST_KNOW_SOLUTION.weight + ", value " + BEST_KNOW_SOLUTION.value + " and evaluate result of " + BEST_KNOW_SOLUTION.result);
}

/* Auxiliar functions */

function startPreparation() {
	/* Get UI parameters */
	BAG_CAPACITY = document.getElementById("bag-capacity").value;
	MAX_ITERATIONS= document.getElementById("iterations").value;
	MAX_ITERATIONS_NO_IMPROVE= document.getElementById("iterations-no-improve").value;
	TABU_LIST_SIZE= document.getElementById("tabu-list-size").value;
	ALPHA = document.getElementById("alpha-grasp").value;
	
	/* Restart variables */
	TABU_LIST = [];
	BEST_KNOW_SOLUTION = null;
	INITIAL_SOLUTION = {}
	ACTUAL_SOLUTION  = {}

	VALUE_PER_WEIGHT = []
	SCHEMA = []
	LRC = []
	GRASP_INITIAL_SOLUTION = []

	document.getElementById("result").innerHTML = "&nbsp";

	document.getElementById("loading-icon").classList.remove("hide-load");
	document.getElementById("btn-start").innerHTML = "Processing...";
	document.getElementById("loading-icon").className += " fa fa-cog fa-spin fa-5x fa-fw";

	/* Timeout for the UI changes */
	setTimeout(start, 50);
}

/* Initialize the GUI */
function intializeUI() {
	document.getElementById("btn-start").addEventListener("click", startPreparation);

	document.getElementById("bag-capacity").value = BAG_CAPACITY;
	document.getElementById("iterations").value = MAX_ITERATIONS;
	document.getElementById("iterations-no-improve").value = MAX_ITERATIONS_NO_IMPROVE;
	document.getElementById("tabu-list-size").value = TABU_LIST_SIZE;
	document.getElementById("alpha-grasp").value = ALPHA;
}


/*
	[1]: https://stackoverflow.com/a/1527820
*/