softmax <- function (x) {
    m <- max(x)
    exps <- exp(x - m)
    s <- sum(exps)
    return(exps / s)
}
