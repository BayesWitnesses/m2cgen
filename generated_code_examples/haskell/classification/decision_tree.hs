module Model where
score :: [Double] -> [Double]
score input =
    func0
    where
        func0 =
            if (((input) !! (2)) <= (2.45))
                then
                    [1.0, 0.0, 0.0]
                else
                    if (((input) !! (3)) <= (1.75))
                        then
                            if (((input) !! (2)) <= (4.95))
                                then
                                    if (((input) !! (3)) <= (1.6500001))
                                        then
                                            [0.0, 1.0, 0.0]
                                        else
                                            [0.0, 0.0, 1.0]
                                else
                                    [0.0, 0.3333333333333333, 0.6666666666666666]
                        else
                            [0.0, 0.021739130434782608, 0.9782608695652174]
