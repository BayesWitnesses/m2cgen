defp softmax(x) do
    max_elem = Enum.max(for <<f::float <- x>>, do: f)
    exps = for <<f::float <- x>>, do: :math.exp(f-max_elem)
    sum_exps = Enum.sum(exps)
    for i <- exps, into: <<>>, do: <<(i/sum_exps)::float>>
end
