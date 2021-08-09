function softmax(x) {
    var size = x.length;
    var result = new Array(size);
    var max = x[0];
    for (var i = 1; i < size; ++i) {
        if (x[i] > max)
            max = x[i];
    }
    var sum = 0.0;
    for (var i = 0; i < size; ++i) {
        result[i] = Math.exp(x[i] - max);
        sum += result[i];
    }
    for (var i = 0; i < size; ++i)
        result[i] /= sum;
    return result;
}
