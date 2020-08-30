let score (input : double list) =
    let func0 =
        if ((input.[5]) > (6.918000000000001)) then
            if ((input.[5]) > (7.437)) then
                24.81112131071211
            else
                23.5010290754961
        else
            if ((input.[12]) > (14.365)) then
                21.796569516771488
            else
                22.640634908349323
    let func1 =
        if ((input.[12]) > (9.63)) then
            if ((input.[12]) > (19.23)) then
                -0.9218520876020193
            else
                -0.30490175606373926
        else
            if ((input.[5]) > (7.437)) then
                2.028554553190867
            else
                0.45970642160364367
    (func0) + (func1)
