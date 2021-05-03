List<double> softmax(List<double> x) {
    int size = x.length;
    List<double> result = new List<double>.filled(size, 0.0);
    double maxElem = x.reduce(max);
    double sum = 0.0;
    for (int i = 0; i < size; ++i) {
        result[i] = exp(x[i] - maxElem);
        sum += result[i];
    }
    for (int i = 0; i < size; ++i)
        result[i] /= sum;
    return result;
}
