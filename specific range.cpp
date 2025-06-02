#include <iostream>
#include <iomanip>  // for setw()
using namespace std;

int main() {
    int range;

    // Ask user to input a specific distance (range in km)
    cout << "Enter specific radar range to view (km): ";
    cin >> range;

    // Validate input (must be positive)
    if (range <= 0) {
        cout << "Please enter a positive integer for the range.\n";
        return 1; // Exit with error
    }

    // Display radar grid only for the specific input distance
    cout << "\nRadar Grid at Distance: " << range << " km\n\n";

    // Print column headers
    cout << "     ";  // Space for row numbers
    for (int col = 0; col < range; ++col) {
        cout << setw(3) << col << " ";
    }
    cout << "\n";

    // Print the top border of the grid
    cout << "    +";
    for (int i = 0; i < range; ++i) cout << "---+";
    cout << "\n";

    // Print each row of the grid
    for (int row = 0; row < range; ++row) {
        // Print row number at the beginning
        cout << setw(3) << row << " |";

        for (int col = 0; col < range; ++col) {
            // Show '*' at the bottom-right corner (range-1, range-1)
            if (row == range - 1 && col == range - 1)
                cout << " * |";
            else
                cout << "   |";
        }
        cout << "\n";

        // Print the row separator line
        cout << "    +";
        for (int i = 0; i < range; ++i) cout << "---+";
        cout << "\n";
    }

    return 0;
}
