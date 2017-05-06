/* 
Airton Bordin Junior
airtonbjunior@gmail.com


Genetic Programming

Computational Intelligence - Federal University of Goias (UFG)
UFG master's program 
*/

/* PROBLEM PARAMETERS */
OPERATORS = ['+', '-', '*', '/'];
VARIABLES = ["x"];

HEIGHT_TREE = 2; /* 2^h operators and 2^h-1 constants */
/* PROBLEM PARAMETERS */



/* It's a toy problem = I want to find the function x^2 + 1 */
/**/
function generatePopulation() {
	var n_operators = parseInt(Math.pow(2, HEIGHT_TREE) - 1);
	var n_terminals = parseInt(Math.pow(2, HEIGHT_TREE));

	/* 
	I'll represent the tree in a array 
	The children->left is the (2*i + 1) position 
	The children->right is the (2*i + 2) position 
	*/

	console.log("Number of operators: " + n_operators);
	console.log("Number of terminals: " + n_terminals);
}

generatePopulation();