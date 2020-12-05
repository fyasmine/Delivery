import csv
from hashTable import HashTable
from hashTable import table
import datetime

# executes deliveries by finding the drop-off location closest to the hub and from there the address closest to that location
class Delivery:
    # declares global variables
    global distance_file
    global package_file
    global file1
    global file2
    global total_miles
    global delivery_time
    global t2_depart
    global t3_depart
    # opens and reads files
    file1 = open('WGUPS Package File CSV.csv')
    package_file = csv.reader(file1)
    file2 = open('WGUPS Distance Table CSV.csv')
    distance_file = csv.reader(file2)
    total_miles = 0
    # packages on each truck
    truck1 = ['37', '38', '15', '16', '30', '34', '21', '4', '1', '29', '7', '5', '8', '14', '40', '20']
    truck2_deadline = ['26', '25', '32', '31', '6', '13', '39']
    truck2_EOD = ['2', '27', '35', '28', '33', '36', '3', '17']
    truck3 = ['12', '10', '11', '23', '19', '9', '24', '18', '22']

    # time first truck departs from hub
    delivery_time = datetime.datetime(1, 1, 1, 8, 00, 00)

    # calculates total distance for first and third trip by determining which location is the closest to the last by iterating through the list
    # once a package is delivered, it is removed from the list and added to a new list
    def distance(list):
        global delivery_time
        # new empty list to move delivered packages to
        new_list = []
        # sets starting miles as -1
        shortest_miles = -1
        # O(N)
        # sets time package left hub
        for i in list:
            table.add_depart_status(i, str(delivery_time.time()))

        # 2O(N) + 3O(1)
        # iterates through packages in list to find drop-off address closest to hub
        # package closest to the hub is removed from list
        for i in list:
            address = ' ' + table.get(i)[0]

            # corrects address for package 9
            # O(1)
            if i == '9':
                address = ' 410 S State St'
            # O(N) + 2O(1)
            # gets address from each row
            for row in distance_file:
                address_row = row[0]
                # gets only address part from cells
                table_title = address_row.splitlines()[1:2]
                table_address = row[1][:-8]
                # 2O(1)
                # finds row that matches address
                if address in table_title or address in table_address:
                    # sets package and miles if lower than any of the previous miles calculated
                    # O(1)
                    if shortest_miles == -1 or float(row[2]) < float(shortest_miles):
                        # gets ID of package closest to hub
                        shortest_package = i
                        # gets index of package
                        shortest_index = list.index(i)
                        # gets miles for package
                        shortest_miles = row[2]
            # resets search to begin at beginning of file
            file2.seek(0)

        # O(N^3) + 3O(1)
        # finds distance between 2 points
        def findMiles(address1, address2):
            # O(1)
            # replaces Station with Sta for address 3575
            if '3575' in address1:
                address1 = address1.replace(' Station ', ' Sta ')
            # resets search to begin at beginning of file
            file2.seek(0)
            # gets row of addresses from distance file
            address_row = next(distance_file)
            address_index = 1
            # O(N^3) + 2O(1)
            # finds first address in table and gets index
            for i in address_row:
                # gets address part from cell
                top_address = i.splitlines()[1:2]
                # O(N^2) + 2O(1)
                # iterates through addresses in top row
                for line in top_address:
                    address_number = str(top_address)[2:8]
                    address_index += 1
                    # O(N) + 2O(1)
                    # finds address from top row matching drop-off address
                    if address1 in line:
                        # O(N) + O(1)
                        # finds second address in table
                        for row in distance_file:
                            address_row = row[0]
                            table_title = address_row.splitlines()[1:2]
                            table_address = row[1][:-8]
                            # O(1)
                            # uses index of first address to get distance between addresses
                            if address2 in table_address or address2 in table_title:
                                # returns distance between addresses
                                return float(row[address_index])

        global total_miles
        # removes package closest to hub from list and adds to new list
        list.pop(shortest_index)
        # adds package to new list
        new_list.append(shortest_package)
        total_miles += float(shortest_miles)
        # calculates delivery time
        delivery_time = delivery_time + datetime.timedelta(minutes = (float(shortest_miles) / 18 * 60))
        # adds delivery time to package ID
        table.add_time(shortest_package, str(delivery_time.time()))

        # resets values to 0 or -1 for comparison
        shortest_index = 0
        shortest_package = 0
        shortest_miles = -1

        # O(N^2) + 4O(1)
        # iterates through undelivered packages to determine location closest to package just delivered
        while len(list) > 0:
            # O(N) + 4O(1)
            for i in list:
                address1 = ' ' + table.get(new_list[len(new_list) - 1])[0]
                address2 = ' ' + table.get(i)[0]
                # corrects address for package 9
                # O(1)
                if new_list[len(new_list) - 1] == '9':
                    address1 = ' 410 S State St'
                # O(1)
                if i == '9':
                    address2 = ' 410 S State St'
                # O(1)
                # determines which order to send parameters in
                if (address1 < address2):
                    miles = findMiles(address1, address2)
                else:
                    miles = findMiles(address2, address1)
                # O(1)
                # saves closest package
                if shortest_miles == -1 or float(miles) < float(shortest_miles):
                    # gets ID of package closest to hub
                    shortest_package = i
                    # gets index of package
                    shortest_index = list.index(i)
                    # gets miles for package
                    shortest_miles = miles
            # removes package from list
            list.pop(shortest_index)
            # adds package to new list
            new_list.append(shortest_package)
            total_miles += float(shortest_miles)
            # calculates delivery time
            delivery_time = delivery_time + datetime.timedelta(minutes=(float(shortest_miles) / 18 * 60))
            # adds delivery time to package ID
            table.add_time(shortest_package, str(delivery_time.time()))

            # resets values to 0 or -1
            shortest_index = 0
            shortest_package = 0
            shortest_miles = -1

        # resets search to begin at beginning of file
        file2.seek(0)

        address = ' ' + table.get(i)[0]
        # corrects address for package 9
        # O(1)
        if i == '9':
            address = ' 410 S State St'
        # O(N) + O(1)
        # gets address from each row
        for row in distance_file:
            address_row = row[0]
            # gets only address part from cells
            table_title = address_row.splitlines()[1:2]
            table_address = row[1][:-8]
            # O(1)
            # finds row that matches address
            if address in table_title or address in table_address:
                # sets package and miles if lower than any of the previous miles
                miles = row[2]
        total_miles += float(miles)
        # adds time to get back to hub
        delivery_time = delivery_time + datetime.timedelta(minutes = (float(miles) / 18 * 60))

    # calculates second trips total distance by finding distance for all packages with deadlines then distance for packages with EOD deadline
    # method is similar to distance() method and finds package with drop-off location closest to the hub and then finding drop-off locations closest to the last point
    def distance_t2(list, list2):
        global delivery_time
        # new empty list to move delivered packages to
        new_list = []
        # sets starting miles as -1
        shortest_miles = -1

        # O(N)
        # sets time package left hub
        for i in list:
            table.add_depart_status(i, str(delivery_time.time()))
            # sets time package left hub
        # O(N)
        for i in list2:
            table.add_depart_status(i, str(delivery_time.time()))

        # O(N^2) + 2O(1)
        # iterates through packages in list to find drop-off address closest to hub
        for i in list:
            address = ' ' + table.get(i)[0]
            # O(N) + 3O(1)
            # corrects address for package 9
            if i == '9':
                address = ' 410 S State St'
            # O(N) + 2O(1)
            # gets address from each row
            for row in distance_file:
                address_row = row[0]
                # gets only address part from cells
                table_title = address_row.splitlines()[1:2]
                table_address = row[1][:-8]
                # 2O(1)
                # finds row that matches address
                if address in table_title or address in table_address:
                    # sets package and miles if lower than any of the previous miles
                    # O(1)
                    if shortest_miles == -1 or float(row[2]) < float(shortest_miles):
                        # gets ID of package closest to hub
                        shortest_package = i
                        # gets index of package
                        shortest_index = list.index(i)
                        # gets miles for package
                        shortest_miles = row[2]
            # resets search to begin at beginning of file
            file2.seek(0)
        # O(N^3) + 3O(1)
        # finds distance between 2 points for second trip
        def findMiles(address1, address2):
            # O(1)
            # replaces Station with Sta for address 3575
            if '3575' in address1:
                address1 = address1.replace(' Station ', ' Sta ')
            # resets search to begin at beginning of file
            file2.seek(0)
            # gets row of addresses from distance file
            address_row = next(distance_file)
            address_index = 1
            # O(N^3) + 2O(1)
            # finds first address in table and gets index
            for i in address_row:
                # gets address part from cell
                top_address = i.splitlines()[1:2]
                # O(N^2) + 2O(1)
                # iterates through addresses in top row
                for line in top_address:
                    address_number = str(top_address)[2:8]
                    address_index += 1
                    # O(N) + 2O(1)
                    # finds address from top row matching drop-off address
                    if address1 in line:
                        # O(N) + O(1)
                        # finds second address in table
                        for row in distance_file:
                            address_row = row[0]
                            table_title = address_row.splitlines()[1:2]
                            table_address = row[1][:-8]
                            # O(1)
                            # uses index of first address to get distance between addresses
                            if address2 in table_address or address2 in table_title:
                                # returns distance between addresses
                                return float(row[address_index])

        global total_miles
        # removes package closest to hub from list and adds to new list
        list.pop(shortest_index)
        # adds package to new list
        new_list.append(shortest_package)
        total_miles += float(shortest_miles)

        # calculates delivery time
        delivery_time = delivery_time + datetime.timedelta(minutes=(float(shortest_miles) / 18 * 60))
        # adds delivery time to package ID
        table.add_time(shortest_package, str(delivery_time.time()))

        # resets values to 0 or -1 for comparison
        shortest_index = 0
        shortest_package = 0
        shortest_miles = -1

        # O(N^2) + 4O(1)
        #finds shortest distance between points for first list
        while len(list) > 0:
            # O(N)
            for i in list:
                address1 = ' ' + table.get(new_list[len(new_list) - 1])[0]
                address2 = ' ' + table.get(i)[0]
                # corrects address for package 9
                # O(1)
                if new_list[len(new_list) - 1] == '9':
                    address1 = ' 410 S State St'
                # O(1)
                if i == '9':
                    address2 = ' 410 S State St'
                # O(1)
                # determines which order to send parameters in
                if (address1 < address2):
                    miles = findMiles(address1, address2)
                else:
                    miles = findMiles(address2, address1)
                # O(1)
                if shortest_miles == -1 or float(miles) < float(shortest_miles):
                    # gets ID of package closest to hub
                    shortest_package = i
                    # gets index of package
                    shortest_index = list.index(i)
                    # gets miles for package
                    shortest_miles = miles
            # removes package from list
            list.pop(shortest_index)
            # adds package to new list
            new_list.append(shortest_package)
            total_miles += float(shortest_miles)

            # calculates delivery time
            delivery_time = delivery_time + datetime.timedelta(minutes=(float(shortest_miles) / 18 * 60))
            # adds delivery time to package ID
            table.add_time(shortest_package, str(delivery_time.time()))

            # resets values to 0 or -1
            shortest_index = 0
            shortest_package = 0
            shortest_miles = -1

        # finds shortest distance between points for second list
        # O(N^2) + 4O(1)
        while len(list2) > 0:
            # O(N) + 4O(1)
            for i in list2:
                address1 = ' ' + table.get(new_list[len(new_list) - 1])[0]
                address2 = ' ' + table.get(i)[0]
                # O(1)
                # corrects address for package 9
                if new_list[len(new_list) - 1] == '9':
                    address1 = ' 410 S State St'
                # O(1)
                if i == '9':
                    address2 = ' 410 S State St'
                # O(1)
                # determines which order to send parameters in
                if (address1 < address2):
                    miles = findMiles(address1, address2)
                else:
                    miles = findMiles(address2, address1)
                # O(1)
                if shortest_miles == -1 or float(miles) < float(shortest_miles):
                    # gets ID of package closest to hub
                    shortest_package = i
                    # gets index of package
                    shortest_index = list2.index(i)
                    # gets miles for package
                    shortest_miles = miles
            # removes package from list
            list2.pop(shortest_index)
            # adds package to new list
            new_list.append(shortest_package)
            total_miles += float(shortest_miles)

            # calculates delivery time
            delivery_time = delivery_time + datetime.timedelta(minutes=(float(shortest_miles) / 18 * 60))
            # adds delivery time to package ID
            table.add_time(shortest_package, str(delivery_time.time()))

            # resets values to 0 or -1
            shortest_index = 0
            shortest_package = 0
            shortest_miles = -1

        # resets search to begin at beginning of file
        file2.seek(0)
        address = ' ' + table.get(i)[0]
        # O(1)
        # corrects address for package 9
        if i == '9':
            address = ' 410 S State St'
        # gets address from each row
        # O(N) + O(1)
        for row in distance_file:
            address_row = row[0]
            # gets only address part from cells
            table_title = address_row.splitlines()[1:2]
            table_address = row[1][:-8]
            # finds row that matches address
            # O(1)
            if address in table_title or address in table_address:
                # sets package and miles if lower than any of the previous miles
                miles = row[2]
        total_miles += float(miles)
        # adds time to get back to hub
        delivery_time = delivery_time + datetime.timedelta(minutes=(float(miles) / 18 * 60))

    # calls methods and passes necessary package lists
    distance(truck1)
    distance_t2(truck2_deadline, truck2_EOD)
    distance(truck3)

    print("All packages were able to be delivered on time in", round(total_miles, 1), "miles")

