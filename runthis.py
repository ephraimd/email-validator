import os
import os.path

print('Getting started....')
import main
import filechunker

if os.path.exists('email_chunks') is False:
    print('setting up file chunks')
    filechunker.Chunker()

print('Starting Validator...\n')
main.EmailValidator()
