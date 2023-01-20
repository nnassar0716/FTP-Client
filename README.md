#**README**
###Nathan Nassar

##High Level Approach
My approach when completing this assignment was very similar to 
the suggested implementation approach that was given to us in the 
details for the project. I first did research to learn how to use
the urlib.parse library so that I could learn how to parse through a url.
I then implemented the argparse library so that I could organize 
the parameters that I would need for this assignment. Once I
had properly parsed through a FTP url and set up my argparser,
I then moved on to setting up the initial connection to the 
FTP server. I used the socket logic from the last assignment
to connect to the server, send the basic FTP commands needed to set up the 
server, and ensured that I was receiving the right information.
I then moved on to figuring out how to open the data channel
with the use of a secondary socket. I learned how to make use of 
the passive command so that I could get the correct IP address 
and port number needed for the second socket. Once I set this up, I moved
onto using the FTP commands that require a data connection to 
support the use of the last operations needed. I then organized all
of my code into functions and helper functions and was finished.

##Challenges Faced
The biggest challenges I faced during this assignment occured when
I began to work with the aspects of the assignment that required
the use of a data channel. I first had to figure out how to 
ensure that I could always get the proper port for my second
socket to connect to, since it was different with each run 
of my program. Once I figured that out, the majority of my time
with this project was spent learning how to properly communicate 
with the server. This consisted of a lot of trial and error for me,
as I had to try different send and receives with my data 
to learn the proper order needed to communicate with the server.
Learning when to send/receive to the control channel vs the data 
channel proved to be a challenging task for me. Once I got over
the hurdle of learning how to properly communicate with the 
server, I was able to properly implement all operations necessary.

##Overview of Testing
I tested my code largely by making use of print statements and through 
the use of FileZilla in order to see the FTP server through 
the lens of a gui. Initially, printing out the responses I 
received from the server was all I needed to test my code,
as the server would provide me with messages that would indicate
exactly how successful my code was in communicating with the server.
This was thanks to the code system that server employed, where 
codes beginning with 2 meant success, 3 meant more action, and so 
on. However, when I began to try to test my code for operations
like mv and cp, I found that using FileZilla was a much easier
way to ensure that my code was working as intended. With FileZilla,
I was able to create file/directories directly in the server 
so that I could more easily move/copy files with minimal hassle.
It was also useful for checking to see if files/directories
were properly removed, as I could simply reload the server once
I had done an operation and could clearly see if the file was 
gone or not. Through the combination of both my print statements
and FileZilla, testing the effectiveness and correctness of my
code became a more simple process for me. 

