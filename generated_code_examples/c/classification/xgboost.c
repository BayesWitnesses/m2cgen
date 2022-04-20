#include <string.h>
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
void score(double * input, double * output) {
    double var0[3];
    double var1;
    if (input[2] >= 2.45) {
        var1 = -0.21995015;
    } else {
        var1 = 0.4302439;
    }
    double var2;
    if (input[2] >= 2.45) {
        var2 = -0.19691855;
    } else {
        var2 = 0.29493433;
    }
    double var3;
    if (input[2] >= 2.45) {
        if (input[3] >= 1.75) {
            var3 = -0.20051816;
        } else {
            var3 = 0.36912444;
        }
    } else {
        var3 = -0.21512198;
    }
    double var4;
    if (input[2] >= 2.45) {
        if (input[2] >= 4.8500004) {
            var4 = -0.14888482;
        } else {
            var4 = 0.2796613;
        }
    } else {
        var4 = -0.19143805;
    }
    double var5;
    if (input[3] >= 1.6500001) {
        var5 = 0.40298507;
    } else {
        if (input[2] >= 4.95) {
            var5 = 0.21724138;
        } else {
            var5 = -0.21974029;
        }
    }
    double var6;
    if (input[2] >= 4.75) {
        if (input[3] >= 1.75) {
            var6 = 0.28692952;
        } else {
            var6 = 0.06272897;
        }
    } else {
        if (input[3] >= 1.55) {
            var6 = 0.009899145;
        } else {
            var6 = -0.19659369;
        }
    }
    softmax((double[]){0.5 + (var1 + var2), 0.5 + (var3 + var4), 0.5 + (var5 + var6)}, 3, var0);
    memcpy(output, var0, 3 * sizeof(double));
}
