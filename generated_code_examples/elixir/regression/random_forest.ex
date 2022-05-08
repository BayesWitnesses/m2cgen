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
            cond do read(input,12) <= 9.845000267028809 ->
                cond do read(input,5) <= 6.959500074386597 ->
                    cond do read(input,6) <= 96.20000076293945 ->
                        25.093162393162395
                    true ->
                        50.0
                    end
                true ->
                    38.074999999999996
                end
            true ->
                cond do read(input,12) <= 15.074999809265137 ->
                    20.518439716312056
                true ->
                    14.451282051282046
                end
            end
        end
        func1 = fn ->
            cond do read(input,12) <= 9.650000095367432 ->
                cond do read(input,5) <= 7.437000036239624 ->
                    cond do read(input,7) <= 1.47284996509552 ->
                        50.0
                    true ->
                        26.7965317919075
                    end
                true ->
                    44.21176470588236
                end
            true ->
                cond do read(input,12) <= 17.980000495910645 ->
                    19.645652173913035
                true ->
                    12.791919191919195
                end
            end
        end
        (func0.() + func1.()) * 0.5
    end
end
