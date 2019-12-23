Module Model
Function score(ByRef input_vector() As Double) As Double()
    Dim var0 As Double
    If (input_vector(2)) >= (2.45000005) Then
        var0 = -0.0733167157
    Else
        var0 = 0.143414631
    End If
    Dim var1 As Double
    If (input_vector(2)) >= (2.45000005) Then
        var1 = -0.0706516728
    Else
        var1 = 0.125176534
    End If
    Dim var2 As Double
    var2 = Math.Exp(((0.5) + (var0)) + (var1))
    Dim var3 As Double
    If (input_vector(2)) >= (2.45000005) Then
        If (input_vector(3)) >= (1.75) Then
            var3 = -0.0668393895
        Else
            var3 = 0.123041473
        End If
    Else
        var3 = -0.0717073306
    End If
    Dim var4 As Double
    If (input_vector(2)) >= (2.45000005) Then
        If (input_vector(3)) >= (1.75) Then
            var4 = -0.0642274022
        Else
            var4 = 0.10819874
        End If
    Else
        var4 = -0.069036141
    End If
    Dim var5 As Double
    var5 = Math.Exp(((0.5) + (var3)) + (var4))
    Dim var6 As Double
    If (input_vector(3)) >= (1.6500001) Then
        var6 = 0.13432835
    Else
        If (input_vector(2)) >= (4.94999981) Then
            var6 = 0.0724137947
        Else
            var6 = -0.0732467622
        End If
    End If
    Dim var7 As Double
    If (input_vector(3)) >= (1.6500001) Then
        var7 = 0.117797568
    Else
        If (input_vector(2)) >= (4.94999981) Then
            var7 = 0.0702545047
        Else
            var7 = -0.0706570372
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
