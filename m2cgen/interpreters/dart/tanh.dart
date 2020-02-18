double tanh(double x) {
    if (x > 22.0)
        return 1.0;
    if (x < -22.0)
        return -1.0;
    return ((exp(2*x) - 1)/(exp(2*x) + 1));
}
