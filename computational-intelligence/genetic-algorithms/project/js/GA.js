/* 
Airton Bordin Junior
airtonbjunior@gmail.com


Genetic Algorithms

Computational Intelligence - Federal University of Goias (UFG)
UFG master's program 
*/

var AG = angular.module('AG', []);

AG.controller('AGController', ['$scope', function($scope) {

	/* GA Parameters */
	$scope.generations          = 20;
	$scope.populationSize       = 20;
	$scope.mutationProability   = 3;
	$scope.crossoverProbability = 100;
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
	$scope.bestChromosomeValue = [];
		$scope.bestChromosomeValue['evaluateValue'] = -1000;
		$scope.bestChromosomeValue['weightValue']   = 0;

	$scope.itens = itens;

	//$scope.logInfo = [];
	$scope.startButtonLabel = "Start";
	/* Main Functions */

	/* Create the population randomly */
	$scope.createPopulation = function() {
		log("==== Creating population ====");
		for (var i = 0; i < $scope.populationSize; i++) {
			
			$scope.population[i] = new Array();
			
			for (var j = 0; j < $scope.sizeChromosome; j++)
				$scope.population[i].push(Math.round(Math.random()));

		}
		log("Population created. Size: " + $scope.populationSize);
	}



	/* Evaluate each chromosome by the evaluate function - based on maxSizeBag - I want maximize the value here, respecting the constraints*/
	$scope.evaluateFunction = function(index) {
		var totalWeight = 0;
		var totalValue  = 0;

		for (var i = 0; i < $scope.population[index].length; i++) {
			if($scope.population[index][i] === 1) {
				totalWeight += parseInt(itens[i].weight);  // change if I want a floor weight. I can use parselFloat();
				totalValue  += parseInt(itens[i].value);
			}
		}

		if(totalWeight > parseInt($scope.maxSizeBag)) {
			$scope.population[index]['evaluateValue'] = parseFloat(1/(totalWeight - $scope.maxSizeBag)); // penalize here! exceeded^-1
			$scope.population[index]['weightValue']   = 0;	
		}
		else {
			$scope.population[index]['evaluateValue'] = totalValue;
			$scope.population[index]['weightValue']   = totalWeight;
		}
		
		if($scope.population[index]['evaluateValue'] > $scope.bestChromosomeValue['evaluateValue']) {
			$scope.bestChromosomeValue 	= $scope.population[index].slice();
			$scope.bestChromosomeValue['evaluateValue'] = $scope.population[index]['evaluateValue'];
			$scope.bestChromosomeValue['weightValue']   = $scope.population[index]['weightValue'];
		}

		log("Chromosome " + $scope.population[index] + " has a value of " + $scope.population[index]['evaluateValue']);
	}



	/* Evaluate All Chromosomes */
	$scope.evaluateAllChromosomes = function() {
		log("==== Start Evaluation Function ====");
		for (var i = 0; i < $scope.populationSize; i++) {
			$scope.evaluateFunction(i);
		}
		bestValueChromosome = $scope.getBestChromosomeValue();
	}


	/* Tournament - Choose the fathers */ 
	$scope.tournament = function() {
		log("==== Start tournament ====");

		var chromosome1, chromosome2;

		var i = 0; // outside for because I'll put a verification here in the future!
		for (i; i < $scope.populationSize/2; i++) { // half the population to crossover
			
			chromosome1 = $scope.population[Math.floor(Math.random() * $scope.populationSize)]; // choose randomly
			chromosome2 = $scope.population[Math.floor(Math.random() * $scope.populationSize)]; // choose randomly

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
		log("==== Start Crossover ====");

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
		

		var child1 = []
		var child2 = [];
		

		if(Math.random() > ($scope.crossoverProbability / 100)) // Crossover probability
		{ 
			log("The crossover didn't occurs");
			child1 = chromosome1;
			child2 = chromosome2;
		}
		else 
		{
			log("Starting crossover with [" + chromosome1 + "] and [" + chromosome2 + "] using the crosspoint " + crossPoint);
			for (var i = 0; i < crossPoint; i++) {
				child1.push(chromosome1[i]);
				child2.push(chromosome2[i]);
			}
			for (var i = crossPoint; i <= $scope.sizeChromosome; i++) {
				child2.push(chromosome1[i]);
				child1.push(chromosome2[i]);
			}

			log("Crossover generate the childs [" + child1 + "] and [" + child2 + "]");
		}

		if(Math.random() < ($scope.mutationProability / 100))  // Mutation probability
			child1 = $scope.mutate(child1);

		$scope.nextGeneration[$scope.nextGenerationIndex] = new Array();
		$scope.nextGeneration[$scope.nextGenerationIndex] = child1;

		$scope.nextGenerationIndex++;

		// Two times to be more didact
		if(Math.random() < ($scope.mutationProability / 100))  // Mutation probability
			child2 = $scope.mutate(child2);

		$scope.nextGeneration[$scope.nextGenerationIndex] = new Array();
		$scope.nextGeneration[$scope.nextGenerationIndex] = child2;

		$scope.nextGenerationIndex++; // Restart this in some place - I don't know the best place to do that yet
	}


	/* Mutate a chromosome - random position */
	$scope.mutate = function(chromosome) {
		log("==== Start Mutate Function ====");
		// do mutate
		// one bit
		log("Mutate the chromosome [" + chromosome + "]");
		var mutationPosition = Math.floor(Math.random() * $scope.sizeChromosome);
		// didact way (I can use NOT here)
		if (chromosome[mutationPosition] == 0) {
			chromosome[mutationPosition] = 1
		} else {
			chromosome[mutationPosition] = 0
		}

		log("Chromosome mutated on position " + mutationPosition + ". The result is [" + chromosome + "]");
		return chromosome;
	}

	/* Get the best chromosome of the actual generation */
	$scope.getBestChromosomeValue = function() {
		var bestValue = 0;
		for(var i = 0; i < $scope.populationSize; i++) {
			if ($scope.population[i]['evaluateValue'] > bestValue) {
				bestValue = i;
			}
		}
		return bestValue;
	}

	/* Some configs before call "official" start */
	$scope.startGA = function() {
		document.getElementById("loading-icon").classList.remove("hide-load");
		//$scope.startButtonLabel = "Processing...";
		document.getElementById("loading-icon").className += " fa fa-cog fa-spin fa-5x fa-fw";
		
		setTimeout($scope.start, 50); // JS don't write on DOM before function start finish, so I call a little timeout here.
	}


	$scope.start = function() {
		
		/* Flow of GA */ 
		$scope.createPopulation(); // The first population, create randomly
		$scope.bestValuesHistory = []; // Clean the history. Here, the user clicks again on start button, so we don't need store the history of other turns
		$scope.cleanClasses();

		
		for (var i = 1; i <= $scope.generations; i++) {
			log("################ Starting generation " + i + " ################");
			
			if (i > 1) 
				$scope.population = $scope.nextGeneration.slice(); // Copy the next generation for the population array
			
			$scope.nextGenerationIndex = 0;	
			
			/* Main cycle */
			$scope.evaluateAllChromosomes();
			$scope.tournament();
			$scope.crossover(); // mutation occurs inside the crossover


			if($scope.elitism) {
				log("Elitism activated");
				//$scope.nextGeneration[0] = $scope.population[bestValueChromosome]; // Replace the first index (anyone can be replaced here)
				$scope.nextGeneration[0] = $scope.bestChromosomeValue;
				log("Chromosome [" + $scope.bestChromosomeValue + "] with weight " + $scope.bestChromosomeValue['weightValue'] + " and value " + $scope.bestChromosomeValue['evaluateValue'] + " goes to next generation by elitism");
			}

			log("Next generation has " + $scope.nextGenerationIndex + " chromosomes");
			$scope.bestValuesHistory.push($scope.bestChromosomeValue['evaluateValue']);
			log("The best value of generation " + i + " is " + $scope.bestChromosomeValue['evaluateValue']);	

			$scope.bestChromosomeValue['evaluateValue'] = -1000;		
		}
		
		setTimeout(function(){
			document.getElementById("loading-icon").className += " hide-load";
			chart = new Chartist.Line('.ct-chart', {labels: ['Generations'], series: [$scope.bestValuesHistory]}, options);
			$scope.paintChoosedItens();
			//alert("The best chromosome is " + $scope.bestChromosomeValue);

		}, 1000);

		//bestValueChromosome = $scope.getBestChromosomeValue();
		log("The best chromosome is [" + $scope.population[bestValueChromosome] + "] with the value " + $scope.population[bestValueChromosome]['evaluateValue'] + " and weight " + $scope.population[bestValueChromosome]['weightValue']);
	}



	$scope.cleanLoading = function () {
		log("CALLBACK FUNCTION!!!!!!");
		$scope.startButtonLabel = "Start";
		//document.getElementById("loading-icon").classList.remove("fa fa-refresh fa-spin fa-3x fa-fw");	
	}

	/* Aux functions */
	function log(info, textarea) {
		if (!!!textarea) {
			//$scope.logInfo.push(info);
			console.log(info);
		}
		else { // link the textarea here }
			
		}
	}

	/* Graph config options */
	var options = {
	  showPoint: false,
	  lineSmooth: true,
	  axisX: {
	    showGrid: false,
	    showLabel: true,
	  },
	  showArea: true
	};

	/* Set the chossed itens with "selected" class */
	$scope.paintChoosedItens = function() { 
		for (var i = 0; i < $scope.sizeChromosome; i++) {
			if($scope.population[$scope.getBestChromosomeValue()][i] == 1)
				document.getElementById($scope.itens[i].name).className += " selected";
		}
		$scope.startButtonLabel = "Start";

		setTimeout(function() {
			document.getElementById('result').innerHTML = "The best chromosome is [" + $scope.population[bestValueChromosome] + "] with the value " + $scope.population[bestValueChromosome]['evaluateValue'] + " and weight " + $scope.population[bestValueChromosome]['weightValue'];
		}, 50);
	}

	/* Clean the "selected" classes */
	$scope.cleanClasses = function() {
		for (var i = 0; i < $scope.sizeChromosome; i++) {
			document.getElementById($scope.itens[i].name).classList.remove("selected");
		}
	}


}]);


/*
	TO-DO:
	[ ] Select to choose the types of fathers selections (tournament, wheel, etc)

*/