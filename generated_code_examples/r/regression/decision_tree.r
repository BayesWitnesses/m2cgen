score <- function(input) {
    if ((input[6]) <= (6.941)) {
        if ((input[13]) <= (14.4)) {
            if ((input[8]) <= (1.38485)) {
                var0 <- 45.58
            } else {
                var0 <- 22.939004149377574
            }
        } else {
            var0 <- 14.910404624277467
        }
    } else {
        if ((input[6]) <= (7.4370003)) {
            var0 <- 32.11304347826088
        } else {
            var0 <- 45.096666666666664
        }
    }
    return(var0)
}
