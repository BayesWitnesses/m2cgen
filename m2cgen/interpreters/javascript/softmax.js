function softmax(x) {
    let size = x.length;
    let result = new Array(size);
    let max = x[0];
    for (let i = 1; i < size; ++i) {
        if (x[i] > max)
            max = x[i];
    }
    let sum = 0.0;
    for (let i = 0; i < size; ++i) {
        result[i] = Math.exp(x[i] - max);
        sum += result[i];
    }
    for (let i = 0; i < size; ++i)
        result[i] /= sum;
    return result;
}
