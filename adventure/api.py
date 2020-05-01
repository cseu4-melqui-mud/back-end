from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import permissions
from .serializer import RoomSerializer
import json
# instantiate pusher
pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config(
    'PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def generateWorld(request):
    Room.objects.all().delete()
    # generate grid size 14 * 14
    grid = [0] * 14
    for i in range(14):
        grid[i] = [0] * 14

    def generateTitle():
        titles = [
            "Death Knight's Squire",
            "Tyrant of Zhentil Keep",
            "Raven's Cave",
            "The Tortured Land",
            "Drums at Daggerford",
            "Labyrinth of Lies",
            "Lion Maze",
            "Menace of the Icy Spire",
            "Vault of Tgozur",
            "The Oracle Dungeon",
            "Black Opal",
            "Shadow of Waterdeep",
            "Atlas",
            "Ravenloft",
            "Baldur's Gates",
            "Amarunes",
            "The Madhouse of Taska",
            "Eberron Cave",
            "Crimson Vault",
            "Rogue Cave",
            "Reach of Batfolk",
            "Companions Retreat",
            "Hillfar Dungeon",
            "Ruins of Mbala",
            "Hellturel",
            "Saltmarsh Dungeon",
            "Zariel",
            "Dragon's Breath Reach",
            "Xanathar's Lair",
            "Tgozur Vault",
            "Avernus"
        ]

        return random.choice(titles)

    def genDescr(title):
        list1 = ["A grand", "A large", "A massive", "A minor", "A modest",
                 "A narrow", "A short", "A small", "A tall", "A wide"]
        list2 = ["overgrown boulder", "granite door", "pair of granite doors", "broken statue", "worn statue", "pair of worn statues", "boulder",
                 "dark cave", "murky cave", "fallen tree", "waterfall", "crypt", "broken temple", "fallen temple", "graveyard", "fallen tower"]
        list3 = ["bog", "boulder field", "cliff side", "forest", "grove", "marsh", "morass", "mountain base",
                 "mountain range", "mountain top", "snowland", "swamp", "thicket", "wasteland", "woodlands", "woods"]
        list4 = ["large", "small", "massive",
                 "grand", "modest", "scanty", "narrow"]
        list5 = ["broken", "clammy", "crumbling", "damp", "dank", "dark", "deteriorated", "dusty",
                 "filthy", "foggy", "grimy", "humid", "putrid", "ragged", "shady", "timeworn", "weary", "worn"]
        list6 = ["ash", "bat droppings", "broken pottery", "broken stone", "cobwebs", "crawling insects", "dead insects", "dead vermin",
                 "dirt", "large bones", "moss", "puddles of water", "rat droppings", "remains", "roots", "rubble", "small bones"]
        lsit7 = ["a broken statue part of a fountain", "a broken tomb", "a pillaged treasury", "an altar", "an overgrown underground garden", "broken arrows, rusty swords and skeletal remains", "broken cages and torture devices", "broken mining equipment", "broken vats and flasks", "carved out openings filled with pottery", "cases of explosives and mining equipment", "drawings and symbols on the walls", "empty chests and broken statues", "empty shelves and broken pots", "locked chests, vats, crates and pieces of broken wood", "prison cells",
                 "remnants of a small camp", "remnants of sacks, crates and caskets", "remnants of statues", "remnants of what once must've been a mess hall of sorts", "remnants of what was once a decorated room with a now unknown purpose", "rows of statues", "rows of tombs and several statues", "rows of vertical tombs", "ruins of what seems to be a crude throne room", "the remnants of a pillaged burial chamber", "triggered traps and skeletal remains", "warped and molten metal remnants", "weapons racks and locked crates", "what seems like some form of a sacrificial chamber"]
        list8 = ["is a single path", "are two paths, you take the right", "are two paths, but the right is a dead end", "are two paths, you take the left",
                 "are two paths, but the left is a dead end", "are three paths, you take the right", "are three paths, you take the left", "are three paths, you take the middle"]
        list9 = ["downwards", "onwards", "passed broken and pillaged tombs", "passed collapsed rooms and pillaged treasuries", "passed countless other pathways",
                 "passed countless rooms", "passed long lost rooms and tombs", "passed lost treasuries, unknown rooms and armories", "passed pillaged rooms", "passed several empty rooms"]
        list10 = ["clammy", "crumbled", "damp", "dank", "dark", "dusty", "filthy", "foggy", "ghastly",
                  "ghostly", "grimy", "humid", "putrid", "ragged", "shady", "timeworn", "weary", "worn"]
        list11 = ["An altar in the center is covered in runes, some of which are glowing", "An enormous beastly skeleton is chained to the walls", "Countless traps, swinging axes and other devices move all around. They're either still active, or just activated", "It's filled with hanging cages which still hold skeletal remains", "It's filled with strange glowing crystals and countless dead vermin", "It's filled with tombs, but their owners are spread across the floor", "It's filled with tombs, some of which no longer hold their owner", "It's littered with skeletons, but no weaponry in sight", "It's packed with boxes full of runes and magical equipment, as well as skeletons", "Piles and piles of gold lie in the center, several skeletons lie next to it", "Remnants of a makeshift barricade still 'guard' the group of skeletons behind it", "Rows upon rows of shelves are packed with books or remnants of books. In the center sits a single skeleton", "Several cages hold skeletal remains of various animals. Next to the cages are odd machines",
                  "Several stacks of gunpowder barrels are stacked against a wall. A skeleton holding a torch lies before it", "Small holes and carved paths cover the walls, it looks like a community or burrow for small creatures", "Spiderwebs cover everything, large figures seem to be wrapped in the same web", "The floor is riddled with shredded blue prints and a half finished machine sits in a corner", "The room is filled with lifelike statues of terrified people", "There are several braziers scattered around, somehow they're still burning, or burning again", "There's a demolished door with a sign that says \"don't open\"", "There's a huge skeleton in the center, along with dozens of human skeletons", "There's a pile of skeletons in the center, all burned and black", "There's a round stone in the center, around it are a dozen skeletons in a circle", "There's a seemingly endless hole in the center. Around it are what seem like runes", "There's machinery all over the place, probably part of a workshop of sorts"]
        list12 = ["advance carefully", "carefully continue", "cautiously proceed",
                  "continue", "move", "press", "proceed", "slowly march", "slowly move", "tread"]
        list13 = ["darkness", "depths", "expanse", "mysteries",
                  "secret passages", "secrets", "shadows"]
        list14 = ["a few more passages", "a few more rooms and passages", "countless passages", "dozens of similar rooms and passages",
                  "many different passages", "many rooms and passages", "various different rooms and countless passages", "various passages"]
        list15 = ["A big", "A grand", "A huge", "A large", "A massive", "A mysterious",
                  "A tall", "A thick", "A vast", "A wide", "An enormous", "An immense", "An ominous"]
        list16 = ["wooden", "granite", "metal"]
        list17 = ["some are dead ends, others lead to who knows where, or what", "some have collapsed, others are dead ends or too dangerous to try", "most of which are far too ominous looking to try out", "most of which have collapsed or were dead ends to begin with", "some of them have collapsed, others seem to go on forever", "some are dead ends, others seem to have no end at all", "each leading to who knows where, or what",
                  "most of which probably lead to other depths of this dungeon", "most of which look just like the other", "they all look so similar, this whole place is a maze", "each seem to go on forever, leading to who knows what", "some look awfully familiar, others stranger everything else", "each with their own twists, turns and destinations", "most lead to nowhere or back to this same path", "it's one big labyrinth of twists and turns"]
        list18 = ["Ash and soot is", "Countless odd symbols are", "Countless runes are", "Dire warning messages are", "Dried blood splatters are",
                  "Intricate carvings are", "Large claw marks are", "Messages in strange languages are", "Ominous symbols are", "Strange writing is", "Various odd symbols are"]
        list19 = ["did something just move behind this door?", "you're sure you saw a shadow under the cracks of the door.", "did the door just change its appearance?", "what was that sound?", "you're pretty sure you're being watched.", "was that a growl coming from behind the door?", "did somebody just knock on the door?", "you hear the faint sound of footsteps behind you.",
                  "is that a scratching sound coming from behind the door?", "you think you can hear a whisper coming from behind the door.", "light's coming through the gap below the door.", "you hear a loud bang in the distance from which you came.", "you hear a faint laugh coming from behind the door.", "suddenly the door slowly opens on its own.", "something just grabbed your shoulder."]
        list20 = ["bleak", "dark", "dire", "eerie", "foggy", "gloomy", "grim",
                  "misty", "murky", "overcast", "shadowy", "shady", "sinister", "somber"]
        list21 = ["aged", "battered", "busted", "decayed", "demolished", "destroyed", "deteriorated",
                  "forgotten", "frayed", "long lost", "pillaged", "tattered", "wasted", "weathered", "worn", "worn down"]
        list22 = ["absorbed", "butchered", "claimed", "consumed", "defaced", "desolated", "devoured", "dismantled",
                  "drained", "eaten", "maimed", "mutilated", "ravaged", "ravished", "spoiled", "taken", "wiped out", "wrecked"]

        firstP = f"{random.choice(list1)} {random.choice(list2)} in a {random.choice(list20)} {random.choice(list3)} marks the entrance to this dungeon. Beyond the {random.choice(list2)} lies a {random.choice(list4)}, {random.choice(list5)} room. It's covered in {random.choice(list6)}, {random.choice(list6)} and {random.choice(list6)}."

        secondP = f"You {random.choice(list12)} onwards, deeper into the {title} {random.choice(list13)}. You pass {random.choice(list14)}, {random.choice(list17)}. You eventually make it to what is likely the final room. {random.choice(list15)} {random.choice(list16)} door blocks your path. {random.choice(list18)} all over it, somehow untouched by time and the elements. You step closer to inspect it and.. wait.. {random.choice(list19)}"

        return f"{firstP} \n {secondP}"

    rooms = dict()
    # iterating over each column
    for y in range(0, len(grid)):
        # for each column check each cell in the row
        for x in range(0, len(grid)):
            # if cell is not empty
            if grid[y][x] != 0:
                # move to the next cell
                continue
            # create new instance of room
            new_room = Room(
                title=generateTitle(),
                description="",
                x=x,
                y=y)

            new_room.description = genDescr(new_room.title)

            # generate a random shape between 1 and 3
            chosen_type = random.randint(1, 3)
            # save instance of room in database
            new_room.save()

            shape_not_found = True
            # while shape is not found iterate
            while shape_not_found:
                # if chosen type is 1
                if chosen_type == 1:
                    # place on grid the room id
                    grid[y][x] = new_room.id
                    # exit loop
                    new_room.setType(chosen_type)
                    shape_not_found = False
                # chosen type is equal to 2 [][]
                if chosen_type == 2:
                    # check if next cell is available
                    if (new_room.x + 1) > (len(grid) - 1):
                        # if not available on x axis, then check
                        # if avaiable on y axis
                        if (new_room.y + 1) > (len(grid) - 1):
                            # if not available then just use 1 (single cell)
                            chosen_type = 1
                        # else if y axis is available
                        else:
                            # change shape to num 3
                            chosen_type = 3
                    # if is available
                    elif grid[y][x+1] == 0:
                        # place room in grid
                        grid[y][x] = new_room.id
                        # assign to the very next room the same id
                        grid[y][x+1] = new_room.id
                        # exit loop
                        new_room.setType(2)
                        shape_not_found = False
                    else:
                        chosen_type = 1

                # if chose type is 3 []
                #                    []
                if chosen_type == 3:
                    # if y axis + 1 is within grid or not
                    # and if is within grid x axis or not
                    if (new_room.y + 1) > (len(grid) - 1):
                        if (new_room.x + 1) > (len(grid) - 1):
                            # if not available in both direction
                            # then chose 1 (single cell)
                            chosen_type = 1
                        else:
                            chosen_type = 2
                    # if within
                    else:
                        # place room in grid
                        grid[y][x] = new_room.id
                        # give to the next room the same room id
                        grid[y+1][x] = new_room.id
                        # close while loop
                        new_room.setType(chosen_type)
                        shape_not_found = False

            rooms[new_room.id] = new_room

    def getRoomById(y, x):
        if x >= 0 and x < len(grid) and y >= 0 and y < len(grid):
            room_id = grid[y][x]
            return rooms[room_id]
        return None

    for y in range(len(grid)):
        for x in range(len(grid)):
            current_room = getRoomById(y, x)
            north_room = getRoomById(y - 1, x)  # -1, 0
            east_room = getRoomById(y, x + 1)
            south_room = getRoomById(y + 1, x)
            west_room = getRoomById(y, x - 1)

            # if north
            # if room to the north is not outside of grid & two rooms don't share same id
            if (y - 1) >= 0 and north_room is not None:
                if current_room.n_to != 0:
                    choice = random.choice([current_room.n_to, north_room.id])
                    if choice == current_room.n_to:
                        continue
                if current_room.id != north_room.id:
                    # if current room has no connection in that direction
                    current_room.connectRooms(north_room, 'n')
                    north_room.connectRooms(current_room, 's')
            # if east
            if (x + 1) < len(grid) and east_room is not None:
                if current_room.e_to != 0:
                    choice = random.choice([current_room.e_to, east_room.id])
                    if choice == current_room.e_to:
                        continue
                # if current room has no connection in that direction
                if current_room.id != east_room.id:
                    current_room.connectRooms(east_room, 'e')
                    east_room.connectRooms(current_room, 'w')
            # if south
            if (y + 1) < len(grid) and south_room is not None:
                if current_room.s_to != 0:
                    choice = random.choice([current_room.s_to, south_room.id])
                    if choice == current_room.s_to:
                        continue
                # if current room has no connection in that direction
                if current_room.id != south_room.id:
                    current_room.connectRooms(south_room, 's')
                    south_room.connectRooms(current_room, 'n')

            # if west
            if (x - 1) >= 0 and west_room is not None:
                # if current room has no connection in that direction
                if current_room.w_to != 0:
                    choice = random.choice([current_room.w_to, west_room.id])
                    if choice == current_room.w_to:
                        continue

                if current_room.id != west_room.id:
                    current_room.connectRooms(west_room, 'w')
                    west_room.connectRooms(current_room, 'e')

    # return grid in response
    allRooms = RoomSerializer(Room.objects.all(), many=True).data
    return JsonResponse({'map': grid, 'rooms': allRooms, 'number': len(allRooms)},  safe=True)


@csrf_exempt
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def rooms(request):
    allRooms = Room.objects.all()

    grid = [0] * 14
    for i in range(14):
        grid[i] = [0] * 14

    for room in allRooms:
        grid[room.y][room.x] = room.id
        if room.room_type == 2:
            grid[room.y][room.x+1] = room.id
        if room.room_type == 3:
            grid[room.y+1][room.x] = room.id

    return JsonResponse({'map': grid, 'rooms': RoomSerializer(Room.objects.all(), many=True).data}, safe=True)


@csrf_exempt
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = room.playerNames(player_id)
    return JsonResponse({'uuid': uuid, 'name': player.user.username, 'room': RoomSerializer(room).data, 'players': players}, safe=True)


@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def move(request):
    dirs = {"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    room = player.room()
    nextRoomID = None
    if direction == "n":
        nextRoomID = room.n_to
    elif direction == "s":
        nextRoomID = room.s_to
    elif direction == "e":
        nextRoomID = room.e_to
    elif direction == "w":
        nextRoomID = room.w_to
    if nextRoomID is not None and nextRoomID > 0:
        nextRoom = Room.objects.get(id=nextRoomID)
        player.currentRoom = nextRoomID
        player.save()
        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
        for p_uuid in currentPlayerUUIDs:
            pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {
                           'message': f'{player.user.username} has walked {dirs[direction]}.'})
        for p_uuid in nextPlayerUUIDs:
            pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {
                           'message': f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({'name': player.user.username, 'title': nextRoom.title, 'description': nextRoom.description, 'players': players, 'error_msg': ""}, safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse({'name': player.user.username, 'room': RoomSerializer(nextRoom).data, 'players': players, 'error_msg': "You cannot move that way."}, safe=True)


@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def say(request):
    # IMPLEMENT
    data = json.loads(request.body)
    message = data.message
    player = request.user.player
    room = player.room()
    currentPlayerUUIDs = room.playerUUIDs(player_id)
    for p_uuid in currentPlayerUUIDs:
        pusher.trigger(f'p-channel-{p_uuid}', u'broadcast',
                       {'message': f"{player} says \"{message}\""})

    # return JsonResponse({'error': "Not yet implemented"}, safe=True, status=500)
