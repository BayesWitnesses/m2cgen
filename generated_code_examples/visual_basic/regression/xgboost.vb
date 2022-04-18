Module Model
Function Score(ByRef inputVector() As Double) As Double
    Dim var0 As Double
    If inputVector(12) >= 9.725 Then
        If inputVector(12) >= 19.23 Then
            var0 = 3.5343752
        Else
            var0 = 5.5722494
        End If
    Else
        If inputVector(5) >= 6.941 Then
            var0 = 11.1947155
        Else
            var0 = 7.4582143
        End If
    End If
    Dim var1 As Double
    If inputVector(12) >= 5.1549997 Then
        If inputVector(12) >= 15.0 Then
            var1 = 2.8350503
        Else
            var1 = 4.8024607
        End If
    Else
        If inputVector(5) >= 7.406 Then
            var1 = 10.0011215
        Else
            var1 = 6.787523
        End If
    End If
    Score = 0.5 + (var0 + var1)
End Function
End Module
