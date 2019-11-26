namespace ML {
    public static class Model {
        public static double Score(double[] input) {
            double var0;
            if ((input[12]) >= (9.72500038)) {
                if ((input[12]) >= (19.8299999)) {
                    var0 = 1.1551429;
                } else {
                    var0 = 1.8613131;
                }
            } else {
                if ((input[5]) >= (6.94099998)) {
                    var0 = 3.75848508;
                } else {
                    var0 = 2.48056006;
                }
            }
            double var1;
            if ((input[12]) >= (7.68499994)) {
                if ((input[12]) >= (15)) {
                    var1 = 1.24537706;
                } else {
                    var1 = 1.92129695;
                }
            } else {
                if ((input[5]) >= (7.43700027)) {
                    var1 = 3.96021533;
                } else {
                    var1 = 2.51493931;
                }
            }
            return ((0.5) + (var0)) + (var1);
        }
    }
}
