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

HEIGHT_TREE = 2; /* 2^h terminals and 2^h-1 operators */

GENERATIONS = 1000;
POP_SIZE    = 750;
POPULATION  = [];

CHILDRENS = [];

REPRODUTION_PROBABILITY = 0;
CROSSOVER_PROBABILITY = 75;
MUTATE_PROBABILITY = 5;
PERMUTATION_PROBABILITY = 5;

SELECTION_TYPE = "elitism";
DESTRUCTION_TREE = false;

TEST_VALUES  = ["1", "2", "3", "4", "5", "6"];
RESULT_TESTS = ["2", "5", "10", "17", "26", "37"];
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
}


/*	Evaluate the expression 
	Use the Mean Square Error
	http://sciencing.com/calculate-mse-8464173.html

	Sum([square of differences between estimator and estimated])/n
*/
function evaluate(expression) {
	var exp;

	/* Tests for a certain function x^2+1 (toy problem for now) */
	/* Get this parameters in GUI */
	var test_values = TEST_VALUES;
	var result_test = RESULT_TESTS;
	var differences = [];
	/* Tests for the function x^2+1 */

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


/* Process the next generation */
function nextGeneration() {
	var nextPopulation = [];

	if(getRandom(0, 100) <= CROSSOVER_PROBABILITY) {
		doCrossover(POPULATION[getRandom(0, POP_SIZE - 1)], POPULATION[getRandom(0, POP_SIZE - 1)]);
	}
	/* if don't cross, copy 2 random elements to childrens */
	else {
		CHILDRENS.push(POPULATION[getRandom(0, POP_SIZE - 1)]);
		CHILDRENS.push(POPULATION[getRandom(0, POP_SIZE - 1)]);
	}

	if(SELECTION_TYPE == "elitism") {
		/* Concat the two arrays (POPULATION and CHILDRENS), sort and get the best to next generation */
		nextPopulation = POPULATION.concat(CHILDRENS);
		nextPopulation.sort(sortComparator);
		POPULATION = nextPopulation.slice(0, POP_SIZE);
	}
	/* Tournament */
	else {
		nextPopulation = POPULATION.concat(CHILDRENS);
		var choosed = [];

		for (var i = 0; i < POP_SIZE; i++) {
			var pos1 = getRandom(0, nextPopulation.length - 1);
			var pos2 = getRandom(0, nextPopulation.length - 1);
			if(nextPopulation[pos1].fitness < nextPopulation[pos2].fitness) 
				choosed.push(nextPopulation[pos1]);
			else
				choosed.push(nextPopulation[pos2]);
		}

		POPULATION = choosed;
	}

	CHILDRENS = [];
}


/* 	Do the crossover between two nodes (expression trees) 
	
	I'm using the same crosspoint to the same tree. 
	Consider, here, that I'm using only perfect trees.
	The height of the tree is a hard constraint in my project
	There's others solutions to handle this
*/
function doCrossover(node1, node2) {
	log("=========================================");
	log("###### Crossover ######");
	log("Crossover between " + node1.expression + " and " + node2.expression);

	var childNode1 = {};
	var childNode2 = {};
	childNode1.expression = "";
	childNode2.expression = "";

	do {
		crosspoint = getRandom(0, node1.expression.length - 1);
	} while(node1.expression.charAt(crosspoint) === "(" || node1.expression.charAt(crosspoint) === ")");

	/* Internal trivial expression? (5+x) for example */
	if(node1.expression.charAt(crosspoint + 1) !== "(") {
		
		/* It's the operator inside the expression */
		if(OPERATORS.indexOf(node1.expression.charAt(crosspoint)) != -1) {
			var partNode1 = node1.expression.substring(crosspoint - 1, crosspoint + 2);	
			var partNode2 = node2.expression.substring(crosspoint - 1, crosspoint + 2);	

			/* Node 1 with part of Node 2 */
			childNode1.expression = node1.expression.substring(0, crosspoint - 1) 
							 	+ partNode2
							 	+ node1.expression.substring(crosspoint + 2);

			/* Node 2 with part of Node 1 */
			childNode2.expression = node2.expression.substring(0, crosspoint - 1) 
							 	+ partNode1
							 	+ node2.expression.substring(crosspoint + 2);		
		}
		/* It's a terminal inside the expression */
		else {
			/* Exchange the terminals of the tree */
			var partNode1 = node1.expression.charAt(crosspoint);	
			var partNode2 = node2.expression.charAt(crosspoint);

			childNode1.expression = node1.expression.substring(0, crosspoint)
								  + partNode2
								  + node1.expression.substring(crosspoint + 1);

			childNode2.expression = node2.expression.substring(0, crosspoint)
								  + partNode1
								  + node2.expression.substring(crosspoint + 1);								  
		}							 
	}
	/* Not an internal expression */
	else {

		/* It's the root */
		if(crosspoint == Math.floor(node1.expression.length/2)) {
			log("it's the tree root");
			var partNode1 = node1.expression.substring(0, crosspoint + 1);
			var partNode2 = node2.expression.substring(0, crosspoint + 1);

			childNode1.expression = partNode2 + node1.expression.substring(crosspoint + 1);
			childNode2.expression = partNode1 + node2.expression.substring(crosspoint + 1);
		}
		/* Not an internal expression AND not the root */
		else {
			log("not the root and not an internal operator");

			var partNode1 = node1.expression.substring(crosspoint -5, crosspoint + 6);
			var partNode2 = node2.expression.substring(crosspoint -5, crosspoint + 6);

			childNode1.expression = node1.expression.substring(0, crosspoint - 5) + partNode2 + node1.expression.substring(crosspoint + 6);
			childNode2.expression = node2.expression.substring(0, crosspoint - 5) + partNode1 + node2.expression.substring(crosspoint + 6);
		}
	}

	log("Child 1 -> " + childNode1.expression);
	log("Child 2 -> " + childNode2.expression);

	/* Mutation or Permutation (2 times to be more didact) */
	if(getRandom(0, 100) < MUTATE_PROBABILITY) {
		doMutation(childNode1);
	} else {
		if(getRandom(0, 100) < PERMUTATION_PROBABILITY) {
			doPermutation(childNode1);
		}
	}
	
	/* Mutation or Permutation */
	if(getRandom(0, 100) < MUTATE_PROBABILITY) {
		doMutation(childNode2);
	} else {
		if(getRandom(0, 100) < PERMUTATION_PROBABILITY) {
			doPermutation(childNode2);
		}
	}

	childNode1.fitness = evaluate(childNode1.expression);
	childNode2.fitness = evaluate(childNode2.expression);
	CHILDRENS.push(childNode1);
	CHILDRENS.push(childNode2);

	CHILDRENS.sort(sortComparator);

	log(node1.expression.charAt(crosspoint) + " at position " + crosspoint);
}


/* Do the mutation in a node */
function doMutation(node) {
	log("=========================================");
	log("###### Mutation ######");
	log("Mutate the expression " + node.expression);

	do {
		mutatePoint = getRandom(0, node.expression.length - 1);
	} while(node.expression.charAt(mutatePoint) === "(" || node.expression.charAt(mutatePoint) === ")");

	/* Verify if it's a operator */
	if(OPERATORS.indexOf(node.expression.charAt(mutatePoint)) != -1) {

		log("I'll change the OPERATOR " + node.expression.charAt(mutatePoint) + " at position " + mutatePoint);
		do {
			newOperator = OPERATORS[getRandom(0, OPERATORS.length - 1)];
		} while (newOperator === node.expression.charAt(mutatePoint));
	
		node.expression = node.expression.substring(0, mutatePoint) + newOperator + node.expression.substring(mutatePoint+1);
	}
	/* It's a terminal */
	else {
		log("I'll change the TERMINAL " + node.expression.charAt(mutatePoint) + " at position " + mutatePoint);

		/* Verify if it's a number or variable */
		if(isNaN(node.expression.charAt(mutatePoint))) {
			node.expression = node.expression.substring(0, mutatePoint) + getRandom(0, 9) + node.expression.substring(mutatePoint+1);	
		}
		else {
			if(getRandom(0, 1) == 0) 
				node.expression = node.expression.substring(0, mutatePoint) + TERMINALS[getRandom(0, TERMINALS.length -1)] + node.expression.substring(mutatePoint+1);
			else
				node.expression = node.expression.substring(0, mutatePoint) + getRandom(0, 9) + node.expression.substring(mutatePoint+1);	
		}			
	}
	log("The result is " + node.expression);
}


/* Do the permutation */
function doPermutation(node) {
	log("=========================================");
	log("###### Permutation ######");
	log(node.expression);

	do {
		permutationPoint = getRandom(0, node.expression.length - 1);
	} while(node.expression.charAt(permutationPoint) === "(" 
			|| node.expression.charAt(permutationPoint) === ")"
			|| OPERATORS.indexOf(node.expression.charAt(permutationPoint)) == -1); // Permutation point needs to be a operator

	/* Verify if it's a internal expression like (5+x) */
	if(node.expression.charAt(permutationPoint + 1) !== "(") {
		var operator = node.expression.charAt(permutationPoint);
		var term1    = node.expression.charAt(permutationPoint - 1);
		var term2    = node.expression.charAt(permutationPoint + 1);

		node.expression = node.expression.substring(0, permutationPoint - 1) + term2 + operator + term1 + node.expression.substring(permutationPoint+2);

		log("Permutate internal expression -> (" + term1 + operator + term2 + ") -> " + node.expression);
	}
	else {
		/* Verify if it's the tree root */
		if(permutationPoint == Math.floor(node.expression.length/2)) {
			log("it's the tree root");
			var operator = node.expression.charAt(permutationPoint);
			var part1 	 = node.expression.substring(0, permutationPoint);
			var part2 	 = node.expression.substring(permutationPoint + 1);

			node.expression = part2 + operator + part1;

			log("Permutate root operator -> " + part1 + operator + part2 + " -> " + node.expression);
		}
		/* Not an internal expression AND not the root */
		else {
			log("not the root and not an internal operator");
			var operator = node.expression.charAt(permutationPoint);
			var part1 = node.expression.substring(permutationPoint - 5, permutationPoint);  // change this, it's hardcoded by now
			var part2 = node.expression.substring(permutationPoint + 1, permutationPoint + 6) // change this, it's hardcoded by now

			node.expression = node.expression.substring(0, permutationPoint - 5) 
							+ part2 + operator + part1
							+ node.expression.substring(permutationPoint + 6);

			log("Permutate other operator -> " + part1 + operator + part2 + " -> " + node.expression);
		}
	}

}

/* Sort the population by fitness */
function sortComparator(a, b) {
	return parseFloat(a.fitness) - parseFloat(b.fitness);
}
/* Main functions */




/* Start the preparation to the main flow */
function startPreparation() {
	GENERATIONS = document.getElementById("generations").value;
	POP_SIZE = document.getElementById("populationSize").value;
	CROSSOVER_PROBABILITY = document.getElementById("crossoverProbability").value;
	MUTATE_PROBABILITY = document.getElementById("mutateProbability").value;
	PERMUTATION_PROBABILITY = document.getElementById("permutationProbability").value;
	HEIGHT_TREE = document.getElementById("treeHeight").value;

	var e = document.getElementById("selection-type");
	SELECTION_TYPE = e.options[e.selectedIndex].value;

	for(var i = 0; i < TEST_VALUES.length; i++) {
		TEST_VALUES[i] = document.getElementById("param"+i).value;
		RESULT_TESTS[i] = document.getElementById("result"+i).value;
	}

	POPULATION = [];
	CHILDRENS  = [];

	document.getElementById("result").innerHTML = "&nbsp";

	document.getElementById("loading-icon").classList.remove("hide-load");
	document.getElementById("btn-start").innerHTML = "Processing...";
	document.getElementById("loading-icon").className += " fa fa-cog fa-spin fa-5x fa-fw";
	
	/* Timeout for the UI changes */
	setTimeout(start, 50);
}

intializeUI();


/* Start the main flow*/
function start() {
	var generation_encountered = 0;
	
	/* Main flow of Genetic Programming */
	generatePopulation();
	POPULATION.sort(sortComparator);

	for (var i = 0; i < GENERATIONS; i++) {
		/* Check if the solution was found */
		if(POPULATION[0].fitness === 0) {
			generation_encountered = i;
			break;
		}
		nextGeneration();
		generation_encountered++;
	}

	document.getElementById("result").innerHTML = POPULATION[0].expression 
												+ "<br> with square error "
												+ POPULATION[0].fitness;

	/* Restart the default screen */
	document.getElementById("loading-icon").className += " hide-load";
	document.getElementById("btn-start").innerHTML = "Start";
	/* Restart the default screen */

	/* Some results log */
	console.log(POPULATION);
	console.log("Total of generations -> " + generation_encountered);
	console.log("The result is " + POPULATION[0].expression + " with square error " + POPULATION[0].fitness);
}


/* Initialize the GUI */
function intializeUI() {
	document.getElementById("btn-start").addEventListener("click", startPreparation);

	document.getElementById("generations").value = GENERATIONS;
	document.getElementById("populationSize").value = POP_SIZE;
	document.getElementById("crossoverProbability").value = CROSSOVER_PROBABILITY;
	document.getElementById("mutateProbability").value = MUTATE_PROBABILITY;
	document.getElementById("permutationProbability").value = PERMUTATION_PROBABILITY;
	document.getElementById("treeHeight").value = HEIGHT_TREE;

	/* TO-DO: when the user can grow the parameters list, do this dynamically */
	for(var i = 0; i < TEST_VALUES.length; i++) {
		document.getElementById("param"+i).value = TEST_VALUES[i];	
		document.getElementById("result"+i).value = RESULT_TESTS[i];
	}
}




/* Aux functions */

/* Get a random INTEGER between min and max */
function getRandom(min, max) {
	return Math.floor(Math.random()*(max-min+1)+min);
}

/* Soon will log on page */
function log(msg, input) {
	console.log(msg)
}

