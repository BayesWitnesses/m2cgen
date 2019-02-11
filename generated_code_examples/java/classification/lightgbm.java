public class Model {

    public static double[] score(double[] input) {
        double var0;
        var0 = Math.exp(subroutine0(input));
        double var1;
        var1 = Math.exp(subroutine1(input));
        double var2;
        var2 = Math.exp(subroutine2(input));
        double var3;
        var3 = ((var0) + (var1)) + (var2);
        return new double[] {(var0) / (var3), (var1) / (var3), (var2) / (var3)};
    }
    public static double subroutine0(double[] input) {
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
        return ((0) + (var0)) + (var1);
    }
    public static double subroutine1(double[] input) {
        double var0;
        if ((input[2]) <= (1.8)) {
            var0 = -1.1952609652674462;
        } else {
            if ((input[2]) <= (4.8500000000000005)) {
                var0 = -0.9831932134295853;
            } else {
                var0 = -1.1807342692411888;
            }
        }
        double var1;
        if ((input[2]) <= (1.8)) {
            var1 = -0.07151978915296087;
        } else {
            if ((input[2]) <= (4.8500000000000005)) {
                var1 = 0.11960489254350348;
            } else {
                var1 = -0.05694282927518771;
            }
        }
        return ((0) + (var0)) + (var1);
    }
    public static double subroutine2(double[] input) {
        double var0;
        if ((input[2]) <= (4.8500000000000005)) {
            if ((input[2]) <= (4.250000000000001)) {
                var0 = -1.1524760761934856;
            } else {
                var0 = -1.1322413652523249;
            }
        } else {
            if ((input[3]) <= (1.9500000000000002)) {
                var0 = -0.9632815288936335;
            } else {
                var0 = -0.9298942558407184;
            }
        }
        double var1;
        if ((input[2]) <= (4.8500000000000005)) {
            if ((input[2]) <= (4.250000000000001)) {
                var1 = -0.07292857712854424;
            } else {
                var1 = -0.052710589717642864;
            }
        } else {
            if ((input[3]) <= (1.9500000000000002)) {
                var1 = 0.09898817876916756;
            } else {
                var1 = 0.12809276954555665;
            }
        }
        return ((0) + (var0)) + (var1);
    }
}
