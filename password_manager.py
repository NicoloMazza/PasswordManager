import json, hashlib, getpass, os, pyperclip, sys
from cryptography.fernet import Fernet

# Funzione per generare una chiave per codifica e decodifica

def generate_key():
   return Fernet.generate_key()                                                         # Genera la chiave

def initialize_cipher(key):
   return Fernet(key)                                                                   # Uso il costruttore di Fernet per memorizzare la chiave che user├á lo script per codificare e decodificare

def encrypt_password(cipher, password):
   return cipher.encrypt(password.encode()).decode()                                    # La catena di funzioni ├¿ la seguente: password.encode() viene utilizzata per convertire la stringa in byte, la funzione encrypt() invece viene usata per cifrarla, mantenendola in byte, per poi riconvertirla in stringa tramite la funzione decode() e poterla salvare sul file

def decrypt_password(cipher, encrypted_password):
   return cipher.decrypt(encrypted_password.encode()).decode()                          # L'esatto opposto della funzione precedente mantendendo la logica della catena

def hash_password(password):
   sha256 = hashlib.sha256()                                                            # crea un oggetto di tipo sha256 per l'utilizzo di funzioni hash
   sha256.update(password.encode())                                                     # codifica la password tramite la funzione encode(), aggionra l'oggetto sha256 tramite la funzione update()
   return sha256.hexdigest()                                                            # genera l'hash della password codificata tramite la funzione hexdigest()

# Funzione per la registrazione dell'utente

def register(username, master_password):
   hashed_master_password = hash_password(master_password)                              # codifica la masterpassword
   user_data = {'username': username, 'master_password': hashed_master_password}        # crea un dizionario con username e password
   file_name = 'user_data.json'                                                         # Crea una variabile file_name per cercare il file user_data
   if os.path.exists(file_name) and os.path.getsize(file_name) == 0:                    # verifica se il file esiste e se ├¿ vuoto
       with open(file_name, 'w') as file:                                               # se esiste ed ├¿ vuoto, scrive le credenziali e registrazione appo
           json.dump(user_data, file)                                                   # funzione dump: serve a creare un json a partire da un dizionario
           print("\n[+] Registrazione completata!\n")
   else:
       with open(file_name, 'x') as file:                                               # altrimenti, crea il file e ti registra
           json.dump(user_data, file)                                                   # il fatto di aprirlo in modalit├á esecuzione serve a crearlo
           print("\n[+] Registrazione completata!\n")                                   # nel caso in cui non esista

# Funzione per effettuare il login

def login(username, entered_password):
   try:
       with open('user_data.json', 'r') as file:
           user_data = json.load(file)                                                               # Carica il file json con le credenziali dell'utente
       stored_password_hash = user_data.get('master_password')                                       # prende la password principale
       entered_password_hash = hash_password(entered_password)                                       # codifica la password inserita
       if entered_password_hash == stored_password_hash and username == user_data.get('username'):   # se gli hash coincidono
           print("\n[+] Login eseguito con successo\n")                                              # login effettuato con successo
       else:
           print("\n[-] Credenzali non valide. Usa quelle utilizzate in fase di registrazione\n")    # altrimenti il login non va a buon fine
           sys.exit()                                                                                # termina l'esecuzione del programma
   except Exception:
       print("\n[-] Non sei registrato... Registrati\n")
       sys.exit()

def view_websites():
   try:
       with open('passwords.json', 'r') as data:
           view = json.load(data)
           print("\nSiti memorizzati: \n")
           for x in view:
               print(x['website'])
           print('\n')
   except FileNotFoundError:
       print("\n[-] Nessuna password memorizzata! !\n")

def add_password(website, password):
   if not os.path.exists('passwords.json'):
       data = []
   else:
       try:
           with open('passwords.json', 'r') as file:
               data = json.load(file)
       except json.JSONDecodeError:                                                     # Se ├¿ vuoto o non valido inizializza un array vuoto
           data = []
   encrypted_password = encrypt_password(cipher, password)                              # Codifica la password
   password_entry = {'website': website, 'password': encrypted_password}
   data.append(password_entry)
   with open('passwords.json', 'w') as file:
       json.dump(data, file, indent=4)

def get_password(website):
   if not os.path.exists('passwords.json'):
       return None
   try:
       with open('passwords.json', 'r') as file:
           data = json.load(file)
   except json.JSONDecodeError:
       data = []
   for entry in data:
       if entry['website'] == website:
           decrypted_password = decrypt_password(cipher, entry['password'])
           return decrypted_password
   return None


# MAIN
key_filename = 'encryption_key.key'
if os.path.exists(key_filename):
   with open(key_filename, 'rb') as key_file:
       key = key_file.read()
else:
   key = generate_key()
   with open(key_filename, 'wb') as key_file:
       key_file.write(key)

cipher = initialize_cipher(key)

while True:
   print("1. Registrati")
   print("2. Accedi")
   print("3. Esci")
   choice = input("Scegli un opzione: ")
   if choice == '1':                                                                    # registrazione (pu├▓ essere fatto solo una volta)
       file = 'user_data.json'
       if os.path.exists(file) and os.path.getsize(file) != 0:
           print("\n[-] Registrazione gi├á avvenuta!")
           sys.exit()
       else:
           username = input("Inserisci il tuo username: ")
           master_password = getpass.getpass("Inserisci la tua password: ")
           register(username, master_password)
   elif choice == '2':                                                                  # Log in
       file = 'user_data.json'
       if os.path.exists(file):
           username = input("Inserisci il tuo username: ")
           master_password = getpass.getpass("Inserisci la tua password: ")
           login(username, master_password)
       else:
           print("\n[-] Non sei registrato... Registrati.\n")
           sys.exit()
       while True:
           print("1. Aggiungi Password")
           print("2. Vedi Password")
           print("3. Vedi siti web memorizzati")
           print("4. Esci")
           password_choice = input("Scegli un opzione: ")
           if password_choice == '1':                                                   # Aggiungere una nuova password
               website = input("Inserisci sito web: ")
               password = getpass.getpass("Inserisci la password: ")
               add_password(website, password)
               print("\n[+] Password salvata!\n")
           elif password_choice == '2':                                                 # Accedere ad una password
               website = input("Inserisci sito web: ")
               decrypted_password = get_password(website)
               if website and decrypted_password:
                   pyperclip.copy(decrypted_password)
                   print(f"\n[+] La password per {website}: {decrypted_password}\n[+]. \n")
               else:
                   print("\n[-] Password non trovata! Sei sicuro di averla salvata?"
                         "\n[-] Usa l'opzione 3 per accedere ai siti web memorizzati.\n")
           elif password_choice == '3':                                                 # vedere siti memorizzati e password
               view_websites()
           elif password_choice == '4':                                                 # uscire dal password manager
               break
   elif choice == '3':                                                                  # uscire dal programma
       break
