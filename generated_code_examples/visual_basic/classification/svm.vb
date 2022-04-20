Module Model
Function Score(ByRef inputVector() As Double) As Double()
    Dim var0 As Double
    var0 = Math.Exp(-0.06389634699048878 * ((5.1 - inputVector(0)) ^ 2.0 + (2.5 - inputVector(1)) ^ 2.0 + (3.0 - inputVector(2)) ^ 2.0 + (1.1 - inputVector(3)) ^ 2.0))
    Dim var1 As Double
    var1 = Math.Exp(-0.06389634699048878 * ((4.9 - inputVector(0)) ^ 2.0 + (2.4 - inputVector(1)) ^ 2.0 + (3.3 - inputVector(2)) ^ 2.0 + (1.0 - inputVector(3)) ^ 2.0))
    Dim var2 As Double
    var2 = Math.Exp(-0.06389634699048878 * ((6.3 - inputVector(0)) ^ 2.0 + (2.5 - inputVector(1)) ^ 2.0 + (4.9 - inputVector(2)) ^ 2.0 + (1.5 - inputVector(3)) ^ 2.0))
    Dim var3 As Double
    var3 = Math.Exp(-0.06389634699048878 * ((5.4 - inputVector(0)) ^ 2.0 + (3.0 - inputVector(1)) ^ 2.0 + (4.5 - inputVector(2)) ^ 2.0 + (1.5 - inputVector(3)) ^ 2.0))
    Dim var4 As Double
    var4 = Math.Exp(-0.06389634699048878 * ((6.2 - inputVector(0)) ^ 2.0 + (2.2 - inputVector(1)) ^ 2.0 + (4.5 - inputVector(2)) ^ 2.0 + (1.5 - inputVector(3)) ^ 2.0))
    Dim var5 As Double
    var5 = Math.Exp(-0.06389634699048878 * ((5.6 - inputVector(0)) ^ 2.0 + (2.9 - inputVector(1)) ^ 2.0 + (3.6 - inputVector(2)) ^ 2.0 + (1.3 - inputVector(3)) ^ 2.0))
    Dim var6 As Double
    var6 = Math.Exp(-0.06389634699048878 * ((6.7 - inputVector(0)) ^ 2.0 + (3.0 - inputVector(1)) ^ 2.0 + (5.0 - inputVector(2)) ^ 2.0 + (1.7 - inputVector(3)) ^ 2.0))
    Dim var7 As Double
    var7 = Math.Exp(-0.06389634699048878 * ((5.0 - inputVector(0)) ^ 2.0 + (2.3 - inputVector(1)) ^ 2.0 + (3.3 - inputVector(2)) ^ 2.0 + (1.0 - inputVector(3)) ^ 2.0))
    Dim var8 As Double
    var8 = Math.Exp(-0.06389634699048878 * ((6.0 - inputVector(0)) ^ 2.0 + (2.7 - inputVector(1)) ^ 2.0 + (5.1 - inputVector(2)) ^ 2.0 + (1.6 - inputVector(3)) ^ 2.0))
    Dim var9 As Double
    var9 = Math.Exp(-0.06389634699048878 * ((5.9 - inputVector(0)) ^ 2.0 + (3.2 - inputVector(1)) ^ 2.0 + (4.8 - inputVector(2)) ^ 2.0 + (1.8 - inputVector(3)) ^ 2.0))
    Dim var10 As Double
    var10 = Math.Exp(-0.06389634699048878 * ((5.7 - inputVector(0)) ^ 2.0 + (2.6 - inputVector(1)) ^ 2.0 + (3.5 - inputVector(2)) ^ 2.0 + (1.0 - inputVector(3)) ^ 2.0))
    Dim var11 As Double
    var11 = Math.Exp(-0.06389634699048878 * ((5.0 - inputVector(0)) ^ 2.0 + (3.0 - inputVector(1)) ^ 2.0 + (1.6 - inputVector(2)) ^ 2.0 + (0.2 - inputVector(3)) ^ 2.0))
    Dim var12 As Double
    var12 = Math.Exp(-0.06389634699048878 * ((5.4 - inputVector(0)) ^ 2.0 + (3.4 - inputVector(1)) ^ 2.0 + (1.7 - inputVector(2)) ^ 2.0 + (0.2 - inputVector(3)) ^ 2.0))
    Dim var13 As Double
    var13 = Math.Exp(-0.06389634699048878 * ((5.7 - inputVector(0)) ^ 2.0 + (3.8 - inputVector(1)) ^ 2.0 + (1.7 - inputVector(2)) ^ 2.0 + (0.3 - inputVector(3)) ^ 2.0))
    Dim var14 As Double
    var14 = Math.Exp(-0.06389634699048878 * ((4.8 - inputVector(0)) ^ 2.0 + (3.4 - inputVector(1)) ^ 2.0 + (1.9 - inputVector(2)) ^ 2.0 + (0.2 - inputVector(3)) ^ 2.0))
    Dim var15 As Double
    var15 = Math.Exp(-0.06389634699048878 * ((4.5 - inputVector(0)) ^ 2.0 + (2.3 - inputVector(1)) ^ 2.0 + (1.3 - inputVector(2)) ^ 2.0 + (0.3 - inputVector(3)) ^ 2.0))
    Dim var16 As Double
    var16 = Math.Exp(-0.06389634699048878 * ((5.7 - inputVector(0)) ^ 2.0 + (4.4 - inputVector(1)) ^ 2.0 + (1.5 - inputVector(2)) ^ 2.0 + (0.4 - inputVector(3)) ^ 2.0))
    Dim var17 As Double
    var17 = Math.Exp(-0.06389634699048878 * ((5.1 - inputVector(0)) ^ 2.0 + (3.8 - inputVector(1)) ^ 2.0 + (1.9 - inputVector(2)) ^ 2.0 + (0.4 - inputVector(3)) ^ 2.0))
    Dim var18 As Double
    var18 = Math.Exp(-0.06389634699048878 * ((5.1 - inputVector(0)) ^ 2.0 + (3.3 - inputVector(1)) ^ 2.0 + (1.7 - inputVector(2)) ^ 2.0 + (0.5 - inputVector(3)) ^ 2.0))
    Dim var19 As Double
    var19 = Math.Exp(-0.06389634699048878 * ((6.2 - inputVector(0)) ^ 2.0 + (2.8 - inputVector(1)) ^ 2.0 + (4.8 - inputVector(2)) ^ 2.0 + (1.8 - inputVector(3)) ^ 2.0))
    Dim var20 As Double
    var20 = Math.Exp(-0.06389634699048878 * ((7.2 - inputVector(0)) ^ 2.0 + (3.0 - inputVector(1)) ^ 2.0 + (5.8 - inputVector(2)) ^ 2.0 + (1.6 - inputVector(3)) ^ 2.0))
    Dim var21 As Double
    var21 = Math.Exp(-0.06389634699048878 * ((6.1 - inputVector(0)) ^ 2.0 + (3.0 - inputVector(1)) ^ 2.0 + (4.9 - inputVector(2)) ^ 2.0 + (1.8 - inputVector(3)) ^ 2.0))
    Dim var22 As Double
    var22 = Math.Exp(-0.06389634699048878 * ((6.0 - inputVector(0)) ^ 2.0 + (3.0 - inputVector(1)) ^ 2.0 + (4.8 - inputVector(2)) ^ 2.0 + (1.8 - inputVector(3)) ^ 2.0))
    Dim var23 As Double
    var23 = Math.Exp(-0.06389634699048878 * ((4.9 - inputVector(0)) ^ 2.0 + (2.5 - inputVector(1)) ^ 2.0 + (4.5 - inputVector(2)) ^ 2.0 + (1.7 - inputVector(3)) ^ 2.0))
    Dim var24 As Double
    var24 = Math.Exp(-0.06389634699048878 * ((7.9 - inputVector(0)) ^ 2.0 + (3.8 - inputVector(1)) ^ 2.0 + (6.4 - inputVector(2)) ^ 2.0 + (2.0 - inputVector(3)) ^ 2.0))
    Dim var25 As Double
    var25 = Math.Exp(-0.06389634699048878 * ((5.6 - inputVector(0)) ^ 2.0 + (2.8 - inputVector(1)) ^ 2.0 + (4.9 - inputVector(2)) ^ 2.0 + (2.0 - inputVector(3)) ^ 2.0))
    Dim var26 As Double
    var26 = Math.Exp(-0.06389634699048878 * ((6.0 - inputVector(0)) ^ 2.0 + (2.2 - inputVector(1)) ^ 2.0 + (5.0 - inputVector(2)) ^ 2.0 + (1.5 - inputVector(3)) ^ 2.0))
    Dim var27 As Double
    var27 = Math.Exp(-0.06389634699048878 * ((6.3 - inputVector(0)) ^ 2.0 + (2.8 - inputVector(1)) ^ 2.0 + (5.1 - inputVector(2)) ^ 2.0 + (1.5 - inputVector(3)) ^ 2.0))
    Dim var28(2) As Double
    var28(0) = 0.11172510039290856 + var0 * -0.8898986041811555 + var1 * -0.8898986041811555 + var2 * -0.0 + var3 * -0.0 + var4 * -0.0 + var5 * -0.756413813553974 + var6 * -0.0 + var7 * -0.8898986041811555 + var8 * -0.0 + var9 * -0.0 + var10 * -0.8898986041811555 + var11 * 0.04218875216876044 + var12 * 0.7142250613852136 + var13 * 0.0 + var14 * 0.8898986041811555 + var15 * 0.8898986041811555 + var16 * 0.0 + var17 * 0.8898986041811555 + var18 * 0.8898986041811555
    var28(1) = -0.04261957451303831 + var19 * -0.37953658977037247 + var20 * -0.0 + var21 * -0.0 + var22 * -0.37953658977037247 + var23 * -0.37953658977037247 + var24 * -0.26472396872040066 + var25 * -0.3745962010653211 + var26 * -0.10077618026650095 + var27 * -0.0 + var11 * 0.0 + var12 * 0.0 + var13 * 0.37953658977037247 + var14 * 0.37953658977037247 + var15 * 0.3044555865539922 + var16 * 0.05610417372785803 + var17 * 0.37953658977037247 + var18 * 0.37953658977037247
    var28(2) = 1.8136162062461285 + var19 * -110.34516826676301 + var20 * -13.999391039896215 + var21 * -108.44329471899991 + var22 * -110.34516826676301 + var23 * -22.21095753342801 + var24 * -0.0 + var25 * -0.0 + var26 * -65.00217641452454 + var27 * -110.34516826676301 + var0 * 0.0 + var1 * 0.0 + var2 * 110.34516826676301 + var3 * 62.115561183470184 + var4 * 37.19509025661546 + var5 * 0.0 + var6 * 110.34516826676301 + var7 * 0.0 + var8 * 110.34516826676301 + var9 * 110.34516826676301 + var10 * 0.0
    Score = var28
End Function
End Module
