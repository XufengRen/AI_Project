# This code is used to set the user email address, which is used to send emails to.
import os

email = input("Enter email address: \n")
with open('./userEmail.txt','w') as file:
   file.write(email)
