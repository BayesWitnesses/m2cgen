let private softmax x =
    let maxElem = List.reduce max x
    let exps = List.map (fun i -> exp (i - maxElem)) x
    let sumExps = List.sum exps
    List.map (fun i -> i / sumExps) exps
