void softmax(double *x, int size, double *result) {
    double max = x[0];
    for (int i = 1; i < size; ++i) {
        if (x[i] > max)
            max = x[i];
    }
    double sum = 0.0;
    for (int i = 0; i < size; ++i) {
        result[i] = exp(x[i] - max);
        sum += result[i];
    }
    for (int i = 0; i < size; ++i)
        result[i] /= sum;
}
