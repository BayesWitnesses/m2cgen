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
            cond do read(input,2) > 3.1500000000000004 ->
                -1.1986122886681099
            true ->
                cond do read(input,1) > 3.35 ->
                    -0.8986122886681098
                true ->
                    -0.9136122886681098
                end
            end
        end
        func1 = fn ->
            cond do read(input,2) > 3.1500000000000004 ->
                cond do read(input,2) > 4.450000000000001 ->
                    -0.09503010837903424
                true ->
                    -0.09563272415214283
                end
            true ->
                cond do read(input,1) > 3.35 ->
                    0.16640323607832397
                true ->
                    0.15374604217339707
                end
            end
        end
        func2 = fn ->
            cond do read(input,2) > 1.8 ->
                cond do read(input,3) > 1.6500000000000001 ->
                    -1.2055899476674514
                true ->
                    -0.9500445227622534
                end
            true ->
                -1.2182214705715104
            end
        end
        func3 = fn ->
            cond do read(input,3) > 0.45000000000000007 ->
                cond do read(input,3) > 1.6500000000000001 ->
                    -0.08146437273923739
                true ->
                    0.14244886188108738
                end
            true ->
                cond do read(input,2) > 1.4500000000000002 ->
                    -0.0950888159264695
                true ->
                    -0.09438233722389686
                end
            end
        end
        func4 = fn ->
            cond do read(input,3) > 1.6500000000000001 ->
                cond do read(input,2) > 5.3500000000000005 ->
                    -0.8824095771015287
                true ->
                    -0.9121126703829481
                end
            true ->
                cond do read(input,2) > 4.450000000000001 ->
                    -1.1277829563828181
                true ->
                    -1.1794405099157212
                end
            end
        end
        func5 = fn ->
            cond do read(input,2) > 4.750000000000001 ->
                cond do read(input,2) > 5.150000000000001 ->
                    0.16625543464258166
                true ->
                    0.09608601737074281
                end
            true ->
                cond do read(input,0) > 4.950000000000001 ->
                    -0.09644547407948921
                true ->
                    -0.08181864271444342
                end
            end
        end
        softmax([func0.() + func1.(), func2.() + func3.(), func4.() + func5.()])
    end
defp softmax(x) do
    max_elem = Enum.max(x)
    exps = for f <- x, do: :math.exp(f-max_elem)
    sum_exps = Enum.sum(exps)
    for i <- exps, do: i/sum_exps
end
end
