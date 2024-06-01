def ask_permission():
    while True:
        response = input("Are you sure you want to continue? (y/n): ").strip().lower()
        if response == "y":
            print("Permission granted. Continuing...")
            return True
        elif response == "n":
            print("Permission denied. Exiting...")
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
