#include <math.h>
void assign_array(double source[], double *target, int size) {
    for(int i = 0; i < size; ++i)
        target[i] = source[i];
}
void score(double * input, double * output) {
    double var0;
    if ((input[2]) <= (1.8)) {
        var0 = -0.9486122853153485;
    } else {
        if ((input[2]) <= (4.250000000000001)) {
            var0 = -1.1633850173886202;
        } else {
            var0 = -1.1736122903444903;
        }
    }
    double var1;
    if ((input[2]) <= (1.8)) {
        var1 = 0.12984943093573026;
    } else {
        if ((input[1]) <= (3.0500000000000003)) {
            var1 = -0.07237070828653688;
        } else {
            var1 = -0.06193194743580539;
        }
    }
    double var2;
    var2 = exp(((0) + (var0)) + (var1));
    double var3;
    if ((input[2]) <= (1.8)) {
        var3 = -1.1952609652674462;
    } else {
        if ((input[2]) <= (4.8500000000000005)) {
            var3 = -0.9831932134295853;
        } else {
            var3 = -1.1807342692411888;
        }
    }
    double var4;
    if ((input[2]) <= (1.8)) {
        var4 = -0.07151978915296087;
    } else {
        if ((input[2]) <= (4.8500000000000005)) {
            var4 = 0.11960489254350348;
        } else {
            var4 = -0.05694282927518771;
        }
    }
    double var5;
    var5 = exp(((0) + (var3)) + (var4));
    double var6;
    if ((input[2]) <= (4.8500000000000005)) {
        if ((input[2]) <= (4.250000000000001)) {
            var6 = -1.1524760761934856;
        } else {
            var6 = -1.1322413652523249;
        }
    } else {
        if ((input[3]) <= (1.9500000000000002)) {
            var6 = -0.9632815288936335;
        } else {
            var6 = -0.9298942558407184;
        }
    }
    double var7;
    if ((input[2]) <= (4.8500000000000005)) {
        if ((input[2]) <= (4.250000000000001)) {
            var7 = -0.07292857712854424;
        } else {
            var7 = -0.052710589717642864;
        }
    } else {
        if ((input[3]) <= (1.9500000000000002)) {
            var7 = 0.09898817876916756;
        } else {
            var7 = 0.12809276954555665;
        }
    }
    double var8;
    var8 = exp(((0) + (var6)) + (var7));
    double var9;
    var9 = ((var2) + (var5)) + (var8);
    assign_array((double[]){(var2) / (var9), (var5) / (var9), (var8) / (var9)}, output, 3);
}
