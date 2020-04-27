module Model where
score :: [Double] -> Double
score input =
    func0
    where
        func0 =
            if (((input) !! (5)) <= (6.941))
                then
                    if (((input) !! (12)) <= (14.4))
                        then
                            if (((input) !! (7)) <= (1.38485))
                                then
                                    45.58
                                else
                                    22.939004149377574
                        else
                            14.910404624277467
                else
                    if (((input) !! (5)) <= (7.4370003))
                        then
                            32.11304347826088
                        else
                            45.096666666666664
