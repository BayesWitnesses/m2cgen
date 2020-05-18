double tanh(double x) {
    // Implementation is taken from
    // https://github.com/golang/go/blob/master/src/math/tanh.go
    double z;
    z = x.abs();
    if (z > 44.0148459655565271479942397125) {
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
        * ((-0.964399179425052238628 * s + -99.2877231001918586564) * s + -1614.68768441708447952)
        / (((s + 112.811678491632931402) * s + 2235.48839060100448583) * s + 4844.06305325125486048);
    return z;
}
