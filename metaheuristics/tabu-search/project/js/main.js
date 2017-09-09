/* 
Airton Bordin Junior
airtonbjunior@gmail.com


Tabu Search

Metaheuristics - Federal University of Goias (UFG)
UFG master's program 
*/

TABU_LIST_SIZE = 10;
TABU_LIST = [];
BEST_KNOW_SOLUTION = null;
MAX_ITERATIONS = 10;
MAX_ITERATIONS_NO_IMPROVE = 50;

INITIAL_SOLUTION = [] // only for log and comparsion
ACTUAL_SOLUTION  = []

BAG_CAPACITY = 180;
ITENS_QUANTITY = itens.length;


/* Choose a start solution. Default: randomly */
function initializeSolution() {
	/* For has much better performance than forEach */
	for(var i = 0; i < ITENS_QUANTITY; i++) {
		INITIAL_SOLUTION.push(Math.round(Math.random()));
	}
	
	ACTUAL_SOLUTION    = INITIAL_SOLUTION;
	BEST_KNOW_SOLUTION = ACTUAL_SOLUTION;
	
	console.log("[START INITIAL SOLUTION]: " + INITIAL_SOLUTION)
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
	console.log("[LOG] [Get neighbors of solution] [" + actual_solution + "]")

	var neighbors = []
	var neighbor = {}
	var solution = actual_solution.join().split(",")
	
	for (var i = 0; i < solution.length; i++) {
		if (solution[i] == "0") { solution[i] = "1" } else { solution[i] = "0" }
		
		neighbor.solution = solution;
		neighbor.value  = valueSolution(solution)
		neighbor.weight = weightSolution(solution)
		neighbor.result = evaluateSolution(solution)

		neighbors.push(neighbor)

		/* restart variables */
		solution = actual_solution.join().split(",")
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
	console.log("[LOG] [Moving to the next solution]")
	if(TABU_LIST.length <= TABU_LIST_SIZE) {
		TABU_LIST.push(actual_solution);
	}
	else {
		// remove the older value
	}

	var bestNeighbor = getBestNeighbor(actual_solution);
	if(containsSolution(bestNeighbor, TABU_LIST)) {
		console.log("Solution already in Tabu List");
		// get the other best
	} else {		
		ACTUAL_SOLUTION = bestNeighbor;
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


initializeSolution();

/* Main loop. Encapsulate this on start function */
for (var i = 0; i < MAX_ITERATIONS; i++) {
	moveNextSolution(ACTUAL_SOLUTION)
	console.log("Tabu List: " + TABU_LIST)
}

//console.log(getNeighbors(INITIAL_SOLUTION))
//console.log(getBestNeighbor(INITIAL_SOLUTION))
//console.log("Tabu List: " + TABU_LIST)
//console.log(moveNextSolution(INITIAL_SOLUTION))
//console.log("Tabu List: " + TABU_LIST)