#include <iostream>
using namespace std;

int main() {
    int range;

    // Ask the user to enter the radar range
    cout << "Enter radar range (km): ";
    cin >> range;

    // Basic input validation (range should be positive)
    if (range <= 0) {
        cout << "Please enter a positive integer for the range.\n";
        return 1; // Exit program with error
    }

    // Loop through each distance from 1 to the input range
    for (int dist = 1; dist <= range; ++dist) {
        cout << "Distance: " << dist << " km\n";

        // Print top border of the grid
        cout << "+";
        for (int i = 0; i < range; ++i) cout << "---+";
        cout << "\n";

        // Loop through each row in the grid
        for (int row = 0; row < range; ++row) {
            cout << "|";  // Left border of grid row

            // Loop through each column in the grid
            for (int col = 0; col < range; ++col) {
                if (row == dist - 1 && col == dist - 1)
                    cout << " * |";  // Mark detected position with '*'
                else
                    cout << "   |";  // Empty space
            }
            cout << "\n";

            // Print the border line under each row
            cout << "+";
            for (int i = 0; i < range; ++i) cout << "---+";
            cout << "\n";
        }
        cout << "\n";  // Blank line between different distance grids
    }

    return 0;
}
