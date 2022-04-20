Module Model
Function Score(ByRef inputVector() As Double) As Double()
    Dim var0(2) As Double
    var0(0) = 9.700311953536998 + inputVector(0) * -0.4128360473754751 + inputVector(1) * 0.9680426131053453 + inputVector(2) * -2.498310603183548 + inputVector(3) * -1.0723230787022542
    var0(1) = 2.1575759475871163 + inputVector(0) * 0.5400806228605453 + inputVector(1) * -0.3245383349519669 + inputVector(2) * -0.2034493200950831 + inputVector(3) * -0.9338183426196143
    var0(2) = -11.857887901124615 + inputVector(0) * -0.12724457548509432 + inputVector(1) * -0.6435042781533917 + inputVector(2) * 2.7017599232786216 + inputVector(3) * 2.006141421321863
    Score = var0
End Function
End Module
