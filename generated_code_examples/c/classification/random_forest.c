#include <string.h>
void add_vectors(double *v1, double *v2, int size, double *result) {
    for(int i = 0; i < size; ++i)
        result[i] = v1[i] + v2[i];
}
void mul_vector_number(double *v1, double num, int size, double *result) {
    for(int i = 0; i < size; ++i)
        result[i] = v1[i] * num;
}
void score(double * input, double * output) {
    double var0[3];
    double var1[3];
    double var2[3];
    if (input[3] <= 0.75) {
        memcpy(var2, (double[]){1.0, 0.0, 0.0}, 3 * sizeof(double));
    } else {
        if (input[2] <= 4.75) {
            memcpy(var2, (double[]){0.0, 1.0, 0.0}, 3 * sizeof(double));
        } else {
            if (input[2] <= 5.049999952316284) {
                if (input[3] <= 1.75) {
                    memcpy(var2, (double[]){0.0, 0.8333333333333334, 0.16666666666666666}, 3 * sizeof(double));
                } else {
                    memcpy(var2, (double[]){0.0, 0.08333333333333333, 0.9166666666666666}, 3 * sizeof(double));
                }
            } else {
                memcpy(var2, (double[]){0.0, 0.0, 1.0}, 3 * sizeof(double));
            }
        }
    }
    double var3[3];
    if (input[3] <= 0.800000011920929) {
        memcpy(var3, (double[]){1.0, 0.0, 0.0}, 3 * sizeof(double));
    } else {
        if (input[0] <= 6.25) {
            if (input[2] <= 4.8500001430511475) {
                memcpy(var3, (double[]){0.0, 0.9487179487179487, 0.05128205128205128}, 3 * sizeof(double));
            } else {
                memcpy(var3, (double[]){0.0, 0.0, 1.0}, 3 * sizeof(double));
            }
        } else {
            if (input[3] <= 1.550000011920929) {
                memcpy(var3, (double[]){0.0, 0.8333333333333334, 0.16666666666666666}, 3 * sizeof(double));
            } else {
                memcpy(var3, (double[]){0.0, 0.02564102564102564, 0.9743589743589743}, 3 * sizeof(double));
            }
        }
    }
    add_vectors(var2, var3, 3, var1);
    mul_vector_number(var1, 0.5, 3, var0);
    memcpy(output, var0, 3 * sizeof(double));
}
