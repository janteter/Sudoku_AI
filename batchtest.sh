#!/bin/bash
echo "begining batch test"
finalNum=5
prefixStrArray=("easy" "intermed" "hard" "expert")

for aprefixstr in ${prefixStrArray[@]};do

    echo "Section: ${aprefixstr}"

    for ((i=0;i<finalNum;i++));do
        echo "On $i"
        python3 Sudoku_Python_Shell/src/Main.py FC Sudoku_Generator/${aprefixstr}_${i}.txt >out${aprefixstr}${i}.txt

    done

done

# python3 Sudoku_Python_Shell/src/Main.py FC Sudoku_Generator/expert_0.txt >outexp0.txt
# python3 Sudoku_Python_Shell/src/Main.py FC Sudoku_Generator/expert_1.txt >outexp1.txt
# python3 Sudoku_Python_Shell/src/Main.py FC Sudoku_Generator/expert_2.txt >outexp2.txt
# python3 Sudoku_Python_Shell/src/Main.py FC Sudoku_Generator/expert_3.txt >outexp3.txt
# python3 Sudoku_Python_Shell/src/Main.py FC Sudoku_Generator/expert_4.txt >outexp4.txt

echo "Done"