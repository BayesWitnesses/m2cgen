Module Model
Function Score(ByRef inputVector() As Double) As Double()
    Dim var0 As Double
    If inputVector(2) > 3.1500000000000004 Then
        var0 = -1.1986122886681099
    Else
        If inputVector(1) > 3.35 Then
            var0 = -0.8986122886681098
        Else
            var0 = -0.9136122886681098
        End If
    End If
    Dim var1 As Double
    If inputVector(2) > 3.1500000000000004 Then
        If inputVector(2) > 4.450000000000001 Then
            var1 = -0.09503010837903424
        Else
            var1 = -0.09563272415214283
        End If
    Else
        If inputVector(1) > 3.35 Then
            var1 = 0.16640323607832397
        Else
            var1 = 0.15374604217339707
        End If
    End If
    Dim var2 As Double
    If inputVector(2) > 1.8 Then
        If inputVector(3) > 1.6500000000000001 Then
            var2 = -1.2055899476674514
        Else
            var2 = -0.9500445227622534
        End If
    Else
        var2 = -1.2182214705715104
    End If
    Dim var3 As Double
    If inputVector(3) > 0.45000000000000007 Then
        If inputVector(3) > 1.6500000000000001 Then
            var3 = -0.08146437273923739
        Else
            var3 = 0.14244886188108738
        End If
    Else
        If inputVector(2) > 1.4500000000000002 Then
            var3 = -0.0950888159264695
        Else
            var3 = -0.09438233722389686
        End If
    End If
    Dim var4 As Double
    If inputVector(3) > 1.6500000000000001 Then
        If inputVector(2) > 5.3500000000000005 Then
            var4 = -0.8824095771015287
        Else
            var4 = -0.9121126703829481
        End If
    Else
        If inputVector(2) > 4.450000000000001 Then
            var4 = -1.1277829563828181
        Else
            var4 = -1.1794405099157212
        End If
    End If
    Dim var5 As Double
    If inputVector(2) > 4.750000000000001 Then
        If inputVector(2) > 5.150000000000001 Then
            var5 = 0.16625543464258166
        Else
            var5 = 0.09608601737074281
        End If
    Else
        If inputVector(0) > 4.950000000000001 Then
            var5 = -0.09644547407948921
        Else
            var5 = -0.08181864271444342
        End If
    End If
    Dim var6(2) As Double
    var6(0) = var0 + var1
    var6(1) = var2 + var3
    var6(2) = var4 + var5
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
