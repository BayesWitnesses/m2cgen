private static double sigmoid(double x) {
    if (x < 0.0) {
        double z = Math.exp(x);
        return z / (1.0 + z);
    }
    return 1.0 / (1.0 + Math.exp(-x));
}
