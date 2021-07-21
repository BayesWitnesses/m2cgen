def sigmoid(x)
    if x < 0.0
        z = Math.exp(x)
        return z / (1.0 + z)
    end
    1.0 / (1.0 + Math.exp(-x))
end
