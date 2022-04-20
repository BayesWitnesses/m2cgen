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
            cond do read(input,12) <= 9.724999904632568 ->
                cond do read(input,5) <= 7.437000036239624 ->
                    cond do read(input,7) <= 1.4849499464035034 ->
                        50.0
                    true ->
                        26.681034482758605
                    end
                true ->
                    44.96896551724139
                end
            true ->
                cond do read(input,12) <= 16.085000038146973 ->
                    20.284353741496595
                true ->
                    14.187142857142863
                end
            end
        end
        func0.()
    end
end
