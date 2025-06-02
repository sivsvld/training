#include <iostream>
#include <string>
using namespace std;

int main() {
   string username, password;                       // Declare variables for user input
    string correctUsername = "nrtdc.admin";         // Store the correct username
    string correctPassword = "NRTDC2028";           // Store the correct password
    int attempts = 0;                               // Initialize attempt counter
    const int maxAttempts = 4;                      // Set maximum allowed attempts

    while (attempts < maxAttempts) {                // Loop while attempts are less than maxAttempts
        cout << "🔐 Enter username: ";              // Prompt user to enter username
        cin >> username;                            // Read username input
        cout << "🔐 Enter password: ";              // Prompt user to enter password
        cin >> password;                            // Read password input

        if (username == correctUsername && password == correctPassword) {  // Check if credentials are correct
            cout << R"(                      
     _    ____ ____ _____ ____ ____     ____ ____      _    _   _ _____ _____ ____
   / \  / ___/ ___| ____/ ___/ ___|    / ___|  _ \    / \  | \ | |_   _| ____|  _ \
  / _ \| |  | |   |  _| \___ \___ \   | |  _| |_) |  / _ \ |  \| | | | |  _| | | | |
 / ___ \ |__| |___| |___ ___) |__) |  | |_| |  _ <  / ___ \| |\  | | | | |___| |_| |
/_/   \_\____\____|_____|____/____/    \____|_| \_\/_/   \_\_| \_| |_| |_____|____/      
                                                   
✅ ACCESS GRANTED!
)" << endl;
            return 0;                      // Exit program with success code
        } else {                          // If credentials are wrong
            attempts++;                   // Increment attempt counter
             // Specific feedback
            if (username != correctUsername && password != correctPassword) {
                cout << "❌ Both username and password are incorrect.\n";
            } else if (username != correctUsername) {
                cout << "❌ Username is incorrect.\n";
            } else {
                cout << "❌ Password is incorrect.\n";
            }
            cout << R"(
    _    ____ ____ _____ ____ ____    ____  _____ _   _ ___ _____ ____  
   / \  / ___/ ___| ____/ ___/ ___|  |  _ \| ____| \ | |_ _| ____|  _ \ 
  / _ \| |  | |   |  _| \___ \___ \  | | | |  _| |  \| || ||  _| | | | |
 / ___ \ |__| |___| |___ ___) |__) | | |_| | |___| |\  || || |___| |_| |
/_/   \_\____\____|_____|____/____/  |____/|_____|_| \_|___|_____|____/ 
                                           
                                           
❌ ACCESS DENIED. Attempt )" << attempts << " of " << maxAttempts << ".\n\n";        // Show attempt count
        }
    }
    cout << "🚫 Too many failed attempts. Access permanently denied.\n";            // Lock out after max attempts
    return 1;                                                                       // Exit program with failure code
}