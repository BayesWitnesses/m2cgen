Function ChebyshevBroucke(ByVal x As Double, _
                          ByRef coeffs() As Double) As Double
    Dim b2 as Double
    Dim b1 as Double
    Dim b0 as Double
    Dim x2 as Double
    b2 = 0.0
    b1 = 0.0
    b0 = 0.0
    x2 = x * 2
    Dim i as Integer
    For i = UBound(coeffs) - 1 To 0 Step -1
        b2 = b1
        b1 = b0
        b0 = x2 * b1 - b2 + coeffs(i)
    Next i
    ChebyshevBroucke = (b0 - b2) * 0.5
End Function
Function Log1p(ByVal x As Double) As Double
    If x = 0.0 Then
        Log1p = 0.0
        Exit Function
    End If
    If x = -1.0 Then
        On Error Resume Next
        Log1p = -1.0 / 0.0
        Exit Function
    End If
    If x < -1.0 Then
        On Error Resume Next
        Log1p = 0.0 / 0.0
        Exit Function
    End If
    Dim xAbs As Double
    xAbs = Math.Abs(x)
    If xAbs < 0.5 * 4.94065645841247e-324 Then
        Log1p = x
        Exit Function
    End If
    If (x > 0.0 AND x < 1e-8) OR (x > -1e-9 AND x < 0.0) Then
        Log1p = x * (1.0 - x * 0.5)
        Exit Function
    End If
    If xAbs < 0.375 Then
        Dim coeffs(22) As Double
        coeffs(0)  =  0.10378693562743769800686267719098e+1
        coeffs(1)  = -0.13364301504908918098766041553133e+0
        coeffs(2)  =  0.19408249135520563357926199374750e-1
        coeffs(3)  = -0.30107551127535777690376537776592e-2
        coeffs(4)  =  0.48694614797154850090456366509137e-3
        coeffs(5)  = -0.81054881893175356066809943008622e-4
        coeffs(6)  =  0.13778847799559524782938251496059e-4
        coeffs(7)  = -0.23802210894358970251369992914935e-5
        coeffs(8)  =  0.41640416213865183476391859901989e-6
        coeffs(9)  = -0.73595828378075994984266837031998e-7
        coeffs(10) =  0.13117611876241674949152294345011e-7
        coeffs(11) = -0.23546709317742425136696092330175e-8
        coeffs(12) =  0.42522773276034997775638052962567e-9
        coeffs(13) = -0.77190894134840796826108107493300e-10
        coeffs(14) =  0.14075746481359069909215356472191e-10
        coeffs(15) = -0.25769072058024680627537078627584e-11
        coeffs(16) =  0.47342406666294421849154395005938e-12
        coeffs(17) = -0.87249012674742641745301263292675e-13
        coeffs(18) =  0.16124614902740551465739833119115e-13
        coeffs(19) = -0.29875652015665773006710792416815e-14
        coeffs(20) =  0.55480701209082887983041321697279e-15
        coeffs(21) = -0.10324619158271569595141333961932e-15
        Log1p = x * (1.0 - x * ChebyshevBroucke(x / 0.375, coeffs))
        Exit Function
    End If
    Log1p = Math.log(1.0 + x)
End Function
