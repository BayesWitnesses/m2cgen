private static double[] Softmax(double[] x) {
    int size = x.Length;
    double[] result = new double[size];
    double max = x[0];
    for (int i = 1; i < size; ++i) {
        if (x[i] > max)
            max = x[i];
    }
    double sum = 0.0;
    for (int i = 0; i < size; ++i) {
        result[i] = Exp(x[i] - max);
        sum += result[i];
    }
    for (int i = 0; i < size; ++i)
        result[i] /= sum;
    return result;
}
