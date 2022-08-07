import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
from psuedoSensor import PseudoSensor as ps
from time import sleep
from datetime import datetime
 
class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print('new connection')
        self.ps = ps()
        self.stop_index = False
      
    def on_message(self, message):
        print('request received')
        if message == "read single value":
            id = "single"
            hum, temp = self.ps.generate_values()
            self.write_message(id + ':' + str(hum) + ":" + str(temp))
        elif message == "read multiple values":
            for i in range(0, 10):
                id = "multiple"
                hum, temp = self.ps.generate_values()
                timestampe = str(datetime.now().time().strftime('%H-%M-%S'))
                msg = id + ':' + str(hum) + ":" + str(temp) + ":" + timestampe
                self.write_message(msg)
                sleep(1)
        if message == "close":
            self.write_message("Closeing the server")
            tornado.ioloop.IOLoop.instance().stop()
 
    def on_close(self):
        print ('connection closed')
        

    def stop_it(self):
        tornado.ioloop.stop()
 
    def check_origin(self, origin):
        return True
 
application = tornado.web.Application([
    (r'/ws', WSHandler),
])
 
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print ('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()
    
