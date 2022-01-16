defp softmax(x) do
    max_elem = Enum.max(x)
    exps = for f <- x, do: :math.exp(f-max_elem)
    sum_exps = Enum.sum(exps)
    for i <- exps, do: i/sum_exps
end
