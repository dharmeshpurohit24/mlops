from .core import addition,subraction,multiplication,division,DivisionError

def main():
    print("Basic calculator provide values:-")

    val1 = float(input("Give value a: "))
    val2 = float(input("Give value b: "))
    
    print("Addition:", addition(val1, val2))
    print("Subtraction:", subraction(val1, val2))
    print("Multiplication:", multiplication(val1, val2))
    
    try:
        print("Division:", division(val1, val2))
    except DivisionError as e:
        print("Not possible:",e)
    except Exception as e:
        print("Cannot perform operation:",e)

if __name__ == "__main__":
    main()