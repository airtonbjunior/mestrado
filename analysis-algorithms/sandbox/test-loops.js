function nestedLoops2(n) {
	var counter = 0;

	for (var i = 0; i < n*n; ++i) {
		counter++;
		for (var j = 0; j < i*i; ++j) {
			counter++;
		}
	}

	return counter;
}

console.log(nestedLoops2(2));