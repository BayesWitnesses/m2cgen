Module Model
Function Score(ByRef inputVector() As Double) As Double()
    Dim var0() As Double
    If inputVector(3) <= 0.75 Then
        Dim var1(2) As Double
        var1(0) = 1.0
        var1(1) = 0.0
        var1(2) = 0.0
        var0 = var1
    Else
        If inputVector(2) <= 4.75 Then
            Dim var2(2) As Double
            var2(0) = 0.0
            var2(1) = 1.0
            var2(2) = 0.0
            var0 = var2
        Else
            If inputVector(2) <= 5.049999952316284 Then
                If inputVector(3) <= 1.75 Then
                    Dim var3(2) As Double
                    var3(0) = 0.0
                    var3(1) = 0.8333333333333334
                    var3(2) = 0.16666666666666666
                    var0 = var3
                Else
                    Dim var4(2) As Double
                    var4(0) = 0.0
                    var4(1) = 0.08333333333333333
                    var4(2) = 0.9166666666666666
                    var0 = var4
                End If
            Else
                Dim var5(2) As Double
                var5(0) = 0.0
                var5(1) = 0.0
                var5(2) = 1.0
                var0 = var5
            End If
        End If
    End If
    Dim var6() As Double
    If inputVector(3) <= 0.800000011920929 Then
        Dim var7(2) As Double
        var7(0) = 1.0
        var7(1) = 0.0
        var7(2) = 0.0
        var6 = var7
    Else
        If inputVector(0) <= 6.25 Then
            If inputVector(2) <= 4.8500001430511475 Then
                Dim var8(2) As Double
                var8(0) = 0.0
                var8(1) = 0.9487179487179487
                var8(2) = 0.05128205128205128
                var6 = var8
            Else
                Dim var9(2) As Double
                var9(0) = 0.0
                var9(1) = 0.0
                var9(2) = 1.0
                var6 = var9
            End If
        Else
            If inputVector(3) <= 1.550000011920929 Then
                Dim var10(2) As Double
                var10(0) = 0.0
                var10(1) = 0.8333333333333334
                var10(2) = 0.16666666666666666
                var6 = var10
            Else
                Dim var11(2) As Double
                var11(0) = 0.0
                var11(1) = 0.02564102564102564
                var11(2) = 0.9743589743589743
                var6 = var11
            End If
        End If
    End If
    Score = MulVectorNumber(AddVectors(var0, var6), 0.5)
End Function
Function AddVectors(ByRef v1() As Double, ByRef v2() As Double) As Double()
    Dim resLength As Integer
    resLength = UBound(v1) - LBound(v1)
    Dim result() As Double
    ReDim result(resLength)

    Dim i As Integer
    For i = LBound(v1) To UBound(v1)
        result(i) = v1(i) + v2(i)
    Next i

    AddVectors = result
End Function
Function MulVectorNumber(ByRef v1() As Double, ByVal num As Double) As Double()
    Dim resLength As Integer
    resLength = UBound(v1) - LBound(v1)
    Dim result() As Double
    ReDim result(resLength)

    Dim i As Integer
    For i = LBound(v1) To UBound(v1)
        result(i) = v1(i) * num
    Next i

    MulVectorNumber = result
End Function
End Module
