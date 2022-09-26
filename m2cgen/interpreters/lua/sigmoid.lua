function sigmoid(x)
    if x < 0.0 then
        local z = math.exp(x)
        return z / (1.0 + z)
    end
    return 1.0 / (1.0 + math.exp(-x))
end
