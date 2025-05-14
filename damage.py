class Damage():
    def damage(self, person, attack):
        person.hp -= attack
        person.save()