defp sigmoid(x) do
    1.0 / (1.0 + :math.exp(-x))
end
