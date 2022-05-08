Module Model
Function Score(ByRef inputVector() As Double) As Double()
    Dim var0 As Double
    If inputVector(2) >= 2.45 Then
        var0 = -0.21995015
    Else
        var0 = 0.4302439
    End If
    Dim var1 As Double
    If inputVector(2) >= 2.45 Then
        var1 = -0.19691855
    Else
        var1 = 0.29493433
    End If
    Dim var2 As Double
    If inputVector(2) >= 2.45 Then
        If inputVector(3) >= 1.75 Then
            var2 = -0.20051816
        Else
            var2 = 0.36912444
        End If
    Else
        var2 = -0.21512198
    End If
    Dim var3 As Double
    If inputVector(2) >= 2.45 Then
        If inputVector(2) >= 4.8500004 Then
            var3 = -0.14888482
        Else
            var3 = 0.2796613
        End If
    Else
        var3 = -0.19143805
    End If
    Dim var4 As Double
    If inputVector(3) >= 1.6500001 Then
        var4 = 0.40298507
    Else
        If inputVector(2) >= 4.95 Then
            var4 = 0.21724138
        Else
            var4 = -0.21974029
        End If
    End If
    Dim var5 As Double
    If inputVector(2) >= 4.75 Then
        If inputVector(3) >= 1.75 Then
            var5 = 0.28692952
        Else
            var5 = 0.06272897
        End If
    Else
        If inputVector(3) >= 1.55 Then
            var5 = 0.009899145
        Else
            var5 = -0.19659369
        End If
    End If
    Dim var6(2) As Double
    var6(0) = 0.5 + (var0 + var1)
    var6(1) = 0.5 + (var2 + var3)
    var6(2) = 0.5 + (var4 + var5)
    Score = Softmax(var6)
End Function
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
End Module
