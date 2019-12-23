Module Model
Function addVectors(ByRef v1() As Double, ByRef v2() As Double) As Double()
    Dim resLength As Integer
    resLength = UBound(v1) - LBound(v1)
    Dim result() As Double
    ReDim result(resLength)

    Dim i As Integer
    For i = LBound(v1) To UBound(v1)
        result(i) = v1(i) + v2(i)
    Next i

    addVectors = result
End Function
Function mulVectorNumber(ByRef v1() As Double, ByVal num As Double) As Double()
    Dim resLength As Integer
    resLength = UBound(v1) - LBound(v1)
    Dim result() As Double
    ReDim result(resLength)

    Dim i As Integer
    For i = LBound(v1) To UBound(v1)
        result(i) = v1(i) * num
    Next i

    mulVectorNumber = result
End Function
Function score(ByRef input_vector() As Double) As Double()
    Dim var0() As Double
    If (input_vector(3)) <= (0.8) Then
        Dim var1(2) As Double
        var1(0) = 1.0
        var1(1) = 0.0
        var1(2) = 0.0
        var0 = var1
    Else
        If (input_vector(2)) <= (4.8500004) Then
            Dim var2(2) As Double
            var2(0) = 0.0
            var2(1) = 0.9622641509433962
            var2(2) = 0.03773584905660377
            var0 = var2
        Else
            If (input_vector(3)) <= (1.75) Then
                If (input_vector(3)) <= (1.6500001) Then
                    Dim var3(2) As Double
                    var3(0) = 0.0
                    var3(1) = 0.25
                    var3(2) = 0.75
                    var0 = var3
                Else
                    Dim var4(2) As Double
                    var4(0) = 0.0
                    var4(1) = 1.0
                    var4(2) = 0.0
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
    If (input_vector(3)) <= (0.8) Then
        Dim var7(2) As Double
        var7(0) = 1.0
        var7(1) = 0.0
        var7(2) = 0.0
        var6 = var7
    Else
        If (input_vector(0)) <= (6.1499996) Then
            If (input_vector(2)) <= (4.8500004) Then
                Dim var8(2) As Double
                var8(0) = 0.0
                var8(1) = 0.9090909090909091
                var8(2) = 0.09090909090909091
                var6 = var8
            Else
                Dim var9(2) As Double
                var9(0) = 0.0
                var9(1) = 0.0
                var9(2) = 1.0
                var6 = var9
            End If
        Else
            If (input_vector(3)) <= (1.75) Then
                Dim var10(2) As Double
                var10(0) = 0.0
                var10(1) = 0.8666666666666667
                var10(2) = 0.13333333333333333
                var6 = var10
            Else
                Dim var11(2) As Double
                var11(0) = 0.0
                var11(1) = 0.0
                var11(2) = 1.0
                var6 = var11
            End If
        End If
    End If
    score = addVectors(mulVectorNumber(var0, 0.5), mulVectorNumber(var6, 0.5))
End Function
End Module
