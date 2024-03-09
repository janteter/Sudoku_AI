#!/bin/bash
echo "begining batch test for Justin Boards"
finalNum=50
prefixStrArray=("expert")
argsParam="NOR MRV LCV"

trimmed_string=$(echo $argsParam | tr -d ' ')

for aprefixstr in ${prefixStrArray[@]};do

    echo "Section: ${aprefixstr}"

    for ((i=0;i<finalNum;i++));do
        echo "On $i"

        { time python3 Sudoku_Python_Shell/src/Main.py ${argsParam} Sudoku_Generator/JustinBoards/${aprefixstr}_${i}.txt >out${trimmed_string}${aprefixstr}${i}.txt ; } 2> time${trimmed_string}${aprefixstr}${i}.txt

    done

done

echo "Done"