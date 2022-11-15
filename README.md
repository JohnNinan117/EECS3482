# EECS3482: Introduction to Computer Security

## Assignment 1: Securing server/client application

You're presented with a simple client/sever chat application for sending messages and files among its users. 

As part of the assignment, you need to complete the following tasks:

-   User authentication
-   Key exchange between the client and server on initialization of the connection.
-   Key exchange between client and client on initialization of a chat session
-   Confidentiality through encryption of client-sever and client-client massages
-   Integrity through use of a MAC appended to all messages (client-server and client-client)
-   Resistance against replay attack


### Files

* server.py - server app
* client.py  - client app
* chat.py – chat functionality
* lib folder - includes helper function to facilitate communication 
* files folder - where sent files are stored.
* dh - Diffie-Hellman implementation.

### Set-up

To install all the relevant packages run:

* make clean
* make

## Usage 

To use the Chat app you first need to run the server. Once the server is running, you run client app to connect to the server. (see instruction below). We assume that both the server and all clients will run locally (i.e., on localhost). 

 Once the client is connected, the user needs to be authenticated with a username and a password.
 
To test the system initially, you can login with one of the ample users: **user1,** **user2**, **user3** 

Password: 123 (for all)

When at least two users have logged in, the program supports the following functionality.

* Sending messages between two users by first "pinging" the user with @user_id and then once a chat connection has established, the user can send one message at a time (this is not very user friendly, but you don't need to worry about the user experience for the assignment purposes)

* Send files using send @userID command. 

* Request a list of users from the server `list` command.

* Echo the server using `echo server` command

* Logout using the `exit' command

#### Sample interaction

```

\-\+\-\+\-\+\-\+\-\+\-\+\-\+ \+\-\+\-\+ \+\-\+\-\+\-\+ +-+-+-+-+-+-+

|W|e|l|c|o|m|e| |t|o| |t|h|e| |M|a|t|r|i|x|

\+\-\+\-\+\-\+\-\+\-\+\-\+\-\+ \+\-\+\-\+ \+\-\+\-\+\-\+ +-+-+-+-+-+-+

   

   

 ===== Online User ====:

| *  user2            |

| *  user3            |

=======================

\[user1\] Enter command: 

Initiating a chat session with  user2

Sending the chat session details

Chat session is on port 54860

Waiting for chat connection...

Accepted a connection from ('127.0.0.1', 54861)...

user2>Testing

@user2

New session

Received port 54863

Chat server on port 54863

Enter your message to \[user2\]:Hello World

\[user1\] Enter command: user2>Hello back!

   

Initiating a chat session with  user2

Sending the chat session details

Chat session is on port 54875

Waiting for chat connection...

Accepted a connection from ('127.0.0.1', 54876)...

Ready to receive files

Receiving henry-Shakespeare.txt
```



## Instructions 

### Server app
To run a server in a  terminal run 
	* make server
	or (without make)
	*  python3 server.py –p [port #]

### Client app
*  client.py is client app 
    *  To run a client: make client
    *   or python3 client.py –p [port #]













