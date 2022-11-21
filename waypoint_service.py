# -*- coding: utf-8 -*-


import http.server
import socketserver
import json

PORT = 80

class WaypointService(http.server.BaseHTTPRequestHandler):
    
    def __init__(self, *args):
        super().__init__(*args)
        self.fields = {}
        
    def compute_waypoints_from_polygon(self,polygon):
        waypoints = []
        return waypoints
    
    def register_new_field(self, field_name, polygon):
        waypoints = self.compute_waypoints_from_polygon(polygon)
        field = {
            "field_name": field_name,
            "polygon": polygon,
            "waypoints": waypoints,
            "waypoint_nb": 0
            }
        self.fields[field_name]= field
        
    def get_next_waypoint(self, field_name):
        field = self.fields[field_name]
        next_waypoint = field["waypoints"][field["waypoint_nb"]]
        field["waypoint_nb"] +=1
        return next_waypoint
        
    def get_query_variables(self, path: str):
        queries = {}
        b,m,a= path.partition("?")
        l = a.split("&")
        for e in l:
            k,s,v= e.partition("=")
            queries[k]=v
        return queries
        
        
    def do_GET(self):
        if self.path.startswith("/waypoint"):
            print("query received")
            queries = self.get_query_variables(self.path) 
            print(queries)
            field_name = queries["field"]
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
                    
            payload = self.get_next_waypoint(field_name)
                    
            payload = payload.encode("utf8")
            self.wfile.write(payload)
            
    def do_POST(self):
        if self.path.startswith("/register"):
            length = int(self.headers.getheader('content-length'))
            message = json.loads(self.rfile.read(length))
            field_name = message["field"] 
            polygon = message["polygon"]
            self.register_new_field(field_name, polygon)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
                    
            payload = "field registered"
                    
            payload = payload.encode("utf8")
            self.wfile.write(payload)
        
        

httpd = socketserver.TCPServer(("", PORT), WaypointService)
print("serving at port", PORT)
httpd.serve_forever()
