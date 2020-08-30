let private addVectors v1 v2 = List.map2 (+) v1 v2
let private mulVectorNumber v1 num = List.map (fun i -> i * num) v1
