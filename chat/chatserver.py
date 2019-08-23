from asyncore import dispatcher
from asynchat import async_chat
import socket
import asyncore

PORT = 5005
NAME = "TESTCHAT"


class EndSession(Exception):
    pass


class CommandHandle:
    """

    """
    def unknown(self, session, cmd):
        session.push(b"UnKnown command")

    def handle(self, session, line):
        line = line.decode()
        if not line.strip():
            return
        parts = line.split(' ', 1)
        cmd = parts[0]
        try:
            line = parts[1].strip()
        except IndexError:
            line = ''
        meth = getattr(self, 'do_' + cmd, None)
        try:
            meth(session, line)
        except TypeError:
            self.unknown(session, cmd)


class Room(CommandHandle):
    def __init__(self, server):
        self.server = server
        self.sessions = []

    def add(self, session):
        self.sessions.append(session)

    def remove(self, session):
        self.sessions.remove(session)

    def broadcast(self, line):
        for session in self.sessions:
            session.push(line)

    def do_logout(self, session, line):
        raise EndSession


class LoginRoom(Room):
    def add(self, session):
        Room.add(self, session)
        session.push(b'Connect Success')

    def unknown(self, session, cmd):
        session.push(b"Please log in")

    def do_login(self, session, line):
        name = line.strip()
        if not name:
            session.push(b"UserName Empty")
        elif name in self.server.users:
            session.push(b"UserName Exist")
        else:
            session.name = name
            session.enter(self.server.main_room)


class ChatRoom(Room):
    def add(self, session):
        session.push(b"Login Success")
        self.broadcast((session.name + " enter\n").encode('utf-8'))
        self.server.users[session.name] = session
        Room.add(self, session)

    def remove(self, session):
        Room.remove(self, session)
        self.broadcast((session.name + " left\n").encode('utf-8'))

    def do_say(self, session, line):
        self.broadcast((session.name + ": " + line).encode('utf-8'))

    def do_look(self, session, line):
        session.push(b"The following are in this room:\n")
        for other in self.sessions:
            session.push((other.name + '\n').encode('utf-8'))

    def do_who(self, session, line):
        session.push(b"The following are logged in:\n")
        for name in self.server.users:
            session.push(name.encode('utf-8'))


class LogoutRoom(Room):
    def add(self, session):
        try:
            del self.server.users[session.name]
        except KeyError:
            pass


class ChatSession(async_chat):
    def __init__(self, server, sock):
        async_chat.__init__(self, sock)
        self.server = server
        self.set_terminator(b"\n")
        self.data = []
        self.name = None
        self.enter(LoginRoom(server))

    def enter(self, room):
        try:
            cur = self.room
        except AttributeError:
            pass
        else:
            cur.remove(self)
        self.room = room
        room.add(self)

    def collect_incoming_data(self, data):
        self.data.append(data.decode('utf-8'))

    def found_terminator(self):
        line = ''.join(self.data)
        self.data = []
        try:
            self.room.handle(self, line.encode('utf-8'))
        except EndSession:
            self.handle_close()

    def handle_close(self):
        async_chat.handle_close(self)
        self.enter(LogoutRoom(self.server))


class ChatServer(dispatcher):
    def __init__(self, port, name):
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(5)
        self.name = name
        self.users = {}
        self.main_room = ChatRoom(self)

    def handle_accept(self):
        conn, addr = self.accept()
        ChatSession(self, conn)


if __name__ == "__main__":
    s = ChatServer(PORT, NAME)
    try:
        print("run at '0.0.0.0:{0}'".format(PORT))
        asyncore.loop()
    except KeyboardInterrupt:
        print("main error")

# https://www.cnblogs.com/shijieli/p/10662419.html
