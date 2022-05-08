module Model where
score :: [Double] -> [Double]
score input =
    softmax ([func0 + func1, func2 + func3, func4 + func5])
    where
        func0 =
            if input !! 2 > 3.1500000000000004 then
                (-1.1986122886681099)
            else
                if input !! 1 > 3.35 then
                    (-0.8986122886681098)
                else
                    (-0.9136122886681098)
        func1 =
            if input !! 2 > 3.1500000000000004 then
                if input !! 2 > 4.450000000000001 then
                    (-0.09503010837903424)
                else
                    (-0.09563272415214283)
            else
                if input !! 1 > 3.35 then
                    0.16640323607832397
                else
                    0.15374604217339707
        func2 =
            if input !! 2 > 1.8 then
                if input !! 3 > 1.6500000000000001 then
                    (-1.2055899476674514)
                else
                    (-0.9500445227622534)
            else
                (-1.2182214705715104)
        func3 =
            if input !! 3 > 0.45000000000000007 then
                if input !! 3 > 1.6500000000000001 then
                    (-0.08146437273923739)
                else
                    0.14244886188108738
            else
                if input !! 2 > 1.4500000000000002 then
                    (-0.0950888159264695)
                else
                    (-0.09438233722389686)
        func4 =
            if input !! 3 > 1.6500000000000001 then
                if input !! 2 > 5.3500000000000005 then
                    (-0.8824095771015287)
                else
                    (-0.9121126703829481)
            else
                if input !! 2 > 4.450000000000001 then
                    (-1.1277829563828181)
                else
                    (-1.1794405099157212)
        func5 =
            if input !! 2 > 4.750000000000001 then
                if input !! 2 > 5.150000000000001 then
                    0.16625543464258166
                else
                    0.09608601737074281
            else
                if input !! 0 > 4.950000000000001 then
                    (-0.09644547407948921)
                else
                    (-0.08181864271444342)
softmax :: [Double] -> [Double]
softmax x =
    let
        m = maximum x
        exps = map (\i -> exp (i - m)) x
        sumExps = sum exps
    in map (\i -> i / sumExps) exps
