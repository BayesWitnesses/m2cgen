let score (input : double list) =
    let func0 =
        if ((input.[12]) <= (8.91)) then
            if ((input.[5]) <= (6.902)) then
                if ((input.[7]) <= (1.48495)) then
                    50.0
                else
                    25.320000000000004
            else
                38.34810126582279
        else
            if ((input.[0]) <= (5.84803)) then
                19.99185520361991
            else
                12.102469135802467
    let func1 =
        if ((input.[12]) <= (9.725)) then
            if ((input.[5]) <= (7.4525)) then
                if ((input.[5]) <= (6.7539997)) then
                    24.801739130434775
                else
                    32.47230769230769
            else
                47.075
        else
            if ((input.[12]) <= (15.0)) then
                20.44094488188976
            else
                14.823214285714291
    ((func0) + (func1)) * (0.5)
