Module Model
Function score(ByRef input_vector() As Double) As Double()
    Dim var0 As Double
    If (input_vector(2)) > (1.8) Then
        If (input_vector(2)) > (4.250000000000001) Then
            var0 = -1.1736122903444903
        Else
            var0 = -1.1633850173886202
        End If
    Else
        var0 = -0.9486122853153485
    End If
    Dim var1 As Double
    If (input_vector(2)) > (1.8) Then
        If (input_vector(1)) > (3.0500000000000003) Then
            var1 = -0.06193194743580539
        Else
            var1 = -0.07237070828653688
        End If
    Else
        var1 = 0.12984943093573026
    End If
    Dim var2 As Double
    var2 = Math.Exp(((0) + (var0)) + (var1))
    Dim var3 As Double
    If (input_vector(2)) > (1.8) Then
        If (input_vector(2)) > (4.8500000000000005) Then
            var3 = -1.1807342692411888
        Else
            var3 = -0.9831932134295853
        End If
    Else
        var3 = -1.1952609652674462
    End If
    Dim var4 As Double
    If (input_vector(2)) > (1.8) Then
        If (input_vector(2)) > (4.8500000000000005) Then
            var4 = -0.05694282927518771
        Else
            var4 = 0.11960489254350348
        End If
    Else
        var4 = -0.07151978915296087
    End If
    Dim var5 As Double
    var5 = Math.Exp(((0) + (var3)) + (var4))
    Dim var6 As Double
    If (input_vector(2)) > (4.8500000000000005) Then
        If (input_vector(3)) > (1.9500000000000002) Then
            var6 = -0.9298942558407184
        Else
            var6 = -0.9632815288936335
        End If
    Else
        If (input_vector(2)) > (4.250000000000001) Then
            var6 = -1.1322413652523249
        Else
            var6 = -1.1524760761934856
        End If
    End If
    Dim var7 As Double
    If (input_vector(2)) > (4.8500000000000005) Then
        If (input_vector(3)) > (1.9500000000000002) Then
            var7 = 0.12809276954555665
        Else
            var7 = 0.09898817876916756
        End If
    Else
        If (input_vector(2)) > (4.250000000000001) Then
            var7 = -0.052710589717642864
        Else
            var7 = -0.07292857712854424
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
