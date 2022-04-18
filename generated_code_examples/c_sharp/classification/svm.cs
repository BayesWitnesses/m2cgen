using static System.Math;
namespace ML {
    public static class Model {
        public static double[] Score(double[] input) {
            double var0;
            var0 = Exp(-0.06389634699048878 * (Pow(5.1 - input[0], 2.0) + Pow(2.5 - input[1], 2.0) + Pow(3.0 - input[2], 2.0) + Pow(1.1 - input[3], 2.0)));
            double var1;
            var1 = Exp(-0.06389634699048878 * (Pow(4.9 - input[0], 2.0) + Pow(2.4 - input[1], 2.0) + Pow(3.3 - input[2], 2.0) + Pow(1.0 - input[3], 2.0)));
            double var2;
            var2 = Exp(-0.06389634699048878 * (Pow(6.3 - input[0], 2.0) + Pow(2.5 - input[1], 2.0) + Pow(4.9 - input[2], 2.0) + Pow(1.5 - input[3], 2.0)));
            double var3;
            var3 = Exp(-0.06389634699048878 * (Pow(5.4 - input[0], 2.0) + Pow(3.0 - input[1], 2.0) + Pow(4.5 - input[2], 2.0) + Pow(1.5 - input[3], 2.0)));
            double var4;
            var4 = Exp(-0.06389634699048878 * (Pow(6.2 - input[0], 2.0) + Pow(2.2 - input[1], 2.0) + Pow(4.5 - input[2], 2.0) + Pow(1.5 - input[3], 2.0)));
            double var5;
            var5 = Exp(-0.06389634699048878 * (Pow(5.6 - input[0], 2.0) + Pow(2.9 - input[1], 2.0) + Pow(3.6 - input[2], 2.0) + Pow(1.3 - input[3], 2.0)));
            double var6;
            var6 = Exp(-0.06389634699048878 * (Pow(6.7 - input[0], 2.0) + Pow(3.0 - input[1], 2.0) + Pow(5.0 - input[2], 2.0) + Pow(1.7 - input[3], 2.0)));
            double var7;
            var7 = Exp(-0.06389634699048878 * (Pow(5.0 - input[0], 2.0) + Pow(2.3 - input[1], 2.0) + Pow(3.3 - input[2], 2.0) + Pow(1.0 - input[3], 2.0)));
            double var8;
            var8 = Exp(-0.06389634699048878 * (Pow(6.0 - input[0], 2.0) + Pow(2.7 - input[1], 2.0) + Pow(5.1 - input[2], 2.0) + Pow(1.6 - input[3], 2.0)));
            double var9;
            var9 = Exp(-0.06389634699048878 * (Pow(5.9 - input[0], 2.0) + Pow(3.2 - input[1], 2.0) + Pow(4.8 - input[2], 2.0) + Pow(1.8 - input[3], 2.0)));
            double var10;
            var10 = Exp(-0.06389634699048878 * (Pow(5.7 - input[0], 2.0) + Pow(2.6 - input[1], 2.0) + Pow(3.5 - input[2], 2.0) + Pow(1.0 - input[3], 2.0)));
            double var11;
            var11 = Exp(-0.06389634699048878 * (Pow(5.0 - input[0], 2.0) + Pow(3.0 - input[1], 2.0) + Pow(1.6 - input[2], 2.0) + Pow(0.2 - input[3], 2.0)));
            double var12;
            var12 = Exp(-0.06389634699048878 * (Pow(5.4 - input[0], 2.0) + Pow(3.4 - input[1], 2.0) + Pow(1.7 - input[2], 2.0) + Pow(0.2 - input[3], 2.0)));
            double var13;
            var13 = Exp(-0.06389634699048878 * (Pow(5.7 - input[0], 2.0) + Pow(3.8 - input[1], 2.0) + Pow(1.7 - input[2], 2.0) + Pow(0.3 - input[3], 2.0)));
            double var14;
            var14 = Exp(-0.06389634699048878 * (Pow(4.8 - input[0], 2.0) + Pow(3.4 - input[1], 2.0) + Pow(1.9 - input[2], 2.0) + Pow(0.2 - input[3], 2.0)));
            double var15;
            var15 = Exp(-0.06389634699048878 * (Pow(4.5 - input[0], 2.0) + Pow(2.3 - input[1], 2.0) + Pow(1.3 - input[2], 2.0) + Pow(0.3 - input[3], 2.0)));
            double var16;
            var16 = Exp(-0.06389634699048878 * (Pow(5.7 - input[0], 2.0) + Pow(4.4 - input[1], 2.0) + Pow(1.5 - input[2], 2.0) + Pow(0.4 - input[3], 2.0)));
            double var17;
            var17 = Exp(-0.06389634699048878 * (Pow(5.1 - input[0], 2.0) + Pow(3.8 - input[1], 2.0) + Pow(1.9 - input[2], 2.0) + Pow(0.4 - input[3], 2.0)));
            double var18;
            var18 = Exp(-0.06389634699048878 * (Pow(5.1 - input[0], 2.0) + Pow(3.3 - input[1], 2.0) + Pow(1.7 - input[2], 2.0) + Pow(0.5 - input[3], 2.0)));
            double var19;
            var19 = Exp(-0.06389634699048878 * (Pow(6.2 - input[0], 2.0) + Pow(2.8 - input[1], 2.0) + Pow(4.8 - input[2], 2.0) + Pow(1.8 - input[3], 2.0)));
            double var20;
            var20 = Exp(-0.06389634699048878 * (Pow(7.2 - input[0], 2.0) + Pow(3.0 - input[1], 2.0) + Pow(5.8 - input[2], 2.0) + Pow(1.6 - input[3], 2.0)));
            double var21;
            var21 = Exp(-0.06389634699048878 * (Pow(6.1 - input[0], 2.0) + Pow(3.0 - input[1], 2.0) + Pow(4.9 - input[2], 2.0) + Pow(1.8 - input[3], 2.0)));
            double var22;
            var22 = Exp(-0.06389634699048878 * (Pow(6.0 - input[0], 2.0) + Pow(3.0 - input[1], 2.0) + Pow(4.8 - input[2], 2.0) + Pow(1.8 - input[3], 2.0)));
            double var23;
            var23 = Exp(-0.06389634699048878 * (Pow(4.9 - input[0], 2.0) + Pow(2.5 - input[1], 2.0) + Pow(4.5 - input[2], 2.0) + Pow(1.7 - input[3], 2.0)));
            double var24;
            var24 = Exp(-0.06389634699048878 * (Pow(7.9 - input[0], 2.0) + Pow(3.8 - input[1], 2.0) + Pow(6.4 - input[2], 2.0) + Pow(2.0 - input[3], 2.0)));
            double var25;
            var25 = Exp(-0.06389634699048878 * (Pow(5.6 - input[0], 2.0) + Pow(2.8 - input[1], 2.0) + Pow(4.9 - input[2], 2.0) + Pow(2.0 - input[3], 2.0)));
            double var26;
            var26 = Exp(-0.06389634699048878 * (Pow(6.0 - input[0], 2.0) + Pow(2.2 - input[1], 2.0) + Pow(5.0 - input[2], 2.0) + Pow(1.5 - input[3], 2.0)));
            double var27;
            var27 = Exp(-0.06389634699048878 * (Pow(6.3 - input[0], 2.0) + Pow(2.8 - input[1], 2.0) + Pow(5.1 - input[2], 2.0) + Pow(1.5 - input[3], 2.0)));
            return new double[3] {0.11172510039290856 + var0 * -0.8898986041811555 + var1 * -0.8898986041811555 + var2 * -0.0 + var3 * -0.0 + var4 * -0.0 + var5 * -0.756413813553974 + var6 * -0.0 + var7 * -0.8898986041811555 + var8 * -0.0 + var9 * -0.0 + var10 * -0.8898986041811555 + var11 * 0.04218875216876044 + var12 * 0.7142250613852136 + var13 * 0.0 + var14 * 0.8898986041811555 + var15 * 0.8898986041811555 + var16 * 0.0 + var17 * 0.8898986041811555 + var18 * 0.8898986041811555, -0.04261957451303831 + var19 * -0.37953658977037247 + var20 * -0.0 + var21 * -0.0 + var22 * -0.37953658977037247 + var23 * -0.37953658977037247 + var24 * -0.26472396872040066 + var25 * -0.3745962010653211 + var26 * -0.10077618026650095 + var27 * -0.0 + var11 * 0.0 + var12 * 0.0 + var13 * 0.37953658977037247 + var14 * 0.37953658977037247 + var15 * 0.3044555865539922 + var16 * 0.05610417372785803 + var17 * 0.37953658977037247 + var18 * 0.37953658977037247, 1.8136162062461285 + var19 * -110.34516826676301 + var20 * -13.999391039896215 + var21 * -108.44329471899991 + var22 * -110.34516826676301 + var23 * -22.21095753342801 + var24 * -0.0 + var25 * -0.0 + var26 * -65.00217641452454 + var27 * -110.34516826676301 + var0 * 0.0 + var1 * 0.0 + var2 * 110.34516826676301 + var3 * 62.115561183470184 + var4 * 37.19509025661546 + var5 * 0.0 + var6 * 110.34516826676301 + var7 * 0.0 + var8 * 110.34516826676301 + var9 * 110.34516826676301 + var10 * 0.0};
        }
    }
}
