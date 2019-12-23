Module Model
Function score(ByRef input_vector() As Double) As Double()
    Dim var0() As Double
    If (input_vector(2)) <= (2.45) Then
        Dim var1(2) As Double
        var1(0) = 1.0
        var1(1) = 0.0
        var1(2) = 0.0
        var0 = var1
    Else
        If (input_vector(3)) <= (1.75) Then
            If (input_vector(2)) <= (4.95) Then
                If (input_vector(3)) <= (1.6500001) Then
                    Dim var2(2) As Double
                    var2(0) = 0.0
                    var2(1) = 1.0
                    var2(2) = 0.0
                    var0 = var2
                Else
                    Dim var3(2) As Double
                    var3(0) = 0.0
                    var3(1) = 0.0
                    var3(2) = 1.0
                    var0 = var3
                End If
            Else
                Dim var4(2) As Double
                var4(0) = 0.0
                var4(1) = 0.3333333333333333
                var4(2) = 0.6666666666666666
                var0 = var4
            End If
        Else
            Dim var5(2) As Double
            var5(0) = 0.0
            var5(1) = 0.021739130434782608
            var5(2) = 0.9782608695652174
            var0 = var5
        End If
    End If
    score = var0
End Function
End Module
