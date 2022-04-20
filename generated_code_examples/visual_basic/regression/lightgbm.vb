Module Model
Function Score(ByRef inputVector() As Double) As Double
    Dim var0 As Double
    If inputVector(12) > 9.725000000000003 Then
        If inputVector(12) > 16.205000000000002 Then
            var0 = 21.71499740307178
        Else
            var0 = 22.322292901846218
        End If
    Else
        If inputVector(5) > 7.418000000000001 Then
            var0 = 24.75760617150803
        Else
            var0 = 23.02910423871904
        End If
    End If
    Dim var1 As Double
    If inputVector(5) > 6.837500000000001 Then
        If inputVector(5) > 7.462000000000001 Then
            var1 = 2.0245964808123453
        Else
            var1 = 0.859548540618913
        End If
    Else
        If inputVector(12) > 14.365 Then
            var1 = -0.7009440524656984
        Else
            var1 = 0.052794864734003494
        End If
    End If
    Score = var0 + var1
End Function
End Module
