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

HEIGHT_TREE = 3; /* 2^h operators and 2^h-1 constants */

GENERATIONS = 10;
POPULATION = [];
/* PROBLEM PARAMETERS */



/* It's a toy problem = I want to find the function x^2 + 1 */
/**/
function generatePopulation() {
	var node = {};
	var operators = [];
	var terminals = [];

	var expression = "";

	var n_operators = parseInt(Math.pow(2, HEIGHT_TREE) - 1);
	var n_terminals = parseInt(Math.pow(2, HEIGHT_TREE));

	/* 
	I'll represent the tree in a array 
	The children->left is the (2*i + 1) position 
	The children->right is the (2*i + 2) position 
	*/

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

	node.operators = operators;
	node.terminals = terminals;
	node.expression = expression;
	node.fitness = 0;

	POPULATION.push(node);
}

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


for (var i = 0; i < GENERATIONS; i++) {
	generatePopulation();
}

mountExpression();
console.log(POPULATION);




/* Aux functions */

/* Get a random INTEGER between min and max */
function getRandom(min, max) {
	return Math.floor(Math.random()*(max-min+1)+min);
}