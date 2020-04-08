addVectors :: [Double] -> [Double] -> [Double]
addVectors v1 v2 = zipWith (+) v1 v2
mulVectorNumber :: [Double] -> Double -> [Double]
mulVectorNumber v1 num = [i * num | i <- v1]
