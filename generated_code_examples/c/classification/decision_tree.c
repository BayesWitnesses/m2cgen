#include <string.h>
void score(double * input, double * output) {
    double var0[3];
    if (input[2] <= 2.449999988079071) {
        memcpy(var0, (double[]){1.0, 0.0, 0.0}, 3 * sizeof(double));
    } else {
        if (input[3] <= 1.75) {
            if (input[2] <= 4.950000047683716) {
                if (input[3] <= 1.6500000357627869) {
                    memcpy(var0, (double[]){0.0, 1.0, 0.0}, 3 * sizeof(double));
                } else {
                    memcpy(var0, (double[]){0.0, 0.0, 1.0}, 3 * sizeof(double));
                }
            } else {
                memcpy(var0, (double[]){0.0, 0.3333333333333333, 0.6666666666666666}, 3 * sizeof(double));
            }
        } else {
            memcpy(var0, (double[]){0.0, 0.021739130434782608, 0.9782608695652174}, 3 * sizeof(double));
        }
    }
    memcpy(output, var0, 3 * sizeof(double));
}
