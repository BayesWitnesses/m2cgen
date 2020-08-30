let private addVectors v1 v2 = List.map2 (+) v1 v2
let private mulVectorNumber v1 num = List.map (fun i -> i * num) v1
let score (input : double list) =
    let func0 =
        if ((input.[3]) <= (0.8)) then
            [1.0; 0.0; 0.0]
        else
            if ((input.[2]) <= (4.8500004)) then
                [0.0; 0.9622641509433962; 0.03773584905660377]
            else
                if ((input.[3]) <= (1.75)) then
                    if ((input.[3]) <= (1.6500001)) then
                        [0.0; 0.25; 0.75]
                    else
                        [0.0; 1.0; 0.0]
                else
                    [0.0; 0.0; 1.0]
    let func1 =
        if ((input.[3]) <= (0.8)) then
            [1.0; 0.0; 0.0]
        else
            if ((input.[0]) <= (6.1499996)) then
                if ((input.[2]) <= (4.8500004)) then
                    [0.0; 0.9090909090909091; 0.09090909090909091]
                else
                    [0.0; 0.0; 1.0]
            else
                if ((input.[3]) <= (1.75)) then
                    [0.0; 0.8666666666666667; 0.13333333333333333]
                else
                    [0.0; 0.0; 1.0]
    mulVectorNumber (addVectors (func0) (func1)) (0.5)
