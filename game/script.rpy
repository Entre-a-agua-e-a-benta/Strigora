# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.
default name_side = "left"

default dia = 1
default interacao = 100

## Variaveis do diálogo com o Vincent
default progressoVincent = 0
default progrediuVincent = False
default ontemVincent = False
default suspeitoVincent = False

## Personagens
define personagens_list = list()
define personagens_dict = dict()
define v = Character("Vincent")
define p = Character("Padre")

# The game starts here.

label start:

    show screen HUD

    python:
        personagens_list = ["Bartolomeu", "Salvatore", "Holga", "Leproso", "Joana", "Margarida", "Agnes", "Bêbado", "Wiliam", "Vincent", "Seren"]
        for personagem in personagens_list:
            personagens_dict[personagem] = [False, 0]

        def alterar_interacao(valor: int):
            global interacao
            interacao = interacao + valor
            if valor >= 0:
                sinal = "+"
            else:
                sinal = ""
            renpy.notify(sinal + str(valor) + " interação")
        
        def passar_dia():
            global dia, personagens_list, personagens_dict
            dia = dia + 1
            for personagem in personagens_list:
                personagens_dict[personagem][0] = False
            renpy.notify("passou o dia")
        
        def progredir(personagem: str):
            global personagens_dict
            personagens_dict[personagem][0] = True
            personagens_dict[personagem][1] += 1

## Cena da taverna externa
    scene  bg taverna ext
    call screen botao_taverna_entrar

## Cena dentro da taverna
label tavernaint:

    scene bg taverna int
    call screen vincent_parado

## Arruma posição dos personagens dentro do dialogo
transform padre_left:
    ypos 0.3
    xpos -0.09

transform vincent_right:
    zoom 0.9
    ypos 0.3
    xpos 0.63

## Dialogo com o Vincent ao clicar no personagem
label dialogo_vincent:

    show padre at padre_left
    p "Buongiorno… Agradeço a hospitalidade, dizem que é perigoso ficar andando de noite por aí… Então me sinto agradecido por ter onde dormir…"
    p "Agora…"
    jump escolhas_vincent
    
label escolhas_vincent:
    hide vincent
    show padre at padre_left
    menu:
        "Me conte sobre você" if personagens_dict["Vincent"] == [False, 0]:
            $ progredir("Vincent")
            jump meconte_vincent
        "O que aconteceu com a esposa do seu irmão?" if personagens_dict["Vincent"] == [False, 1] and dia >= 2:
            $ progredir("Vincent")
            jump esposa_vincent
        "Posso falar com a criança?" if personagens_dict["Vincent"] == [False, 2] and dia >= 3:
            $ progredir("Vincent")
            jump crianca_dialogo

        "Onde e o que você fez ontem a noite?":
            if ontemVincent == False:
                jump ontem_vincent
            else:
                jump default_vincent
        "Algum habitante te parece estranho?":
            if suspeitoVincent == False:
                jump suspeito_vincent
            else:
                jump default_vincen
        
        "Passar dia":
            $ passar_dia()
            jump tavernaint

        "Não perguntar nada":
            jump tavernaint

label meconte_vincent:
    #diminui interação do jogador
    $ alterar_interacao(-1)
    hide padre
    # essa variavel faz com que o nome do personagem apareça na direita
    $ name_side = "right"
    show vincent at vincent_right
    v "Bom… Eu sou o Vincent, cuido da taverna e da estalagem… Ou o que sobrou dela, parece que a aldeia resolveu que o medo é  desculpa para parar de beber."
    v "Mas desde que você chegou, tenho limpado o quarto duas vezes por dia, pelo menos um pouco de trabalho para manter a mente ocupada …. "
    v "Não gosto de falar do que não vi com meus próprios olhos. E, pra ser sincero, ultimamente, prefiro ver cada vez menos. Gente demais sussurrando. Portas que antes ficavam abertas agora estão fechadas…"
    v "Mas minha porta… essa fica aberta. Sempre tem quem precise esquecer o que viu. Meu irmão aparece por aqui às vezes… Mas nunca fica muito tempo e nem fala muito."

    hide vincent
    show padre at padre_left
    p "Quem é seu irmão?"
    hide padre
    show vincent at vincent_right
    v "Ah, com certeza você vai vê- lo por aí… Ele está sempre pelos cantos da aldeia. Ele vem aqui, bebe sem pagar, mas não tenho coragem de cobrar."
    v "Depois que a mulher dele se foi, sobrou pouco dele também."
    jump tavernaint


label esposa_vincent:
    $ alterar_interacao(-1)
    hide padre
    show vincent at vincent_right
    v "Ela estava grávida…Foi um parto difícil, apenas ela e a parteira dentro do quarto…"
    v "Infelizmente ela não resistiu, mas deu a luz a uma garotinha… Isso faz 10 anos, e desde então ele vive nesse estado…Conspiracionando e dizendo que há culpados pela morte da esposa."
    hide vincent
    show padre at padre_left
    p "E a criança? Onde ela está?"
    hide padre
    show vincent at vincent_right
    v "A menina… Bom… Ela está viva, isso é mais do que posso dizer de muita gente…"
    v "Eu cuido dela, mas de um tempo para cá, ela parece doente, às vezes fala coisa dormindo e acorda com febre alta. Eu tento ser como um pai para ela, mas mesmo assim acho que às vezes não sou o suficiente."
    jump tavernaint

label crianca_dialogo:
    if 
    c "eu sou crianca"
    return


label ontem_vincent:
    $ ontemvincent = True
    hide padre
    show vincent at vincent_right
    v "Fiz o que faço toda noite. Fechei a estalagem tarde, como sempre. Tinha um bêbado vomitando na entrada e um quarto reservado pro padre…"
    v "Passei a vassoura, contei os barris, limpei as mesas. E quando a lenha terminou, fui buscar mais atrás do depósito. Voltei antes da meia-noite."
    v "Tranquei tudo por dentro. Ninguém entrou depois disso, nem mesmo meu irmão, que vive dizendo que a bebida chama por ele."

    jump tavernaint

label suspeito_vincent:
    $ habitantevincent = True   
    hide padre
    show vincent at vincent_right
    v "Estranhos? Aqui todos andam com o pescoço encolhido, como galinha no fio da faca."
    v "Mas se quer saber… Há alguém que me parece estranho, não sei o nome dele, mas ele mora quase fora da aldeia, isolado com razão. Alguém com o corpo ferido daquele jeito, com certeza boa coisa não fez e agora Deus o castiga pelos seus pecados."
    v "Não o deixo entrar aqui, mas não é pela doença. É por tudo o resto. Por esse silêncio dele que pesa, pelas coisas que diz sem dizer nada. Tem gente que traz má sorte sem precisar levantar a mão."

    jump tavernaint

label default_vincent:
    hide padre
    show vincent at vincent_right
    v "Nós já conversamos sobre isso..."
    jump tavernaint