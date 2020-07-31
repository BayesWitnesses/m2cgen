private static double Sigmoid(double x) {
    if (x < 0.0) {
        double z = Exp(x);
        return z / (1.0 + z);
    }
    return 1.0 / (1.0 + Exp(-x));
}
