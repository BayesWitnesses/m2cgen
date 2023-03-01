module Model
    implicit none
contains
    function score(input)
        implicit none
        double precision, dimension(:) :: input
        double precision :: var0
        double precision :: var1
        double precision :: var2
        double precision :: var3
        double precision :: var4
        double precision :: var5
        double precision :: var6
        double precision :: var7
        double precision :: var8
        double precision :: var9
        double precision :: var10
        double precision :: var11
        double precision :: var12
        double precision :: var13
        double precision :: var14
        double precision :: var15
        double precision :: var16
        double precision :: var17
        double precision :: var18
        double precision :: var19
        double precision :: var20
        double precision :: var21
        double precision :: var22
        double precision :: var23
        double precision :: var24
        double precision :: var25
        double precision :: var26
        double precision :: var27
        double precision, dimension(3) :: score
        var0 = EXP(-0.06389634699048878d0 * ((5.1d0 - input(1)) ** 2.0d0 + (2.5d0 - input(2)) ** 2.0d0 + (3.0d0 - input(3)) ** 2.0d0 + (1.1d0 - input(4)) ** 2.0d0))
        var1 = EXP(-0.06389634699048878d0 * ((4.9d0 - input(1)) ** 2.0d0 + (2.4d0 - input(2)) ** 2.0d0 + (3.3d0 - input(3)) ** 2.0d0 + (1.0d0 - input(4)) ** 2.0d0))
        var2 = EXP(-0.06389634699048878d0 * ((6.3d0 - input(1)) ** 2.0d0 + (2.5d0 - input(2)) ** 2.0d0 + (4.9d0 - input(3)) ** 2.0d0 + (1.5d0 - input(4)) ** 2.0d0))
        var3 = EXP(-0.06389634699048878d0 * ((5.4d0 - input(1)) ** 2.0d0 + (3.0d0 - input(2)) ** 2.0d0 + (4.5d0 - input(3)) ** 2.0d0 + (1.5d0 - input(4)) ** 2.0d0))
        var4 = EXP(-0.06389634699048878d0 * ((6.2d0 - input(1)) ** 2.0d0 + (2.2d0 - input(2)) ** 2.0d0 + (4.5d0 - input(3)) ** 2.0d0 + (1.5d0 - input(4)) ** 2.0d0))
        var5 = EXP(-0.06389634699048878d0 * ((5.6d0 - input(1)) ** 2.0d0 + (2.9d0 - input(2)) ** 2.0d0 + (3.6d0 - input(3)) ** 2.0d0 + (1.3d0 - input(4)) ** 2.0d0))
        var6 = EXP(-0.06389634699048878d0 * ((6.7d0 - input(1)) ** 2.0d0 + (3.0d0 - input(2)) ** 2.0d0 + (5.0d0 - input(3)) ** 2.0d0 + (1.7d0 - input(4)) ** 2.0d0))
        var7 = EXP(-0.06389634699048878d0 * ((5.0d0 - input(1)) ** 2.0d0 + (2.3d0 - input(2)) ** 2.0d0 + (3.3d0 - input(3)) ** 2.0d0 + (1.0d0 - input(4)) ** 2.0d0))
        var8 = EXP(-0.06389634699048878d0 * ((6.0d0 - input(1)) ** 2.0d0 + (2.7d0 - input(2)) ** 2.0d0 + (5.1d0 - input(3)) ** 2.0d0 + (1.6d0 - input(4)) ** 2.0d0))
        var9 = EXP(-0.06389634699048878d0 * ((5.9d0 - input(1)) ** 2.0d0 + (3.2d0 - input(2)) ** 2.0d0 + (4.8d0 - input(3)) ** 2.0d0 + (1.8d0 - input(4)) ** 2.0d0))
        var10 = EXP(-0.06389634699048878d0 * ((5.7d0 - input(1)) ** 2.0d0 + (2.6d0 - input(2)) ** 2.0d0 + (3.5d0 - input(3)) ** 2.0d0 + (1.0d0 - input(4)) ** 2.0d0))
        var11 = EXP(-0.06389634699048878d0 * ((5.0d0 - input(1)) ** 2.0d0 + (3.0d0 - input(2)) ** 2.0d0 + (1.6d0 - input(3)) ** 2.0d0 + (0.2d0 - input(4)) ** 2.0d0))
        var12 = EXP(-0.06389634699048878d0 * ((5.4d0 - input(1)) ** 2.0d0 + (3.4d0 - input(2)) ** 2.0d0 + (1.7d0 - input(3)) ** 2.0d0 + (0.2d0 - input(4)) ** 2.0d0))
        var13 = EXP(-0.06389634699048878d0 * ((5.7d0 - input(1)) ** 2.0d0 + (3.8d0 - input(2)) ** 2.0d0 + (1.7d0 - input(3)) ** 2.0d0 + (0.3d0 - input(4)) ** 2.0d0))
        var14 = EXP(-0.06389634699048878d0 * ((4.8d0 - input(1)) ** 2.0d0 + (3.4d0 - input(2)) ** 2.0d0 + (1.9d0 - input(3)) ** 2.0d0 + (0.2d0 - input(4)) ** 2.0d0))
        var15 = EXP(-0.06389634699048878d0 * ((4.5d0 - input(1)) ** 2.0d0 + (2.3d0 - input(2)) ** 2.0d0 + (1.3d0 - input(3)) ** 2.0d0 + (0.3d0 - input(4)) ** 2.0d0))
        var16 = EXP(-0.06389634699048878d0 * ((5.7d0 - input(1)) ** 2.0d0 + (4.4d0 - input(2)) ** 2.0d0 + (1.5d0 - input(3)) ** 2.0d0 + (0.4d0 - input(4)) ** 2.0d0))
        var17 = EXP(-0.06389634699048878d0 * ((5.1d0 - input(1)) ** 2.0d0 + (3.8d0 - input(2)) ** 2.0d0 + (1.9d0 - input(3)) ** 2.0d0 + (0.4d0 - input(4)) ** 2.0d0))
        var18 = EXP(-0.06389634699048878d0 * ((5.1d0 - input(1)) ** 2.0d0 + (3.3d0 - input(2)) ** 2.0d0 + (1.7d0 - input(3)) ** 2.0d0 + (0.5d0 - input(4)) ** 2.0d0))
        var19 = EXP(-0.06389634699048878d0 * ((6.2d0 - input(1)) ** 2.0d0 + (2.8d0 - input(2)) ** 2.0d0 + (4.8d0 - input(3)) ** 2.0d0 + (1.8d0 - input(4)) ** 2.0d0))
        var20 = EXP(-0.06389634699048878d0 * ((7.2d0 - input(1)) ** 2.0d0 + (3.0d0 - input(2)) ** 2.0d0 + (5.8d0 - input(3)) ** 2.0d0 + (1.6d0 - input(4)) ** 2.0d0))
        var21 = EXP(-0.06389634699048878d0 * ((6.1d0 - input(1)) ** 2.0d0 + (3.0d0 - input(2)) ** 2.0d0 + (4.9d0 - input(3)) ** 2.0d0 + (1.8d0 - input(4)) ** 2.0d0))
        var22 = EXP(-0.06389634699048878d0 * ((6.0d0 - input(1)) ** 2.0d0 + (3.0d0 - input(2)) ** 2.0d0 + (4.8d0 - input(3)) ** 2.0d0 + (1.8d0 - input(4)) ** 2.0d0))
        var23 = EXP(-0.06389634699048878d0 * ((4.9d0 - input(1)) ** 2.0d0 + (2.5d0 - input(2)) ** 2.0d0 + (4.5d0 - input(3)) ** 2.0d0 + (1.7d0 - input(4)) ** 2.0d0))
        var24 = EXP(-0.06389634699048878d0 * ((7.9d0 - input(1)) ** 2.0d0 + (3.8d0 - input(2)) ** 2.0d0 + (6.4d0 - input(3)) ** 2.0d0 + (2.0d0 - input(4)) ** 2.0d0))
        var25 = EXP(-0.06389634699048878d0 * ((5.6d0 - input(1)) ** 2.0d0 + (2.8d0 - input(2)) ** 2.0d0 + (4.9d0 - input(3)) ** 2.0d0 + (2.0d0 - input(4)) ** 2.0d0))
        var26 = EXP(-0.06389634699048878d0 * ((6.0d0 - input(1)) ** 2.0d0 + (2.2d0 - input(2)) ** 2.0d0 + (5.0d0 - input(3)) ** 2.0d0 + (1.5d0 - input(4)) ** 2.0d0))
        var27 = EXP(-0.06389634699048878d0 * ((6.3d0 - input(1)) ** 2.0d0 + (2.8d0 - input(2)) ** 2.0d0 + (5.1d0 - input(3)) ** 2.0d0 + (1.5d0 - input(4)) ** 2.0d0))
        score(:) = (/ 0.11172510039290856d0 + var0 * -0.8898986041811555d0 + var1 * -0.8898986041811555d0 + var2 * -0.0d0 + var3 * -0.0d0 + var4 * -0.0d0 + var5 * -0.756413813553974d0 + var6 * -0.0d0 + var7 * -0.8898986041811555d0 + var8 * -0.0d0 + var9 * -0.0d0 + var10 * -0.8898986041811555d0 + var11 * 0.04218875216876044d0 + var12 * 0.7142250613852136d0 + var13 * 0.0d0 + var14 * 0.8898986041811555d0 + var15 * 0.8898986041811555d0 + var16 * 0.0d0 + var17 * 0.8898986041811555d0 + var18 * 0.8898986041811555d0, -0.04261957451303831d0 + var19 * -0.37953658977037247d0 + var20 * -0.0d0 + var21 * -0.0d0 + var22 * -0.37953658977037247d0 + var23 * -0.37953658977037247d0 + var24 * -0.26472396872040066d0 + var25 * -0.3745962010653211d0 + var26 * -0.10077618026650095d0 + var27 * -0.0d0 + var11 * 0.0d0 + var12 * 0.0d0 + var13 * 0.37953658977037247d0 + var14 * 0.37953658977037247d0 + var15 * 0.3044555865539922d0 + var16 * 0.05610417372785803d0 + var17 * 0.37953658977037247d0 + var18 * 0.37953658977037247d0, 1.8136162062461285d0 + var19 * -110.34516826676301d0 + var20 * -13.999391039896215d0 + var21 * -108.44329471899991d0 + var22 * -110.34516826676301d0 + var23 * -22.21095753342801d0 + var24 * -0.0d0 + var25 * -0.0d0 + var26 * -65.00217641452454d0 + var27 * -110.34516826676301d0 + var0 * 0.0d0 + var1 * 0.0d0 + var2 * 110.34516826676301d0 + var3 * 62.115561183470184d0 + var4 * 37.19509025661546d0 + var5 * 0.0d0 + var6 * 110.34516826676301d0 + var7 * 0.0d0 + var8 * 110.34516826676301d0 + var9 * 110.34516826676301d0 + var10 * 0.0d0 /)
        return
    end function score
end module Model
