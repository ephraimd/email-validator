# Email Validator Script #
A console based software for validating Email Addresses without blacklisting your IP address

----------
### Requirements ###
Every python script requires some other script on which it depends on the script can either be bundled with python package install or you will need to install the script online via pip. You need the following scripts in order to run the Email Validator scripts

- idna
- dns
- email_validator
- lxml
- requests
- queue

### Installing the dependencies ###
You can install python dependency scripts via your command line interface. Simply follow the steps below

1. Open your cmd (Command Console, cmd.exe)
2. Make sure you are connected to the internet
3. To install a script online, this is the format you will type `pip install <script-name>`
4. So for instance you wanna install the idna script online, you type `pip install idna` in the command console.
5. Then press enter and let pip handle the rest


### Running The Script ###

Once you have installed all the dependencies, simply extract the script archive i sent, extract it to preferred folder.
You will find a text file name *email_list.txt*, this is where all the emails will be saved. Don't worry, the script will split the long list into chunks for easy processing, you will see the chunks in the email_chunks folder once the script strats running.
So then double click the main script which is named *runthis.py* to start the program. You should see the program at work now.

### The Results ###

The script will create text files containing the name of the category of emails in it.

- Clean emails: Good and valid ones
- Bad emails: spam and invalid emails
- blacklisted: Spam and bot emails
- role emails: dummy emails like no-reply@site.com

### Notes ###

The script will be made to be very much faster. 