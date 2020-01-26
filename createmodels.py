from party_mode.models import Animal, Adjective

adjetivos = open('/media/moutella/projetos/useful-info/todos-os-adjetivos.txt', 'r')
adjetivos = adjetivos.readline()
for adj in adjetivos.split(","):
    try:
        Adjective.objects.get(name=adj)
    except:
        adj = Adjective(
            name=adj
        )
        adj.save()

animais = open('/media/moutella/projetos/useful-info/animais.txt', 'r')
animais = animais.readline()
for animal in animais.split(","):
    try:
        Animal.objects.get(name=adj)
    except:
        ani = Animal(
            name=animal
        )
        ani.save()