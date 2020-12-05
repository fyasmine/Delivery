import datetime
from hashTable import table
from hashTable import HashTable
from delivery import Delivery

# used to look up the delivery status of a package
class PackageLookup:
    global package_id
    global current_time
    global ids
    ids = 40
    timeformat = "%H:%M:%S"
    # opening message to user detailing the total miles for all deliveries and asks what the user would like to accomplish
    print("Welcome to Western Governors University Parcel Service (WGUPS)")
    print("If you would like to exit, type 'exit'")
    package_id = input("If you would like to add a package to the database, type 'insert' or type 'search' to look up the status and details of a package:")

    # O(1)
    # adds package to list by asking for necessary information, adding the information to a list, and passing the list to the HashTable.add() function
    # a package ID is returned
    def addPackage():
        global ids
        ids += 1
        new_address = input("What address will the package be delivered to?")
        new_city = input("What city is this address is in?")
        new_state = input("What is the abbreviation for the state this address is in?")
        new_zip = input("What is the zip code?")
        new_deadline = input("When is the delivery deadline?")
        new_weight = input("What is the weight of the package in kg?")
        new_note = input("Would you like to add any special notes? If you wish to skip this step, press enter.")
        # adds all user input into list to pass as parameter
        item = [new_address, new_city, new_state, new_zip, new_deadline, new_weight, new_note, 'At hub', -1]
        # calls method in HashTable file to add new package
        added = table.add(str(ids), item)
        if added:
            print("Your package has been successfully added. The package ID is:", ids)
        else:
            print("Failed to add package.")
        print()

    # checks for package using ID provided by searching for ID in hash table
    # method determines if time user gives is before or after the delivery time and the time it departs the hub
    # method also is used to retrieve all the packages if user wants to see status of every package by iterating through the hash table and printing the information for each item
    def check():
        global package_id
        # O(N^2) + 3O(1)
        # checks that user wants to search for package
        while package_id != 'exit' and package_id != 'insert':
            # O(N) + 3O(1)
            while package_id != 'all' and package_id != 'exit':
                values = table.get(package_id)
                # 3O(1)
                # prints package information if package exists
                if values != None:
                    print("Package ID:", package_id)
                    print("Address:", values[0])
                    print("City:", values[1])
                    print("State:", values[2])
                    print("Zip code:", values[3])
                    print("Package weight(kg):", values[5])
                    print("Delivery deadline:", values[4])
                    # 2O(1)
                    # determines if package has already been delivered
                    if int(package_id) > 40:
                        print("Delivery status: At hub")
                    else:
                        # O(1)
                        # prints information if package is delivered
                        if values[8] < current_time and values[7] < current_time:
                            print("Delivery status:", "Delivered at", values[8], "by truck 2")
                        # prints information if package is out for delivery
                        elif values[8] > current_time and values[7] < current_time:
                            print("Delivery status: Out for delivery")
                        # prints information if package is at hub
                        else:
                            print("Delivery status: At hub")
                    print()
                    # prompts user for another package ID or 'all' if they would like to see the status of all packages
                    package_id = input("Please enter the ID for the package you would like to lookup or track. Or enter 'all' to view status of all packages:")
                    return package_id
                else:
                    # prompts user for another package ID if the one entered is not found in the hash table
                    print("Invalid package ID. Package does not exist in system.")
                    package_id = input("Please enter the ID for the package you would like to lookup or track. Or enter 'all' to view status of all packages:")
                    print()
                    return package_id

            # O(N) + O(2)
            # prints data for all packages by iterating through entire hash table and printing information for each individual package
            # which block of text is executed depends on the delivery status of the package
            if package_id == 'all':
                delivery_list = []
                delivered_list = []
                hub_list = []
                # O(N) + O(1)
                # iterates through packages to get information
                for i in range(ids):
                    values = table.get(str(i + 1))
                    # O(1)
                    # if the package was just inserted by the user, a delivery status of 'At hub' is given
                    if int(i) > 39:
                        print("Package ID:", i + 1, "   Address:", values[0], "   City:", values[1],
                              "   State:", values[2], "   Zip code:",
                              values[3], "   Package weight(kg):", values[5], "   Delivery deadline:",
                              values[4], "   Delivery status: At hub")
                        hub_list.append(i + 1)
                    else:
                        # prints information if package has been delivered
                        if values[8] < current_time and values[7] < current_time:
                            print("Package ID:", i + 1, "   Address:", values[0], "   City:", values[1],
                                "   State:", values[2], "   Zip code:",
                                values[3], "   Package weight(kg):", values[5], "   Delivery deadline:",
                                values[4], "   Delivery status: Delivered at", values[8], "by truck 2")
                            delivered_list.append(i + 1)
                        # prints information if package is out for delivery
                        elif values[8] > current_time and values[7] < current_time:
                            print("Package ID:", i + 1, "   Address:", values[0], "   City:", values[1],
                                "   State:", values[2], "   Zip code:",
                                values[3], "   Package weight(kg):", values[5], "   Delivery deadline:",
                                values[4], "   Delivery status: Out for delivery")
                            delivery_list.append(i + 1)
                        # prints information if package is at hub
                        else:
                            print("Package ID:", i + 1, "   Address:", values[0], "   City:", values[1],
                                "   State:", values[2], "   Zip code:",
                                values[3], "   Package weight(kg):", values[5], "   Delivery deadline:",
                                values[4], "   Delivery status: At hub")
                            hub_list.append(i + 1)
                print()
                #prints lists of packages delivered, at hub, and out for delivery
                print("Packages currently at hub:", hub_list)
                print("Packages currently out for delivery:", delivery_list)
                print("Packages already delivered:", delivered_list)
                print()
                print()
                # prompts user for package ID
                package_id = input("If you would like to look up a specific package, please enter the ID:")
        exit()

    # checks that input is valid
    while package_id != 'exit' and package_id != 'insert' and package_id != 'search':
        package_id = input(
            "Input invalid. If you would like to add a package to the database, type 'insert' or type 'search' to look up the status and details of a package:")

    # calls addPackage function if user wants to insert new package and asks for a time and a package ID
    if package_id == 'insert':
        addPackage()
    current_time = input("Please enter a time in HH:MM:SS format using military time:")
    package_id = input("Please enter the ID for the package you would like to lookup or track. Or enter 'all' to view status of all packages:")
    print()

    # O(N^2)
    # calls check method if input time is valid
    while package_id != 'exit' and package_id != 'insert':
        # O(N)
        # checks that user input valid time and if time is invalid, user is asked to input a new time
        while current_time != None:
            try:
                validtime = datetime.datetime.strptime(current_time, timeformat)
                check()
            except ValueError:
                current_time = input("Invalid time. Please enter a time in HH:MM:SS format using military time:")

    # exits program
    exit()