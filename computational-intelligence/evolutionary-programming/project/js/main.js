/*
Airton Bordin Junior
airtonbjunior@gmail.com

Evolutionary Programming

Computational Intelligence - Federal University of Goias (UFG)
UFG master's program 
*/

/* Main variables */
POPULATION         = [];
POPULATION_SIZE    = 4;
GENERATIONS        = 30;
FUNCTION_CHOOSED   = "beale";
FUNC_LOWER_LIMIT   = -4.5;
FUNC_UPPER_LIMIT   = 4.5;

GAUSS_VARIATION    = 2;
CHILD_POPULATION   = [];

BEST_EACH_GEN      = [];

/* Main functions */
/* Create the population */
function createPopulation() {
	log("==== Creating population ====");
	var x, y = 0;

	for (var i = 0; i < POPULATION_SIZE; i++) {		
		
		x = getRandom(FUNC_LOWER_LIMIT, FUNC_UPPER_LIMIT);
		y = getRandom(FUNC_LOWER_LIMIT, FUNC_UPPER_LIMIT);
		
		POPULATION.push(
			{
				x_value: x,
				y_value: y,
				fitness: evaluate([x, y])
			}
		);
	}
}

/* Evaluate using the function choosed */
function evaluate(values, func) {
	return parseFloat(beale(values[0], values[1]));
}


function mutate() {
	log("==== Mutation ====");
	var x, y = 0;

	for(var i = 0; i < POPULATION_SIZE; i++) {

		x = POPULATION[0].x_value + (GAUSS_VARIATION * getRandom(-1, 1));
		y = POPULATION[0].y_value + (GAUSS_VARIATION * getRandom(-1, 1));
		
		CHILD_POPULATION.push(
			{
				x_value: x,
				y_value: y,
				fitness: evaluate([x, y])
			}
		);
	}
}

function nextGeneration() {
	var population_all = POPULATION.concat(CHILD_POPULATION);
	population_all.sort(sortComparator);
	
	POPULATION = population_all.slice(0, POPULATION_SIZE);
	CHILD_POPULATION = [];

	BEST_EACH_GEN.push(POPULATION[0].fitness);
}


/* Sort the population by Fitness value (ASC) */
function sortPopulationByFitness() {
	POPULATION.sort(sortComparator);
}
function sortComparator(a, b) {
	return parseFloat(a.fitness) - parseFloat(b.fitness);
}
/* Main functions */


initializeUI();

function start() {
	/* Main workflow */
	getVariables();
	createPopulation();

	for(var i = 0; i < GENERATIONS; i++) {
		log(POPULATION);

		mutate();

		log(CHILD_POPULATION);

		nextGeneration();
	}
	
	document.getElementById("result").value = "The best value is " + POPULATION[0].fitness;
	
	//log(BEST_EACH_GEN);

	chart = new Chartist.Line('.ct-chart', {labels: ['Generations'], series: [BEST_EACH_GEN]}, options);

	POPULATION    = []; // Reset, because the user can click start again
	BEST_EACH_GEN = []; // Reset, because the user can click start again
	/* Main workflow */
}


/* Aux functions */
function initializeUI() {

	document.getElementById("btn-start").addEventListener("click", start);

	document.getElementById("generations").value = GENERATIONS;
	document.getElementById("populationSize").value = POPULATION_SIZE;
	document.getElementById("mutateVariation").value = GAUSS_VARIATION;

	FUNCTION_CHOOSED = document.querySelector('input[name="func"]:checked').value;
}

function getVariables() {
	GENERATIONS = document.getElementById("generations").value;
	POPULATION_SIZE = document.getElementById("populationSize").value;
	GAUSS_VARIATION = document.getElementById("mutateVariation").value;
}

function getRandom(min, max) {
  return Math.random() * (max - min) + min;
}

function log(msg, input) {
	console.log(msg);
}

var options = {
  showPoint: false,
  lineSmooth: true,
  axisX: {
    showGrid: false,
    showLabel: true,
  },
  showArea: true
};


/* Aux functions */



/* Two variables functions */
/*
 * References: https://www.sfu.ca/~ssurjano/beale.html
 */
function beale(x, y) {
	part1 = Math.pow((1.5 - x + x*y), 2);
	part2 = Math.pow((2.25 - x + x*Math.pow(y, 2)),2);
	part3 = Math.pow((2.625 - x + x*Math.pow(y, 3)), 2);

	return part1 + part2 + part3;
}


function goldesteinPrice(x, y) {
	part1a = Math.pow((x + y + 1),2);
	part1b = 19 - (14*x) + Math.pow((3*x),2) - (14*y) + (6*x*y) + Math.pow((3*y),2);
	part1 = 1 + part1a * part1b;

	part2a = Math.pow((2*x - 3*y),2);
	part2b = 18 - (32*x) + (Math.pow((12*x),2)) + (48*y) - (36*x*y) + Math.pow((27*y),2);
	part2 = 30 + part2a * part2b;

	return part1 * part2;
}

