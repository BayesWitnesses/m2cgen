using static System.Math;
namespace ML {
    public static class Model {
        public static double[] Score(double[] input) {
            double var0;
            if (input[2] > 3.1500000000000004) {
                var0 = -1.1986122886681099;
            } else {
                if (input[1] > 3.35) {
                    var0 = -0.8986122886681098;
                } else {
                    var0 = -0.9136122886681098;
                }
            }
            double var1;
            if (input[2] > 3.1500000000000004) {
                if (input[2] > 4.450000000000001) {
                    var1 = -0.09503010837903424;
                } else {
                    var1 = -0.09563272415214283;
                }
            } else {
                if (input[1] > 3.35) {
                    var1 = 0.16640323607832397;
                } else {
                    var1 = 0.15374604217339707;
                }
            }
            double var2;
            if (input[2] > 1.8) {
                if (input[3] > 1.6500000000000001) {
                    var2 = -1.2055899476674514;
                } else {
                    var2 = -0.9500445227622534;
                }
            } else {
                var2 = -1.2182214705715104;
            }
            double var3;
            if (input[3] > 0.45000000000000007) {
                if (input[3] > 1.6500000000000001) {
                    var3 = -0.08146437273923739;
                } else {
                    var3 = 0.14244886188108738;
                }
            } else {
                if (input[2] > 1.4500000000000002) {
                    var3 = -0.0950888159264695;
                } else {
                    var3 = -0.09438233722389686;
                }
            }
            double var4;
            if (input[3] > 1.6500000000000001) {
                if (input[2] > 5.3500000000000005) {
                    var4 = -0.8824095771015287;
                } else {
                    var4 = -0.9121126703829481;
                }
            } else {
                if (input[2] > 4.450000000000001) {
                    var4 = -1.1277829563828181;
                } else {
                    var4 = -1.1794405099157212;
                }
            }
            double var5;
            if (input[2] > 4.750000000000001) {
                if (input[2] > 5.150000000000001) {
                    var5 = 0.16625543464258166;
                } else {
                    var5 = 0.09608601737074281;
                }
            } else {
                if (input[0] > 4.950000000000001) {
                    var5 = -0.09644547407948921;
                } else {
                    var5 = -0.08181864271444342;
                }
            }
            return Softmax(new double[3] {var0 + var1, var2 + var3, var4 + var5});
        }
        private static double[] Softmax(double[] x) {
            int size = x.Length;
            double[] result = new double[size];
            double max = x[0];
            for (int i = 1; i < size; ++i) {
                if (x[i] > max)
                    max = x[i];
            }
            double sum = 0.0;
            for (int i = 0; i < size; ++i) {
                result[i] = Exp(x[i] - max);
                sum += result[i];
            }
            for (int i = 0; i < size; ++i)
                result[i] /= sum;
            return result;
        }
    }
}
