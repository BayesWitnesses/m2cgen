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
    if ((input[3]) <= (0.8)) {
        memcpy(var2, (double[]){1.0, 0.0, 0.0}, 3 * sizeof(double));
    } else {
        if ((input[2]) <= (4.8500004)) {
            memcpy(var2, (double[]){0.0, 0.9622641509433962, 0.03773584905660377}, 3 * sizeof(double));
        } else {
            if ((input[3]) <= (1.75)) {
                if ((input[3]) <= (1.6500001)) {
                    memcpy(var2, (double[]){0.0, 0.25, 0.75}, 3 * sizeof(double));
                } else {
                    memcpy(var2, (double[]){0.0, 1.0, 0.0}, 3 * sizeof(double));
                }
            } else {
                memcpy(var2, (double[]){0.0, 0.0, 1.0}, 3 * sizeof(double));
            }
        }
    }
    mul_vector_number(var2, 0.5, 3, var1);
    double var3[3];
    double var4[3];
    if ((input[3]) <= (0.8)) {
        memcpy(var4, (double[]){1.0, 0.0, 0.0}, 3 * sizeof(double));
    } else {
        if ((input[0]) <= (6.1499996)) {
            if ((input[2]) <= (4.8500004)) {
                memcpy(var4, (double[]){0.0, 0.9090909090909091, 0.09090909090909091}, 3 * sizeof(double));
            } else {
                memcpy(var4, (double[]){0.0, 0.0, 1.0}, 3 * sizeof(double));
            }
        } else {
            if ((input[3]) <= (1.75)) {
                memcpy(var4, (double[]){0.0, 0.8666666666666667, 0.13333333333333333}, 3 * sizeof(double));
            } else {
                memcpy(var4, (double[]){0.0, 0.0, 1.0}, 3 * sizeof(double));
            }
        }
    }
    mul_vector_number(var4, 0.5, 3, var3);
    add_vectors(var1, var3, 3, var0);
    memcpy(output, var0, 3 * sizeof(double));
}
