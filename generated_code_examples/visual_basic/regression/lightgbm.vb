Module Model
Function Score(ByRef inputVector() As Double) As Double
    Dim var0 As Double
    If (inputVector(5)) > (6.8455) Then
        If (inputVector(5)) > (7.437) Then
            var0 = 24.906664851995615
        Else
            var0 = 23.513674700555555
        End If
    Else
        If (inputVector(12)) > (14.395000000000001) Then
            var0 = 21.863487452747595
        Else
            var0 = 22.70305627629392
        End If
    End If
    Dim var1 As Double
    If (inputVector(12)) > (9.63) Then
        If (inputVector(12)) > (19.830000000000002) Then
            var1 = -0.9644646678713786
        Else
            var1 = -0.30629733662250097
        End If
    Else
        If (inputVector(5)) > (7.437) Then
            var1 = 2.0368334157126293
        Else
            var1 = 0.4576204330349962
        End If
    End If
    Score = ((0) + (var0)) + (var1)
End Function
End Module
