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

BAG_CAPACITY = 150;
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
	sum = 0;
	for (var i = 0; i < solution.length; i++) {
		if(solution[i] == 1) {
			sum += parseInt(itens[i].value);
		}
	}
	return sum;
}

/* Weight of the solution */
function weightSolution(solution) {
	sum = 0;
	for (var i = 0; i < solution.length; i++) {
		if(solution[i] == 1) {
			sum += parseInt(itens[i].weight);
		}
	}
	return sum;
}

/* Get the neighbors of a solution */
function getNeighbors(actual_solution) {
	var neighbors = []
	var neighbor = {}
	var solution = actual_solution.join().split(",")
	
	for (var i = 0; i < solution.length; i++) {
		if (solution[i] == "0") { solution[i] = "1" } else { solution[i] = "0" }
		
		neighbor.solution = solution;
		neighbor.value = valueSolution(solution)
		neighbor.weight = weightSolution(solution)

		neighbors.push(neighbor)

		/* restart variables */
		solution = actual_solution.join().split(",")
		neighbor = {}
	}
	return neighbors;
}

initializeSolution();

console.log(getNeighbors(INITIAL_SOLUTION))