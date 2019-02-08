double score(double * input) {
    double var0;
    if ((input[5]) <= (6.941)) {
        if ((input[12]) <= (14.395)) {
            if ((input[7]) <= (1.43365)) {
                var0 = 45.58;
            } else {
                var0 = 22.865022421524642;
            }
        } else {
            var0 = 14.924358974358983;
        }
    } else {
        if ((input[5]) <= (7.4370003)) {
            var0 = 32.09534883720931;
        } else {
            var0 = 45.275;
        }
    }
    return var0;
}
