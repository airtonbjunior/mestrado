var AG = angular.module('AG', []);

AG.controller('AGController', ['$scope', function($scope) {

	/* GA Parameters */
	$scope.generations          = 5;
	$scope.populationSize       = 20;
	$scope.mutationProability   = 0.3;
	$scope.crossoverProbability = 0;
	$scope.elitism 				= false;
	/* GA Parameters */


	/* Main Variables */
	$scope.population     = [];
	$scope.sizeChromosome = itens.length; // Size of itens list
	$scope.maxSizeBag = 100;
	/* Main Variables */

	$scope.winnersGeneration   = [];
	$scope.nextGeneration      = [];
	$scope.nextGenerationIndex = 0;
	$scope.bestValuesHistory   = [];

	$scope.itens = itens;

	/* Main Functions */

	/* Create the population randomly */
	$scope.createPopulation = function() {
		log("Creating population");
		for (var i = 0; i < $scope.populationSize; i++) {
			
			$scope.population[i] = new Array();
			
			for (var j = 0; j < $scope.sizeChromosome; j++)
				$scope.population[i].push(Math.round(Math.random()));

		}
		log("Population created. Size: " + $scope.populationSize);
	}



	/* Evaluate each chromosome by the evaluate function - based on maxSizeBag - I want maximize the value here, respecting the constraints*/
	$scope.evaluateFunction = function(chromosome) {
		log("Evaluate the chromosome " + chromosome);

		var totalWeight = 0;
		var totalValue  = 0;

		for (var i = 0; i < chromosome.length; i++) {
			if(chromosome[i] === 1) {
				totalWeight += parseInt(itens[i].weight);  // change if I want a floor weight. I can use parselFloat();
				totalValue  += parseInt(itens[i].value);
			}
		}

		if(totalWeight > parseInt($scope.maxSizeBag)) {
			chromosome['evaluateValue'] = parseFloat(1/(totalWeight - $scope.maxSizeBag)); // penalize here! exceeded^-1
			chromosome['weightValue']   = 0;	
		}
		else {
			chromosome['evaluateValue'] = totalValue;
			chromosome['weightValue']   = totalWeight;
		}
		
		log("The evaluate value of chromosome " + chromosome + " is " + chromosome['evaluateValue']);
	}



	/* Evaluate All Chromosomes */
	$scope.evaluateAllChromosomes = function() {
		for (var i = 0; i < $scope.populationSize; i++) {
			$scope.evaluateFunction($scope.population[i]);
		}
	}


	/* Tournament - Choose the fathers */ 
	$scope.tournament = function() {
		log("Starting tournament");

		var chromosome1, chromosome2;

		for (var i = 0; i < $scope.populationSize/2; i++) { // half the population to crossover
			
			chromosome1 = $scope.population[Math.floor(Math.random() * $scope.populationSize)]; // choose randomly
			chromosome2 = $scope.population[Math.floor(Math.random() * $scope.populationSize)]; // choose randomly

			log("the choosed chromosome are [" + chromosome1 + "] and [" + chromosome2 + "]")

			if(chromosome1['evaluateValue'] >= chromosome2['evaluateValue']) { // greater and equal. In this case, doesn't matter
				log("Chromosome 1 wins - score: Chromosome 1 [" + chromosome1['evaluateValue'] + "] X [" + chromosome2['evaluateValue'] + "] Chromossome 2");
				$scope.winnersGeneration.push(chromosome1);
			}
			else {
				log("Chromosome 2 wins - score: Chromosome 1 [" + chromosome1['evaluateValue'] + "] X [" + chromosome2['evaluateValue'] + "] Chromossome 2");
				$scope.winnersGeneration.push(chromosome2);
			}
		}

		log("Choosed " + $scope.winnersGeneration.length + " winners chromosomes on tournament");
	}


	$scope.crossover = function() {
		var crossPoint = 0;
		var chromosome1, chromosome2; 

		for (var i = 0; i < $scope.winnersGeneration.length; i++) {
			chromosome1 = $scope.winnersGeneration[Math.floor(Math.random() * $scope.winnersGeneration.length)];
			chromosome2 = $scope.winnersGeneration[Math.floor(Math.random() * $scope.winnersGeneration.length)];

			crossPoint = Math.floor(Math.random() * $scope.sizeChromosome + 1);

			$scope.doCrossover(chromosome1, chromosome2, crossPoint);
		}

		$scope.winnersGeneration = []; // Kill all fathers! ¬¬
	}


	/* Crossover in fact */
	$scope.doCrossover = function (chromosome1, chromosome2, crossPoint) {
		log("Starting crossover with " + chromosome1 + " and " + chromosome2 + " using the crosspoint " + crossPoint);

		var child1 = []
		var child2 = [];
		
		for (var i = 0; i < crossPoint; i++) {
			child1.push(chromosome1[i]);
			child2.push(chromosome2[i]);
		}
		for (var i = crossPoint; i <= $scope.sizeChromosome; i++) {
			child2.push(chromosome1[i]);
			child1.push(chromosome2[i]);
		}

		log("Crossover generate the childs " + child1 + " and " + child2);

		if(Math.random() < $scope.mutationProability)  // Mutation probability
			child1 = $scope.mutate(child1);

		$scope.nextGeneration[$scope.nextGenerationIndex] = new Array();
		$scope.nextGeneration[$scope.nextGenerationIndex] = child1;

		$scope.nextGenerationIndex++;


		// Two times to be more didact
		if(Math.random() < $scope.mutationProability)  // Mutation probability
			child2 = $scope.mutate(child2);

		$scope.nextGeneration[$scope.nextGenerationIndex] = new Array();
		$scope.nextGeneration[$scope.nextGenerationIndex] = child2;

		$scope.nextGenerationIndex++; // Restart this in some place - I don't know the best place to do that yet

		log("Crossover finished");
	}


	/* Mutate a chromosome - random position */
	$scope.mutate = function(chromosome) {
		// do mutate
		// one bit

		log("=== MUTATION === Mutate the chromosome " + chromosome);
		var mutationPosition = Math.floor(Math.random() * $scope.sizeChromosome);
		// didact way
		if (chromosome[mutationPosition] == 0) {
			chromosome[mutationPosition] = 1
		} else {
			chromosome[mutationPosition] = 0
		}

		return chromosome;

		log("chromosome mutated on position " + mutationPosition + ". The result is " + chromosome);
	}

	$scope.getBestChromosomeValue = function() {
		var bestValue = 0;
		for(var i = 0; i < $scope.populationSize; i++) {
			if ($scope.population[i]['evaluateValue'] > bestValue) {
				bestValue = i;
			}
		}
		return bestValue;
	}

	
	$scope.start = function() {

		/* Flow of GA */ 
		$scope.createPopulation(); // The first population, create randomly
		$scope.cleanClasses();
		
		for (var i = 1; i <= $scope.generations; i++) {
			log("################ Starting generation " + i + " ################");
			
			if (i > 1) $scope.population = $scope.nextGeneration.slice();
			
			$scope.nextGenerationIndex = 0;
			$scope.evaluateAllChromosomes(); // The first evaluation
			$scope.tournament();
			$scope.crossover(); // mutate occurs inside the crossover

			log("Next generation has " + $scope.nextGenerationIndex + " chromosomes");
			$scope.bestValuesHistory.push($scope.population[$scope.getBestChromosomeValue()]['evaluateValue']);
			log("The best value of generation " + i + " is " + $scope.bestValuesHistory[$scope.bestValuesHistory.length-1]);
			
			
		}

		var bestValueChromosome = $scope.getBestChromosomeValue();
		chart = new Chartist.Line('.ct-chart', bestChromosomeValuesHistory);
		
		log("The best chromosome is " + $scope.population[$scope.getBestChromosomeValue()] + " with the value " + $scope.population[$scope.getBestChromosomeValue()]['evaluateValue'] + " and weight " + $scope.population[$scope.getBestChromosomeValue()]['weightValue']);
		

		for (var i = 0; i < $scope.sizeChromosome; i++) {
			if($scope.population[$scope.getBestChromosomeValue()][i] == 1)
				document.getElementById($scope.itens[i].name).className += " selected";
		}
	}


	/* Clean the "selected" classes */
	$scope.cleanClasses = function() {
		for (var i = 0; i < $scope.sizeChromosome; i++) {
			document.getElementById($scope.itens[i].name).classList.remove("selected");
		}
	}



	/* Aux functions */
	function log(info, textarea) {
		if (!!!textarea)
			console.log(info)
		else { // link the textarea here }
			
		}
	}




	var bestChromosomeValuesHistory = {
	  // A labels array that can contain any sort of values
	  labels: ['Generations'],
	  // Our series array that contains series objects or in this case series data arrays
	  series: [
	    $scope.bestValuesHistory
	  ]
	};

	chart = new Chartist.Line('.ct-chart', bestChromosomeValuesHistory);


}]);


/*
	TO-DO:

	[ ] Update the graph each generation
	[ ] Best of each generation to show on screen the evolution
	[ ] Crossover probability
	[ ] Fathers are all diying
	[ ] Select to choose the types of fathers selections (tournament, wheel, etc)
	[ ] Population odd (when pop/2 on crossover)
	[ ] I'm always doing the crossover. If I don'd do, I need to reply the fathers to the next generation?

*/