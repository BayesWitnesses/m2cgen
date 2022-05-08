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
            cond do read(input,12) > 9.725000000000003 ->
                cond do read(input,12) > 16.205000000000002 ->
                    21.71499740307178
                true ->
                    22.322292901846218
                end
            true ->
                cond do read(input,5) > 7.418000000000001 ->
                    24.75760617150803
                true ->
                    23.02910423871904
                end
            end
        end
        func1 = fn ->
            cond do read(input,5) > 6.837500000000001 ->
                cond do read(input,5) > 7.462000000000001 ->
                    2.0245964808123453
                true ->
                    0.859548540618913
                end
            true ->
                cond do read(input,12) > 14.365 ->
                    -0.7009440524656984
                true ->
                    0.052794864734003494
                end
            end
        end
        func0.() + func1.()
    end
end
