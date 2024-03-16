import os
from collections import defaultdict 

PATHTOSEARCH = "outNORMADLCV"


def main():
    print("running stats")

    #define default dicts
    NumOccurPerBType = defaultdict(int)
    SumBTPerBtype = defaultdict(int)

  


    #try to open and get the line
    for (root, dirs, file) in os.walk(PATHTOSEARCH):
        for f in file:
            if '.txt' in f:
                print(root)
                print(f)

                ThePrefix = f.split("_")[0]

                print("prefix " + str(ThePrefix))

                # string to search in file
                print(os.path.join(root,f))
                with open(os.path.join(root,f), 'r') as fp:
                    
                    TheBacktrackLine = [line for line in fp if line.startswith("Backtracks")]

                    if len(TheBacktrackLine) > 0:
                        ProcessLineBT = TheBacktrackLine[0].strip()

                        TheBtnum = int(ProcessLineBT.split(":")[1].strip())

                        print("The process line, " + str(ProcessLineBT))
                        print(TheBtnum)

                        #increment the num occurance
                        NumOccurPerBType[ThePrefix] += 1

                        #add to the Sum dict
                        SumBTPerBtype[ThePrefix] += TheBtnum


    print(NumOccurPerBType)
    print("Sum dict")
    print(SumBTPerBtype)

    KeyIntersection = set(NumOccurPerBType.keys()).intersection(set(SumBTPerBtype.keys()))

    print("intersection of keys")
    print(KeyIntersection)

    print("Stats:")

    for athing in KeyIntersection:
        print(f"Section: {athing}")

        print("Total completed:")

        print(NumOccurPerBType[athing])

        print(f"Avg:")

        avgcomp = SumBTPerBtype[athing]/NumOccurPerBType[athing]

        print(avgcomp)



                    






if __name__ == "__main__":
    main()