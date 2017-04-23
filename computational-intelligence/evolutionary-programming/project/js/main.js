/*
Airton Bordin Junior
airtonbjunior@gmail.com

Evolutionary Programming

Computational Intelligence - Federal University of Goias (UFG)
UFG master's program 
*/

/* Main variables */
POPULATION_VALUES  = [];
POPULATION_FITNESS = [];
POPULATION_SIZE    = 10;
LOWER_LIMIT        = 1;
UPPER_LIMIT        = 5;


createPopulation();

/* Create the population */
function createPopulation() {
	log("==== Creating population ====");

	for (var i = 0; i < POPULATION_SIZE; i++) {		
		POPULATION_VALUES[i]  = [getRandom(LOWER_LIMIT, UPPER_LIMIT), getRandom(LOWER_LIMIT, UPPER_LIMIT )];
		POPULATION_FITNESS[i] = 0;
	}

	log(POPULATION_VALUES);
}



function sortPopulationByFitness() {

}




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