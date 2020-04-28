from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json

# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))

@api_view(["GET"])
def generateWorld(request):
    Room.objects.all().delete()
    # generate grid size 14 * 14
    grid = [0] * 14

    for i in range(14):
        grid[i] = [0] * 14

    # iterating over each column
    for y in range(0, len(grid)):
        for x in range(0, len(grid)):
            if grid[y][x] != 0:
                continue

            new_room = Room(
                title="Outside Cave Entrance",
                description="North of you, the cave mount beckons",
                x=x,
                y=y)
            chosen_type = new_room.randRoom()

            new_room.save()

            shape_not_found = True
            # while true iterate
            while shape_not_found:                
                # if chosen type is 1
                if chosen_type == 1:
                    # place on grid
                    grid[y][x] = new_room.id
                    shape_not_found = False
                    # maybe ?  save >> new_room.save()
                    # or this at the end grid.save()

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
                    else:
                        # place in reserved the next value {'room_id': (x + 1, y)}

                        # place room in grid
                        grid[y][x] = new_room.id
                        grid[y][x+1] = new_room.id
                        shape_not_found = False

                # if chose type is 3 []
                #                    []
                if chosen_type == 3:
                    # if y axis + 1 is within grid or not
                    if (new_room.y + 1) > (len(grid) -1 ):
                        # and if is within grid x axis or not
                        if (new_room.y + 1) > (len(grid) - 1):
                            # if not available in both direction
                            # then chose 1 (single cell)
                            chosen_type = 1
                        else:
                            chosen_type = 2
                    # if within 
                    else:
                        # place in reserved the next value {'room_id': (x, y + 1)}

                        # place room in grid
                        grid[y][x] = new_room.id
                        grid[y+1][x] = new_room.id
                        shape_not_found = False
                
    return JsonResponse({'map': grid }, safe=True)


@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = room.playerNames(player_id)
    return JsonResponse({'uuid': uuid, 'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players}, safe=True)


# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs={"n": "north", "s": "south", "e": "east", "w": "west"}
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
        player.currentRoom=nextRoomID
        player.save()
        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
        # for p_uuid in currentPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        # for p_uuid in nextPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({'name':player.user.username, 'title':nextRoom.title, 'description':nextRoom.description, 'players':players, 'error_msg':""}, safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse({'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'error_msg':"You cannot move that way."}, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error':"Not yet implemented"}, safe=True, status=500)


# # generate grid size 
# used_grid_cells = []

# # maybe get from the user request the size of the maze, 100 or 500??

# # clear previously generated world >> (i.e. using - Room.objects.all().delete())

# for i in range(0, 100):


#     found=False
#     # while loop until it finds free space in grid
#     if not in user_grid_cells:
#         # place 
#     else: 
#         # generate new randomInt x and y 
#             # if this shape 
#             # once found free cells 
#                 # found=True
#                 # place in used_grid_cell
#                 return room
        

#     # choose a random type of room to generate within instantiation

#     # create new intance of the room, with all necessary properties

#     # add all properties, like a randomized title and description

#     # save room at each iteration on the matrix using >> .save()

# # iterate over matrix once more and create connections between rooms using a corridor
#     # use both x,y axis and see if when room is reached if it has
#     # already a connection on that cardinal point or not
#         # if not connect
#         # else try changing direction
#             # if possible make connection
#             # else try opposite direction
#             # if not possible maybe connect also to previously connected room?

# # return JSON version serialized version of the world to the client
# # research how to return serialized dictionaries, etc..