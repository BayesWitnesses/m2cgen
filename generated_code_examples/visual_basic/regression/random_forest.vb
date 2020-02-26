Module Model
Function Score(ByRef inputVector() As Double) As Double
    Dim var0 As Double
    If (inputVector(5)) <= (6.92) Then
        If (inputVector(12)) <= (14.3) Then
            If (inputVector(7)) <= (1.47415) Then
                var0 = 50.0
            Else
                var0 = 23.203669724770638
            End If
        Else
            var0 = 15.177333333333326
        End If
    Else
        If (inputVector(5)) <= (7.4370003) Then
            var0 = 32.92407407407408
        Else
            var0 = 45.04827586206897
        End If
    End If
    Dim var1 As Double
    If (inputVector(12)) <= (9.725) Then
        If (inputVector(5)) <= (7.4525) Then
            If (inputVector(5)) <= (6.7539997) Then
                var1 = 24.805
            Else
                var1 = 32.55238095238095
            End If
        Else
            var1 = 47.88333333333334
        End If
    Else
        If (inputVector(12)) <= (15.0) Then
            var1 = 20.52100840336134
        Else
            var1 = 14.718709677419358
        End If
    End If
    Score = ((var0) * (0.5)) + ((var1) * (0.5))
End Function
End Module
