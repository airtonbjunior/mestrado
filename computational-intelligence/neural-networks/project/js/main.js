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
OUTPUT_LAYER = [];
INPUTS = 2;
OUTPUTS = 1;
ACTIVATION_FUNCTION = "default";
DECIMAL_PLACES = 9;

/* Reference structure of a perceptron */
PERCEPTRON = {
	inputs: [],
	weights: [],
	transfer_function_value: 0, 
	activation_function_value: 0
}

/* dataset of test */
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


// First line: Create a hidden layer (hardcoded 3 yet)
// Second line: Quantity of perceptrons of the last layer is the number of inputs of the last layer
create_layer(3, INPUTS, "hidden");
create_layer(OUTPUTS, HIDDEN_LAYER[HIDDEN_LAYER.length-1].length, "output"); 

console.log(HIDDEN_LAYER);
console.log(OUTPUT_LAYER);

training_network();

console.log(HIDDEN_LAYER);
console.log(OUTPUT_LAYER);


/* Train the network with the dataset of test */
function training_network () {
	/* hardcoded because I'm always using 1 hidden layer. Change this to do this dinamically (loop through HIDDEN_LAYER) */
	for (var i = 0; i < HIDDEN_LAYER[0].length; i++) {
		set_inputs(HIDDEN_LAYER[0][i], INPUT_TEST[0].input, "hidden");		

		/* Calc the transfer and activation function */
		HIDDEN_LAYER[0][i].transfer_function_value 	 = transfer_function(HIDDEN_LAYER[0][i]);
		HIDDEN_LAYER[0][i].activation_function_value = activation_function(HIDDEN_LAYER[0][i], ACTIVATION_FUNCTION);
	}	

	/* The outputs of the last hidden layer is the input of the output layer */
	for (var i = 0; i < OUTPUT_LAYER.length; i++) {
		set_inputs(OUTPUT_LAYER[i], null, "output");
		OUTPUT_LAYER[i].transfer_function_value = transfer_function(OUTPUT_LAYER[i]);
		OUTPUT_LAYER[i].activation_function_value = activation_function(OUTPUT_LAYER[i], ACTIVATION_FUNCTION);
	}


	// hardcoded on [0]
	var output_error = INPUT_TEST[0].output - get_output(OUTPUT_LAYER).activation_function_value;
	var delta_output_sum = (calc_sigmoid_derivative(get_output(OUTPUT_LAYER)) * (output_error)); 

	update_weights(delta_output_sum, "output");
	update_weights(delta_output_sum, "hidden");


	//console.log(INPUT_TEST[0].output + " - " + get_output(OUTPUT_LAYER).activation_function_value);
	//console.log("output_error " + output_error);
	//console.log(calc_sigmoid_derivative(get_output(OUTPUT_LAYER)) + " * " + output_error);
	//console.log("delta_output_sum " + delta_output_sum);

}


/* Update the weights */
function update_weights(delta_output_sum, layer_type) {
	var delta_weight = 0;
	if(layer_type === "output") {
		for (var i = 0; i < HIDDEN_LAYER[0].length; i++) {
			delta_weight = parseFloat(HIDDEN_LAYER[0][i].activation_function_value * delta_output_sum);
			
			console.log("delta weight " + delta_weight);
			console.log("previous value " + OUTPUT_LAYER[0].weights[i]);
			console.log("new value (delta + previous) " + parseFloat(OUTPUT_LAYER[0].weights[i] + delta_weight));
			
			OUTPUT_LAYER[0].weights[i] = OUTPUT_LAYER[0].weights[i] + delta_weight; // update the weights (harcoded)
		}
	}	
	else if (layer_type === "hidden") {
		
	}
}


/* Create a layer */
function create_layer(num_perceptrons, num_weights, type_layer) {
	var layer = [];
	var perceptron;

	for(var i = 0; i < num_perceptrons; i++) {
		
		perceptron = {
			inputs: [], 
			weights: [], 
			transfer_function_value: 0, 
			activation_function_value: 0
		}

		initialize_weights(perceptron, num_weights);
		layer.push(perceptron);

		perceptron = {};
	}

	if(type_layer === "hidden")
		HIDDEN_LAYER.push(layer);	
	else if(type_layer === "output")
		OUTPUT_LAYER = layer;	
}


/* Initialize the weights randomly [0,1] */
function initialize_weights(perceptron, quantity) {
	for(var i = 0; i < quantity; i++) {
		perceptron.weights[i] = parseFloat(Math.random().toFixed(2)); // Fixed 2 decimal places
	}
}


/* Set the input values to the perceptron */
function set_inputs(perceptron, inputs, type_layer) {
	if(type_layer === "hidden")
		perceptron.inputs = inputs;
	else if(type_layer === "output") {
		var last_hidden_layer = HIDDEN_LAYER[HIDDEN_LAYER.length-1];
		for (var i = 0; i < last_hidden_layer.length; i++) {
			perceptron.inputs[i] = last_hidden_layer[i].activation_function_value;
		}
	}
}


/* Function that return the output of the network */
function get_output(output_layer) {
	return output_layer[0]; // hardcoded now
}

/* Sum of inputs * weights */
function transfer_function(perceptron) {
	var sum = 0;
	for(var i = 0; i < perceptron.inputs.length; i++) {
		sum += perceptron.inputs[i] * perceptron.weights[i];
	}

	return sum.toFixed(DECIMAL_PLACES);
}


/* Calc the activation function */
function activation_function(perceptron, type_function) {
	if(type_function === "default") {
		return calc_sigmoid(perceptron).toFixed(DECIMAL_PLACES);
	}
}


/* Calc the sigmoid function */
function calc_sigmoid(perceptron) {
	return 1/(1+Math.pow(Math.E, -perceptron.transfer_function_value)); //verify
}


/* Calc the sigmoid derivative */
function calc_sigmoid_derivative(perceptron) {
	return calc_sigmoid(perceptron) * (1 - calc_sigmoid(perceptron)); // verify
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


/* References */
/*
	https://stevenmiller888.github.io/mind-how-to-build-a-neural-network/

*/