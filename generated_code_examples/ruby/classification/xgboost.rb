def score(input)
    if (input[2]) >= (2.45)
        var0 = -0.219950154
    else
        var0 = 0.430243909
    end
    if (input[2]) >= (2.45)
        var1 = -0.196918547
    else
        var1 = 0.294934332
    end
    var2 = Math.exp(((0.5) + (var0)) + (var1))
    if (input[2]) >= (2.45)
        if (input[3]) >= (1.75)
            var3 = -0.200518161
        else
            var3 = 0.369124442
        end
    else
        var3 = -0.215121984
    end
    if (input[2]) >= (2.45)
        if (input[2]) >= (4.8500004)
            var4 = -0.148884818
        else
            var4 = 0.279661298
        end
    else
        var4 = -0.191438049
    end
    var5 = Math.exp(((0.5) + (var3)) + (var4))
    if (input[3]) >= (1.6500001)
        var6 = 0.402985066
    else
        if (input[2]) >= (4.95)
            var6 = 0.217241377
        else
            var6 = -0.219740286
        end
    end
    if (input[2]) >= (4.75)
        if (input[3]) >= (1.75)
            var7 = 0.286929518
        else
            var7 = 0.0627289712
        end
    else
        if (input[3]) >= (1.55)
            var7 = 0.00989914499
        else
            var7 = -0.196593687
        end
    end
    var8 = Math.exp(((0.5) + (var6)) + (var7))
    var9 = ((var2) + (var5)) + (var8)
    [(var2).fdiv(var9), (var5).fdiv(var9), (var8).fdiv(var9)]
end
