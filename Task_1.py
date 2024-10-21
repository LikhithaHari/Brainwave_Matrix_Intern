class ATM:
    def __init__(self, balance=0):
        self.balance = balance

    def check_balance(self):
        print(f"\nYour current balance is: ${self.balance:.2f}")

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"\nYou've successfully deposited ${amount:.2f}.")
            self.check_balance()
        else:
            print("\nInvalid deposit amount. Please try again.")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"\nYou've successfully withdrawn ${amount:.2f}.")
            self.check_balance()
        elif amount > self.balance:
            print("\nInsufficient funds. Please try a smaller amount.")
        else:
            print("\nInvalid withdrawal amount. Please try again.")

    def menu(self):
        while True:
            print("\n----- ATM Menu -----")
            print("1. Check Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Exit")
            choice = input("\nEnter the number of your choice: ")

            if choice == '1':
                self.check_balance()
            elif choice == '2':
                amount = float(input("\nEnter the amount to deposit: "))
                self.deposit(amount)
            elif choice == '3':
                amount = float(input("\nEnter the amount to withdraw: "))
                self.withdraw(amount)
            elif choice == '4':
                print("\nThank you for using the ATM. Goodbye!")
                break
            else:
                print("\nInvalid choice. Please try again.")

# Create an ATM instance with an initial balance (e.g., $500)
atm = ATM(500)
atm.menu()
