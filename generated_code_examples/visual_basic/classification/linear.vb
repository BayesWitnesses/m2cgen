Module Model
Function Score(ByRef inputVector() As Double) As Double()
    Dim var0(2) As Double
    var0(0) = ((((9.699944289095386) + ((inputVector(0)) * (-0.4130233139914477))) + ((inputVector(1)) * (0.9683469583830324))) + ((inputVector(2)) * (-2.4984059588369045))) + ((inputVector(3)) * (-1.0715202355664082))
    var0(1) = ((((2.1566741402654785) + ((inputVector(0)) * (0.5401926550713264))) + ((inputVector(1)) * (-0.32448882769641735))) + ((inputVector(2)) * (-0.20330362136041338))) + ((inputVector(3)) * (-0.9342738330217771))
    var0(2) = ((((-11.856618429361765) + ((inputVector(0)) * (-0.12716934107987374))) + ((inputVector(1)) * (-0.6438581306866125))) + ((inputVector(2)) * (2.701709580197313))) + ((inputVector(3)) * (2.0057940685881865))
    Score = var0
End Function
End Module
