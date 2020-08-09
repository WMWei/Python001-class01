from abc import ABC, abstractmethod


# 动物类
# 抽象基类
class Animal(ABC):
    Category = (
        '食草',
        '食肉',
        '杂食',
    )
    Size = {
        '大': 3,
        '中': 2,
        '小': 1,
    }
    Character = (
        '温顺',
        '凶猛',
    )

    def __init__(self,
                 category,
                 size,
                 character):
        self.category = category
        self.size = __class__.Size[size]
        self.character = character
    
    @property
    def isviolent(self):
        '''判断是否是凶猛动物'''
        return self.size >= __class__.Size['中'] and self.character == '凶猛'

    @abstractmethod
    def __eq__(self, other):
        '''用于动物及其子类实例之间的比较'''


class Cat(Animal):
    Voice = None

    def __init__(self,
                 name,
                 category,
                 size,
                 character):
        super(Cat, self).__init__(category,
                                  size,
                                  character)
        self.name = name

    def __eq__(self, other):
        '''判断是否是同一只猫'''
        return (self.name == other.name and
                self.category == other.category and
                self.size == other.size and
                self.character == other.character)
    
    def __str__(self):
        return self.name
    
    __repr__ = __str__
    
    @property
    def ispet(self):
        return not self.isviolent


class Zoo(object):
    def __init__(self, name):
        self.name = name
        self.__animals = {}

    @property
    def animals(self):
        return self.__animals
    
    def add_animal(self, animal: 'Animal'):
        cur_animals = self.__animals.get(animal.__class__.__name__, None)
        if cur_animals is None:
            self.__animals[animal.__class__.__name__] = [animal]
            print(f'成功添加{animal.name}')
        else:
            if animal not in cur_animals:
                cur_animals.append(animal)
                print(f'成功添加{animal.name}')
            else:
                print(f'{animal.name}已存在')
    
    def have_animal(self, animal_type):
        have_ani = self.__animals.get(animal_type, None)
        if have_ani:
            return True
        return False




if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    # 增加一只猫到动物园
    z.add_animal(cat1)
    print(z.animals)
    # 动物园是否有猫这种动物
    print(z.have_animal('Cat'))