Module Model
Function Score(ByRef inputVector() As Double) As Double()
    Dim var0(2) As Double
    var0(0) = ((((0.2614587435880605) + ((inputVector(0)) * (0.42474116053569605))) + ((inputVector(1)) * (1.3963906033045026))) + ((inputVector(2)) * (-2.215054318516674))) + ((inputVector(3)) * (-0.9587396176450289))
    var0(1) = ((((1.1348839223808307) + ((inputVector(0)) * (0.2567965976997648))) + ((inputVector(1)) * (-1.3904789369836008))) + ((inputVector(2)) * (0.596683023311173))) + ((inputVector(3)) * (-1.2690022726388828))
    var0(2) = ((((-1.2162802012560197) + ((inputVector(0)) * (-1.6357766989177105))) + ((inputVector(1)) * (-1.5040638728422817))) + ((inputVector(2)) * (2.427835933129272))) + ((inputVector(3)) * (2.3469310693367276))
    Score = var0
End Function
End Module
