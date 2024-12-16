import os
import time
import random

# File to store player registry
REGISTRY_FILE = "player_registry.txt"

# Display starting menu
def prompt():
    print("\t\tWelcome to the Quest of the Dungeon!\n\n\
You must collect all six items before fighting the boss.\n\n\
Moves:\t'go {direction}' (travel north, south, east, or west)\n\
\t'yes/no {item}' (add nearby item to inventory)\n\
\t'run' (escape from danger if encountered)\n")
    print("Enter the dungeon and explore!\n")


# Clear screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# Load registry from file
def load_registry():
    """Load the player registry from the file."""
    if os.path.exists(REGISTRY_FILE):
        registry = {}
        with open(REGISTRY_FILE, "r") as file:
            for line in file:
                try:
                    # Parse each line in the format: name|current_room|health|item1|item2|...
                    player_name, current_room, health, *inventory = line.strip().split("|")
                    registry[player_name] = {
                        'inventory': inventory,
                        'current_room': current_room,
                        'health': int(health) if health.isdigit() else 100,  # Default to 100 if invalid
                    }
                except ValueError:
                    # Skip invalid lines with a warning
                    print(f"Warning: Skipping invalid registry line: {line.strip()}")
        return registry
    else:
        # Return an empty registry if the file does not exist
        return {}


# Save registry to file
def save_registry(registry):
    with open(REGISTRY_FILE, "w") as file:
        for player_name, data in registry.items():
            file.write(f"{player_name}|{data['current_room']}|{data['health']}|{'|'.join(data['inventory'])}\n")


# Map of the dungeon
rooms = {
    'Liminal Space': {
        'Description': "A strange, endless corridor with flickering lights and echoing footsteps. You were given three direction to go where do you to go?",
        'North': 'Mirror Maze',
        'South': 'Bat Cavern',
        'East': 'Bazaar',
        'Item': None
    },
    'Mirror Maze': {
        'Description': "You arrive at a glittering room full of reflective surfaces, where your own image stares back at you.",
        'South': 'Liminal Space',
        'Item': 'Crystal'
    },
    'Bat Cavern': {
        'Description': "A dark, damp cave filled with the distant screeches of bats flitting above.",
        'North': 'Liminal Space',
        'East': 'Volcano',
        'Item': 'Staff'
    },
    'Bazaar': {
        'Description': "A bustling marketplace filled with peculiar merchants selling exotic goods.",
        'West': 'Liminal Space',
        'North': 'Meat Locker',
        'East': 'Dragons Lair',
        'South': 'Thunder Chamber',
        'Item': 'Altoids'
    },
    'Meat Locker': {
        'Description': "A frigid room lined with slabs of meat hanging on hooks. Your breath fogs up the air.",
        'South': 'Bazaar',
        'East': 'Quicksand Pit',
        'South': 'Dragons Lair',
        'Item': 'Fig'
    },
    'Quicksand Pit': {
        'Description': "A treacherous pit where the ground shifts and swallows anything that lingers too long.",
        'West': 'Meat Locker',
        'Item': 'Robe'
    },
    'Volcano': {
        'Description': "A fiery chamber with molten lava bubbling dangerously close.",
        'West': 'Bat Cavern',
        'East': 'Thunder Chamber',
        'Item': 'Fireball Tome',
    },
    'Dragons Lair': {
        'Description': "A serene training hall with wooden floors and a powerful presence. The dragon awaits.",
        'West': 'Bazaar',
        'Boss': 'Dragon', # to defeat the dragon you need to hit 3 attack which is 2 spell and physical attack
        'Item': None
    },
    'Thunder Chamber': {
        'Description': "You arrive at an electrified room filled with arcing bolts of lightning and a charged atmosphere at the middle of the room you find a rare item you looking for an item.",
        'North': 'Bazaar',
        'East': 'Volcano',
        'Item': 'Thunder Scroll',
    }
}


# Updated ASCII Art with directions
ascii_art = {
    'Liminal Space': """\
  
        ========================================
        ||                                   ||
        ||                                   ||
        ||          ~~~~~~~~~~~~~~           ||
        ||          |            |           ||
        ||          |            |           ||
        ||          |            |           ||
        ||          |            |           ||
        ||          |            |           ||
        ||          |            |           ||
        ||          |            |           ||
        ||          |            |           ||
        ||          ~~~~~~~~~~~~~~           ||
        ||                                   ||
        ||                                   ||
        ||      >>>>>    ||    <<<<<         ||
        ||===================================||
        ||                                   ||
        ||                                   ||
        ||                                   ||
        ||       Shadows flicker and fade    ||
        ||       Echoes in endless halls     ||
        ||                                   ||
        ||===================================||                
      
   
    """,
    'Mirror Maze': """\
          _____________________________________________________
     /                                                     \\
    |      _______      _______      _______      _______   |
    |     |       |    |       |    |       |    |       |  |
    |     | (O O) |    | (O O) |    | (O O) |    | (O O) |  |
    |     |   |   |    |   |   |    |   |   |    |   |   |  |
    |     |___|___|    |___|___|    |___|___|    |___|___|  |
    |      /     \      /     \      /     \      /     \   |
    |     /_______\    /_______\    /_______\    /_______\  |
    |                                                     |  
    |     The reflections multiply,                       |  
    |     the paths confuse,                              |  
    |     as whispers echo through the shiny walls.       |  
    |_____________________________________________________|
                     ||                     ||
                     ||                     ||
                   [===]                 [===]
                   [===]                 [===]
                   [===]                 [===]

        Snake-like paths twist and turn, leading you deeper into 
        the labyrinth of endless reflections and illusions.
    """,
    'Bat Cavern': """\
            _.-.
       __.-' ,  \       A dark, damp cave...
      '--.-'    \      You hear distant screeches
          \       \   as bats flit above...
           |,  .-.  \\
           | )/   \  |          
           |/|      \|          
           ||       ||,--.    
      _.-' |       ||   |      
     {_     \       ||   |      
       '-._  '-._   ||   |      
           '-._  './/|   |      
              '-._     _.'      
                 '-.,-'     
    """,
    'Bazaar': """\
    
                  ~~~ Bazaar ~~~
          ______________________________
         |                              |
         |    🐍   Exotic Goods   🐍    |
         |______________________________|
          /                              \\
         /    .---.          .---.        \\
        |    ( o o )        ( o o )        |
         \    '-._.'  🐍🐍  '-._.'        /
          \                              /
           |        🏺   🗡️   📜         |
           |  🌴   ~~~~   🪙   🧪   🌴    |
           |______________________________|
          /         Step inside!          \\
         /__________________________________\\
        |                                    |
        |  Merchants of curiosities await!   |
        |____________________________________|
    """,
    'Meat Locker': """\
    
      _________________________
     /                         \\
    /   MEAT LOCKER             \\
   /_____________________________\\
   ||       ||       ||       || |
   ||  ||   ||  ||   ||  ||   || |
   ||__||___||__||___||__||___||_|
   ||--||---||--||---||--||---||-|
   ||  ||   ||  ||   ||  ||   || |
   ||  ||   ||  ||   ||  ||   || |
   ||  ||   ||  ||   ||  ||   || |
   ||   \\   ||  ||   //       || 
   ||    \\  ||  ||  //        ||
   ||     \\ ||  || //         ||
   ||      \\||  ||//          ||
   ||       \\\\  ///          ||
   ||        \\\\///           ||
   ||         \\//             ||
   ||__________________________||  
   ||||||||||||||||||||||||||||||  
    """,
    'Quicksand Pit': """\
     
           ___
                   .-'   `-.
                  /         \\
                 ;           ;
        ________|           |________
       /                           \    
      /                             \    
     ;                               ;
    |                                 |
    ;                 O                \\
    \                /|\                ;
     \               / \                |
     |                                 ;
     \                               /
      `.                           .'
        `-.                       .-'
           \                     /
            \                   /
             ;                 ;
              |                |
              ;                ;
             /                 \\
            ;                   ;
           /                     \\
         .-`-.                 .-`-.
        /     \               /     \\
       ;       ;             ;       ;
      /         \           /         \\
     /           \         /           \\
    ;             ;       ;             ;
   /               \     /               \\
  ;                 ;   ;                 ;
  ;                 ;   ;                 ;
   \               /     \               /
    `.           .'       `.           .'
      `-._____.'           `-._____.-'
            |                    |
            |                    |
            |                    |
            |      PIT           |
            |       OF            |
            |      DOOM          |
            |                    |
            |                    |
            |                    |



    """,
    'Volcano': """\

                   🔥
                  /   \\
                 /     \\
                /       \\
               /         \\
              /           \\
         ~~~~~~~~~~~~~~~~~~~~~~
   
    """,
    'Dragons Lair': """\

           /\     ____
          //\\   ||||||
         //__\\  ||||||   /\  /\   ____
        //____\\ ||||||  //\\//\\ ||||||
       //      \\|||||| //__\/__\\||||||
       ===============================||
       ||          DRAGON'S         ||||
       ||           LAIR            ||||
       ||============================||||
       ||    Beware the mighty      ||||
       ||    dragon guarding its    ||||
       ||    treasure!              ||||
       ||============================||||
       ||||                        ||||||
       ||||________________________||||||
       ||============================||||
       ||||||||||||||||||||||||||||||||||
       ||||||||||||||||||||||||||||||||||
       ||||||||||||||||||||||||||||||||||
    
    """,
    'Thunder Chamber': """\
       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      ~    ⚡ Thunder Chamber ⚡   ~
      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        |                      |
        |   ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡   |
        |                      |
        | ⚡     ⚡     ⚡     ⚡  |
        |                      |
        |   ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡   |
        |                      |
        ~~~~~~~~~~~~~~~~~~~~~~~~~
    """
}

# Initialize registry and player info
registry = load_registry()
current_player = None

def select_player():
    """Allow the user to select an existing player or create a new one."""
    global current_player, registry
    print("Player Registry:")
    print("Existing Players:")
    for idx, player in enumerate(registry.keys(), start=1):
        print(f"{idx}. {player}")

    print(f"{len(registry) + 1}. Create a new player")
    choice = int(input("Select a player (or create a new one): "))

    if choice == len(registry) + 1:
        name = input("Enter the name for your new player: ").strip()
        if name in registry:
            print("This player already exists. Try again.")
            select_player()
        else:
            registry[name] = {'inventory': [],'skills': [], 'current_room': 'Liminal Space', 'health': 100}
            current_player = name
    else:
        current_player = list(registry.keys())[choice - 1]

    print(f"Welcome, {current_player}!")


def save_player_progress():
    """Save the current player's progress in the registry."""
    registry[current_player]['inventory'] = inventory
    registry[current_player]['current_room'] = current_room
    registry[current_player]['health'] = health
    save_registry(registry)


# Danger event chance
def danger_event():
    """Random chance of danger occurring in the current room."""
    dangers = [
        "a pack of wild bats swoops down at you!",
        "a collapsing ceiling threatens to crush you!",
        "a shadowy figure with glowing eyes approaches menacingly!"
    ]
    return random.choice(dangers) if random.random() < 0.3 else None


def enemy_attack():
    """Simulate an enemy attack."""
    attacks = [
        {'name': 'wild bats', 'damage': random.randint(5, 15)},
        {'name': 'falling debris', 'damage': random.randint(10, 20)},
        {'name': 'shadow figure', 'damage': random.randint(8, 18)}
    ]
    return random.choice(attacks)

# enemy Handling
def handle_enemy(enemy):
    if enemy == 'Dragon':
        if len(inventory) < 6:
            print("You cannot defeat the Dragon without all six items! You are automatically defeated.")
            return False  # Player loses if they don't have all items
    else:
     """Handle the fight with an enemy or boss."""
    print(f"You are facing {enemy}! Prepare for battle.")

    # Player and enemy attributes
    player_health = health
    enemy_health = 50  # Example boss health
    spells = ['fireball', 'thunder strike', ]  
    
    while player_health > 0 and enemy_health > 0:
        print(f"Your health: {player_health} | {enemy}'s health: {enemy_health}")
        print("Choose your action:")
        print("1. Physical attack")
        print("2. Cast a spell")
        
        choice = input("> ").strip()
        
        if choice == "1":
            # Physical attack
            damage = random.randint(10, 20)
            print(f"You strike {enemy} and deal {damage} damage!")
            enemy_health -= damage
        
        elif choice == "2":
            # Spell attack
            print("Choose a spell to cast:")
            for i, spell in enumerate(spells, 1):
                print(f"{i}. {spell}")
            spell_choice = input("> ").strip()
            
            if spell_choice.isdigit() and 1 <= int(spell_choice) <= len(spells):
                spell_damage = random.randint(15, 30)
                print(f"You cast {spells[int(spell_choice) - 1]} and deal {spell_damage} damage!")
                enemy_health -= spell_damage
            else:
                print("Invalid spell choice. You lose your turn!")
        
        else:
            print("Invalid action. You lose your turn!")
        
        # Enemy's turn
        if enemy_health > 0:
            enemy_damage = random.randint(10, 25)
            print(f"{enemy} attacks and deals {enemy_damage} damage!")
            player_health -= enemy_damage
    
    if player_health > 0:
        print(f"You defeated {enemy}!")
        return True
    else:
        print(f"You were defeated by {enemy}.")
        return False

# Gameplay starts here
clear()
prompt()
select_player()

# Load player progress
inventory = registry[current_player]['inventory']
current_room = registry[current_player]['current_room']
health = registry[current_player]['health']
msg = ""

    # random 1 or 2
    # if equal to 1, pick_item
    # if equal to 2, enemy encounter

def user():
    print(ascii_art.get(current_room, ""))
    time.sleep(2)

    # Display player info
    room_desc = rooms[current_room]['Description']
    print(f"You are in the {current_room}\n{room_desc}")
    print(f"Inventory: {inventory}")
    print(f"Health: {health}\n{'-' * 30}")
    

# def pick_item():
#
#
# def event():
#     global health



# Updated Main Gameplay Loop
# Updated Main Gameplay Loop
while True:
    clear()
    user()

    # Display available directions
    directions = [key for key in rooms[current_room].keys() if key in ['North', 'South', 'East', 'West']]
    print("Available directions: ", ", ".join(directions))
    print("\nType the keyword 'Go' before the direction")
    user_input = input("Choose Direction: ").strip()
    next_move = user_input.split(' ')
    action = next_move[0].title()

    if action == "Go":
        direction = next_move[1].title()
        if direction in rooms[current_room]:
            current_room = rooms[current_room][direction]
            msg = f"You travel {direction}."
            print("\n" + msg)
        else:
            msg = "You can't go that way."

    elif action == "Exit":
        save_player_progress()
        print("Goodbye! Your progress has been saved.")
        break

    else:
        print("Invalid command. Try again.")
        continue  # Skip the rest of the loop and ask for input again

    user()
    # num = random.randint(1, 2)
    # if num == 1:
    #     pick_item()
    #     enemy_encounter()
    # else:
    #     enemy_encounter()
    #     pick_item()
    # Check for items in the room


    # Check if the player is in the boss room
    if 'Boss' in rooms[current_room]:
        boss = rooms[current_room]['Boss']
        print(f"You have entered the {current_room}. {rooms[current_room]['Description']}")
        print(f"A {boss} stands before you!")
        
        # Invoke boss fight
        boss_defeated = handle_enemy(boss)
        if boss_defeated:
            print("Congratulations! You have defeated the Dragon and completed your quest!")
            save_player_progress()
            break
        else:
            print("You have been defeated by the Dragon. Game over!")
            save_player_progress()
            break

    # Danger event (optional, before item pickup)
    danger = danger_event()
    if danger:
        print(f"Suddenly, {danger}")
        print("Do you want to run? (Type 'run') Or face the danger (Type 'stay')?")
        choice = input("\nEnter your choice: ").strip().lower()
        if choice == "run":
            print("You ran away safely! But you feel a bit shaken.")
            health -= 10
        elif choice == "stay":
            attack = enemy_attack()
            print(f"You bravely faced the {attack['name']}! It attacks and deals {attack['damage']} damage.")
            health -= attack['damage']
        else:
            print("Invalid choice! You hesitated, and the danger inflicted 10 damage.")
            health -= 10

        if health <= 0:
            print("You have perished in the dungeon. Game over!")
            save_player_progress()
            break

    # Check for items in the room
    if rooms[current_room].get('Item') and rooms[current_room]['Item'] not in inventory:
        item = rooms[current_room]['Item']
        print(f"You see a {item} here. Do you want to pick it up? (yes/no)")
        choice = input("> ").strip().lower()
        if choice == 'yes':
            inventory.append(item)
            print(f"You picked up the {item}!")
            rooms[current_room]['Item'] = None  # Remove the item from the room
        else:
            print("You decided not to pick up the item.")

    # Save progress after each action
    save_player_progress()
