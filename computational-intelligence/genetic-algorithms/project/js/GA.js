var AG = angular.module('AG', []);

AG.controller('AGController', ['$scope', function($scope) {

	/* GA Parameters */
	$scope.generations          = 0;
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

		if(totalWeight > $scope.maxSizeBag) 
			chromosome['evaluateValue'] = 1/(totalWeight - $scope.maxSizeBag); // penalize here! exceeded^-1
		else
			chromosome['evaluateValue'] = totalValue;
		
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

		log("#### MUTATION #### Mutate the chromosome " + chromosome);
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

	
	$scope.start = function() {

		log($scope.populationSize);

		/* Flow of GA */ 
		$scope.createPopulation(); // The first population, create randomly
		$scope.evaluateAllChromosomes(); // The first evaluation
		$scope.tournament();
		$scope.crossover();
		

		log("Next generation has " + $scope.nextGenerationIndex + " chromosomes");
	}









	/* Aux functions */
	function log(info, textarea) {
		if (!!!textarea)
			console.log(info)
		else { // link the textarea here }
			
		}
	}

}]);


/*
	TO-DO:

	[ ] Crossover probability
	[ ] Mutate probability
	[ ] Fathers are all diying
	[ ] Select to choose the types of fathers selections (tournament, wheel, etc)

*/