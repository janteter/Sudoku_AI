#!/bin/bash
echo "begining Instructor batch test"

#Variables
finalNum=9
#"intermediate_board" "hard_board" "z_expert_board"
prefixStrArray=("easy_board" "intermediate_board" "hard_board" "z_expert_board")
argsParam="MRV LCV FC"

trimmed_string=$(echo $argsParam | tr -d ' ')

for aprefixstr in ${prefixStrArray[@]};do

    echo "Section: ${aprefixstr}"

    for ((i=0;i<finalNum;i++));do
        echo "On $i"

        { time python3 Sudoku_Python_Shell/src/Main.py ${argsParam} Sudoku_Generator/InstructorBoards/${aprefixstr}_${i}.txt >out${trimmed_string}${aprefixstr}${i}.txt ; } 2> time${trimmed_string}${aprefixstr}${i}.txt

    done

done

echo "Done"