
#базовый класс для hBodies, lBodies, hObjects и lObjects
#представляет из себя, де-факто, словарь с автодобавлением объектов
#для корректной работы добавления нужно изменить функцию get_essential_key
#обычно на возвращение return obj.mark_id
class SingletonDict:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonDict, cls).__new__(cls)
            cls._instance.objects = {}
        return cls._instance


    

    def __getitem__(self, key):
        return self.objects[key]

    
    def __iter__(self):
        return self.objects.__iter__()

    
    def __next__(self):
        return self.objects.__next__()

    def get_essential_key(self, obj):
        return id(obj)

    def add(self, obj):
        key = self.get_essential_key(obj)
        self.objects[key] = obj

    def contains(self, key):
        return key in self.objects

    def delete(self, key):
        if key in self.objects:
            self.objects.pop(key)




