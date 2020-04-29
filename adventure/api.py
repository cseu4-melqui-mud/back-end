from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
from .serializer import RoomSerializer
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
                title="Outside Cave Entrance",
                description="North of you, the cave mount beckons",
                x=x,
                y=y)
            # generate a random shape between 1 and 3
            chosen_type = new_room.randRoom()
            # save instance of room in database
            new_room.save()
            rooms[new_room.id] = new_room
            shape_not_found = True
            # while shape is not found iterate
            while shape_not_found:
                # if chosen type is 1
                if chosen_type == 1:
                    # place on grid the room id
                    grid[y][x] = new_room.id
                    # new_room.set_connections(y, x)
                    # exit loop
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
                    else:
                        # place room in grid
                        grid[y][x] = new_room.id
                        # assign to the very next room the same id
                        grid[y][x+1] = new_room.id
                        # exit loop
                        shape_not_found = False
                # if chose type is 3 []
                #                    []
                if chosen_type == 3:
                    # if y axis + 1 is within grid or not
                    # and if is within grid x axis or not
                    if (new_room.y + 1) > (len(grid) - 1)
                       if (new_room.y + 1) > (len(grid) - 1):
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
                        shape_not_found = False
    def getRoomById(y, x):
        if x >= 0 and x < len(grid) and y >= 0 and y < len(grid):
            room_id = grid[y][x]
            return rooms[room_id]
        return None
    for y in range(len(grid)):
        for x in range(len(grid)):
            current_room = getRoomById(y, x)
            # if current_room is None:
            #     continue
            north_room = getRoomById(y - 1, x) # -1, 0
            east_room = getRoomById(y, x + 1)
            south_room = getRoomById(y + 1, x)
            west_room = getRoomById(y, x - 1)
            # if north
            # if room to the north is not outside of grid & two rooms don't share same id
            if (y - 1) >= 0 and north_room is not None:
                if current_room.id != north_room.id:
                # if current room has no connection in that direction
                    current_room.connectRooms(north_room, 'n')
                    north_room.connectRooms(current_room, 's')
            # if east
            if (x + 1) < len(grid) and east_room is not None:
                # if current room has no connection in that direction
                if current_room.id != east_room.id:
                    current_room.connectRooms(east_room, 'e')
                    east_room.connectRooms(current_room, 'w')
            # if south
            if (y + 1) < len(grid) and south_room is not None:
                # if current room has no connection in that direction
                if current_room.id != south_room.id:
                    current_room.connectRooms(south_room, 's')
                    south_room.connectRooms(current_room, 'n')
            # if west
            if (x - 1) >= 0 and west_room is not None:
                # if current room has no connection in that direction
                if current_room.id != west_room.id:
                    current_room.connectRooms(west_room, 'w')
                    west_room.connectRooms(current_room, 'e')
    # return grid in response
    return JsonResponse({'map': grid, 'rooms': RoomSerializer(Room.objects.all(), many=True).data}, safe=True)


@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = room.playerNames(player_id)
    return JsonResponse({'uuid': uuid, 'name': player.user.username, 'title':room.title, 'description':room.description, 'players':players}, safe=True)
# @csrf_exempt
@api_view(["POST"])
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
        # for p_uuid in currentPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        # for p_uuid in nextPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({'name': player.user.username, 'title':nextRoom.title, 'description':nextRoom.description, 'players':players, 'error_msg':""}, safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse({'name': player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'error_msg':"You cannot move that way."}, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error': "Not yet implemented"}, safe=True, status=500)
