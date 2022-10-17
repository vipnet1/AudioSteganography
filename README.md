# AudioSteganography

# Description
Hide messsage inside audio file(WAV)

commands:
python main.py hide lsb_basic FILENAME MESSAGE_TO_HIDE
python main.py extract lsb_basic FILENAME

python main.py hide lsb_key_based FILENAME MESSAGE_TO_HIDE
python main.py extract lsb_key_based FILENAME PERSONAL_KEY

python main.py hide lsb_file FILENAME FILE_TO_HIDE
python main.py extract lsb_file FILENAME PERSONAL_KEY

python main.py hide frequency_embedding FILENAME MESSAGE_TO_HIDE
python main.py extract frequency_embedding FILENAME

currently suppose MESSAGE_TO_HIDE contains only ascii characters

# End Description
  
Create virtual env (as long you didn't deleted it, run it on time):  
  
```  
python3 -m venv ./venv/ && ./venv/Scripts/activate.bat  
```  
  
Install dependencies:  
  
```  
pip3 install -r requirements.txt  
```  
  
To destroy virtual env:  
  
```  
deactivate && rm venv  
```