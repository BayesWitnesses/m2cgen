let score (input : double list) =
    let func0 =
        if ((input.[2]) > (3.1500000000000004)) then
            -1.1736122903444903
        else
            if ((input.[1]) > (3.35)) then
                -0.9486122853153485
            else
                -0.9598622855668056
    let func1 =
        if ((input.[2]) > (3.1500000000000004)) then
            if ((input.[2]) > (4.450000000000001)) then
                -0.07218200074594171
            else
                -0.0725391787456957
        else
            if ((input.[1]) > (3.35)) then
                0.130416969124648
            else
                0.12058330491181404
    let func2 =
        exp ((func0) + (func1))
    let func3 =
        if ((input.[2]) > (1.8)) then
            if ((input.[3]) > (1.6500000000000001)) then
                -1.1840003561812273
            else
                -0.99234128317334
        else
            -1.1934739985732523
    let func4 =
        if ((input.[3]) > (0.45000000000000007)) then
            if ((input.[3]) > (1.6500000000000001)) then
                -0.06203313079859976
            else
                0.11141505233015861
        else
            if ((input.[2]) > (1.4500000000000002)) then
                -0.0720353255122301
            else
                -0.07164473223425313
    let func5 =
        exp ((func3) + (func4))
    let func6 =
        if ((input.[3]) > (1.6500000000000001)) then
            if ((input.[2]) > (5.3500000000000005)) then
                -0.9314095846701695
            else
                -0.9536869036452162
        else
            if ((input.[2]) > (4.450000000000001)) then
                -1.115439610985773
            else
                -1.1541827744206368
    let func7 =
        if ((input.[2]) > (4.750000000000001)) then
            if ((input.[2]) > (5.150000000000001)) then
                0.12968922424213622
            else
                0.07468384042736965
        else
            if ((input.[1]) > (2.7500000000000004)) then
                -0.07311533184609437
            else
                -0.06204412771870974
    let func8 =
        exp ((func6) + (func7))
    let func9 =
        ((func2) + (func5)) + (func8)
    [(func2) / (func9); (func5) / (func9); (func8) / (func9)]
