/* 
Airton Bordin Junior
airtonbjunior@gmail.com


Tabu Search

Metaheuristics - Federal University of Goias (UFG)
UFG master's program 
*/

TABU_LIST_SIZE = 10;
TABU_LIST = [];
BEST_KNOW_SOLUTION = "";

INITIAL_SOLUTION = [] // only for log and comparsion
ACTUAL_SOLUTION = []

BAG_CAPACITY = 180;
ITENS_QUANTITY = itens.length;


/* Choose a start solution. Default: randomly */
function initializeSolution() {
	/* For has much better performance than forEach */
	for(var i = 0; i < ITENS_QUANTITY; i++) {
		INITIAL_SOLUTION.push(Math.round(Math.random()));
	}
	ACTUAL_SOLUTION = INITIAL_SOLUTION;
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
	var bestNeighbor = neighbors[0].result

	for (var i = 1; i < neighbors.length; i++) {
		if(neighbors[i].result > bestNeighbor) { 
			bestNeighbor = neighbors[i].result; 
		}
	}

	return bestNeighbor;
}

/* Move to the next solution on the search space */
function moveNextSolution(actual_solution) {
	var neighbors = getNeighbors(actual_solution)
	// ...
}


initializeSolution();

console.log(getNeighbors(INITIAL_SOLUTION))
console.log(getBestNeighbor(INITIAL_SOLUTION))