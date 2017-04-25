/*
Airton Bordin Junior
airtonbjunior@gmail.com

Evolutionary Programming

Computational Intelligence - Federal University of Goias (UFG)
UFG master's program 
*/

/* Main variables */
POPULATION         = [];
POPULATION_SIZE    = 50;
GENERATIONS        = 50;
FUNCTION_CHOOSED   = 0;
FUNC_LOWER_LIMIT   = -4.5;
FUNC_UPPER_LIMIT   = 4.5;

GAUSS_VARIATION    = 2;
CHILD_POPULATION   = [];

SELECTION_TYPE     = "elitism";
MUTATION_TYPE      = "nonAdaptative";

BEST_EACH_GEN      = [];

/* Math functions for optimization - https://en.wikipedia.org/wiki/Test_functions_for_optimization */
FUNCTIONS = [];
FUNCTIONS.push({name: 'beale', min: -4.5, max: 4.5});
FUNCTIONS.push({name: 'matya', min: -10, max: 10});
FUNCTIONS.push({name: 'booth', min: -10, max: 10});
FUNCTIONS.push({name: 'schafferF6', min: -100, max: 100});


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
				fitness: evaluate([x, y], FUNCTION_CHOOSED)
			}
		);
	}
}

/* Evaluate using the function choosed */
function evaluate(values, func) {
	switch(func) {
	    case "0":
	        return parseFloat(beale(values[0], values[1]));
	        break;
	    case "1":
	        return parseFloat(matya(values[0], values[1]));
	        break;
	    case "2":
	        return parseFloat(booth(values[0], values[1]));
	        break;
	    case "3":
	        return parseFloat(schafferF6(values[0], values[1]));
	        break;
	    default:
	        //alert("Choose one function");
	        break;
	}
}

/* Mutate the population - In EP, is the only source of variation */
function mutate() {
	log("==== Mutation ====");
	var x, y = 0;

	for(var i = 0; i < POPULATION_SIZE; i++) {

		/* Change here when I code the other mutation types */
		if(MUTATION_TYPE == "nonAdaptative" || true) {
			/* Here, apply some mutate strategy */
			x = POPULATION[i].x_value + (GAUSS_VARIATION * getRandom(-1, 1));
			y = POPULATION[i].y_value + (GAUSS_VARIATION * getRandom(-1, 1));

			/* Separated for didact reasons :D */
			if(x > FUNC_UPPER_LIMIT) { x = getRandom(FUNC_LOWER_LIMIT, FUNC_UPPER_LIMIT); }
			if(x < FUNC_LOWER_LIMIT) { x = getRandom(FUNC_LOWER_LIMIT, FUNC_UPPER_LIMIT); }
			if(y > FUNC_UPPER_LIMIT) { y = getRandom(FUNC_LOWER_LIMIT, FUNC_UPPER_LIMIT); }
			if(y < FUNC_LOWER_LIMIT) { y = getRandom(FUNC_LOWER_LIMIT, FUNC_UPPER_LIMIT); }
			
			CHILD_POPULATION.push(
				{
					x_value: x,
					y_value: y,
					fitness: evaluate([x, y], FUNCTION_CHOOSED)
				}
			);
		}
	}
}

/* Prepare the next generation, based on the selecion type (elitism/tournament) */
function nextGeneration() {
	log("==== Processing next generation ====");

	var population_all = POPULATION.concat(CHILD_POPULATION);
	population_all.sort(sortComparator);

	console.log(population_all);

	if(SELECTION_TYPE == "elitism") 
	{
		POPULATION = population_all.slice(0, POPULATION_SIZE); // Get the best ones
	}
	else if(SELECTION_TYPE == "tournament") 
	{
		var choosed1, choosed2;
		var chooseds = [];

		for(var i = 0; i < POPULATION_SIZE; i++) {
			choosed1 = population_all[Math.floor(getRandom(0, population_all.length))];
			choosed2 = population_all[Math.floor(getRandom(0, population_all.length))];

			if(choosed1.fitness <= choosed2.fitness) { chooseds.push(choosed1); } else { chooseds.push(choosed2); }
		}
		POPULATION = chooseds;
		POPULATION.sort(sortComparator);
	}
	
	BEST_EACH_GEN.push(POPULATION[0].fitness);
	CHILD_POPULATION = [];
}


/* Sort the population by Fitness value (ASC) */
function sortPopulationByFitness() {
	POPULATION.sort(sortComparator);
}
function sortComparator(a, b) {
	return parseFloat(a.fitness) - parseFloat(b.fitness);
}
/* Main functions */


/* Initialize  UI */
initializeUI();

/* Pre-start 
 * Loading icon, change the button label, set timeout and call start()
 */
function startPreparation() {
	
	getVariables();
	if(document.getElementById("mutateVariation").value <= 0 && MUTATION_TYPE == "nonAdaptative") {
		alert("Mutate Variation must be greater than zero");
		return;
	}

	document.getElementById("loading-icon").classList.remove("hide-load");
	document.getElementById("btn-start").innerHTML = "Processing...";
	document.getElementById("loading-icon").className += " fa fa-cog fa-spin fa-5x fa-fw";
	
	setTimeout(start, 50);
}


/* Start the Evolotionary Programming */
function start() {
	/* Main workflow */
	createPopulation();

	for(var i = 0; i < GENERATIONS; i++) {
		log(POPULATION);

		mutate();

		log(CHILD_POPULATION);

		nextGeneration();
	}
	
	document.getElementById("result").innerHTML = "The minimum of " + FUNCTIONS[FUNCTION_CHOOSED].name + " is " + POPULATION[0].fitness.toPrecision(3) + " with x = " + POPULATION[0].x_value.toPrecision(3) + " and y = " +POPULATION[0].y_value.toPrecision(3);
	
	chart = new Chartist.Line('.ct-chart', {labels: ['Generations'], series: [BEST_EACH_GEN]}, options);

	POPULATION    = []; // Reset, because the user can click start again
	BEST_EACH_GEN = []; // Reset, because the user can click start again
	/* Main workflow */

	/* Restart the default screen */
	document.getElementById("loading-icon").className += " hide-load";
	document.getElementById("btn-start").innerHTML = "Start";
}


/* Aux functions */
function initializeUI() {

	new Opentip("#beale-function", { target: true, tipJoint: "left", background: "#ffffff"}).setContent("<img src='img/beale.png'></img>");
	new Opentip("#matya-function", { target: true, tipJoint: "left", background: "#ffffff" }).setContent("<img src='img/matya.png'></img>");
	new Opentip("#booth-function", { target: true, tipJoint: "left", background: "#ffffff" }).setContent("<img src='img/booth.png'></img>");
	new Opentip("#schaffer-function", { target: true, tipJoint: "left", background: "#ffffff"}).setContent("<img src='img/schaffer.gif'></img>");

	document.getElementById("btn-start").addEventListener("click", startPreparation);

	document.getElementById("generations").value = GENERATIONS;
	document.getElementById("populationSize").value = POPULATION_SIZE;
	document.getElementById("mutateVariation").value = GAUSS_VARIATION;

	FUNCTION_CHOOSED = document.querySelector('input[name="func"]:checked').value;

	document.getElementById("min-func").innerHTML = "Interval [" + FUNCTIONS[FUNCTION_CHOOSED].min + ", " + FUNCTIONS[FUNCTION_CHOOSED].max + "]";
}

/* Get users values on GUI */
function getVariables() {
	GENERATIONS = document.getElementById("generations").value;
	POPULATION_SIZE = document.getElementById("populationSize").value;
	GAUSS_VARIATION = document.getElementById("mutateVariation").value;

	FUNC_LOWER_LIMIT = parseFloat(FUNCTIONS[FUNCTION_CHOOSED].min);
	FUNC_UPPER_LIMIT = parseFloat(FUNCTIONS[FUNCTION_CHOOSED].max);


	var e = document.getElementById("selection-type");
	SELECTION_TYPE = e.options[e.selectedIndex].value;

	MUTATION_TYPE = document.querySelector('input[name="mutation-type"]:checked').value;
}

/* When the user changes the function on radio buttons */
function changeFunction(param) {
	FUNCTION_CHOOSED = param.value;
	document.getElementById("min-func").innerHTML = "Interval [" + FUNCTIONS[FUNCTION_CHOOSED].min + ", " + FUNCTIONS[FUNCTION_CHOOSED].max + "]";
}

/* When the user changes the mutation type on radio buttons */
function changeMutation(param) {
	MUTATION_TYPE = document.querySelector('input[name="mutation-type"]:checked').value;
	/* TO-DO: disable the input when the type is different of nonAdaptative */
}

/* Get a random value between min and max*/
function getRandom(min, max) {
	return Math.random() * (max - min) + min;
}

/* Log the message */
function log(msg, input) {
	console.log(msg);
}

/* Chart options*/
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


/* 
 * References: https://www.sfu.ca/~ssurjano/matya.html 
 */
function matya(x, y) {
	return (0.26) * (Math.pow(x, 2) + Math.pow(y, 2)) - 0.48*x*y;
}


function booth(x, y) {
	return Math.pow((x + 2*y - 7), 2) + Math.pow((2*x + y -5), 2);
}

function schafferF6(x, y) {
	var part1 = Math.pow((Math.sin(Math.sqrt((x**2) + (y**2)))), 2);
	var part2 = Math.pow((1.0 + 0.001 * (x**2 + y**2)), 2);
	return 0.5 + ((part1 - 0.5) / part2);
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

