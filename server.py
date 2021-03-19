import os
import random

import cherrypy

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""

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

class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "",  # TODO: Your Battlesnake Username
            "color": "#2E66FF",  # TODO: Personalize
            "head": "bwc-ski",  # TODO: Personalize
            "tail": "bolt",  # TODO: Personalize
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        data = cherrypy.request.json
        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
