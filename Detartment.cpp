#include <iostream>
#include <vector>
#include <map>
#include <string>

using namespace std;

// Define Product structure
struct Product {
    string name;
    double price;
    int quantity;
};

// Define Employee structure
struct Employee {
    string name;
    string role;
};

// Define Customer structure
struct Customer {
    string name;
    string contactInfo;
};

// Define Store class
class Store {
private:
    map<string, Product> inventory;
    vector<Employee> employees;
    vector<Customer> customers;
    double totalSales;

public:
    Store() : totalSales(0.0) {}

    // Add product to inventory
    void addProduct(string name, double price, int quantity) {
        Product p = {name, price, quantity};
        inventory[name] = p;
    }

    // Sell product
    bool sellProduct(string name, int quantity) {
        if (inventory.count(name) && inventory[name].quantity >= quantity) {
            inventory[name].quantity -= quantity;
            totalSales += inventory[name].price * quantity;
            return true;
        }
        return false;
    }

    // Display inventory
    void displayInventory() {
        cout << "Inventory:\n";
        for (const auto& pair : inventory) {
            cout << pair.first << " - $" << pair.second.price << " - Quantity: " << pair.second.quantity << endl;
        }
    }

    // Add employee
    void addEmployee(string name, string role) {
        Employee e = {name, role};
        employees.push_back(e);
    }

    // Display employees
    void displayEmployees() {
        cout << "Employees:\n";
        for (const auto& emp : employees) {
            cout << "Name: " << emp.name << " | Role: " << emp.role << endl;
        }
    }

    // Add customer
    void addCustomer(string name, string contactInfo) {
        Customer c = {name, contactInfo};
        customers.push_back(c);
    }

    // Display customers
    void displayCustomers() {
        cout << "Customers:\n";
        for (const auto& cust : customers) {
            cout << "Name: " << cust.name << " | Contact Info: " << cust.contactInfo << endl;
        }
    }

    // Generate sales report
    void generateSalesReport() {
        cout << "Total Sales: $" << totalSales << endl;
    }
};

int main() {
    // Create a store
    Store store;

    // Add some products to inventory
    store.addProduct("Shirt", 25.99, 50);
    store.addProduct("Jeans", 39.99, 30);
    store.addProduct("Shoes", 49.99, 20);

    // Display initial inventory
    store.displayInventory();

    // Add employees
    store.addEmployee("John Doe", "Cashier");
    store.addEmployee("Jane Smith", "Sales Associate");

    // Display employees
    store.displayEmployees();

    // Add customers
    store.addCustomer("Alice", "alice@example.com");
    store.addCustomer("Bob", "bob@example.com");

    // Display customers
    store.displayCustomers();

    // Sell some products
    if (store.sellProduct("Shirt", 5)) {
        cout << "Sold 5 shirts.\n";
    } else {
        cout << "Failed to sell shirts.\n";
    }

    // Display updated inventory
    store.displayInventory();

    // Generate sales report
    store.generateSalesReport();

    return 0;
}
