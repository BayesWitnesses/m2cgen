defmodule Model do
    @compile {:inline, read: 2}
    defp read(bin, pos) do
        <<_::size(pos)-unit(64)-binary, value::float, _::binary>> = bin
        value
    end
    defp list_to_binary(list) do
        for i <- list, into: <<>>, do: <<i::float>>
    end
    def score(input) do
        input = list_to_binary(input)
        func0 = fn ->
            cond do read(input,2) >= 2.45 ->
                -0.21995015
            true ->
                0.4302439
            end
        end
        func1 = fn ->
            cond do read(input,2) >= 2.45 ->
                -0.19691855
            true ->
                0.29493433
            end
        end
        func2 = fn ->
            cond do read(input,2) >= 2.45 ->
                cond do read(input,3) >= 1.75 ->
                    -0.20051816
                true ->
                    0.36912444
                end
            true ->
                -0.21512198
            end
        end
        func3 = fn ->
            cond do read(input,2) >= 2.45 ->
                cond do read(input,2) >= 4.8500004 ->
                    -0.14888482
                true ->
                    0.2796613
                end
            true ->
                -0.19143805
            end
        end
        func4 = fn ->
            cond do read(input,3) >= 1.6500001 ->
                0.40298507
            true ->
                cond do read(input,2) >= 4.95 ->
                    0.21724138
                true ->
                    -0.21974029
                end
            end
        end
        func5 = fn ->
            cond do read(input,2) >= 4.75 ->
                cond do read(input,3) >= 1.75 ->
                    0.28692952
                true ->
                    0.06272897
                end
            true ->
                cond do read(input,3) >= 1.55 ->
                    0.009899145
                true ->
                    -0.19659369
                end
            end
        end
        softmax([0.5 + (func0.() + func1.()), 0.5 + (func2.() + func3.()), 0.5 + (func4.() + func5.())])
    end
defp softmax(x) do
    max_elem = Enum.max(x)
    exps = for f <- x, do: :math.exp(f-max_elem)
    sum_exps = Enum.sum(exps)
    for i <- exps, do: i/sum_exps
end
end
