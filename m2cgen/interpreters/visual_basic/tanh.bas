Function Tanh(ByVal number As Double) As Double
    If number > 44.0 Then  ' exp(2*x) <= 2^127
        Tanh = 1.0
        Exit Function
    End If
    If number < -44.0 Then
        Tanh = -1.0
        Exit Function
    End If
    Tanh = (Math.Exp(2 * number) - 1) / (Math.Exp(2 * number) + 1)
End Function
