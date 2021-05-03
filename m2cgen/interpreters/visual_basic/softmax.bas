Function Softmax(ByRef x() As Double) As Double()
    Dim size As Integer
    size = UBound(x) - LBound(x)
    Dim result() As Double
    ReDim result(size)
    Dim max As Double
    max = x(LBound(x))
    Dim i As Integer
    For i = LBound(x) + 1 To UBound(x)
        If x(i) > max Then
            max = x(i)
        End If
    Next i
    Dim sum As Double
    sum = 0.0
    For i = LBound(x) To UBound(x)
        result(i) = Math.Exp(x(i) - max)
        sum = sum + result(i)
    Next i
    For i = LBound(x) To UBound(x)
        result(i) = result(i) / sum
    Next i
    Softmax = result
End Function
