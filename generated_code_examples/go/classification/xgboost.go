import "math"
func score(input []float64) []float64 {
    var var0 float64
    if (input[2]) >= (2.45000005) {
        var0 = -0.0733167157
    } else {
        var0 = 0.143414631
    }
    var var1 float64
    if (input[2]) >= (2.45000005) {
        var1 = -0.0706516728
    } else {
        var1 = 0.125176534
    }
    var var2 float64
    var2 = math.Exp(((0.5) + (var0)) + (var1))
    var var3 float64
    if (input[2]) >= (2.45000005) {
        if (input[3]) >= (1.75) {
            var3 = -0.0668393895
        } else {
            var3 = 0.123041473
        }
    } else {
        var3 = -0.0717073306
    }
    var var4 float64
    if (input[2]) >= (2.45000005) {
        if (input[3]) >= (1.75) {
            var4 = -0.0642274022
        } else {
            var4 = 0.10819874
        }
    } else {
        var4 = -0.069036141
    }
    var var5 float64
    var5 = math.Exp(((0.5) + (var3)) + (var4))
    var var6 float64
    if (input[3]) >= (1.6500001) {
        var6 = 0.13432835
    } else {
        if (input[2]) >= (4.94999981) {
            var6 = 0.0724137947
        } else {
            var6 = -0.0732467622
        }
    }
    var var7 float64
    if (input[3]) >= (1.6500001) {
        var7 = 0.117797568
    } else {
        if (input[2]) >= (4.94999981) {
            var7 = 0.0702545047
        } else {
            var7 = -0.0706570372
        }
    }
    var var8 float64
    var8 = math.Exp(((0.5) + (var6)) + (var7))
    var var9 float64
    var9 = ((var2) + (var5)) + (var8)
    return []float64{(var2) / (var9), (var5) / (var9), (var8) / (var9)}
}
