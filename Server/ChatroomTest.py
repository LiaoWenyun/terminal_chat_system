import unittest
from Chatroom import *
from User import User
from Message import Message
import time


class ChatroomTest(unittest.TestCase):
    def testAddMessageFromOwner(self):
        owner = User("ownername", 123,"password")
        roomName = "general"
        messageText = "123"
        messageTime = int(time.time())
        chatroom = Chatroom(roomName,owner)
        message = Message(owner, messageText, messageTime)

        chatroom.addMessage(message)
        messages = chatroom.getMessagesByIndex(-1, owner)

        self.assertMessageListEquals(messages[1], [Message(owner,messageText,messageTime)])

    def testAddMessageFromNotFromOwner(self):
        owner = User("ownername", 123, "password")
        user = User("username", 1234,"password")
        roomName = "general"
        messageText = "123"
        messageTime = int(time.time())
        chatroom = Chatroom(roomName,owner)
        message = Message(user, messageText, messageTime)

        chatroom.addMessage(message)
        messages = chatroom.getMessagesByIndex(-1, user)

        self.assertMessageListEquals(messages[1], [Message(user, messageText, messageTime)])


    def testAddMessageFromBannedUser(self):
        owner = User(123, "ownername", "password")
        user = User(1234, "username", "password")
        roomName = "general"
        messageText = "123"
        messageTime = int(time.time())
        chatroom = Chatroom(roomName,owner)
        message = Message(user, messageText, messageTime)

        chatroom.addMessage(message)
        messages = chatroom.getMessagesByIndex(-1, owner)
        self.assertEqual(messages[0], 0)

        messages = messages[1]
        self.assertEqual(len(messages), 1)
        receivedMessage = messages[0]
        self.assertEqual(receivedMessage.user.name, user.name)
        self.assertEqual(receivedMessage.text, messageText)
        self.assertEqual(receivedMessage.time, messageTime)

    def testGetMessageByIndexWithIndex(self):
        owner = User(123, "ownername", "password")
        user = User(1234, "username", "password")

        roomName = "general"
        messageTime = int(time.time())
        message0 = Message(user, "text0", messageTime)
        messageTime += 1
        message1 = Message(user, "text1", messageTime)
        messageTime += 1
        message2 = Message(user, "text2", messageTime)
        messageTime += 1
        message3 = Message(user, "text3", messageTime)
        messageTime += 1
        message4 = Message(user, "text4", messageTime)
        messageTime += 1
        message5 = Message(user, "text5", messageTime)
        messageTime += 1

        chatroom = Chatroom(roomName, owner)

        chatroom.addMessage(message0)
        chatroom.addMessage(message1)
        chatroom.addMessage(message2)
        chatroom.addMessage(message3)
        chatroom.addMessage(message4)
        chatroom.addMessage(message5)

        #Get from middle of list
        messages = chatroom.getMessagesByIndex(2, user)
        self.assertEqual(messages[0], 5)
        messages = messages[1]
        self.assertMessageListEquals(messages,[message3, message4, message5])

        #Get from end of list
        messages = chatroom.getMessagesByIndex(5, user)
        self.assertEqual(messages[0], 5)
        messages = messages[1]
        self.assertMessageListEquals(messages, [])

        #Get from beyond end of list
        messages = chatroom.getMessagesByIndex(6, user)
        self.assertEqual(messages[0], 5)
        messages = messages[1]
        self.assertMessageListEquals(messages, [])

    def testGetMessagesByTimeBanned(self):
        owner = User(123, "ownername", "password")
        user = User(1234, "username", "password")

        roomName = "general"
        messageTime = int(time.time())
        messages = []

        for i in xrange(100):
            messages.append(Message(user,"text" + str(i), messageTime + i))

        chatroom = Chatroom(roomName, owner)

        # populate message list
        for message in messages:
            chatroom.addMessage(message)

        chatroom.banUser(owner, user)

        #Get Messages should fail
        try:
            messages = chatroom.getMessagesByTime(messageTime + 50, user)
            self.fail()
        except UserBannedException:
            pass

    def testGetMessagesByTime(self):
        owner = User(123, "ownername", "password")
        user = User(1234, "username", "password")
        roomName = "general"
        messageTime = int(time.time())
        messages = []

        for i in xrange(100):
            messages.append(Message(user,"text" + str(i), messageTime + i))

        chatroom = Chatroom(roomName, owner)

        #populate message list
        for message in messages:
            chatroom.addMessage(message)

        #Get from before list
        receivedMessages = chatroom.getMessagesByTime(messageTime - 1, user)
        self.assertMessageListEquals(receivedMessages[1], messages)
        self.assertEqual(receivedMessages[0], 99)

        #Get with time = first time
        receivedMessages = chatroom.getMessagesByTime(messageTime, user)
        self.assertMessageListEquals(receivedMessages[1], messages)
        self.assertEqual(receivedMessages[0], 99)

        #Get from middle of list
        receivedMessages = chatroom.getMessagesByTime(messageTime + 50, user)
        self.assertMessageListEquals(receivedMessages[1], messages[50:])
        self.assertEqual(receivedMessages[0], 99)

        #Get from end of list
        receivedMessages = chatroom.getMessagesByTime(messageTime + 99, user)
        self.assertMessageListEquals(receivedMessages[1], messages[-1:])
        self.assertEqual(receivedMessages[0], 99)

        #Get from beyond end of list
        receivedMessages = chatroom.getMessagesByTime(messageTime + 100, user)
        self.assertMessageListEquals(receivedMessages[1], [])
        self.assertEqual(receivedMessages[0], 99)

    def testGetMessagesByTimeEmpty(self):
        owner = User(123, "ownername", "password")
        user = User(1234, "username", "password")
        roomName = "general"
        messageText = "123"
        messageTime = int(time.time())
        chatroom = Chatroom(roomName, owner)

        messages = chatroom.getMessagesByTime(messageTime - 1, user)
        self.assertMessageListEquals(messages[1],[])
        self.assertEqual(messages[0], -1)

    def testGetMessageByIndexBannedUser(self):
        owner = User(123, "ownername", "password")
        user = User(1234, "username", "password")
        roomName = "general"
        messageText = "123"
        messageTime = int(time.time())
        chatroom = Chatroom(roomName,owner)
        message = Message(owner, messageText, messageTime)

        chatroom.addMessage(message)
        messages = chatroom.getMessagesByIndex(-1, user)

        # user is not banned yet, should be able to see chat
        self.assertMessageListEquals(messages[1], [Message(owner, messageText, messageTime)])

        chatroom.banUser(owner, user)

        # user is banned, should result in an exception
        try:
            messages = chatroom.getMessagesByIndex(-1, user)
            self.fail()
        except UserBannedException:
            pass


    def testBanOwner(self):
        owner = User(123, "ownername", "password")
        user = User(1234, "username", "password")
        roomName = "general"
        messageText = "123"
        messageTime = int(time.time())
        chatroom = Chatroom(roomName,owner)
        message = Message(owner, messageText, messageTime)

        chatroom.addMessage(message)
        chatroom.banUser(owner, user)

        #Should not be able to ban the owner of the chatroom
        try:
            messages = chatroom.getMessagesByIndex(-1, user)
            self.fail()
        except UserBannedException:
            pass


    def testBanUserNotOwner(self):
        owner = User("ownername", 123, "password")
        user1 = User("user1name", 1234, "password")
        user2 = User("user2name", 12345, "password")
        roomName = "general"
        messageText = "123"
        messageTime = int(time.time())
        chatroom = Chatroom(roomName, owner)
        message = Message(owner, messageText, messageTime)

        chatroom.addMessage(message)
        messages = chatroom.getMessagesByIndex(-1, user1)

        self.assertMessageListEquals(messages[1], [Message(owner, messageText, messageTime)])

        #Only owner should be able to ban users
        try:
            chatroom.banUser(user1, user2)
            self.fail()
        except NotOwnerException:
            pass

        messages = chatroom.getMessagesByIndex(-1, user2)

        self.assertMessageListEquals(messages[1], [Message(owner, messageText, messageTime)])

    def testUnbanUser(self):
        owner = User(123, "ownername", "password")
        user = User(1234, "username", "password")

        roomName = "general"
        messageText = "123"
        messageTime = int(time.time())
        chatroom = Chatroom(roomName, owner)
        message = Message(owner, messageText, messageTime)

        chatroom.addMessage(message)

        chatroom.banUser(owner, user)
        chatroom.unbanUser(owner, user)

        messages = chatroom.getMessagesByIndex(-1, user)

        self.assertMessageListEquals(messages[1], [Message(owner, messageText, messageTime)])

    def testBanUnbanBan(self):
        owner = User(123, "ownername", "password")
        user = User(1234, "username", "password")

        roomName = "general"
        messageText = "123"
        messageTime = int(time.time())
        chatroom = Chatroom(roomName, owner)
        message = Message(owner, messageText, messageTime)

        chatroom.addMessage(message)

        chatroom.banUser(owner, user)
        chatroom.unbanUser(owner, user)
        chatroom.banUser(owner, user)

        try:
            messages = chatroom.getMessagesByIndex(-1, user)
            self.fail()
        except UserBannedException:
            pass

    def testUnbanUserNotBanned(self):
        owner = User(123, "ownername", "password")
        user = User(1234, "username", "password")

        roomName = "general"
        messageText = "123"
        messageTime = int(time.time())
        chatroom = Chatroom(roomName, owner)
        message = Message(owner, messageText, messageTime)

        chatroom.addMessage(message)

        try:
            chatroom.unbanUser(owner, user)
            self.fail()
        except UserNotBannedException:
            pass

    def testbanUserTwice(self):
        owner = User(123, "ownername","password")
        user = User(1234, "username","password")
        roomName = "general"
        messageText = "123"
        messageTime = int(time.time())
        chatroom = Chatroom(roomName,owner)
        message = Message(owner, messageText, messageTime)

        chatroom.addMessage(message)
        chatroom.banUser(owner, user)
        chatroom.banUser(owner, user)

        try:
            messages = chatroom.getMessagesByIndex(-1, user)
            self.fail()
        except UserBannedException:
            pass

    def testUnbanUserNotOwner(self):
        owner = User("ownername", 123, "password")
        user1 = User("user1name", 1234, "password")
        user2 = User("user2name", 12345, "password")
        roomName = "general"
        messageText = "123"
        messageTime = int(time.time())
        chatroom = Chatroom(roomName,owner)
        message = Message(owner, messageText, messageTime)

        chatroom.addMessage(message)
        chatroom.banUser(owner, user2)

        try:
            chatroom.unbanUser(user1, user2)
            self.fail()
        except NotOwnerException:
            pass

        try:
            messages = chatroom.getMessagesByIndex(-1, user2)
            self.fail()
        except UserBannedException:
            pass

    def testNoOwner(self):
        owner = None
        user = User(1234, "username", "password")
        roomName = "general"
        chatroom = Chatroom(roomName, owner)

        try:
            chatroom.banUser(owner, user)
            self.fail()
        except NotOwnerException:
            pass

    def testJoin(self):
        owner = None
        user = User(1234, "username", "password")
        roomName = "general"
        chatroom = Chatroom(roomName, owner)

        chatroom.join(user)

    def testJoinBanned(self):
        owner = User("ownername", 123, "password")
        user = User(1234, "username", "password")
        roomName = "general"
        chatroom = Chatroom(roomName, owner)
        chatroom.banUser(owner, user)

        try:
            chatroom.join(user)
            self.fail()
        except UserBannedException:
            pass

    #Helper method, checks that 2 message lists are the same
    def assertMessageListEquals(self, left, right):
        if len(left) != len(right):
            self.assertEqual(len(left),len(right))
            return

        for i in xrange(len(left)):
            leftMessage = left[i]
            rightMessage = right[i]

            self.assertEqual(leftMessage.user.name, rightMessage.user.name)
            self.assertEqual(leftMessage.user.id, rightMessage.user.id)
            self.assertEqual(leftMessage.text, rightMessage.text)
            self.assertEqual(leftMessage.time, rightMessage.time)

unittest.main()