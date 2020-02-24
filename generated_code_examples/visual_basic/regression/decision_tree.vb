Module Model
Function Score(ByRef inputVector() As Double) As Double
    Dim var0 As Double
    If (inputVector(5)) <= (6.941) Then
        If (inputVector(12)) <= (14.395) Then
            If (inputVector(7)) <= (1.43365) Then
                var0 = 45.58
            Else
                var0 = 22.865022421524642
            End If
        Else
            var0 = 14.924358974358983
        End If
    Else
        If (inputVector(5)) <= (7.4370003) Then
            var0 = 32.09534883720931
        Else
            var0 = 45.275
        End If
    End If
    Score = var0
End Function
End Module
