score <- function(input) {
    return(((subroutine0(input)) * (0.5)) + ((subroutine1(input)) * (0.5)))
}
subroutine0 <- function(input) {
    if ((input[4]) <= (0.8)) {
        var0 <- c(1.0, 0.0, 0.0)
    } else {
        if ((input[3]) <= (4.8500004)) {
            var0 <- c(0.0, 0.9622641509433962, 0.03773584905660377)
        } else {
            if ((input[4]) <= (1.75)) {
                if ((input[4]) <= (1.6500001)) {
                    var0 <- c(0.0, 0.25, 0.75)
                } else {
                    var0 <- c(0.0, 1.0, 0.0)
                }
            } else {
                var0 <- c(0.0, 0.0, 1.0)
            }
        }
    }
    return(var0)
}
subroutine1 <- function(input) {
    if ((input[4]) <= (0.8)) {
        var0 <- c(1.0, 0.0, 0.0)
    } else {
        if ((input[1]) <= (6.1499996)) {
            if ((input[3]) <= (4.8500004)) {
                var0 <- c(0.0, 0.9090909090909091, 0.09090909090909091)
            } else {
                var0 <- c(0.0, 0.0, 1.0)
            }
        } else {
            if ((input[4]) <= (1.75)) {
                var0 <- c(0.0, 0.8666666666666667, 0.13333333333333333)
            } else {
                var0 <- c(0.0, 0.0, 1.0)
            }
        }
    }
    return(var0)
}
