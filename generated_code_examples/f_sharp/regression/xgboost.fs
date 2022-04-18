let score (input : double list) =
    let func0 =
        if input.[12] >= 9.725 then
            if input.[12] >= 19.23 then
                3.5343752
            else
                5.5722494
        else
            if input.[5] >= 6.941 then
                11.1947155
            else
                7.4582143
    let func1 =
        if input.[12] >= 5.1549997 then
            if input.[12] >= 15.0 then
                2.8350503
            else
                4.8024607
        else
            if input.[5] >= 7.406 then
                10.0011215
            else
                6.787523
    0.5 + (func0 + func1)
