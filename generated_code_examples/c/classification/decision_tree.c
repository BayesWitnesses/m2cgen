void assign_array(double source[], double *target, int size) {
    for(int i = 0; i < size; ++i)
        target[i] = source[i];
}
void score(double * input, double * output) {
    double var0[3];
    if ((input[2]) <= (2.6)) {
        assign_array((double[]){1.0, 0.0, 0.0}, var0, 3);
    } else {
        if ((input[2]) <= (4.8500004)) {
            if ((input[3]) <= (1.6500001)) {
                assign_array((double[]){0.0, 1.0, 0.0}, var0, 3);
            } else {
                assign_array((double[]){0.0, 0.3333333333333333, 0.6666666666666666}, var0, 3);
            }
        } else {
            if ((input[3]) <= (1.75)) {
                assign_array((double[]){0.0, 0.42857142857142855, 0.5714285714285714}, var0, 3);
            } else {
                assign_array((double[]){0.0, 0.0, 1.0}, var0, 3);
            }
        }
    }
    assign_array(var0, output, 3);
}
