sigmoid :: Double -> Double
sigmoid x
    | x < 0.0 = z / (1.0 + z)
    | otherwise = 1.0 / (1.0 + exp (-x))
  where
    z = exp x
