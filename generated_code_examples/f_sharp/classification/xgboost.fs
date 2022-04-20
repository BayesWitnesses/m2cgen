let private softmax x =
    let maxElem = List.reduce max x
    let exps = List.map (fun i -> exp (i - maxElem)) x
    let sumExps = List.sum exps
    List.map (fun i -> i / sumExps) exps
let score (input : double list) =
    let func0 =
        if input.[2] >= 2.45 then
            -0.21995015
        else
            0.4302439
    let func1 =
        if input.[2] >= 2.45 then
            -0.19691855
        else
            0.29493433
    let func2 =
        if input.[2] >= 2.45 then
            if input.[3] >= 1.75 then
                -0.20051816
            else
                0.36912444
        else
            -0.21512198
    let func3 =
        if input.[2] >= 2.45 then
            if input.[2] >= 4.8500004 then
                -0.14888482
            else
                0.2796613
        else
            -0.19143805
    let func4 =
        if input.[3] >= 1.6500001 then
            0.40298507
        else
            if input.[2] >= 4.95 then
                0.21724138
            else
                -0.21974029
    let func5 =
        if input.[2] >= 4.75 then
            if input.[3] >= 1.75 then
                0.28692952
            else
                0.06272897
        else
            if input.[3] >= 1.55 then
                0.009899145
            else
                -0.19659369
    softmax ([0.5 + (func0 + func1); 0.5 + (func2 + func3); 0.5 + (func4 + func5)])
