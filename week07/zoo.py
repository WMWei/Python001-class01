from abc import ABC, abstractmethod


# 动物类
# 抽象基类
class Animal(ABC):
    @abstractmethod
    def __init__(self,
                 name: str,
                 category: str,
                 size: str,
                 character: str):
        self.name = name
        self.category = category
        self.size = size
        self.character = character
    
    @property
    def is_violent(self) -> bool:
        '''判断是否是凶猛动物'''
        return (self.size != '小' and 
                self.character == '凶猛' and 
                self.category == '食肉')
    
    def __str__(self):
        return (f'({self.__class__.__name__}: '
                f'{self.name},'
                f'{self.category},'
                f'{self.size},'
                f'{self.character},'
                f'凶猛动物({self.is_violent}))')

    __repr__ = __str__



class Cat(Animal):
    Voice = '喵~'
    def __init__(self,
                 name: str,
                 category: str,
                 size: str,
                 character: str):
        super().__init__(name, category, size, character)

    @property
    def as_pet(self) -> bool:
        '''判断是否适合作为宠物'''
        return not self.isviolent


class Zoo(object):
    def __init__(self, name):
        self.name = name
        self.__animals = {}

    def add_animal(self, animal: 'Animal'):
        self.__animals.setdefault(animal.__class__.__name__, set()).add(animal)

    def __getattr__(self, class_: str) -> bool:
        return class_ in self.__animals
    
    def __str__(self):
        return f'动物园：{self.name}\n动物：{self.__animals!s}'


if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫', '食肉', '小', '温顺')
    cat2 = Cat('大白猫', '食肉', '大', '凶猛')

    # 增加一只猫到动物园
    z.add_animal(cat1)
    z.add_animal(cat1)
    z.add_animal(cat2)

    print(z)
    print(getattr(z, 'Cat'))