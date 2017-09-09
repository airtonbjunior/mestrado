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

BAG_CAPACITY = 300;
ITENS_QUANTITY = itens.length;

/* Choose a start solution. Default: randomly */
function initializeSolution() {
	for(var i = 0; i < ITENS_QUANTITY; i++) {
		INITIAL_SOLUTION.push(Math.round(Math.random()));
	}
	ACTUAL_SOLUTION = INITIAL_SOLUTION;
	console.log("[START INITIAL SOLUTION]: " + INITIAL_SOLUTION)
}


/* Evaluate the solution value */
function evaluateSolution(solution) {
	sum = 0;
	/* For has much better performance than forEach */
	for (var i = 0; i < solution.length; i++) {
		if(solution[i] == 1) {
			sum += parseInt(itens[i].value);
		}
	}
	return sum;
}

function getNeighbors(actual_solution) {

}


/* Move to the next element in search space */
function move() {

}


initializeSolution();
console.log(INITIAL_SOLUTION);
console.log(evaluateSolution(INITIAL_SOLUTION))