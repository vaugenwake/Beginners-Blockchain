import os

"""
This class will manage and maintain a blockchain users wallet

- When a new user registers they will be generated a public & private key.
- The private key will be used to identify them on the blockchain
- The public key will be used to verify their signed transactions.

---------------------------------------------------------------------------
The wallet will act as the entrypoint for users to interact with and
transact on the blockchain. A user will login to their wallet and
will be able to:
- Make and sign a transaction
- View their balance
"""


class Wallet:

    def __init__(self) -> None:
        self.display_welcome_message()

        choice = ''
        while choice != 'q':
            print("\n[1] Setup a new wallet")
            print("[2] Login to existing wallet")
            print("[q] Quit\n")

            choice = input('What would you like to do? ')

            if choice == '1':
                self.create_a_new_wallet()
            elif choice == '2':
                print("\nLogin to your wallet")
                self.login_user()
            elif choice == 'q':
                print("\nGoodbye!")
            else:
                print(f"\nPlease try again, {choice} is not an option")

    def create_a_new_wallet(self) -> None:
        choice = ''
        while choice != 'q':
            print("\n[1] Generate random wallet")
            print("[2] Setup a personal wallet")
            print("[q] Go back to start\n")

            choice = input("What kind of wallet would you like to setup? ")

    """
    Will generate a new set of key pairs
    """
    def generate_new_wallet_keys():
        pass

    """
    Will accept a private key and login a user
    - We can get the users public key & address from their private key
    """

    def login_user(self):
        private_key = ''

        while private_key != 'q':
            private_key = input("\nEnter private key (or 'q' to quit): ")

            if private_key != 'q':
                print(f"\nLoggin in: {private_key}")

    def display_welcome_message(self):
        os.system('clear')

        print("\t*****************************")
        print("\t***   WELCOME TO WALLET   ***")
        print("\t*****************************")


if __name__ == "__main__":
    wallet = Wallet()
