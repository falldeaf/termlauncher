import keyring
#keyring.set_password("system", "OPENAI_KEY", "")
key = keyring.get_password("system", "OPENAI_KEY")
print(key)
