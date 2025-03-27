from graph_search import bfs, dfs
from vc_metro import vc_metro
from vc_landmarks import vc_landmarks
from landmark_choices import landmark_choices

landmark_string = "" 
stations_under_construction = []#List of stations under construction
for letter, landmark in landmark_choices.items():
    landmark_string += "{0} - {1}\n".format(letter, landmark)

def greet():
    print("Hi there and welcome to SkyRoute!")    
    print("We'll help you find the shortest route between the following landmarks:\n"+landmark_string)

def skyroute():
    greet()
    new_route()
    goodbye()

   

def set_start_and_end(start_point, end_point):
   if start_point:
       change_point = input("What would you like to change ? You can enter 'o' for origin, 'd' for destination or 'b' for both:  ")
       if change_point == 'o':
           start_point = get_start()
       elif change_point == 'd':
           end_point = get_end()
       elif change_point == 'b':
           start_point = get_start()
           end_point = get_end()
       else:
            print("'Invalid input, enter 'o' for origin, 'd' for destination or 'b' for both ")
            set_start_and_end(start_point, end_point)
   else:
       start_point = get_start()
       end_point = get_end()

   return start_point, end_point


def get_start():
    start_point_letter = input("Where are you coming from? Type in the corresponding letter: ")
    if start_point_letter in landmark_choices:
        return landmark_choices[start_point_letter]
       
    else:
        print('That\'s not a landmark we have data on. Please try again')
        return get_start()

def get_end():
    end_point_letter = input("Where are you going to? Type in the corresponding letter: ")
    if end_point_letter in landmark_choices:
       return landmark_choices[end_point_letter]
    
    else:
        print("That\'s not a valid Landmark. Please try again!")
        return get_end()

def new_route(start_point = None, end_point = None):## a wrapper function for the bulk of the program that we can use to: get and set origin for the destination, call search for the recommended route, and ask user if they want to find another route
    start_point, end_point = set_start_and_end(start_point, end_point)
    if start_point == end_point:
        print("You are already at your destination! No other route could be found.")
        again = input("Would you like to find another route? Enter y/n:")
        if again == 'y':
            new_route(start_point, end_point)
        else:
            print('Thanks for using SkyRoute!')
            return    
    
    
    
    shortest_route = get_route(start_point, end_point)
    if shortest_route:
        shortest_route_string = '\n'.join(shortest_route)
        print(f"The shortest metro route from {start_point} to {end_point} is : {shortest_route_string}")
    else:
        print(f"Unfortunately, there is currently no path between {start_point} and {end_point} due to maintenance.")
    
    
    again = input("Would you like to find another route? Enter y/n:")
    if again == 'y':
        new_route(start_point, end_point)

    else:
        print('Thanks for using SkyRoute!')


def show_landmarks():
    see_landmarks = input("Would you like to see the list of landmarks again? Enter y/n:")
    if see_landmarks == 'y':
        print(landmark_string)
    else:
        print("Have a great day!")


def get_route(start_point, end_point):
    start_stations = vc_landmarks[start_point]#grabs a set of at least one metro station
    
    end_stations = vc_landmarks[end_point]
    
    routes = [] #List of possible shortest routes
    for start_station in start_stations:
        for end_station in end_stations:
            metro_system = get_active_stations() if stations_under_construction else vc_metro
            if stations_under_construction:
                possible_route = dfs(metro_system, start_station, end_station)
                if not possible_route:
                    continue
                
            route = bfs(metro_system, start_station, end_station) #finds the shortest route between the two stations
        if route:
            routes.append(route)    
    
    if routes:
        return min(routes, key=len)#returns the shortest route found
    
    else:
        return None


def get_active_stations(): ### automatically generates an updated graph based on what is added to the              stations_under_construction list

    updated_metro = vc_metro.copy()
    for station_under_construction in stations_under_construction:
        for current_station, neighboring_stations in vc_metro.items():
            if current_station != station_under_construction:
                updated_metro[current_station] -= set(stations_under_construction)
            else:
                updated_metro[current_station] = set()
    return updated_metro                



def goodbye():
    print("Thank you for using SkyRoute!")


# Call get_route with two landmark names and print the result
test_route = get_route("Marine Building", "Scotiabank Field at Nat Bailey Stadium")
print(f"Test Route: {test_route}")

# Call new_route to start the program and find a route
show_landmarks()    
new_route()
skyroute()
