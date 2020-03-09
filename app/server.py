import json
import os
import random

import bottle
from bottle import HTTPResponse

def open_spaces(data):
    spaces = []
    for y in range(0,data['board']['height']):
        for x in range(0,data['board']['width']):
            spaces.append({"y": y,"x": x})
    for snake in data['board']['snakes']:
        for position in snake['body']:
            if position in spaces: spaces.remove(position)
    return spaces

def next_pos(head, dir):
    #returns the next position of my snake if moved in a given direction
    head=head.copy()
    if dir == "up":
        head['y']-=1
    elif dir == "down":
        head['y']+=1
    elif dir == "left":
        head['x']-=1
    elif dir == "right":
        head['x']+=1
    return head
    
def possible_movez(head):
    data = bottle.request.json
    directions=["left", "right", "up", "down"]
    possible_moves = []
    for dir in directions:
        if next_pos(head, dir) in open_spaces(data):
            possible_moves.append(dir)
    return possible_moves
    
@bottle.route("/")
def index():
    return "Your Battlesnake is alive!"


@bottle.post("/ping")
def ping():
    """
    Used by the Battlesnake Engine to make sure your snake is still working.
    """
    return HTTPResponse(status=200)


@bottle.post("/start")
def start():
    """
    Called every time a new Battlesnake game starts and your snake is in it.
    Your response will control how your snake is displayed on the board.
    """
    data = bottle.request.json
    print("START:", json.dumps(data,sort_keys=True))

    
    response = {"color": "#2E66FF", "headType": "bwc-ski", "tailType": "bolt"}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )


@bottle.post("/move")
def move():
    """
    Called when the Battlesnake Engine needs to know your next move.
    The data parameter will contain information about the board.
    Your response must include your move of up, down, left, or right.
    """
    data = bottle.request.json
    print("MOVE:", data['turn'])
    print(json.dumps(data['you'],sort_keys=True))
    move = "none"
    # Choose a random direction to move in
    head = data['you']['body'][0]
    possible_moves = possible_movez(head)
    directions=["left", "right", "up", "down"]
    for move in possible_moves:
        if possible_movez(next_pos(head,move)) ==[]:
            possible_moves.remove(move)
    #move = random.choice(possible_moves)
    dict={}
    food = "false"
    for mv in possible_moves:
        if next_pos(head, mv) in data['board']['food']:
            move = mv
            food = "true"
    
    if food =="false":
        for mv in possible_moves:
            i=0
            if mv =="up":
                head1=head.copy()
                head1['y']-=1
                while next_pos(head1,mv) in open_spaces(data):
                    head1['y']-=1
                    i+=1
            elif mv =="down":
                head2=head.copy()
                head2['y']+=1
                while next_pos(head2,mv) in open_spaces(data):
                    head2['y']+=1
                    i+=1
            elif mv =="left":
                head3=head.copy()
                head3['x']-=1
                while next_pos(head3,mv) in open_spaces(data):
                    head3['x']-=1
                    i+=1
            elif mv =="right":
                head4=head.copy()
                head4['x']+=1
                while next_pos(head4,mv) in open_spaces(data):
                    head4['x']+=1
                    i+=1
            dict[mv]=i
    move = max(dict, key=lambda key: dict[key])

    #repeat for other directions
    #out of the remaining directions, choose the one that gives the most distance from a wall or from another snake.
    #if one space away from food, get the food
    
    
    # Shouts are messages sent to all the other snakes in the game.
    # Shouts are not displayed on the game board.
    shout = "I am a python snake!"
    print(possible_moves)
    print(move)
    response = {"move": move, "shout": shout}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )


@bottle.post("/end")
def end():
    """
    Called every time a game with your snake in it ends.
    """
    data = bottle.request.json
    print("END:", json.dumps(data))
    return HTTPResponse(status=200)


def main():
    bottle.run(
        application,
        host=os.getenv("IP", "0.0.0.0"),
        port=os.getenv("PORT", "8080"),
        debug=os.getenv("DEBUG", True),
    )


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == "__main__":
    main()
