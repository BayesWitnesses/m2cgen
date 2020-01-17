score <- function(input) {
    var0 <- exp(subroutine0(input))
    var1 <- exp(subroutine1(input))
    var2 <- exp(subroutine2(input))
    var3 <- ((var0) + (var1)) + (var2)
    return(c((var0) / (var3), (var1) / (var3), (var2) / (var3)))
}
subroutine0 <- function(input) {
    return(((0.5) + (subroutine3(input))) + (subroutine4(input)))
}
subroutine1 <- function(input) {
    return(((0.5) + (subroutine5(input))) + (subroutine6(input)))
}
subroutine2 <- function(input) {
    return(((0.5) + (subroutine7(input))) + (subroutine8(input)))
}
subroutine3 <- function(input) {
    if ((input[3]) >= (2.45000005)) {
        var0 <- -0.0733167157
    } else {
        var0 <- 0.143414631
    }
    return(var0)
}
subroutine4 <- function(input) {
    if ((input[3]) >= (2.45000005)) {
        var0 <- -0.0706516728
    } else {
        var0 <- 0.125176534
    }
    return(var0)
}
subroutine5 <- function(input) {
    if ((input[3]) >= (2.45000005)) {
        if ((input[4]) >= (1.75)) {
            var0 <- -0.0668393895
        } else {
            var0 <- 0.123041473
        }
    } else {
        var0 <- -0.0717073306
    }
    return(var0)
}
subroutine6 <- function(input) {
    if ((input[3]) >= (2.45000005)) {
        if ((input[4]) >= (1.75)) {
            var0 <- -0.0642274022
        } else {
            var0 <- 0.10819874
        }
    } else {
        var0 <- -0.069036141
    }
    return(var0)
}
subroutine7 <- function(input) {
    if ((input[4]) >= (1.6500001)) {
        var0 <- 0.13432835
    } else {
        if ((input[3]) >= (4.94999981)) {
            var0 <- 0.0724137947
        } else {
            var0 <- -0.0732467622
        }
    }
    return(var0)
}
subroutine8 <- function(input) {
    if ((input[4]) >= (1.6500001)) {
        var0 <- 0.117797568
    } else {
        if ((input[3]) >= (4.94999981)) {
            var0 <- 0.0702545047
        } else {
            var0 <- -0.0706570372
        }
    }
    return(var0)
}
