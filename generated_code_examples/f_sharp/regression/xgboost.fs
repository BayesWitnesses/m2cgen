let score (input : double list) =
    let func0 =
        if ((input.[12]) >= (9.725)) then
            if ((input.[12]) >= (16.085)) then
                4.09124994
            else
                5.89006901
        else
            if ((input.[5]) >= (6.941)) then
                11.241127
            else
                7.45130444
    let func1 =
        if ((input.[12]) >= (5.1549997)) then
            if ((input.[12]) >= (14.4)) then
                3.00165963
            else
                4.8301239
        else
            if ((input.[5]) >= (7.406)) then
                9.98775578
            else
                6.78264093
    (0.5) + ((func0) + (func1))
