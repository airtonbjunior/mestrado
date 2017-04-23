/*
Airton Bordin Junior
airtonbjunior@gmail.com

Evolutionary Programming

Computational Intelligence - Federal University of Goias (UFG)
UFG master's program 
*/

/* Main variables */
POPULATION         = [];
POPULATION_SIZE    = 10;
LOWER_LIMIT        = -4.5;
UPPER_LIMIT        = 4.5;
FUNCTION_CHOOSED   = "beale";
GAUSS_VARIATION    = 2;
CHILD_POPULATION   = [];


/* Create the population */
function createPopulation() {
	log("==== Creating population ====");
	var x, y = 0;

	for (var i = 0; i < POPULATION_SIZE; i++) {		
		
		x = getRandom(LOWER_LIMIT, UPPER_LIMIT);
		y = getRandom(LOWER_LIMIT, UPPER_LIMIT);
		
		POPULATION.push(
			{
				x_value: x,
				y_value: y,
				fitness: evaluate([x, y])
			}
		);
	}

	log(POPULATION);
}

/* Evaluate using the function choosed */
function evaluate(values, func) {
	return parseFloat(beale(values[0], values[1]));
}


function mutate() {
	log("==== Mutation ====");
	var x, y = 0;

	for(var i = 0; i < POPULATION_SIZE; i++) {

		x = POPULATION[0].x_value + getRandom(LOWER_LIMIT, UPPER_LIMIT);
		y = POPULATION[0].y_value + getRandom(LOWER_LIMIT, UPPER_LIMIT);
		
		CHILD_POPULATION.push(
			{
				x_value: x,
				y_value: y,
				fitness: evaluate([x, y])
			}
		);
	}
	
}


/* Sort the population by Fitness value (ASC) */
function sortPopulationByFitness() {
	POPULATION.sort(sortComparator);
}
function sortComparator(a, b) {
	return parseFloat(a.fitness) - parseFloat(b.fitness);
}


/* Main workflow */
createPopulation();
//sortPopulationByFitness();



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

console.log(beale(3, 0.5));


function getRandom(min, max) {
  return Math.random() * (max - min) + min;
}

function log(msg, input) {
	console.log(msg);
}