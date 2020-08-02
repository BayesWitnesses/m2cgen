softmax :: [Double] -> [Double]
softmax x =
    let
        m = maximum x
        exps = map (\i -> exp (i - m)) x
        sumExps = sum exps
    in map (\i -> i / sumExps) exps
