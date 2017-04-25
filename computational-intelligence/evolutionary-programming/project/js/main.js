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

FITNESS_MEAN       = [];
VARIANCE           = [];

X_MEAN 			   = [];
Y_MEAN 			   = [];

MUTATE_VARIATION   = 2;
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
	var x, y, individualFitness, mean, xmean, ymean = 0;
	var fitnessSum = parseFloat(0);
	var xsum = parseFloat(0); var ysum = parseFloat(0);

	for (var i = 0; i < POPULATION_SIZE; i++) {		
		
		x = getRandom(FUNC_LOWER_LIMIT, FUNC_UPPER_LIMIT);
		y = getRandom(FUNC_LOWER_LIMIT, FUNC_UPPER_LIMIT);
		individualFitness = evaluate([x, y], FUNCTION_CHOOSED);

		POPULATION.push(
			{
				x_value: x,
				y_value: y,
				fitness: individualFitness
			}
		);
		fitnessSum = parseFloat(individualFitness) + parseFloat(fitnessSum);
		xsum = parseFloat(x) + parseFloat(xsum);
		ysum = parseFloat(y) + parseFloat(ysum);
	}
	mean = parseFloat(fitnessSum / POPULATION_SIZE);
	xmean = parseFloat(xsum / POPULATION_SIZE);
	ymean = parseFloat(ysum / POPULATION_SIZE);

	//console.log(xmean);
	//console.log(ymean);

	X_MEAN.push(xmean);
	Y_MEAN.push(ymean);
	FITNESS_MEAN.push(mean);

	calcDeviation();
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
	var x, y, fitnessSum = 0;

	for(var i = 0; i < POPULATION_SIZE; i++) {

		/* Change here when I code the other mutation types */
		if(MUTATION_TYPE == "nonAdaptative" || true) {
			/* Here, apply some mutate strategy */
			x = POPULATION[i].x_value + (MUTATE_VARIATION * getRandom(-1, 1));
			y = POPULATION[i].y_value + (MUTATE_VARIATION * getRandom(-1, 1));
			fitnessSum = evaluate([x, y], FUNCTION_CHOOSED);

			/* Separated for didact reasons :D */
			if(x > FUNC_UPPER_LIMIT) { x = getRandom(FUNC_LOWER_LIMIT, FUNC_UPPER_LIMIT); }
			if(x < FUNC_LOWER_LIMIT) { x = getRandom(FUNC_LOWER_LIMIT, FUNC_UPPER_LIMIT); }
			if(y > FUNC_UPPER_LIMIT) { y = getRandom(FUNC_LOWER_LIMIT, FUNC_UPPER_LIMIT); }
			if(y < FUNC_LOWER_LIMIT) { y = getRandom(FUNC_LOWER_LIMIT, FUNC_UPPER_LIMIT); }
			
			CHILD_POPULATION.push(
				{
					x_value: x,
					y_value: y,
					fitness: fitnessSum
				}
			);
		} else if(MUTATION_TYPE == "dynamic") {
			/* Normal Distribution (Gaussian) */
			/* For x and y values */
			var ePower = parseFloat((Math.pow((POPULATION[i].fitness - FITNESS_MEAN[FITNESS_MEAN.length-1]), 2))) / parseFloat((2 * Math.pow(VARIANCE[VARIANCE.length-1], 2)));
			var normalDistribution = parseFloat((1/Math.sqrt((2 * Math.PI * Math.pow(VARIANCE[VARIANCE.length-1], 2))))) * parseFloat(Math.pow(Math.E, ePower));
			console.log(normalDistribution);
		}
	}
}

/* Prepare the next generation, based on the selecion type (elitism/tournament) */
function nextGeneration() {
	log("==== Processing next generation ====");

	var population_all = POPULATION.concat(CHILD_POPULATION);
	population_all.sort(sortComparator);

	if(SELECTION_TYPE == "elitism") 
	{
		POPULATION = population_all.slice(0, POPULATION_SIZE); // Get the best individuals
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
	getFitnessMean();
	getXYMean();
	calcDeviation();
	calcVariance();

	/* fill the CHILD_POPULATION array */
	CHILD_POPULATION = [];
}


/* Calc the variance */
function calcVariance() {
	var squareSum = parseFloat(0);

	for (var i = 0; i < POPULATION_SIZE; i++) {
		squareSum = parseFloat(Math.pow(POPULATION[i].deviation, 2)) + parseFloat(squareSum);
	}
	VARIANCE.push(parseFloat(squareSum) / POPULATION_SIZE);
}


/* Calc the deviation of each individual (fitness - mean) */
function calcDeviation() {
	for(var i = 0; i < POPULATION_SIZE; i++) {
		POPULATION[i].deviation = parseFloat(POPULATION[i].fitness) - parseFloat(FITNESS_MEAN[FITNESS_MEAN.length-1]);
		POPULATION[i].x_deviation = parseFloat(POPULATION[i].x_value) - parseFloat(X_MEAN[X_MEAN.length-1]);
		POPULATION[i].y_deviation = parseFloat(POPULATION[i].y_value) - parseFloat(Y_MEAN[Y_MEAN.length-1]);	
	}
}

/* Calc the X and Y means */
function getXYMean() {
	var xsum = parseFloat(0);
	var ysum = parseFloat(0);
	for (var i = 0; i < POPULATION_SIZE; i++) {
		xsum = parseFloat(POPULATION[i].x_value) + parseFloat(xsum);
		ysum = parseFloat(POPULATION[i].x_value) + parseFloat(ysum);
	}
	X_MEAN.push(parseFloat(xsum / POPULATION_SIZE));
	Y_MEAN.push(parseFloat(ysum / POPULATION_SIZE));	
}


/* Calc the Fintess Mean of a generation */
function getFitnessMean() {
	fitnessSum = parseFloat(0);
	for (var i = 0; i < POPULATION_SIZE; i++) {
		fitnessSum = parseFloat(POPULATION[i].fitness) + parseFloat(fitnessSum);
	}
	FITNESS_MEAN.push(fitnessSum / POPULATION_SIZE);
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

	POPULATION    = []; // Reset, because the user can click start again
	BEST_EACH_GEN = []; // Reset, because the user can click start again
	FITNESS_MEAN  = []; // Reset, because the user can click start again
	VARIANCE      = []; // Reset, because the user can click start again
	X_MEAN        = []; // Reset, because the user can click start again
	Y_MEAN        = []; // Reset, because the user can click start again

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
		
		log("Population of generation " + i);
		log(POPULATION);
		mutate();
		log("Child Population")
		log(CHILD_POPULATION);
		nextGeneration();

	}
	/* Main workflow */

	document.getElementById("result").innerHTML = "The minimum of " + FUNCTIONS[FUNCTION_CHOOSED].name + " is " + POPULATION[0].fitness.toPrecision(3) + " with x = " + POPULATION[0].x_value.toPrecision(3) + " and y = " +POPULATION[0].y_value.toPrecision(3);
	chart = new Chartist.Line('.ct-chart', {labels: ['Generations'], series: [BEST_EACH_GEN]}, options);

	log(FITNESS_MEAN);
	log(VARIANCE);

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
	document.getElementById("mutateVariation").value = MUTATE_VARIATION;

	FUNCTION_CHOOSED = document.querySelector('input[name="func"]:checked').value;

	document.getElementById("min-func").innerHTML = "Interval [" + FUNCTIONS[FUNCTION_CHOOSED].min + ", " + FUNCTIONS[FUNCTION_CHOOSED].max + "]";
}

/* Get users values on GUI */
function getVariables() {
	GENERATIONS = document.getElementById("generations").value;
	POPULATION_SIZE = document.getElementById("populationSize").value;
	MUTATE_VARIATION = document.getElementById("mutateVariation").value;

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

/* 
 * References: https://www.sfu.ca/~ssurjano/booth.html 
 */
function booth(x, y) {
	return Math.pow((x + 2*y - 7), 2) + Math.pow((2*x + y -5), 2);
}

/* 
 * References: http://www.cs.unm.edu/~neal.holts/dga/benchmarkFunction/schafferf6.html 
 */
function schafferF6(x, y) {
	var part1 = Math.pow((Math.sin(Math.sqrt((Math.pow(x, 2)) + (Math.pow(y, 2))))), 2);
	var part2 = Math.pow((1.0 + 0.001 * (Math.pow(x, 2) + Math.pow(y, 2))), 2);
	return 0.5 + ((part1 - 0.5) / part2);
}

