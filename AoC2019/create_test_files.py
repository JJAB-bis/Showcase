import os

Day   = 14
Max_Files = 5




path = '\\'.join( os.path.abspath(__file__).split('\\')[:-1] )
for test in range(Max_Files):
    test += 1
    file_loc = f"""{path}\\Day{Day}\\{f"{f'test_{test}_' if test > 0 else ''}input.txt"}"""
    print( file_loc)
    with open(file_loc, 'a') as f:
        pass

