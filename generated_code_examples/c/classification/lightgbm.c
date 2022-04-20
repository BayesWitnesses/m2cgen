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
    if (input[2] > 3.1500000000000004) {
        var1 = -1.1986122886681099;
    } else {
        if (input[1] > 3.35) {
            var1 = -0.8986122886681098;
        } else {
            var1 = -0.9136122886681098;
        }
    }
    double var2;
    if (input[2] > 3.1500000000000004) {
        if (input[2] > 4.450000000000001) {
            var2 = -0.09503010837903424;
        } else {
            var2 = -0.09563272415214283;
        }
    } else {
        if (input[1] > 3.35) {
            var2 = 0.16640323607832397;
        } else {
            var2 = 0.15374604217339707;
        }
    }
    double var3;
    if (input[2] > 1.8) {
        if (input[3] > 1.6500000000000001) {
            var3 = -1.2055899476674514;
        } else {
            var3 = -0.9500445227622534;
        }
    } else {
        var3 = -1.2182214705715104;
    }
    double var4;
    if (input[3] > 0.45000000000000007) {
        if (input[3] > 1.6500000000000001) {
            var4 = -0.08146437273923739;
        } else {
            var4 = 0.14244886188108738;
        }
    } else {
        if (input[2] > 1.4500000000000002) {
            var4 = -0.0950888159264695;
        } else {
            var4 = -0.09438233722389686;
        }
    }
    double var5;
    if (input[3] > 1.6500000000000001) {
        if (input[2] > 5.3500000000000005) {
            var5 = -0.8824095771015287;
        } else {
            var5 = -0.9121126703829481;
        }
    } else {
        if (input[2] > 4.450000000000001) {
            var5 = -1.1277829563828181;
        } else {
            var5 = -1.1794405099157212;
        }
    }
    double var6;
    if (input[2] > 4.750000000000001) {
        if (input[2] > 5.150000000000001) {
            var6 = 0.16625543464258166;
        } else {
            var6 = 0.09608601737074281;
        }
    } else {
        if (input[0] > 4.950000000000001) {
            var6 = -0.09644547407948921;
        } else {
            var6 = -0.08181864271444342;
        }
    }
    softmax((double[]){var1 + var2, var3 + var4, var5 + var6}, 3, var0);
    memcpy(output, var0, 3 * sizeof(double));
}
