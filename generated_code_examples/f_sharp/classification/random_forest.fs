let private addVectors v1 v2 = List.map2 (+) v1 v2
let private mulVectorNumber v1 num = List.map (fun i -> i * num) v1
let score (input : double list) =
    let func0 =
        if input.[3] <= 0.75 then
            [1.0; 0.0; 0.0]
        else
            if input.[2] <= 4.75 then
                [0.0; 1.0; 0.0]
            else
                if input.[2] <= 5.049999952316284 then
                    if input.[3] <= 1.75 then
                        [0.0; 0.8333333333333334; 0.16666666666666666]
                    else
                        [0.0; 0.08333333333333333; 0.9166666666666666]
                else
                    [0.0; 0.0; 1.0]
    let func1 =
        if input.[3] <= 0.800000011920929 then
            [1.0; 0.0; 0.0]
        else
            if input.[0] <= 6.25 then
                if input.[2] <= 4.8500001430511475 then
                    [0.0; 0.9487179487179487; 0.05128205128205128]
                else
                    [0.0; 0.0; 1.0]
            else
                if input.[3] <= 1.550000011920929 then
                    [0.0; 0.8333333333333334; 0.16666666666666666]
                else
                    [0.0; 0.02564102564102564; 0.9743589743589743]
    mulVectorNumber (addVectors (func0) (func1)) (0.5)
