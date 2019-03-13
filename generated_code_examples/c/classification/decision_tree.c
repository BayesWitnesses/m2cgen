#include <string.h>
void score(double * input, double * output) {
    double var0[3];
    if ((input[2]) <= (2.6)) {
        memcpy(var0, (double[]){1.0, 0.0, 0.0}, 3 * sizeof(double));
    } else {
        if ((input[2]) <= (4.8500004)) {
            if ((input[3]) <= (1.6500001)) {
                memcpy(var0, (double[]){0.0, 1.0, 0.0}, 3 * sizeof(double));
            } else {
                memcpy(var0, (double[]){0.0, 0.3333333333333333, 0.6666666666666666}, 3 * sizeof(double));
            }
        } else {
            if ((input[3]) <= (1.75)) {
                memcpy(var0, (double[]){0.0, 0.42857142857142855, 0.5714285714285714}, 3 * sizeof(double));
            } else {
                memcpy(var0, (double[]){0.0, 0.0, 1.0}, 3 * sizeof(double));
            }
        }
    }
    memcpy(output, var0, 3 * sizeof(double));
}
