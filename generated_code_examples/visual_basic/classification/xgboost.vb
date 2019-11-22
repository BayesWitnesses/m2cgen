Module Model
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
Function score(ByRef input_vector() As Double) As Double()
    Dim var0 As Double
    If (input_vector(2)) >= (2.5999999) Then
        var0 = -0.0731707439
    Else
        var0 = 0.142857149
    End If
    Dim var1 As Double
    If (input_vector(2)) >= (2.5999999) Then
        var1 = -0.0705206916
    Else
        var1 = 0.12477719
    End If
    Dim var2 As Double
    var2 = Math.Exp(((0.5) + (var0)) + (var1))
    Dim var3 As Double
    If (input_vector(2)) >= (2.5999999) Then
        If (input_vector(2)) >= (4.85000038) Then
            var3 = -0.0578680299
        Else
            var3 = 0.132596686
        End If
    Else
        var3 = -0.0714285821
    End If
    Dim var4 As Double
    If (input_vector(2)) >= (2.5999999) Then
        If (input_vector(2)) >= (4.85000038) Then
            var4 = -0.0552999265
        Else
            var4 = 0.116139404
        End If
    Else
        var4 = -0.0687687024
    End If
    Dim var5 As Double
    var5 = Math.Exp(((0.5) + (var3)) + (var4))
    Dim var6 As Double
    If (input_vector(2)) >= (4.85000038) Then
        If (input_vector(3)) >= (1.75) Then
            var6 = 0.142011836
        Else
            var6 = 0.0405405387
        End If
    Else
        If (input_vector(3)) >= (1.6500001) Then
            var6 = 0.0428571403
        Else
            var6 = -0.0730659068
        End If
    End If
    Dim var7 As Double
    If (input_vector(2)) >= (4.85000038) Then
        If (input_vector(3)) >= (1.75) Then
            var7 = 0.124653697
        Else
            var7 = 0.035562478
        End If
    Else
        If (input_vector(3)) >= (1.6500001) Then
            var7 = 0.0425687581
        Else
            var7 = -0.0704230517
        End If
    End If
    Dim var8 As Double
    var8 = Math.Exp(((0.5) + (var6)) + (var7))
    Dim var9 As Double
    var9 = ((var2) + (var5)) + (var8)
    Dim var10(2) As Double
    var10(0) = (var2) / (var9)
    var10(1) = (var5) / (var9)
    var10(2) = (var8) / (var9)
    score = var10
End Function
End Module
