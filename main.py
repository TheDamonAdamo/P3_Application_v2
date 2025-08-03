import subprocess
import sys


def run_script(script_name):
    try:
        subprocess.run([sys.executable, script_name], check=True)
    except subprocess.CalledProcessError:
        print(f"Error running {script_name}")


def main():
    while True:
        print("\n=== Chess Tournament Manager Main Menu ===")
        print("1. Manage Clubs")
        print("2. Manage Tournaments")
        print("Q. Quit")

        choice = input("Select an option: ").strip().lower()

        if choice == "1":
            run_script("manage_clubs.py")
        elif choice == "2":
            run_script("manage_tournaments.py")
        elif choice == "q":
            print("Goodbye!")
            break
        else:
            print("Invalid input. Please try again.")


if __name__ == "__main__":
    main()
