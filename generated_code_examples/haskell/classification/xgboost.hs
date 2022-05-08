module Model where
score :: [Double] -> [Double]
score input =
    softmax ([0.5 + (func0 + func1), 0.5 + (func2 + func3), 0.5 + (func4 + func5)])
    where
        func0 =
            if input !! 2 >= 2.45 then
                (-0.21995015)
            else
                0.4302439
        func1 =
            if input !! 2 >= 2.45 then
                (-0.19691855)
            else
                0.29493433
        func2 =
            if input !! 2 >= 2.45 then
                if input !! 3 >= 1.75 then
                    (-0.20051816)
                else
                    0.36912444
            else
                (-0.21512198)
        func3 =
            if input !! 2 >= 2.45 then
                if input !! 2 >= 4.8500004 then
                    (-0.14888482)
                else
                    0.2796613
            else
                (-0.19143805)
        func4 =
            if input !! 3 >= 1.6500001 then
                0.40298507
            else
                if input !! 2 >= 4.95 then
                    0.21724138
                else
                    (-0.21974029)
        func5 =
            if input !! 2 >= 4.75 then
                if input !! 3 >= 1.75 then
                    0.28692952
                else
                    0.06272897
            else
                if input !! 3 >= 1.55 then
                    0.009899145
                else
                    (-0.19659369)
softmax :: [Double] -> [Double]
softmax x =
    let
        m = maximum x
        exps = map (\i -> exp (i - m)) x
        sumExps = sum exps
    in map (\i -> i / sumExps) exps
