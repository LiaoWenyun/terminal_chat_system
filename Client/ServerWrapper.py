import socket 
import json 
from Message import Message 

class ServerWrapper:
    ServerLocation ='localhost'
    Port= 9321

    def __init__(self, location):
        self.ServerLocation = location

            

    def login(self,Username,Password):
        data={'requestType':'login', 'username': Username, 'password': Password} 
        reply=self.receive_and_parse(data)
        outcome=reply["responseType"]
        if outcome =="Ok":
            
            return reply["userID"]
        
        else:
            
            return self.exceptions(outcome)
        

    def signup(self,Username,Password):
    
        data = {'requestType':'signup', 'username': Username, 'password': Password}
        reply=self.receive_and_parse(data)
        outcome=reply["responseType"]
        if outcome =="Ok":
            return reply["userID"]
        else:
            return self.exceptions(outcome)
    
    def send(self,UserID,Password,Chatroom,Message):
        
        data = {'requestType':'send', 'userID': UserID, 'password': Password,'chatroom':Chatroom,'message':Message}
        reply=self.receive_and_parse(data)  
        outcome=reply["responseType"]
        if outcome =="Ok":
            return True
        else:
            return self.exceptions(outcome)
    
    def get(self,UserID,Password,Chatroom,LastUpdate=None):
    
        if LastUpdate is None:
            data = {'requestType':'get', 'userID': UserID, 'password': Password,'chatroom':Chatroom}
        else:
            data = {'requestType':'get', 'userID': UserID, 'password': Password,'chatroom':Chatroom,'lastUpdate':LastUpdate}
      
        reply= self.receive_and_parse(data)
        outcome=reply["responseType"]

        if outcome =="Ok":
            lastUpdate = reply['lastUpdate']
            message_list=[]
            for item in reply["messages"]:
                message=Message(item["username"],item["text"])           
                message_list.append(message) 
            return (lastUpdate,message_list)   
        else:
            return self.exceptions(outcome)
           
    
    def set_alias(self,UserID,Password,NewUsername):

        data = {'requestType':'set_alias', 'userID': UserID, 'password': Password,'newUsername':NewUsername}
        reply= self.receive_and_parse(data)
        outcome=reply["responseType"]
        if outcome =="Ok":
             return True
        else:
            return self.exceptions(outcome)
        

    def join(self,UserID,Password,Chatroom):
        
        data = {'requestType':'join', 'userID': UserID, 'password': Password,'chatroom':Chatroom}
        reply= self.receive_and_parse(data)
        outcome=reply["responseType"]
        if outcome =="Ok":
             return True
        else:
            return self.exceptions(outcome)
        

    def create(self,UserID,Password,Chatroom):
        
        data = {'requestType':'create', 'userID': UserID, 'password': Password,'chatroom':Chatroom}
        reply= self.receive_and_parse(data)
        outcome=reply["responseType"]
        if outcome =="Ok":
             return True
        else:
            return self.exceptions(outcome)
        

    def block(self,UserID,Password,UserToBlock,Chatroom):
    
        data = {'requestType':'block', 'userID': UserID, 'password': Password,'chatroom':Chatroom,'userToBlock':UserToBlock}
        reply= self.receive_and_parse(data)
        outcome=reply["responseType"]
        if outcome =="Ok":
             return True
        else:
            return self.exceptions(outcome)
    

    def unblock(self,UserID,Password,UserToUnblock,Chatroom):
        
        data = {'requestType':'unblock', 'userID': UserID, 'password': Password,'chatroom':Chatroom,'userToUnblock':UserToUnblock}
        reply= self.receive_and_parse(data)
        outcome=reply["responseType"]
        if outcome =="Ok":
             return True
        else:
            return self.exceptions(outcome)
        

    def delete(self,UserID,Password,Chatroom):
        
        data = {'requestType':'delete', 'userID': UserID, 'password': Password,'chatroom':Chatroom}
        reply= self.receive_and_parse(data)
        outcome=reply["responseType"]
        
        if outcome =="Ok":
             return True
        else:
            return self.exceptions(outcome)
        

    def receive_and_parse(self,data):
        try:
            s = socket.socket()
            requestString = json.dumps(data)

            host = socket.gethostname()
            port = 9321

            s.connect((host, port))
            s.send(requestString)

            response = s.recv(2048)
            return json.loads(response)
        except Exception:
            raise failed_recv_Exception

    def exceptions(self,string):
        if string =='RequestTypeMissing':
            raise requestTypeMissingException
        elif string =='RequestFormatError':
            raise requestFormatErrorException 
        elif string == 'DuplicateUsername':
            raise duplicateUsernameException
        elif string == 'InvalidUsername':
            raise invalidUsernameException
        elif string=='InvalidPassword':
            raise invalidPasswordException
        elif string=='ParametersMissing':
            raise parametersMissingException 
        elif string=='InvalidCredentials':
            raise invalidCredentialsException
        elif string=='InvalidMessage':
            raise invalidMessageException
        elif string=='ChatroomDoesNotExist':
            raise chatroomDoesNotExistException
        elif string=='DuplicateChatrooom':
            raise duplicateChatrooomException
        elif string=='UserDoesNotExist':
            raise userDoesNotExistException
        elif string=='NotOwner':
            raise notOwnerException
        elif string=='UserNotOnList':
            raise userNotOnListException 
        elif string=='ParameterFormatError':
            raise parameterFormatErrorException
        elif string=='InvalidChatroom':
            raise invalidChatroomException
        elif string =='Blocked':
            raise blockedException
        else:
            raise undefinedException




class connectionFailedException(Exception):
    pass

class failed_recv_Exception(Exception):
    pass

class undefinedException(Exception):
    pass

class blockedException(Exception):
    pass

class requestTypeMissingException(Exception):
    pass
    
class requestFormatErrorException(Exception):
    pass

class duplicateUsernameException(Exception):
    pass

class invalidUsernameException(Exception):
    pass

class invalidPasswordException(Exception):
    pass

class parametersMissingException(Exception):
    pass

class invalidCredentialsException(Exception):
    pass

class invalidMessageException(Exception):
    pass

class chatroomDoesNotExistException(Exception):
    pass

class duplicateChatrooomException(Exception):
    pass

class userDoesNotExistException(Exception):
    pass

class notOwnerException(Exception):
    pass

class userNotOnListException(Exception):
    pass

class parameterFormatErrorException(Exception):
    pass

class invalidChatroomException(Exception):
    pass


#user=ServerWrapper()
#user.signup('1234','4321')
#user.send(0,'4321','general','ccc')


#ser.get(0,'4321','general',1)


