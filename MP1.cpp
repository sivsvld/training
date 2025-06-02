#include <iostream>
#include <iomanip>
#include <string>

using namespace std;

int main() {
    const float KM_TO_NM = 0.539957;    // Constant conversion factor from kilometers to nautical miles
    float kilometers;                   // Variable to store user input in kilometers
    float nauticalMiles;                // Variable to store the converted distance in nautical miles
    string userName;                    // Variable to store the user's name
    char choice;                        // Variable to store the user's choice to continue or not

    cout << "Welcome to the Kilometers to Nautical Miles Converter!\n"; // Greeting and prompt for user name
    cout << "Please enter your name: ";
    getline(cin, userName); // Read full name from user input (including spaces)

    do {
        // Prompt for distance in kilometers
        cout << "\nHello, " << userName << "! Enter distance in kilometers: ";
        cin >> kilometers;              // Get user input for distance

        // Conversion
        nauticalMiles = kilometers * KM_TO_NM;

       // Input validation loop for user choice
        do {
            cout << "\nDo you want to convert another distance? (y/n): ";
            cin >> choice;
            choice = tolower(choice);  // Convert to lowercase to simplify check

            if (choice != 'y' && choice != 'n') {
                cout << "Invalid choice. Please enter 'y' for yes or 'n' for no.\n";
            }

        } while (choice != 'y' && choice != 'n'); // Repeat until valid input
        
    } while (choice == 'y' || choice == 'Y');

    cout << "\nGoodbye, " << userName << "! Safe travels.\n";
    return 0;
}
