public class Model {

    public static double score(double[] input) {
        return subroutine0(input);
    }
    public static double subroutine0(double[] input) {
        double var0;
        if ((input[5]) <= (6.8455)) {
            if ((input[12]) <= (14.395000000000001)) {
                var0 = 22.70305627629392;
            } else {
                var0 = 21.863487452747595;
            }
        } else {
            if ((input[5]) <= (7.437)) {
                var0 = 23.513674700555555;
            } else {
                var0 = 24.906664851995615;
            }
        }
        double var1;
        if ((input[12]) <= (9.63)) {
            if ((input[5]) <= (7.437)) {
                var1 = 0.4576204330349962;
            } else {
                var1 = 2.0368334157126293;
            }
        } else {
            if ((input[12]) <= (19.830000000000002)) {
                var1 = -0.30629733662250097;
            } else {
                var1 = -0.9644646678713786;
            }
        }
        return ((0) + (var0)) + (var1);
    }
}
