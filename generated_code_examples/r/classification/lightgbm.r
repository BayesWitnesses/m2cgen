score <- function(input) {
    var0 <- exp(subroutine0(input))
    var1 <- exp(subroutine1(input))
    var2 <- exp(subroutine2(input))
    var3 <- ((var0) + (var1)) + (var2)
    return(c((var0) / (var3), (var1) / (var3), (var2) / (var3)))
}
subroutine0 <- function(input) {
    return(((0) + (subroutine3(input))) + (subroutine4(input)))
}
subroutine1 <- function(input) {
    return(((0) + (subroutine5(input))) + (subroutine6(input)))
}
subroutine2 <- function(input) {
    return(((0) + (subroutine7(input))) + (subroutine8(input)))
}
subroutine3 <- function(input) {
    if ((input[3]) > (3.1500000000000004)) {
        var0 <- -1.1736122903444903
    } else {
        if ((input[2]) > (3.35)) {
            var0 <- -0.9486122853153485
        } else {
            var0 <- -0.9598622855668056
        }
    }
    return(var0)
}
subroutine4 <- function(input) {
    if ((input[3]) > (3.1500000000000004)) {
        if ((input[3]) > (4.450000000000001)) {
            var0 <- -0.07218200074594171
        } else {
            var0 <- -0.0725391787456957
        }
    } else {
        if ((input[2]) > (3.35)) {
            var0 <- 0.130416969124648
        } else {
            var0 <- 0.12058330491181404
        }
    }
    return(var0)
}
subroutine5 <- function(input) {
    if ((input[3]) > (1.8)) {
        if ((input[4]) > (1.6500000000000001)) {
            var0 <- -1.1840003561812273
        } else {
            var0 <- -0.99234128317334
        }
    } else {
        var0 <- -1.1934739985732523
    }
    return(var0)
}
subroutine6 <- function(input) {
    if ((input[4]) > (0.45000000000000007)) {
        if ((input[4]) > (1.6500000000000001)) {
            var0 <- -0.06203313079859976
        } else {
            var0 <- 0.11141505233015861
        }
    } else {
        if ((input[3]) > (1.4500000000000002)) {
            var0 <- -0.0720353255122301
        } else {
            var0 <- -0.07164473223425313
        }
    }
    return(var0)
}
subroutine7 <- function(input) {
    if ((input[4]) > (1.6500000000000001)) {
        if ((input[3]) > (5.3500000000000005)) {
            var0 <- -0.9314095846701695
        } else {
            var0 <- -0.9536869036452162
        }
    } else {
        if ((input[3]) > (4.450000000000001)) {
            var0 <- -1.115439610985773
        } else {
            var0 <- -1.1541827744206368
        }
    }
    return(var0)
}
subroutine8 <- function(input) {
    if ((input[3]) > (4.750000000000001)) {
        if ((input[3]) > (5.150000000000001)) {
            var0 <- 0.12968922424213622
        } else {
            var0 <- 0.07468384042736965
        }
    } else {
        if ((input[2]) > (2.7500000000000004)) {
            var0 <- -0.07311533184609437
        } else {
            var0 <- -0.06204412771870974
        }
    }
    return(var0)
}
