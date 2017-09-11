/* 
Airton Bordin Junior
airtonbjunior@gmail.com


Tabu Search

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

BAG_CAPACITY = 180;
ITENS_QUANTITY = itens.length;


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
	
	INITIAL_SOLUTION.solution = initialSolution;
	INITIAL_SOLUTION.weight = -99999; // improve this inicialization
	INITIAL_SOLUTION.value  = -99999;
	INITIAL_SOLUTION.result = -99999;
	
	ACTUAL_SOLUTION    = INITIAL_SOLUTION;
	BEST_KNOW_SOLUTION = ACTUAL_SOLUTION;
	
	console.log("[START INITIAL SOLUTION]: " + INITIAL_SOLUTION.solution)
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

	for (var i = 1; i < neighbors.length; i++) {
		if(neighbors[i].result > bestNeighbor.result) { 
			bestNeighbor = neighbors[i]; 
		}
	}

	return bestNeighbor;
}

/* Move to the next solution on the search space */
function moveNextSolution(actual_solution) {
	console.log("[LOG][FUNCTION moveNextSolution] [Moving to the next solution]")
	if(TABU_LIST.length <= TABU_LIST_SIZE) {
		TABU_LIST.unshift(actual_solution);
	}
	else {
		var removed = TABU_LIST.pop() 
		console.log("[LOG] [Removed the older value from TABU_LIST] [" + removed.solution + "]")
		TABU_LIST.unshift(actual_solution)
		// remove the older value
	}

	var bestNeighbor = getBestNeighbor(actual_solution);
	if(containsSolution(bestNeighbor, TABU_LIST)) {
		console.log("Solution already in Tabu List");
		// get the other best
	} else {		
		ACTUAL_SOLUTION = bestNeighbor;
		if (ACTUAL_SOLUTION.result > BEST_KNOW_SOLUTION.result) {
			BEST_KNOW_SOLUTION = ACTUAL_SOLUTION;
		}
		console.log("The actual soluction now is: [" + ACTUAL_SOLUTION.solution + "] with weight " + ACTUAL_SOLUTION.weight + ", value " + ACTUAL_SOLUTION.value + " and evaluate result of " + ACTUAL_SOLUTION.result);
	}
}

/* TEST THIS FUNCTION */
function containsSolution(obj, list) {
    for (var i = 0; i < list.length; i++) {
        if (list[i] === obj) {
            return true;
        }
    }

    return false;
}

/* Initialize the UI with the user params */
intializeUI();

function start() {
	initializeSolution();

	/* Main loop. Encapsulate this on start function */
	for (var i = 0; i < MAX_ITERATIONS; i++) {
		console.log("[Starting iteration " + parseInt(i+1) + "]")
		moveNextSolution(ACTUAL_SOLUTION)
		console.log("Tabu List size: " + TABU_LIST.length)
		console.log("Tabu List: " + TABU_LIST)
		console.log(TABU_LIST)
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
	
	/* Restart variables */
	TABU_LIST = [];
	BEST_KNOW_SOLUTION = null;
	INITIAL_SOLUTION = {}
	ACTUAL_SOLUTION  = {}

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
}

