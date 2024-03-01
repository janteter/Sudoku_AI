#!/bin/bash
echo "begining Instructor batch test"

#Variables
finalNum=9
search_dir=Sudoku_Generator/InstructorBoards
#"intermediate_board" "hard_board" "z_expert_board"
prefixStrArray=("easy_board" "intermediate_board" "hard_board" "z_expert_board")
argsParamArray=("MRV FC" "LCV FC" "MRV LCV FC")



for aArgParam in "${argsParamArray[@]}";do

    trimmed_string=$(echo $aArgParam | tr -d ' ')

    echo "ARGUMENT PARAM Section(Heur Used): ${aArgParam}"

    for atestBoardPath in "$search_dir"/*;do

        fileNameWExt=$(basename ${atestBoardPath})
        fileName=${fileNameWExt%.*}
        

        echo "Section: ${fileName} Parm:(${aArgParam})"

        # for ((i=0;i<finalNum;i++));do
        #     echo "On $i"

        # echo "python3 Sudoku_Python_Shell/src/Main.py ${aArgParam} ${atestBoardPath} >out${trimmed_string}${fileName}.txt"

        { time python3 Sudoku_Python_Shell/src/Main.py ${aArgParam} ${atestBoardPath} >out${trimmed_string}${fileName}.txt ; } 2> time${trimmed_string}${fileName}.txt

        # done

    done

done

echo "Done"