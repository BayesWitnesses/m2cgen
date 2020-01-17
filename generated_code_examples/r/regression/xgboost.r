score <- function(input) {
    return(subroutine0(input))
}
subroutine0 <- function(input) {
    return(((0.5) + (subroutine1(input))) + (subroutine2(input)))
}
subroutine1 <- function(input) {
    if ((input[13]) >= (9.72500038)) {
        if ((input[13]) >= (16.0849991)) {
            var0 <- 1.36374998
        } else {
            var0 <- 1.96335626
        }
    } else {
        if ((input[6]) >= (6.94099998)) {
            var0 <- 3.74704218
        } else {
            var0 <- 2.48376822
        }
    }
    return(var0)
}
subroutine2 <- function(input) {
    if ((input[13]) >= (9.63000011)) {
        if ((input[13]) >= (19.2299995)) {
            var0 <- 1.05852115
        } else {
            var0 <- 1.68638802
        }
    } else {
        if ((input[6]) >= (7.43700027)) {
            var0 <- 3.95318961
        } else {
            var0 <- 2.40278864
        }
    }
    return(var0)
}
