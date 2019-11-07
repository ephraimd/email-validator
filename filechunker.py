
import os
import os.path


class Chunker:
    def __init__(self):
        if os.path.exists('email_list.txt') is False:
            print('Error: all the email list must be contained in a file named "email_list.txt" and saved in '+os.getcwd())
            input('..I Quit...')
            return
        if os.path.exists('email_chunks') is False:
            os.mkdir('email_chunks')
        self.fileCount = 0
        self.file = 'email_chunks/email_list_chunk'
        self.writeFile()
        pass
    def writeFile(self):
        fd = open(self.file+str(self.fileCount)+'.txt', 'wt')
        with open('email_list.txt') as fh:
            for count, line in enumerate(fh):
                #if len(line) < 3:
                #    continue
                if (count % 100) == 0: #split list into 100 emails each
                    self.fileCount += 1;
                    fd.close()
                    fd = open(self.file+str(self.fileCount)+'.txt', 'wt')
                fd.write(line)

