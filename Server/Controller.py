from Authenticator import Authenticator
from ChatSystem import *
from Chatroom import *
from ResponseFactory import ResponseFactory


class Controller:
    def __init__(self):
        self.authenticator = Authenticator()
        self.chatSystem = ChatSystem()
        self.responseFactory = ResponseFactory()

    #These functions deal with routing the requests to the proper ChatSystem functions,
    #They assume that all parameters are not None, unless otherwise specified and the
    #parameters are of the proper type
    #The functions return a string corresponding to the proper response type
    #The functions authenticate the users if necessary
    def login(self, username, password):
        try:
            self.__authenticateByName(username, password)
            userID = self.chatSystem.login(username, password)

            if userID is None:
                return self.responseFactory.invalidCredentials()

            return self.responseFactory.loggedIn(userID)
        except Exception as e:
            return self.handleException(e)

    def signup(self, username, password):
        try:
            userID = self.chatSystem.signup(username, password)
            return self.responseFactory.loggedIn(userID)
        except Exception as e:
            return self.handleException(e)

    def send(self, userID, password, chatroom, text):
        try:
            self.__authenticateByID(userID, password)
            self.chatSystem.addMessage(chatroom, userID, text)
            return self.responseFactory.ok()
        except Exception as e:
            return self.handleException(e)

    def get(self, userID, password, chatroom, lastUpdate):
        try:
            self.__authenticateByID(userID, password)

            if lastUpdate is None:
                response = self.chatSystem.getMessagesByTime(chatroom, userID)
            else:
                response = self.chatSystem.getMessagesByIndex(chatroom,userID,lastUpdate)

            return self.responseFactory.returnMessages(response[0], response[1])
        except Exception as e:
            return self.handleException(e)

    def set_alias(self, userID, password, newUsername):
        try:
            self.__authenticateByID(userID, password)
            self.chatSystem.set_alias(userID, newUsername, password)
            return self.responseFactory.ok()
        except Exception as e:
            return self.handleException(e)

    def join(self, userID, password, chatroom):
        try:
            self.__authenticateByID(userID, password)
            self.chatSystem.joinChatroom(chatroom, userID)
            return self.responseFactory.ok()
        except Exception as e:
            return self.handleException(e)

    def create(self, userID, password, chatroom):
        try:
            self.__authenticateByID(userID, password)
            self.chatSystem.addChatroom(userID,chatroom)
            return self.responseFactory.ok()
        except Exception as e:
            return self.handleException(e)

    def delete(self, userID, password, chatroom):
        try:
            self.__authenticateByID(userID, password)
            self.chatSystem.deleteChatroom(userID, chatroom)
            return self.responseFactory.ok()
        except Exception as e:
            return self.handleException(e)

    def block(self, userID, password, chatroom, userToBlock):
        try:
            self.__authenticateByID(userID, password)
            self.chatSystem.banUser(userID, chatroom, userToBlock)
            return self.responseFactory.ok()
        except Exception as e:
            return self.handleException(e)

    def unblock(self, userID, password, chatroom, userToUnblock):
        try:
            self.__authenticateByID(userID, password)
            self.chatSystem.unbanUser(userID, chatroom, userToUnblock)
            return self.responseFactory.ok()
        except Exception as e:
            return self.handleException(e)

    def __authenticateByID(self,userID, password):
        if not self.authenticator.authenticateByID(userID, password):
            raise InvalidCredentialsException

    def __authenticateByName(self, username, password):
        if not self.authenticator.authenticateByName(username, password):
            raise InvalidCredentialsException

    def handleException(self, e):
        if isinstance(e,InvalidCredentialsException):
            return self.responseFactory.invalidCredentials()
        if isinstance(e,ChatroomDoesNotExistException):
            return self.responseFactory.chatroomDoesNotExist()
        elif isinstance(e,DuplicateChatroomException):
            return self.responseFactory.duplicateChatrooom()
        elif isinstance(e,DuplicateUsernameException):
            return self.responseFactory.duplicateUsername()
        elif isinstance(e,ChatroomFormatException):
            return self.responseFactory.invalidChatroom()
        elif isinstance(e,MessageFormatException):
            return self.responseFactory.invalidMessage()
        elif isinstance(e,UsernameFormatException):
            return self.responseFactory.invalidUsername()
        elif isinstance(e,PasswordFormatException):
            return self.responseFactory.invalidPassword()
        elif isinstance(e,UserNotFoundException):
            return self.responseFactory.userDoesNotExist()
        elif isinstance(e,NotOwnerException):
            return self.responseFactory.notOwner()
        elif isinstance(e,UserBannedException):
            return self.responseFactory.blocked()
        elif isinstance(e,UserNotBannedException):
            return self.responseFactory.userNotOnList()
        elif isinstance(e,UserIsOwnerException):
            return self.responseFactory.userIsOwner()
        else:
            return self.responseFactory.serverError()


class InvalidCredentialsException(Exception):
    pass