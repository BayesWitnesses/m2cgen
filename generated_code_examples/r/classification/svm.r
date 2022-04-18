score <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((5.1 - input[1]) ^ 2.0 + (3.3 - input[2]) ^ 2.0 + (1.7 - input[3]) ^ 2.0 + (0.5 - input[4]) ^ 2.0))
    var1 <- exp(-0.06389634699048878 * ((5.7 - input[1]) ^ 2.0 + (2.6 - input[2]) ^ 2.0 + (3.5 - input[3]) ^ 2.0 + (1.0 - input[4]) ^ 2.0))
    return(c(subroutine0(input) + var0 * 0.8898986041811555, subroutine1(input) + var0 * 0.37953658977037247, subroutine2(input) + var1 * 0.0))
}
subroutine0 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((5.1 - input[1]) ^ 2.0 + (3.8 - input[2]) ^ 2.0 + (1.9 - input[3]) ^ 2.0 + (0.4 - input[4]) ^ 2.0))
    return(subroutine3(input) + var0 * 0.8898986041811555)
}
subroutine1 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((5.1 - input[1]) ^ 2.0 + (3.8 - input[2]) ^ 2.0 + (1.9 - input[3]) ^ 2.0 + (0.4 - input[4]) ^ 2.0))
    return(subroutine4(input) + var0 * 0.37953658977037247)
}
subroutine2 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((5.9 - input[1]) ^ 2.0 + (3.2 - input[2]) ^ 2.0 + (4.8 - input[3]) ^ 2.0 + (1.8 - input[4]) ^ 2.0))
    return(subroutine5(input) + var0 * 110.34516826676301)
}
subroutine3 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((5.7 - input[1]) ^ 2.0 + (4.4 - input[2]) ^ 2.0 + (1.5 - input[3]) ^ 2.0 + (0.4 - input[4]) ^ 2.0))
    return(subroutine6(input) + var0 * 0.0)
}
subroutine4 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((5.7 - input[1]) ^ 2.0 + (4.4 - input[2]) ^ 2.0 + (1.5 - input[3]) ^ 2.0 + (0.4 - input[4]) ^ 2.0))
    return(subroutine7(input) + var0 * 0.05610417372785803)
}
subroutine5 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((6.0 - input[1]) ^ 2.0 + (2.7 - input[2]) ^ 2.0 + (5.1 - input[3]) ^ 2.0 + (1.6 - input[4]) ^ 2.0))
    return(subroutine8(input) + var0 * 110.34516826676301)
}
subroutine6 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((4.5 - input[1]) ^ 2.0 + (2.3 - input[2]) ^ 2.0 + (1.3 - input[3]) ^ 2.0 + (0.3 - input[4]) ^ 2.0))
    return(subroutine9(input) + var0 * 0.8898986041811555)
}
subroutine7 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((4.5 - input[1]) ^ 2.0 + (2.3 - input[2]) ^ 2.0 + (1.3 - input[3]) ^ 2.0 + (0.3 - input[4]) ^ 2.0))
    return(subroutine10(input) + var0 * 0.3044555865539922)
}
subroutine8 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((5.0 - input[1]) ^ 2.0 + (2.3 - input[2]) ^ 2.0 + (3.3 - input[3]) ^ 2.0 + (1.0 - input[4]) ^ 2.0))
    return(subroutine11(input) + var0 * 0.0)
}
subroutine9 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((4.8 - input[1]) ^ 2.0 + (3.4 - input[2]) ^ 2.0 + (1.9 - input[3]) ^ 2.0 + (0.2 - input[4]) ^ 2.0))
    return(subroutine12(input) + var0 * 0.8898986041811555)
}
subroutine10 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((4.8 - input[1]) ^ 2.0 + (3.4 - input[2]) ^ 2.0 + (1.9 - input[3]) ^ 2.0 + (0.2 - input[4]) ^ 2.0))
    return(subroutine13(input) + var0 * 0.37953658977037247)
}
subroutine11 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((6.7 - input[1]) ^ 2.0 + (3.0 - input[2]) ^ 2.0 + (5.0 - input[3]) ^ 2.0 + (1.7 - input[4]) ^ 2.0))
    return(subroutine14(input) + var0 * 110.34516826676301)
}
subroutine12 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((5.7 - input[1]) ^ 2.0 + (3.8 - input[2]) ^ 2.0 + (1.7 - input[3]) ^ 2.0 + (0.3 - input[4]) ^ 2.0))
    return(subroutine15(input) + var0 * 0.0)
}
subroutine13 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((5.7 - input[1]) ^ 2.0 + (3.8 - input[2]) ^ 2.0 + (1.7 - input[3]) ^ 2.0 + (0.3 - input[4]) ^ 2.0))
    return(subroutine16(input) + var0 * 0.37953658977037247)
}
subroutine14 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((5.6 - input[1]) ^ 2.0 + (2.9 - input[2]) ^ 2.0 + (3.6 - input[3]) ^ 2.0 + (1.3 - input[4]) ^ 2.0))
    return(subroutine17(input) + var0 * 0.0)
}
subroutine15 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((5.4 - input[1]) ^ 2.0 + (3.4 - input[2]) ^ 2.0 + (1.7 - input[3]) ^ 2.0 + (0.2 - input[4]) ^ 2.0))
    return(subroutine18(input) + var0 * 0.7142250613852136)
}
subroutine16 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((5.4 - input[1]) ^ 2.0 + (3.4 - input[2]) ^ 2.0 + (1.7 - input[3]) ^ 2.0 + (0.2 - input[4]) ^ 2.0))
    return(subroutine19(input) + var0 * 0.0)
}
subroutine17 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((6.2 - input[1]) ^ 2.0 + (2.2 - input[2]) ^ 2.0 + (4.5 - input[3]) ^ 2.0 + (1.5 - input[4]) ^ 2.0))
    return(subroutine20(input) + var0 * 37.19509025661546)
}
subroutine18 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((5.0 - input[1]) ^ 2.0 + (3.0 - input[2]) ^ 2.0 + (1.6 - input[3]) ^ 2.0 + (0.2 - input[4]) ^ 2.0))
    return(subroutine21(input) + var0 * 0.04218875216876044)
}
subroutine19 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((5.0 - input[1]) ^ 2.0 + (3.0 - input[2]) ^ 2.0 + (1.6 - input[3]) ^ 2.0 + (0.2 - input[4]) ^ 2.0))
    return(subroutine22(input) + var0 * 0.0)
}
subroutine20 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((5.4 - input[1]) ^ 2.0 + (3.0 - input[2]) ^ 2.0 + (4.5 - input[3]) ^ 2.0 + (1.5 - input[4]) ^ 2.0))
    return(subroutine23(input) + var0 * 62.115561183470184)
}
subroutine21 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((5.7 - input[1]) ^ 2.0 + (2.6 - input[2]) ^ 2.0 + (3.5 - input[3]) ^ 2.0 + (1.0 - input[4]) ^ 2.0))
    return(subroutine24(input) + var0 * -0.8898986041811555)
}
subroutine22 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((6.3 - input[1]) ^ 2.0 + (2.8 - input[2]) ^ 2.0 + (5.1 - input[3]) ^ 2.0 + (1.5 - input[4]) ^ 2.0))
    return(subroutine25(input) + var0 * -0.0)
}
subroutine23 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((6.3 - input[1]) ^ 2.0 + (2.5 - input[2]) ^ 2.0 + (4.9 - input[3]) ^ 2.0 + (1.5 - input[4]) ^ 2.0))
    return(subroutine26(input) + var0 * 110.34516826676301)
}
subroutine24 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((5.9 - input[1]) ^ 2.0 + (3.2 - input[2]) ^ 2.0 + (4.8 - input[3]) ^ 2.0 + (1.8 - input[4]) ^ 2.0))
    return(subroutine27(input) + var0 * -0.0)
}
subroutine25 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((6.0 - input[1]) ^ 2.0 + (2.2 - input[2]) ^ 2.0 + (5.0 - input[3]) ^ 2.0 + (1.5 - input[4]) ^ 2.0))
    return(subroutine28(input) + var0 * -0.10077618026650095)
}
subroutine26 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((4.9 - input[1]) ^ 2.0 + (2.4 - input[2]) ^ 2.0 + (3.3 - input[3]) ^ 2.0 + (1.0 - input[4]) ^ 2.0))
    return(subroutine29(input) + var0 * 0.0)
}
subroutine27 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((6.0 - input[1]) ^ 2.0 + (2.7 - input[2]) ^ 2.0 + (5.1 - input[3]) ^ 2.0 + (1.6 - input[4]) ^ 2.0))
    return(subroutine30(input) + var0 * -0.0)
}
subroutine28 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((6.2 - input[1]) ^ 2.0 + (2.8 - input[2]) ^ 2.0 + (4.8 - input[3]) ^ 2.0 + (1.8 - input[4]) ^ 2.0))
    var1 <- exp(-0.06389634699048878 * ((7.2 - input[1]) ^ 2.0 + (3.0 - input[2]) ^ 2.0 + (5.8 - input[3]) ^ 2.0 + (1.6 - input[4]) ^ 2.0))
    var2 <- exp(-0.06389634699048878 * ((6.1 - input[1]) ^ 2.0 + (3.0 - input[2]) ^ 2.0 + (4.9 - input[3]) ^ 2.0 + (1.8 - input[4]) ^ 2.0))
    var3 <- exp(-0.06389634699048878 * ((6.0 - input[1]) ^ 2.0 + (3.0 - input[2]) ^ 2.0 + (4.8 - input[3]) ^ 2.0 + (1.8 - input[4]) ^ 2.0))
    var4 <- exp(-0.06389634699048878 * ((4.9 - input[1]) ^ 2.0 + (2.5 - input[2]) ^ 2.0 + (4.5 - input[3]) ^ 2.0 + (1.7 - input[4]) ^ 2.0))
    var5 <- exp(-0.06389634699048878 * ((7.9 - input[1]) ^ 2.0 + (3.8 - input[2]) ^ 2.0 + (6.4 - input[3]) ^ 2.0 + (2.0 - input[4]) ^ 2.0))
    var6 <- exp(-0.06389634699048878 * ((5.6 - input[1]) ^ 2.0 + (2.8 - input[2]) ^ 2.0 + (4.9 - input[3]) ^ 2.0 + (2.0 - input[4]) ^ 2.0))
    return(-0.04261957451303831 + var0 * -0.37953658977037247 + var1 * -0.0 + var2 * -0.0 + var3 * -0.37953658977037247 + var4 * -0.37953658977037247 + var5 * -0.26472396872040066 + var6 * -0.3745962010653211)
}
subroutine29 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((5.1 - input[1]) ^ 2.0 + (2.5 - input[2]) ^ 2.0 + (3.0 - input[3]) ^ 2.0 + (1.1 - input[4]) ^ 2.0))
    return(subroutine31(input) + var0 * 0.0)
}
subroutine30 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((5.0 - input[1]) ^ 2.0 + (2.3 - input[2]) ^ 2.0 + (3.3 - input[3]) ^ 2.0 + (1.0 - input[4]) ^ 2.0))
    return(subroutine32(input) + var0 * -0.8898986041811555)
}
subroutine31 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((6.3 - input[1]) ^ 2.0 + (2.8 - input[2]) ^ 2.0 + (5.1 - input[3]) ^ 2.0 + (1.5 - input[4]) ^ 2.0))
    return(subroutine33(input) + var0 * -110.34516826676301)
}
subroutine32 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((5.1 - input[1]) ^ 2.0 + (2.5 - input[2]) ^ 2.0 + (3.0 - input[3]) ^ 2.0 + (1.1 - input[4]) ^ 2.0))
    var1 <- exp(-0.06389634699048878 * ((4.9 - input[1]) ^ 2.0 + (2.4 - input[2]) ^ 2.0 + (3.3 - input[3]) ^ 2.0 + (1.0 - input[4]) ^ 2.0))
    var2 <- exp(-0.06389634699048878 * ((6.3 - input[1]) ^ 2.0 + (2.5 - input[2]) ^ 2.0 + (4.9 - input[3]) ^ 2.0 + (1.5 - input[4]) ^ 2.0))
    var3 <- exp(-0.06389634699048878 * ((5.4 - input[1]) ^ 2.0 + (3.0 - input[2]) ^ 2.0 + (4.5 - input[3]) ^ 2.0 + (1.5 - input[4]) ^ 2.0))
    var4 <- exp(-0.06389634699048878 * ((6.2 - input[1]) ^ 2.0 + (2.2 - input[2]) ^ 2.0 + (4.5 - input[3]) ^ 2.0 + (1.5 - input[4]) ^ 2.0))
    var5 <- exp(-0.06389634699048878 * ((5.6 - input[1]) ^ 2.0 + (2.9 - input[2]) ^ 2.0 + (3.6 - input[3]) ^ 2.0 + (1.3 - input[4]) ^ 2.0))
    var6 <- exp(-0.06389634699048878 * ((6.7 - input[1]) ^ 2.0 + (3.0 - input[2]) ^ 2.0 + (5.0 - input[3]) ^ 2.0 + (1.7 - input[4]) ^ 2.0))
    return(0.11172510039290856 + var0 * -0.8898986041811555 + var1 * -0.8898986041811555 + var2 * -0.0 + var3 * -0.0 + var4 * -0.0 + var5 * -0.756413813553974 + var6 * -0.0)
}
subroutine33 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((6.0 - input[1]) ^ 2.0 + (2.2 - input[2]) ^ 2.0 + (5.0 - input[3]) ^ 2.0 + (1.5 - input[4]) ^ 2.0))
    return(subroutine34(input) + var0 * -65.00217641452454)
}
subroutine34 <- function(input) {
    var0 <- exp(-0.06389634699048878 * ((6.2 - input[1]) ^ 2.0 + (2.8 - input[2]) ^ 2.0 + (4.8 - input[3]) ^ 2.0 + (1.8 - input[4]) ^ 2.0))
    var1 <- exp(-0.06389634699048878 * ((7.2 - input[1]) ^ 2.0 + (3.0 - input[2]) ^ 2.0 + (5.8 - input[3]) ^ 2.0 + (1.6 - input[4]) ^ 2.0))
    var2 <- exp(-0.06389634699048878 * ((6.1 - input[1]) ^ 2.0 + (3.0 - input[2]) ^ 2.0 + (4.9 - input[3]) ^ 2.0 + (1.8 - input[4]) ^ 2.0))
    var3 <- exp(-0.06389634699048878 * ((6.0 - input[1]) ^ 2.0 + (3.0 - input[2]) ^ 2.0 + (4.8 - input[3]) ^ 2.0 + (1.8 - input[4]) ^ 2.0))
    var4 <- exp(-0.06389634699048878 * ((4.9 - input[1]) ^ 2.0 + (2.5 - input[2]) ^ 2.0 + (4.5 - input[3]) ^ 2.0 + (1.7 - input[4]) ^ 2.0))
    var5 <- exp(-0.06389634699048878 * ((7.9 - input[1]) ^ 2.0 + (3.8 - input[2]) ^ 2.0 + (6.4 - input[3]) ^ 2.0 + (2.0 - input[4]) ^ 2.0))
    var6 <- exp(-0.06389634699048878 * ((5.6 - input[1]) ^ 2.0 + (2.8 - input[2]) ^ 2.0 + (4.9 - input[3]) ^ 2.0 + (2.0 - input[4]) ^ 2.0))
    return(1.8136162062461285 + var0 * -110.34516826676301 + var1 * -13.999391039896215 + var2 * -108.44329471899991 + var3 * -110.34516826676301 + var4 * -22.21095753342801 + var5 * -0.0 + var6 * -0.0)
}
