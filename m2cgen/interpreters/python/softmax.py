def softmax(x):
    m = max(x)
    exps = [math.exp(i - m) for i in x]
    s = sum(exps)
    for idx, _ in enumerate(exps):
        exps[idx] /= s
    return exps
