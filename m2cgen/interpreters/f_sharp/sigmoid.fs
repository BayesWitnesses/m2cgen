let private sigmoid x =
    let z = exp x
    match x with
        | i when i < 0.0 -> z / (1.0 + z)
        | _ -> 1.0 / (1.0 + exp (-x))
