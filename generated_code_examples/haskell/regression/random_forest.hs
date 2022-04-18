module Model where
score :: [Double] -> Double
score input =
    (func0 + func1) * 0.5
    where
        func0 =
            if input !! 12 <= 9.845000267028809 then
                if input !! 5 <= 6.959500074386597 then
                    if input !! 6 <= 96.20000076293945 then
                        25.093162393162395
                    else
                        50.0
                else
                    38.074999999999996
            else
                if input !! 12 <= 15.074999809265137 then
                    20.518439716312056
                else
                    14.451282051282046
        func1 =
            if input !! 12 <= 9.650000095367432 then
                if input !! 5 <= 7.437000036239624 then
                    if input !! 7 <= 1.47284996509552 then
                        50.0
                    else
                        26.7965317919075
                else
                    44.21176470588236
            else
                if input !! 12 <= 17.980000495910645 then
                    19.645652173913035
                else
                    12.791919191919195
