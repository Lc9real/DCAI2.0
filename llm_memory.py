import os




# Todo: Add Memory zusammenfassung
class Memory_System():
        def __init__(self, MemoryKey:str):
            self.memory_key = MemoryKey
            if not os.path.exists(f"./Memory/{self.memory_key}"):
                os.makedirs(f"./Memory/{self.memory_key}")
            if not os.path.exists(f"./Memory/{self.memory_key}/Summary"):
                os.makedirs(f"./Memory/{self.memory_key}/Summary")


        def get_Memory(self, specific_channel:str=None, excluded_channel :list[str]=[]) -> str:
            allfiles = os.listdir(f'./Memory/{self.memory_key}')
            content = ""
            if not specific_channel and not excluded_channel:
                for file in allfiles:
                    f = open(f"./Memory/{self.memory_key}/{file}", "r", encoding="utf-8")
                    content = content + f"\n###{file[:-7]}###\n\n" + f.read() + "\n\n"
                    f.close()
                content = content + "\n\n"
                if content == "":
                    content = "No conversation in other channel"
                return content
            elif specific_channel:
                if os.path.exists(f"./Memory/{self.memory_key}/{specific_channel}.memory"):
                    f = open(f"./Memory/{self.memory_key}/{specific_channel}.memory", "r", encoding="utf-8")
                    content = f"\n###{specific_channel}###\n\n" + f.read()
                    return content
                else:
                    return ""
            else:
                for file in allfiles:
                    f = open(f"./Memory/{self.memory_key}/{file}", "r", encoding="utf-8")
                    if str(file[:-7]) not in excluded_channel:
                        f = open(f"./Memory/{self.memory_key}/{file}", "r", encoding="utf-8")
                        content = content + f"\n###{file[:-7]}###\n\n" + f.read()
                        f.close()
                return content


        def add_Memory(self, username:str, inp:str, channel, time):
            f = open(f"./Memory/{self.memory_key}/{channel}.memory", "a", encoding="utf-8")
            if inp:
                f.write(f"{username}: {inp}; ({time})\n")
            f.close()


        def clear_Memory(self):
            os.remove(f"./Memory/{self.memory_key}")
            os.makedirs(f"./Memory/{self.memory_key}")

        def add_Summary(self, inp:str, channel):
            if inp:
                f = open(f"./Memory/{self.memory_key}/{channel}.memory", "w", encoding="utf-8")
                f.write(inp + "\n\n\n")







