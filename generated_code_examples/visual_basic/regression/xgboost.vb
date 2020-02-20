Module Model
Function Score(ByRef inputVector() As Double) As Double
    Dim var0 As Double
    If (inputVector(12)) >= (9.72500038) Then
        If (inputVector(12)) >= (19.8299999) Then
            var0 = 1.1551429
        Else
            var0 = 1.8613131
        End If
    Else
        If (inputVector(5)) >= (6.94099998) Then
            var0 = 3.75848508
        Else
            var0 = 2.48056006
        End If
    End If
    Dim var1 As Double
    If (inputVector(12)) >= (7.68499994) Then
        If (inputVector(12)) >= (15) Then
            var1 = 1.24537706
        Else
            var1 = 1.92129695
        End If
    Else
        If (inputVector(5)) >= (7.43700027) Then
            var1 = 3.96021533
        Else
            var1 = 2.51493931
        End If
    End If
    Score = ((0.5) + (var0)) + (var1)
End Function
End Module
