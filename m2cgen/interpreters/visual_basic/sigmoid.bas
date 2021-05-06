Function Sigmoid(ByVal number As Double) As Double
    If number < 0.0 Then
        Dim z As Double
        z = Math.Exp(number)
        Sigmoid = z / (1.0 + z)
        Exit Function
    End If
    Sigmoid = 1.0 / (1.0 + Math.Exp(-number))
End Function
