from random import choice
from filecmp import cmp, clear_cache


def pla_generator():
    input_num = int(input("How many input variables does the function have? "))
    pla_num = int(input("How many different PLAs do you want? "))
    for i in range(pla_num):
        actual_number = i+1
        with open(f"pla/pla_{input_num:02d}i_{actual_number:03d}.pla", "w") as f:
            row = 2**input_num
            f.write(f".i {input_num}\n")
            f.write(f".o 1\n")
            for j in range(row):
                input_str = format(j, 'b')  # Binary format. Outputs the number in base 2
                while len(input_str) < input_num:
                    input_str = "0" + input_str
                f.write(input_str + " " + str(choice([0, 1])) + "\n")
    for i in range(pla_num):
        actual_number = i + 1
        f1 = f"pla/pla_{input_num:02d}i_{actual_number:03d}.pla"
        for j in range(pla_num):
            if j == i:
                continue
            else:
                other_pla_number = j+1
                f2 = f"pla/pla_{input_num:02d}i_{other_pla_number:03d}.pla"
                result = cmp(f1, f2, shallow=False)
                if result:
                    print(f1 + " and " + f2 + " are equivalent? " + str(result))
                clear_cache()


