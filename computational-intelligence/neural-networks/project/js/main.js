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
HIDDEN_LAYER = []; // if necessary have more than one layer, the HIDDEN_LAYER is an array
INPUTS = 2;
OUTPUTS = 1;

PERCEPTRON = {
	inputs: [],
	weights: [],
	transfer_function_value: 0
}


INPUT_TEST = [
	{
		input: [1, 1], 
		output: 0
	}, 
	{
		input: [0, 0], 
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


create_hidden_layer(3, INPUTS);
training_network();
console.log(HIDDEN_LAYER);


function training_network () {
	/* hardcoded because I'm always using 1 hidden layer. Change this to do this dinamically (loop through HIDDEN_LAYER) */
	for (var i = 0; i < HIDDEN_LAYER[0].length; i++) {
		set_inputs(HIDDEN_LAYER[0][i], INPUT_TEST[0].input);

		/* Calc the transfer function */
		HIDDEN_LAYER[0][i].transfer_function_value = transfer_function(HIDDEN_LAYER[0][i]);
	}	
}


/* Create a hidden layer */
function create_hidden_layer(num_perceptrons, num_weights) {
	var layer = [];
	var perceptron;

	for(var i = 0; i < num_perceptrons; i++) {
		
		perceptron = {
			inputs: [], 
			weights: [], 
			transfer_function_value: 0
		}

		initialize_weights(perceptron, num_weights);
		layer.push(perceptron);

		perceptron = {};
	}
	HIDDEN_LAYER.push(layer);	
}


/* Initialize the weights randomly [0,1] */
function initialize_weights(perceptron, quantity) {
	for(var i = 0; i < quantity; i++) {
		perceptron.weights[i] = getRandom(0, 1);
	}
}


/* Set the input values to the perceptron */
function set_inputs(perceptron, inputs) {
	perceptron.inputs = inputs;
}


/* Sum of inputs * weights */
function transfer_function(perceptron) {
	var sum = 0;
	for(var i = 0; i < perceptron.inputs.length; i++) {
		sum += perceptron.inputs[i] * perceptron.weights[i];
	}

	return sum;
}


/* Process before call the main start */
function startPreparation() {

}


function start() {
	
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
