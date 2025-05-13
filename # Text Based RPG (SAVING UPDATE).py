# Text Based RPG
# Intro to Programming final project


import random # Random number generation
import json # Save/Load stuffs

# Game configuration
MAP_SIZE = 3
STARTING_TIME = 75
TRAP_PENALTY = 9 # This is to make movement + penalty 10 time loss
Baddie_PENALTY = 4 # And this for 5 time loss including movement

# Global state
world = {}
inventory = []
Player_Pos = [0, 0]
Has_Golden_Idol = False
game_over = False
time_left = STARTING_TIME

directions = { # Values for the move directions
    'up': (-1, 0),
    'down': (1, 0),
    'east': (0, 1),
    'west': (0, -1)
}

def Make_World():
    global world
    world = {}
    for x in range(MAP_SIZE):
        for y in range(MAP_SIZE):
            room = {
                "description": "You see thick jungle and ancient ruins.",
                "items": [],
                "event": random.choice(["none", "trap", "Baddie", "treasure"]),
                "visited": False
            }
            world[(x, y)] = room
    # Place the Golden Idol randomly (not at start)
    while True:
        idol_pos = (random.randint(0, 2), random.randint(0, 2))
        if idol_pos != (0, 0):
            world[idol_pos]["items"].append("Golden Idol")
            world[idol_pos]["event"] = "idol"
            break

def Introduction():
    print("Welcome to the Quest for the Golden Idol!")
    print("Explore the jungle, find the Golden Idol, and return to the start before time runs out.")
    print("You start with 75 time. Moving, traps, and enemies will cost you time. (If you want, draw a 3x3 grid and place yourself at the TOP MIDDLE grid and move while you play the game)")
    print("Your commands are: move up, move down, move east, move west, look, inventory, save, load, quit")

def get_command():
    try:
        return input("\n> ").strip().lower()
    except EOFError:
        return "quit"

def move_player(direction):
    global time_left, game_over
    dx, dy = directions.get(direction, (0, 0))
    new_x = Player_Pos[0] + dx
    new_y = Player_Pos[1] + dy
    if 0 <= new_x < MAP_SIZE and 0 <= new_y < MAP_SIZE:
        Player_Pos[0], Player_Pos[1] = new_x, new_y
        time_left -= 1  # Time penalty for moving
        if time_left <= 0:
            print("You ran out of time while moving. Game over.")
            game_over = True
        else:
            check_room()
    else:
        print("You can't go that way.")

def check_room():
    global Has_Golden_Idol, game_over, time_left
    pos = tuple(Player_Pos)
    room = world[pos]
    if not room["visited"]:
        print(f"You enter a new area: {room['description']}")
        event = room["event"]
        if event == "trap":
            print("A hidden trap springs! You lose 10 time.")
            time_left -= TRAP_PENALTY
        elif event == "Baddie":
            print("A Baddie ambushes you! You escape but lose 5 time.")
            time_left -= Baddie_PENALTY
        elif event == "treasure":
            item = random.choice(["Ancient Coin", "Canteen", "Jungle Compass"]) # These items don't actually do anything
            print(f"You found a {item}!")
            inventory.append(item)
        elif event == "idol":
            print("You found the Golden Idol!")
            inventory.append("Golden Idol")
            Has_Golden_Idol = True
        room["visited"] = True
    else:
        print("You’ve been here before.")
    
    print(f"Time remaining: {time_left}")
    if time_left <= 0:
        print("But you ran out of time. The walls collape down on you. Game over.")
        game_over = True

def show_inventory(): #Lists what you have in inventory
    if inventory:
        print("Inventory:", ", ".join(inventory))
    else:
        print("Your inventory is empty.")

def SAVE(): # Converts the tuple into string keys before saving because it won't work
    data = {
        "Player_Pos": Player_Pos,
        "inventory": inventory,
        "Has_Golden_Idol": Has_Golden_Idol,
        "time_left": time_left,
        "world": {
            f"{x},{y}": room for (x, y), room in world.items()
        }
    }
    try:
        with open("savegame.json", "w") as f:
            json.dump(data, f)
        print("Game saved.")
    except IOError:
        print("Error: Could not save the game.")

def LOAD(): # Has to convert the string keys back into tuple keys
    global Player_Pos, inventory, Has_Golden_Idol, world, time_left
    try:
        with open("savegame.json", "r") as f:
            data = json.load(f)
            Player_Pos = data["Player_Pos"]
            inventory = data["inventory"]
            Has_Golden_Idol = data["Has_Golden_Idol"]
            time_left = data["time_left"]
            world = {
                tuple(map(int, k.split(","))): v for k, v in data["world"].items()
            }
        print("Game loaded.")
    except (IOError, json.JSONDecodeError):
        print("Error: Could not load the game.")

def game_loop():
    global game_over
    Introduction()
    Make_World()
    while not game_over:
        if Player_Pos == [0, 0] and Has_Golden_Idol: # The game is over, but do you have the golden idol and are in the right place?
            print("You returned to the start with the Golden Idol. You win!")
            break
        cmd = get_command()
        if cmd.startswith("move"): # Basically takes the move {direction} and looks for the MOVE preparatory command and then uses only the {direction} executive command
            parts = cmd.split()
            if len(parts) == 2 and parts[1] in directions:
                move_player(parts[1])
            else:
                print("Can't possibly move in that way. Try: move up, move down, move east, move west")
        elif cmd == "look":
            check_room()
        elif cmd == "inventory":
            show_inventory()
        elif cmd == "save":
            SAVE()
        elif cmd == "load":
            LOAD()
        elif cmd == "quit":
            print("Thanks for playing! Seeya!")
            break
        else:
            print("Unknown command. Type \"help\" for help.")

if __name__ == "__main__":
    game_loop()

