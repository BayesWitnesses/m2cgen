double tanh(double x) {
    // Implementation is taken from
    // https://github.com/golang/go/blob/master/src/math/tanh.go
    double z;
    z = x.abs();
    if (z > 0.440148459655565271479942397125e+2) {
        if (x < 0) {
            return -1.0;
        }
        return 1.0;
    }
    if (z >= 0.625) {
        z = 1 - 2 / (exp(2 * z) + 1);
        if (x < 0) {
            z = -z;
        }
        return z;
    }
    if (x == 0) {
        return 0.0;
    }
    double s;
    s = x * x;
    z = x + x * s
        * ((-0.964399179425052238628e+0 * s + -0.992877231001918586564e+2)
        * s + -0.161468768441708447952e+4) / (((s + 0.112811678491632931402e+3)
        * s + 0.223548839060100448583e+4) * s + 0.484406305325125486048e+4);
    return z;
}
