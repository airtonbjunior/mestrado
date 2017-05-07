/* 
Airton Bordin Junior
airtonbjunior@gmail.com


Genetic Programming

Computational Intelligence - Federal University of Goias (UFG)
UFG master's program 
*/

/* PROBLEM PARAMETERS */
OPERATORS = ['+', '-', '*', '/'];
TERMINALS = ["x"];

HEIGHT_TREE = 3; /* 2^h terminals and 2^h-1 operators */

GENERATIONS = 10;
POP_SIZE    = 30;
POPULATION  = [];

REPRODUTION_PROBABILITY = 0;
CROSSOVER_PROBABILITY = 75;
MUTATE_PROBABILITY = 5;
PERMUTATION_PROBABILITY = 0;

ELITISM = true;
DESTRUCTION_TREE = false;
/* PROBLEM PARAMETERS */


/* 
	I'll represent the tree in a array 
	- The children->left is the (2*i + 1) position 
	- The children->right is the (2*i + 2) position 
*/


/* It's a toy problem = I want to find the function x^2 + 1 */

/* 	Generate the population 
	Default: Full Method (perfect trees)
*/
function generatePopulation() {
	log("###### Generate the population ######");
	var node = {};
	//var operators = [];
	//var terminals = [];

	var expression;

	var n_operators = parseInt(Math.pow(2, HEIGHT_TREE) - 1);
	var n_terminals = parseInt(Math.pow(2, HEIGHT_TREE));

	for(var j = 0; j < POP_SIZE; j++) {
		
		expression = "";
		node = {};

		/* Mount the expression */
		for(var i = 0; i < n_operators/2; i++) {
			expression += "("; 

			if(getRandom(0, 1) == 0) 
				expression += TERMINALS[getRandom(0, TERMINALS.length -1)]
			else
				expression += getRandom(0, 9);

			expression += OPERATORS[getRandom(0, OPERATORS.length - 1)];
			
			// Two times (didact reasons)
			if(getRandom(0, 1) == 0) 
				expression += TERMINALS[getRandom(0, TERMINALS.length -1)]
			else
				expression += getRandom(0, 9);		
			
			expression += ")";
			expression += OPERATORS[getRandom(0, OPERATORS.length - 1)];
		}
		expression = expression.substring(0, expression.length - 1); // Remove the last operator
		node.expression = expression;
		node.fitness = evaluate(expression);

		POPULATION.push(node);
	}
	/*
	for (var i = 0; i < n_operators; i++) {
		operators.push(OPERATORS[getRandom(0, OPERATORS.length -1)]);
	}

	for (var i = 0; i < n_terminals; i++) {
		// choose between variables and constants (50%) 
		if(getRandom(0, 1) == 0) 
			terminals.push(TERMINALS[getRandom(0, TERMINALS.length - 1)]);
		else
			terminals.push(getRandom(0, 9));		
	}
	*/

	//node.operators = operators;
	//node.terminals = terminals;

}


/*	Evaluate the expression 
	Use the Mean Square Error

	Sum([square of differences between estimator and estimated])/n
*/
function evaluate(expression) {
	var exp;

	/* Tests for a certain function x^2+1 (toy problem for now) */
	var test_values = ["1", "2", "3", "4", "5"]
	var result_test = ["2", "5", "10", "17", "26"]
	var differences = [];
	/* Tests for a certain function x^2+1*/

	for (var i = 0; i < test_values.length; i++) {
		exp = expression.replace(/x/g, test_values[i]);	
		//console.log(parseFloat(eval(exp)) + " - " + parseFloat(result_test[i]) + " = " + parseFloat(eval(exp) - parseFloat(result_test[i])));
		differences.push(parseFloat(eval(exp) - parseFloat(result_test[i])));
	}

	var squareError = 0;
	for (var i = 0; i < differences.length; i++) {
		squareError += Math.pow(parseFloat(differences[i]), 2);
	}
	return parseFloat(squareError/test_values.length); // return the mean square error
}



function nextGeneration() {
	if(getRandom(0, 100) <= CROSSOVER_PROBABILITY) {
		//doCrossover(POPULATION[getRandom(0, POP_SIZE - 1)], POPULATION[getRandom(0, POP_SIZE - 1)]);

		doMutation(POPULATION[getRandom(0, POP_SIZE - 1)]);
	}
}


function doCrossover(node1, node2) {
	log("Crossover between " + node1.expression + " and " + node2.expression);
	do {
		crosspoint = getRandom(0, node1.expression.length - 1);
	} while(node1.expression.charAt(crosspoint) === "(" || node1.expression.charAt(crosspoint) === ")");

	log(node1.expression.charAt(crosspoint) + " at position " + crosspoint);
}


function doMutation(node) {
	log("Mutate the expression " + node.expression);

	do {
		mutatePoint = getRandom(0, node.expression.length - 1);
	} while(node.expression.charAt(mutatePoint) === "(" || node.expression.charAt(mutatePoint) === ")");


	/* Verify if it's a operator */
	if(OPERATORS.indexOf(node.expression.charAt(mutatePoint)) != -1) {

		log("I'll change the operator " + node.expression.charAt(mutatePoint) + " at position " + mutatePoint);
		do {
			newOperator = OPERATORS[getRandom(0, OPERATORS.length - 1)];
		} while (newOperator === node.expression.charAt(mutatePoint));
	
		node.expression = node.expression.substring(0, mutatePoint) + newOperator + node.expression.substring(mutatePoint+1);
	}
	else {

	}


	log("The result is " + node.expression);
}


/* Sort the population by fitness */
function sortComparator(a, b) {
	return parseFloat(a.fitness) - parseFloat(b.fitness);
}
/* Main functions */


/* Main flow of Genetic Programming */
generatePopulation();
POPULATION.sort(sortComparator);

for (var i = 0; i < GENERATIONS; i++) {
	nextGeneration();
}

console.log(POPULATION);




/* Aux functions */

/* Get a random INTEGER between min and max */
function getRandom(min, max) {
	return Math.floor(Math.random()*(max-min+1)+min);
}

/* Soon will log on page */
function log(msg, input) {
	console.log(msg)
}

/*
function mountExpression() {
	var exp = "";
	var node = POPULATION[0];

	var operatorsIndex = node.operators.length - 1;

	for (var i = node.terminals.length - 1; i >= 0; i--) {
		
		exp += node.terminals[i];
		if(operatorsIndex >= 0) {
			exp += node.operators[operatorsIndex];
			operatorsIndex--;			
		}
	}

	console.log(exp);
}
*/