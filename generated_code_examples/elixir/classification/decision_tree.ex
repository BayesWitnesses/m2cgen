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
            cond do read(input,2) <= 2.449999988079071 ->
                [1.0, 0.0, 0.0]
            true ->
                cond do read(input,3) <= 1.75 ->
                    cond do read(input,2) <= 4.950000047683716 ->
                        cond do read(input,3) <= 1.6500000357627869 ->
                            [0.0, 1.0, 0.0]
                        true ->
                            [0.0, 0.0, 1.0]
                        end
                    true ->
                        [0.0, 0.3333333333333333, 0.6666666666666666]
                    end
                true ->
                    [0.0, 0.021739130434782608, 0.9782608695652174]
                end
            end
        end
        func0.()
    end
end
