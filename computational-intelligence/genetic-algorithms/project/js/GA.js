var AG = angular.module('AG', []);

AG.controller('AGController', ['$scope', function($scope) {

	/* GA Parameters */
	$scope.generations          = 0;
	$scope.populationSize       = 20;
	$scope.mutationProability   = 0;
	$scope.crossoverProbability = 0;
	/* GA Parameters */


	/* Main Variables */
	$scope.population     = [];
	$scope.sizeChromosome = itens.length; // Size of itens list
	$scope.maxSizeBag = 100;
	/* Main Variables */





	/* Evaluate each chromosome by the evaluate function - based on maxSizeBag - I want maximize the value here, respecting the constraints*/
	$scope.evaluateFunction = function(chromosome) {
		
		var totalWeight = 0;
		var totalValue  = 0;

		for (var i = 0; i < chromosome.length; i++) {
			if(chromosome[i] === 1) {
				totalWeight += parseInt(itens[i].weight);  // change if I want a floor weight. I can use parselFloat();
				totalValue  += parseInt(itens[i].value);
			}
		}


		if(totalWeight > $scope.maxSizeBag) 
			chromosome['evaluateValue'] = 0; // penalize here!
		else
			chromosome['evaluateValue'] = totalValue;
		
	}





	/* Create the population randomly */
	$scope.createPopulation = function() {
		for (var i = 0; i < $scope.populationSize; i++) {
			
			$scope.population[i] = new Array();
			
			for (var j = 0; j < $scope.sizeChromosome; j++)
				$scope.population[i].push(Math.round(Math.random()));

		}
	}



	
	$scope.createPopulation();
	$scope.evaluateFunction($scope.population[0])


	log(itens);		
	log($scope.population);





	/* Aux functions */
	function log(info, textarea) {
		if (!!!textarea)
			console.log(info)
		else { // link the textarea here }
			
		}
	}

}]);