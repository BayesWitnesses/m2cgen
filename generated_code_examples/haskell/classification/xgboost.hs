module Model where
score :: [Double] -> [Double]
score input =
    [(func2) / (func9), (func5) / (func9), (func8) / (func9)]
    where
        func0 =
            if (((input) !! (2)) >= (2.45))
                then
                    -0.219950154
                else
                    0.430243909
        func1 =
            if (((input) !! (2)) >= (2.45))
                then
                    -0.196918547
                else
                    0.294934332
        func2 =
            exp (((0.5) + (func0)) + (func1))
        func3 =
            if (((input) !! (2)) >= (2.45))
                then
                    if (((input) !! (3)) >= (1.75))
                        then
                            -0.200518161
                        else
                            0.369124442
                else
                    -0.215121984
        func4 =
            if (((input) !! (2)) >= (2.45))
                then
                    if (((input) !! (2)) >= (4.8500004))
                        then
                            -0.148884818
                        else
                            0.279661298
                else
                    -0.191438049
        func5 =
            exp (((0.5) + (func3)) + (func4))
        func6 =
            if (((input) !! (3)) >= (1.6500001))
                then
                    0.402985066
                else
                    if (((input) !! (2)) >= (4.95))
                        then
                            0.217241377
                        else
                            -0.219740286
        func7 =
            if (((input) !! (2)) >= (4.75))
                then
                    if (((input) !! (3)) >= (1.75))
                        then
                            0.286929518
                        else
                            0.0627289712
                else
                    if (((input) !! (3)) >= (1.55))
                        then
                            0.00989914499
                        else
                            -0.196593687
        func8 =
            exp (((0.5) + (func6)) + (func7))
        func9 =
            ((func2) + (func5)) + (func8)
