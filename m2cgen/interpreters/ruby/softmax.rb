def softmax(x)
    m = x.max
    exps = []
    s = 0.0
    x.each_with_index do |v, i|
        exps[i] = Math.exp(v - m)
        s += exps[i]
    end
    exps.map { |i| i / s }
end
