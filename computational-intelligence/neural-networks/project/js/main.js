/*
Airton Bordin Junior
airtonbjunior@gmail.com

Artificial Neural Network

Computational Intelligence - Federal University of Goias (UFG)
UFG master's program 
*/

LEARN_RATE = 0;
ITERATIONS = 0;
HIDDEN_LAYERS = 1;
HIDDEN_LAYER = [];


PERCEPTRON = {
	inputs: [],
	weights: [],
	total: 0
}


INPUT_TEST = [
	{
		input: [0, 0], 
		output: 0
	}, 
	{
		input: [1, 1], 
		output: 0
	},
	{
		input: [0, 1], 
		output: 1
	},
	{
		input: [1, 0], 
		output: 1
	}	
]

ACTIVATION_FUNCTION = "default";


create_hidden_layer(3, 2);
console.log(HIDDEN_LAYER);


function create_hidden_layer(num_perceptrons, num_weights) {
	var layer = [];
	var perceptron;
	for(var i = 0; i < num_perceptrons; i++) {
		perceptron = new Object(PERCEPTRON)

		// Initialize the weights randomly [0,1]
		initialize_weights(perceptron, num_weights);
		layer.push(perceptron);
	}
	HIDDEN_LAYER.push(layer);	
}


/* Initialize the weights randomly */
function initialize_weights(perceptron, quantity) {
	for(var i = 0; i < quantity; i++) {
		perceptron.weights[i] = getRandom(0, 1);
	}
}


/* Sum of inputs * weights */
function transfer_function(perceptron) {
	var sum = 0;
	for(var i = 0; i < perceptron.inputs.length; i++) {
		sum += inputs[i] * weights[i];
	}

	return sum;
}


/* Process before call the main start */
function startPreparation() {

}


function start() {
	
}

function training() {

}



/* Aux functions */

/* Get a random between min and max */
function getRandom(min, max) {
	return Math.random()*(max-min+1)+min;
}

/* Soon will log on page */
function log(msg, input) {
	console.log(msg)
}
