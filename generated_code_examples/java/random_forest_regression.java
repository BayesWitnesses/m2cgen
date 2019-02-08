public class Model {

    public static double score(double[] input) {
        return ((subroutine0(input)) * (0.5)) + ((subroutine1(input)) * (0.5));
    }
    public static double subroutine0(double[] input) {
        double var0;
        if ((input[5]) <= (6.92)) {
            if ((input[12]) <= (14.3)) {
                if ((input[7]) <= (1.47415)) {
                    var0 = 50.0;
                } else {
                    var0 = 23.203669724770638;
                }
            } else {
                var0 = 15.177333333333326;
            }
        } else {
            if ((input[5]) <= (7.4370003)) {
                var0 = 32.92407407407408;
            } else {
                var0 = 45.04827586206897;
            }
        }
        return var0;
    }
    public static double subroutine1(double[] input) {
        double var0;
        if ((input[12]) <= (9.725)) {
            if ((input[5]) <= (7.4525)) {
                if ((input[5]) <= (6.7539997)) {
                    var0 = 24.805;
                } else {
                    var0 = 32.55238095238095;
                }
            } else {
                var0 = 47.88333333333334;
            }
        } else {
            if ((input[12]) <= (15.0)) {
                var0 = 20.52100840336134;
            } else {
                var0 = 14.718709677419358;
            }
        }
        return var0;
    }
}
