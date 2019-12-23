Module Model
Function score(ByRef input_vector() As Double) As Double()
    Dim var0 As Double
    If (input_vector(2)) > (3.1500000000000004) Then
        var0 = -1.1736122903444903
    Else
        If (input_vector(1)) > (3.35) Then
            var0 = -0.9486122853153485
        Else
            var0 = -0.9598622855668056
        End If
    End If
    Dim var1 As Double
    If (input_vector(2)) > (3.1500000000000004) Then
        If (input_vector(2)) > (4.450000000000001) Then
            var1 = -0.07218200074594171
        Else
            var1 = -0.0725391787456957
        End If
    Else
        If (input_vector(1)) > (3.35) Then
            var1 = 0.130416969124648
        Else
            var1 = 0.12058330491181404
        End If
    End If
    Dim var2 As Double
    var2 = Math.Exp(((0) + (var0)) + (var1))
    Dim var3 As Double
    If (input_vector(2)) > (1.8) Then
        If (input_vector(3)) > (1.6500000000000001) Then
            var3 = -1.1840003561812273
        Else
            var3 = -0.99234128317334
        End If
    Else
        var3 = -1.1934739985732523
    End If
    Dim var4 As Double
    If (input_vector(3)) > (0.45000000000000007) Then
        If (input_vector(3)) > (1.6500000000000001) Then
            var4 = -0.06203313079859976
        Else
            var4 = 0.11141505233015861
        End If
    Else
        If (input_vector(2)) > (1.4500000000000002) Then
            var4 = -0.0720353255122301
        Else
            var4 = -0.07164473223425313
        End If
    End If
    Dim var5 As Double
    var5 = Math.Exp(((0) + (var3)) + (var4))
    Dim var6 As Double
    If (input_vector(3)) > (1.6500000000000001) Then
        If (input_vector(2)) > (5.3500000000000005) Then
            var6 = -0.9314095846701695
        Else
            var6 = -0.9536869036452162
        End If
    Else
        If (input_vector(2)) > (4.450000000000001) Then
            var6 = -1.115439610985773
        Else
            var6 = -1.1541827744206368
        End If
    End If
    Dim var7 As Double
    If (input_vector(2)) > (4.750000000000001) Then
        If (input_vector(2)) > (5.150000000000001) Then
            var7 = 0.12968922424213622
        Else
            var7 = 0.07468384042736965
        End If
    Else
        If (input_vector(1)) > (2.7500000000000004) Then
            var7 = -0.07311533184609437
        Else
            var7 = -0.06204412771870974
        End If
    End If
    Dim var8 As Double
    var8 = Math.Exp(((0) + (var6)) + (var7))
    Dim var9 As Double
    var9 = ((var2) + (var5)) + (var8)
    Dim var10(2) As Double
    var10(0) = (var2) / (var9)
    var10(1) = (var5) / (var9)
    var10(2) = (var8) / (var9)
    score = var10
End Function
End Module
