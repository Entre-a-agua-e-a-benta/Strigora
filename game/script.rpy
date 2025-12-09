# The script of the game goes in this file.

# Define posicao de nome dos personagens
default name_side = "left"

default dia = 1 # Define dia incial
default interacao = 1 # Define quantas interações pode ter

default modificadorEvento = 0 # Modificador de chance para eventos aleatórios

default infoPersonagem = "" # Para o quadro de pistas
default musica_atual = "ambiencia_ext_geral.mp3"
## Variaveis do diálogo com o Lázaro
default dor_lazaro = False
default afastou_lazaro = False

## Personagens
define personagens_list = list()
define personagens_dict = dict()
define p = Character("Padre") ## O JOGADOR
define v = Character("Vincent") ## DONO DA ESTALAGEM/TAVERNA
define s = Character("Seren") ## CRIANÇA GEMEA FILHA DO BEBADO
define m = Character("Margarida") ## Curandeira
define l = Character("Lázaro") ## Leproso
define h = Character("Holga")
define b = Character("Bartolomeu") ## PADEIRO
define be = Character("Bêbado")
define ss = Character("Salvatore") ## Senhor Salvatore
define j = Character("Joana") ## Costureira
define a = Character("Agnes") ## Criança pedinte
define w = Character("William") ## Criança William

# The game starts here.

label start:

    show screen HUD

    init python:
        from unidecode import unidecode
        from random import randint

        class Personagem:
            def __init__(self, nome = "Fulano", genero = 'M', hotspot = (0, 0, 0, 0)):
                self.nome = nome
                self.genero = genero
                self.hotspot = hotspot
                self.conversouHoje = False
                self.progresso = 0
                self.listaPistas = []
                self.listaFalas = []
                self.conhecido = False
                self.conversavel = True
                self.vivo = True
                self.descricao = ""
                self.imagem = f"personagens/{unidecode(nome.lower())}/{unidecode(nome.lower())}.png"
                self.retrato = f"personagens/3x4/{unidecode(nome.lower())} retrato.png"
                self.listaPerguntas = [False, False, False]
        
        ## Inicializa o dicionário de personagens
        personagens_list = [("Bartolomeu", 'M', (596, 188, 212, 285)),
                            ("Salvatore", 'M', (0,0,0,0)),
                            ("Holga", 'F', (461, 554, 213, 282)),
                            ("Lázaro", 'M', (1131, 187, 219, 283)),
                            ("Joana", 'F', (0, 0, 0, 0)),
                            ("Margarida", 'F', (326, 188, 216, 285)),
                            ("Agnes", 'F', (864, 187, 214, 283)),
                            ("Bêbado", 'M', (995, 556, 218, 284)),
                            ("William", 'M', (728, 556, 215, 283)),
                            ("Vincent", 'M', (59, 189, 216, 282)),
                            ("Seren", 'F', (193, 556, 214, 284)),
                            ("Bruxa", 'F', (1388, 206, 498, 668))]
        for personagem in personagens_list:
            personagens_dict[personagem[0]] = Personagem(personagem[0], personagem[1], personagem[2])
        personagens_dict["Bartolomeu"].descricao = "Gay"
        personagens_dict["Salvatore"].descricao = "bebado"
        personagens_dict["Bêbado"].descricao = "Irmão do dono da estalagem taverna (Vincent) e pai de uma menina de 10 anos"

        def checar_interacao():
            global interacao
            if interacao == 0:
                renpy.jump("casapadre_noite")

        def alterar_interacao(valor: int):
            global interacao
            interacao = interacao + valor
            sinal = "+" if valor >= 0 else ""
            renpy.notify(sinal + str(valor) + " interação")

        def passar_dia(matar_personagem=None):
            global dia, interacao, personagens_list, personagens_dict
            dia = dia + 1
            for personagem in personagens_list:
                personagens_dict[personagem[0]].conversouHoje = False
            interacao = 3
            if matar_personagem != None:
                personagens_dict[matar_personagem].vivo = False
                renpy.notify("Matei " + matar_personagem)
            evento_aleatorio()
            renpy.jump("casapadre")

        def evento_aleatorio():
            global interacao, modificadorEvento
            # Chance para cada evento (Ruim, Neutro, Bom)
            if modificadorEvento == 1: # Dia de sorte
                chanceEventos = (20, 50, 30)
            elif modificadorEvento == 0: # Dia normal
                chanceEventos = (25, 50, 25)
            elif modificadorEvento == -1: # Dia de azar
                chanceEventos = (30, 50, 20)
            renpy.notify(f"chance atual de evento: {chanceEventos[0]}/{chanceEventos[1]}/{chanceEventos[2]}") # DEBUG, APAGAR!!!

            #evento = (randint(1, 100), randint(1, 4)) # (1~100, 1~4)
            evento = (10, 1) # manipulando evento pra testes
            if evento[0] <= chanceEventos[0]:  # Evento Ruim
                if evento[1] == 1: # Impossibilitar falar com personagem aleatório
                    personagem = personagens_dict[personagens_list[randint(0, len(personagens_list)-1)][0]]
                    while personagem.vivo != True:
                        personagem = personagens_dict[personagens_list[randint(0, len(personagens_list)-1)][0]]
                    personagem.conversavel = False
                    renpy.notify("Não vou conseguir falar com " + personagem.nome + " hoje...")
                elif evento[1] == 2: # Perder interação (-1 interação)
                    renpy.notify("Perdi interação (-1 interação)")
                    alterar_interacao(-1)
                elif evento[1] == 3: # Animais adoecem (chance maior de evento ruim na próxima noite)
                    renpy.notify("Seus animais adoeceram... (chance maior de evento ruim na próxima noite)")
                    modificadorEvento = -1
                elif evento[1] == 4: # Paranoia: o padre é obrigado a acusar alguém na próxima noite -> mudar
                    renpy.notify("Você está tomado pela paranoia... (será obrigado a acusar alguém na próxima noite)")
            elif evento[0] <= chanceEventos[0] + chanceEventos[1]:  # Evento Neutro
                if evento[1] == 1: # Noite tranquila
                    renpy.notify("Noite tranquila")
                elif evento[1] == 2: # Momento de paz temporária
                    renpy.notify("Momento de paz temporária")
                elif evento[1] == 3: # A Bruxa permanece inativa
                    renpy.notify("A Bruxa permanece inativa")
                elif evento[1] == 4: # O padre entra em conflito interno
                    renpy.notify("O padre entra em conflito interno")
            elif evento[0] > 100 - chanceEventos[2]:
                if evento[1] == 1:
                    # Missa comunitária (+1 interação)
                    renpy.notify("Missa comunitária (+1 interação)")
                    alterar_interacao(+1)
                elif evento[1] == 2: # Dia promissor (+1 interação) - igual ao anterior
                    renpy.notify("Dia promissor")
                elif evento[1] == 3: # Janta comunitária (+ chance de evento bom)
                    renpy.notify("Janta comunitária (+ chance de evento bom na próxima noite)")
                    modificadorEvento = 1
                elif evento[1] == 4: # Ajuda os moradores (abstenção sem punição na próxima noite) -> mudar
                    renpy.notify("Você ajudou os moradores (abstenção sem punição na próxima noite)")
        
        # Progride o diálogo de um personagem específico, aumentando seu progresso em 1 e marcando que já conversou hoje.
        def progredir(personagem: str):
            global personagens_dict
            personagens_dict[personagem].conversouHoje = True
            personagens_dict[personagem].progresso += 1

        """
        Adiciona uma pista à lista de pistas de um personagem específico.
        Após isso, notifica no formato "Pista adquirida: <Personagem> <pista>"
        Args:
            personagem (str): O nome do personagem ao qual a pista será adicionada.
            pista (str): A pista a ser adicionada.
        """
        def adicionar_pista(personagem: str, pista: str):
            global personagens_dict
            if pista not in personagens_dict[personagem].listaPistas:
                personagens_dict[personagem].listaPistas.append(pista)
                renpy.notify("Pista adquirida: " + personagem + " " + pista[0].lower() + pista[1:])
 
        """
        Atualiza a lista de pistas para mostrar na tela de pistas de cada personagem.
        Args:
            personagem (str): O nome do personagem cujas pistas serão atualizadas.
        Returns:
            list: Uma lista contendo as pistas do personagem (no momento são 5 no máximo para cada um).
        """
        def atualizar_pistas(personagem: str)->list:
            pistas_list = ["", "", "", "", ""]
            i = 0
            for pista in personagens_dict[personagem].listaPistas:
                pistas_list[i] = pista
                i += 1
            return pistas_list

        def adicionar_fala(personagem: str, fala: str):
            global personagens_dict
            if fala not in personagens_dict[personagem].listaFalas:
                personagens_dict[personagem].listaFalas.append(fala)
                renpy.notify("Falas de: "+ personagem + "" + + fala[0].lower() + fala[1:])
        
        def atualizar_falas(personagem: str)->list:
            falas_list = ["", "", "", "", "", "", ""]
            i = 0
            for fala in personagens_dict[personagem].listaFalas:
                falas_list[i] = fala
                i += 1
            return falas_list

        def mostrar_personagem(personagem: str, emocao: str):
            global name_side
            name_side = "left" if personagem == "Padre" else "right"
            renpy.show_screen("personagemEmocao", personagem.lower(), emocao)

        def mostrar_botao(posicao: tuple, texto: str, jumpTo: str):
            renpy.show_screen("botao_passos", posicao, texto, jumpTo)

        def tocar_musica(musica: str):
            global musica_atual
            if musica != musica_atual:
                renpy.music.play(musica)
                musica_atual = musica

        

#### $ adicionar_pista("Vincent", "Gosta de HOMENS") #### é assim que bota pista

########################################## AQUI COMEÇA O JOGO ##############################################################    

######################################## LOCAIS PELO MAPA ##############################################################

## Cena externa da taverna
label tavernaext:
    call hide_all_screens
    $ tocar_musica("ambiencia_ext_geral.mp3")
    scene bg taverna ext
    call screen tavernaext

## Cena dentro da taverna
label tavernaint:
    call hide_all_screens
    scene bg taverna int
    call screen tavernaint

## Cena casa do bebado
label casabebadoext:
    call hide_all_screens
    $ tocar_musica("ambiencia_ext_geral.mp3")
    scene bg casa bebado ext
    call screen casabebado

## Cena quarto do padre dentro da taverna
label casapadre:
    call hide_all_screens
    $ tocar_musica("ambiencia_int_casas.wav")
    scene bg casa padre int
    call screen casapadre

## Cena Casa Margarida Ext
label casamargaridaext:
    call hide_all_screens
    $ tocar_musica("ambiencia_ext_geral.mp3")
    scene bg casa curandeira ext
    call screen casaMargaridaEXT

## Cena Casa Lázaro Ext
label caminhoLazaro:
    call hide_all_screens
    $ tocar_musica("ambiencia_ext_floresta.wav")
    scene bg casa leproso ext
    call screen casaLazaroEXT

## Cena Caminho entre bebado e margarida   
label caminhobebado_margarida:
    call hide_all_screens
    $ tocar_musica("ambiencia_ext_floresta.wav")
    scene bg caminho curandeira
    call screen caminhobebado_margarida

## Cena Casa Lázaro Int
label casaLazaroint:
    call hide_all_screens
    $ tocar_musica("ambiencia_int_casas.wav")
    scene bg leproso int
    call screen casaLazaroINT

## Cena Casa Holga
label casaholgaext:
    call hide_all_screens
    $ tocar_musica("ambiencia_ext_geral.mp3")
    scene bg casa holga ext
    call screen casaHolgaEXT

## Cena praca 2 que tem a escultura
label praca2:
    call hide_all_screens
    $ tocar_musica("ambiencia_ext_geral.mp3")
    scene bg praca2
    call screen praca2

## Cena praca 1 que tem igreja e padaria
label praca1:
    call hide_all_screens
    $ tocar_musica("ambiencia_ext_geral.mp3")
    scene bg praca1
    call screen praca1

label igreja:
    call hide_all_screens
    $ tocar_musica("ambiencia_ext_geral.mp3")
    scene bg igreja int
    call screen igrejaINT

label padaria:
    call hide_all_screens
    $ tocar_musica("ambiencia_int_casas.mp3")
    scene bg padaria int
    call screen padariaINT

label casajoanaext:
    call hide_all_screens
    $ tocar_musica("ambiencia_ext_geral.mp3")
    scene bg costureira ext
    call screen casaJoanaEXT

label plantacao:
    call hide_all_screens
    $ tocar_musica("ambiencia_ext_floresta.wav")
    scene bg plantacao
    call screen plantacao

############# Arruma posição dos personagens dentro do dialogo ###############################
transform padre_left:
    zoom 0.5
    ypos 0.1
    xanchor 0.5
    xpos 350
transform personagem_right:
    zoom 0.5
    ypos 0.1
    xpos 0.5

######################################## CENAS QUE OCORREM NA TAVERNA #######################################################

## Dialogo com o Vincent ao clicar no personagem
label dialogo_vincent:
    call hide_all_screens
    if personagens_dict["Vincent"].conversavel:
        if personagens_dict["Vincent"].conhecido == False: # Primeiro diálogo com Vincent
            $ personagens_dict["Vincent"].conhecido = True
            $ mostrar_personagem("Padre", 'F')
            p "Buongiorno… Agradeço a hospitalidade, dizem que é perigoso ficar andando de noite por aí… Então me sinto agradecido por ter onde dormir…"
            $ mostrar_personagem("Padre", 'N')
            p "Agora…"
        jump escolhas_vincent
    else:
        $ mostrar_personagem("Vincent", 'T')
        v "Não estou com vontade de conversar hoje..."
        jump tavernaint
    
label escolhas_vincent:
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Me conte sobre você" if personagens_dict["Vincent"].conversouHoje == False and personagens_dict["Vincent"].progresso == 0:
            $ progredir("Vincent")
            jump meconte_vincent
        "O que aconteceu com a esposa do seu irmão?" if personagens_dict["Vincent"].conversouHoje == False and personagens_dict["Vincent"].progresso == 1:
            $ progredir("Vincent")
            jump esposa_vincent

        "Você conhecia bem o antigo padre?" if personagens_dict["Vincent"].listaPerguntas[0] == False:
            $ personagens_dict["Vincent"].listaPerguntas[0] = True
            jump padre_vincent

        "Onde e o que você fez ontem a noite?" if personagens_dict["Vincent"].listaPerguntas[1] == False:
            $ personagens_dict["Vincent"].listaPerguntas[1] = True
            jump ontem_vincent

        "Algum habitante te parece estranho?" if personagens_dict["Vincent"].listaPerguntas[2] == False:
            $ personagens_dict["Vincent"].listaPerguntas[2] = True
            jump suspeito_vincent
        
        "Passar dia":
            $ passar_dia()
            jump noite

        "Não perguntar nada":
            jump tavernaint

label ontem_vincent:
    $ alterar_interacao(-1)
    $ mostrar_personagem("Vincent", 'N')
    v "Fiz o que faço toda noite. Fechei a estalagem tarde, como sempre. Tinha um bêbado vomitando na entrada e um quarto reservado pro padre…"
    v "Passei a vassoura, contei os barris, limpei as mesas e quando a lenha terminou, fui buscar mais atrás do depósito. Voltei antes da meia-noite."
    v "Tranquei tudo por dentro. Ninguém entrou depois disso, nem mesmo meu irmão, que vive dizendo que a bebida chama por ele."
    $ checar_interacao()
    jump tavernaint

label suspeito_vincent:
    $ alterar_interacao(-1) 
    $ mostrar_personagem("Vincent", 'N')
    v "Estranhos? Aqui todos andam com o pescoço encolhido, como galinha no fio da faca."
    $ mostrar_personagem("Vincent", 'R')
    v "Mas se quer saber… Há alguém que me parece estranho, não sei o nome dele, mas ele mora quase fora da aldeia, isolado com razão. Alguém com o corpo ferido daquele jeito, com certeza boa coisa não fez e agora Deus o castiga pelos seus pecados."
    v "Não o deixo entrar aqui, mas não é pela doença. É por tudo o resto. Por esse silêncio dele que pesa, pelas coisas que diz sem dizer nada. Tem gente que traz má sorte sem precisar levantar a mão."
    $ adicionar_fala("Lázaro", "é acusado por Vincent pois: \"O homem que mora quase fora da aldeia tem o corpo ferido, com certeza não fez coisa boa e foi castigado por Deus. O silêncio dele pesa\".")
    $ checar_interacao()
    jump tavernaint

label default_vincent:
    $ mostrar_personagem("Vincent", 'N')
    v "Não estou num bom dia hoje..."
    jump tavernaint

label meconte_vincent:
    #diminui interação do jogador
    $ alterar_interacao(-1)
    $ mostrar_personagem("Vincent", "N")
    v "Bom… Eu sou o Vincent, cuido da taverna e da estalagem… Ou o que sobrou dela, parece que a aldeia resolveu que o medo é desculpa para parar de beber."
    v "Mas desde que você chegou, tenho limpado o quarto duas vezes por dia, pelo menos um pouco de trabalho para manter a mente ocupada... "
    v "Não gosto de falar do que não vi com meus próprios olhos. E, pra ser sincero, ultimamente, prefiro ver cada vez menos. Gente demais sussurrando. Portas que antes ficavam abertas agora estão fechadas…"
    $ mostrar_personagem("Vincent", 'F')
    v "Mas minha porta… essa fica aberta. Sempre tem quem precise esquecer o que viu. Meu irmão aparece por aqui às vezes… Mas nunca fica muito tempo e nem fala muito."
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Quem é seu irmão?":
            jump irmao_vincent
label irmao_vincent:
    $ mostrar_personagem("Vincent", 'N')
    v "Ah, com certeza você vai vê- lo por aí… Ele está sempre pelos cantos da aldeia. Ele vem aqui, bebe sem pagar, mas não tenho coragem de cobrar."
    $ mostrar_personagem("Vincent", 'T')
    v "Depois que a mulher dele se foi, sobrou pouco dele também."
    $ adicionar_pista("Bêbado", "perdeu a esposa, após o acontecimento Vincent diz que sobrou pouco dele")
    $ checar_interacao()
    jump tavernaint

label esposa_vincent:
    $ alterar_interacao(-1)
    $ mostrar_personagem("Vincent", 'T')
    v "Ela estava grávida… Foi um parto difícil, apenas ela e a parteira dentro do quarto…"
    v "Infelizmente ela não resistiu, mas deu a luz a uma garotinha… Isso faz 10 anos."
    $ adicionar_pista("Bêbado", "Esposa morreu no parto")
    $ adicionar_pista("Bêbado", "Tem uma filha de 10 anos")
    v "Desde então ele vive nesse estado… Conspirando e dizendo que há culpados pela morte da esposa."
    $ adicionar_pista("Bêbado", "Culpa alguém pela morte da esposa")
    $ mostrar_personagem("Padre", 'T')
    menu:
        "E a criança? Onde ela está?":
            jump crianca_vincent
label crianca_vincent:
    $ mostrar_personagem("Vincent", 'N')
    v "A menina… Bom… Ela está viva, isso é mais do que posso dizer de muita gente…"
    $ mostrar_personagem("Vincent", 'F')
    v "Eu cuido dela"
    $ mostrar_personagem("Vincent", 'T')
    v "Mas de um tempo para cá, ela parece doente, às vezes, fala coisa dormindo e acorda com febre alta. Eu tento ser como um pai para ela, mas mesmo assim acho que às vezes não sou o suficiente."
    $ adicionar_fala("Seren", "parece doente, às vezes, fala coisa dormindo e acorda com febre alta")
    $ checar_interacao()
    jump tavernaint

label padre_vincent:
    $ alterar_interacao(-1)
    $ mostrar_personagem("Vincent", 'R')
    v "Bem o suficiente pra saber que se meteu onde não devia."
    v "Vivia metendo o nariz em cantos escuros da aldeia, perguntando demais, rezando de menos."
    v "Um dia sumiu... e quando encontraram, não era mais um homem. Era só um corpo... vazio."
    $ mostrar_personagem("Vincent", 'N')
    v "Você é diferente? Ou vai terminar igual?"
    $ adicionar_fala("Vincent", "acusa o antigo padre de \"sumir e quando encontraram, não era mais um homem. Era só um corpo... vazio.\"")
    $ mostrar_personagem("Padre", 'R')
    menu:
        "Ficar em silêncio":
            jump tavernaint
            $ checar_interacao()
        "Diferente ou não, não vim aqui rezar pelos mortos. Vim para entender porque  estão morrendo.":
            jump tavernaint
            $ checar_interacao()
        "Se sou diferente? Bem, ainda estou vivo, não estou?":
            jump tavernaint
            $ checar_interacao()
        "Espero que sim. Espero que minha fé seja suficiente para me manter de pé… e talvez salvar quem ainda resta.":
            jump tavernaint
            $ checar_interacao()

######################################## CENAS SEREN #######################################################
label dialogo_seren:
    call hide_all_screens
    $ mostrar_personagem("Padre", 'N')
    p "Buongiorno, pequena. Deus lhe abençoe, eu gostaria de conversar um pouco com você."
    menu:
        "Me conte sobre você." if personagens_dict["Seren"].conversouHoje == False and personagens_dict["Seren"].progresso == 0:
            $ progredir("Seren")
            jump meconte_seren
        "Vejo que algo te incomoda. O que é?"if personagens_dict["Seren"].conversouHoje == False and personagens_dict["Seren"].progresso == 1:
            $ progredir("Seren")
            jump incomoda_seren
        "Onde e o que você fez ontem a noite?" if personagens_dict["Seren"].pergunta1 == False:
            $ personagens_dict["Seren"].pergunta1 = True
            jump ontem_seren
        "Algum habitante te parece estranho?" if personagens_dict["Seren"].pergunta2 == False:
            $ personagens_dict["Seren"].pergunta2 = True
            jump habitante_seren
    return

label meconte_seren:
    $ alterar_interacao(-1)
    $ mostrar_personagem("Seren", 'N')
    s "Eu sou a Seren. Tenho dez anos…"
    s "Meu pai mora aqui na aldeia também… Às vezes ele passa por aqui, mas não fica muito."
    $ mostrar_personagem("Seren", 'T')
    s "Ele não gosta que eu fale com estranhos."
    $ mostrar_personagem("Seren", 'F')
    s "Mas o tio disse que você é diferente. Então eu posso responder…"
    $ checar_interacao()

label incomoda_seren:
    $ alterar_interacao(-1)
    $ mostrar_personagem("Seren", 'T')
    s "Queria ser mais forte"
    s "Às vezes eu finjo que não vejo quando meu pai me olha triste."
    s "Eu entendo pq ele me olha assim..."
    s "Ao menos ele bebe pra esquecer, mas eu lembro por nós dois. Lembro mesmo do que nunca vi…"
    $ mostrar_personagem("Seren", 'F')
    s "Ainda bem que o tio me dá pão, me dá coberta, e até me deixa ficar atrás do balcão quando chove."
    s "Ele nunca disse que me ama, mas também nunca me culpou nem me olhou triste"
    $ mostrar_personagem("Seren", 'T')
    s "As vezes acontecem coisas estranhas a noite… Não é todo sonho que dói. Só os que parecem verdade."
    $ adicionar_fala("Seren", "As vezes acontecem coisas estranhas a noite… Não é todo sonho que dói. Só os que parecem verdade.")
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Vcê tem tido sonhos estranhos?":
            jump sonhos_seren
        "Como são esses sonhos?":
            jump sonhos_seren
label sonhos_seren:
    $ mostrar_personagem("Seren", 'N')
    s "No começo, eu só via silhuetas. Um campo, uma árvore sozinha, uma sombra me seguindo de longe. Depois vieram os sussurros. E agora, agora… Agora eu vejo tudo…"
    $ adicionar_pista("Seren", "sonhava vendo silhuetas ou sombras a seguindo e agora \"vê tudo\".")
    s "No sonho, ando pelas ruas da aldeia com passos que não são meus… As mãos... as mãos que estendo são pequenas, como as minhas. Mas elas brilham. Como brasa acesa no escuro. E quando tocam algo, tudo escurece..."
    $ adicionar_pista("Seren", "no sonho, anda pelas ruas da aldeia com passos que não são seus e mãos que brilham como brasa acesa no escuro.")
    $ mostrar_personagem("Seren", 'T')
    s "E o que mais me assusta: há uma voz dentro de mim. Mas ela não fala comigo. Ela me usa… "
    $ adicionar_pista("Seren", "no sonho, há uma voz dentro dela que não fala com ela, mas a usa.")
    s "Mas o pior é quando vejo ele… o menino com voz de mulher… Ele fala, mas a boca não mexe… Ele parece viver numa tristeza que me queima..."
    $ adicionar_fala("Seren", "\"Mas o pior é quando vejo ele… o menino com voz de mulher… Ele fala, mas a boca não mexe… Ele parece viver numa tristeza que me queima...\".")
    s "Quando acordo, a pele está quente como se eu tivesse corrido por horas. A febre queima atrás dos olhos, e minha garganta parece de vidro."
    $ mostrar_personagem("Seren", 'N')
    s "O tio diz que é só vento, ou comida estragada."
    $ mostrar_personagem("Seren", 'T')
    s "Mas toda vez que eu sonho, algo na aldeia amanhece errado. Eu queria contar, gritar... Dizer o que vejo… Mas quem vai acreditar numa menina que até o próprio pai não quis segurar no colo?"
    $ adiconar_pista("Seren", "sente que toda vez que sonha, algo na aldeia amanhece errado.")
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Com o que você sonhou ontem?":
            jump sonhoontem_seren
        "Qual foi o seu sonho mais recente?":
            jump sonhoontem_seren
label sonhoontem_seren:
    $ mostrar_personagem("Seren", 'N')
    s "Ontem… ontem no sonho eu estava em frente ao espelho de uma casa grande, e o menino estava dentro do espelho me olhando de volta. Só que, por um instante, os olhos dele eram os meus…"
    $ adicionar_fala("Seren", "\"o menino estava dentro do espelho me olhando de volta. Só que, por um instante, os olhos dele eram os meus…\".")
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Conte mais sobre esse menino do sonho":
            jump menino_seren
label menino_seren:
    $ mostrar_personagem("Seren", 'N')
    s "Ele parece triste… Sempre me olha de um jeito estranho, como se me conhecesse"
    $ adicionar_fala("Seren", "o menino do sonho \"Sempre me olha de um jeito estranho, como se me conhecesse\".")
    s "Uma vez eu vi meu rosto no lugar do dele. Mas eu sei que não era eu… Eu estava olhando pra mim, mas eu era outra pessoa. Não sei explicar…"
    $ adicionar_fala("Seren", "\"Uma vez eu vi meu rosto no lugar do\" menino do sonho \"Mas eu sei que não era eu… Eu estava olhando pra mim, mas eu era outra pessoa.\".")
    $ checar_interacao()
    jump tavernaint

label ontem_seren:
    $ alterar_interacao(-1)
    $ mostrar_personagem("Seren", 'F')
    s "Eu fiquei aqui na taverna. O tio me deu pão com mel… Eu adoro quando sobra mel."
    $ mostrar_personagem("Seren", 'N')
    s "Eu sentei perto da escada e ouvi as vozes lá embaixo. Depois fui pro quarto."
    $ mostrar_personagem("Seren", 'R')
    s "Quando o salão ficou em silêncio, fechei os olhos. Mas aí o sonho veio… Como se ele me chamasse de algum lugar longe… como se já soubesse onde eu estava."
    $ checar_interacao()
    jump tavernaint

label habitante_seren:
    $ alterar_interacao(-1)
    $ mostrar_personagem("Seren", 'N')
    s "Tem a dona Margarida... Não que ela seja má, eu acho. Mas ela olha pras pessoas como se lesse o que tem dentro."
    $ adiconar_pista("Margarida", "olha pras pessoas como se lesse o que tem dentro.")
    $ mostrar_personagem("Seren", 'R')
    s "Um dia ela olhou pra mim, encostou a mão na minha testa e disse: \"Nem todo espelho mostra só o que é de fora\". Eu não entendi, mas me deu um arrepio."
    $ adiconar_pista("Margarida", "disse \"Nem todo espelho mostra só o que é de fora\" para Seren.")
    $ adicionar_pista("Seren", "escutou Margarida dizendo pra ela \"Nem todo espelho mostra só o que é de fora\".")
    jump tavernaint

######################################## CENAS QUE OCORREM NA CASA DA MARGARIDA #######################################################
label dialogo_margarida:
    call hide_all_screens
    $ mostrar_personagem("Padre", 'N')
    p "Buongio...)"
    $ mostrar_personagem("Margarida", 'N')
    m "A benção, padre."
    m "Veio aqui procurar um motivo para jogar a culpa em mim?"
    $ mostrar_personagem("Padre", 'R')
    p "Não, claro que não. Estou apenas investigando… "
    $ mostrar_personagem("Padre", 'N')
    p "Por favor, fale comigo."
    jump escolhas_margarida

label escolhas_margarida:
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Me conte sobre você" if personagens_dict["Margarida"].pergunta0 == False:
            $ personagens_dict["Margarida"].pergunta0 = True
            jump meconte_margarida
        "Onde e o que você fez ontem a noite?" if personagens_dict["Margarida"].pergunta1 == False:
            $ personagens_dict["Margarida"].pergunta1 = True
            jump ontem_margarida
        "Me conte uma história" if personagens_dict["Margarida"].pergunta2 == False:
            $ personagens_dict["Margarida"].pergunta2 = True
            jump historia_margarida
        "Não perguntar nada":
            jump casamargaridaext

label meconte_margarida:
    $ mostrar_personagem("Margarida", 'N')
    $ alterar_interacao(-1)
    m "Contar? o que? Porque faria isso? Já sei o que pensa. Sei o que todos pensam… "
    $ mostrar_personagem("Margarida", 'R')
    m "Uma mulher sozinha , que mexe com o que não entendem, e já afiam a corda, já juntam lenha…"
    m "Ignorantes…"
    m "Eles me chamam de contadora de histórias, como se eu fosse apenas isso. Eles não se lembram das pessoas que salvei. Já vi mais gente morrer do que você viu nascer. Sei quando a terra adoece, quando o vento muda de cheiro, quando a mão treme antes mesmo de tocar na porta."
    $ adicionar_pista("Margarida", "fala que ela mesma \"sabe quando a terra adoece, quando o vento muda de cheiro, quando a mão treme antes mesmo de tocar na porta.\".")
    m "Mas não me olhe assim, eu não mexo com os mortos e nem falo com sombras. Só aprendi a ouvir o que ninguém mais quer escutar. A Natureza."
    $ mostrar_personagem("Padre", 'T')
    menu:
        "Como acha que a vila está lidando com tudo isso?":
            jump vila_margarida
label vila_margarida:
    $ mostrar_personagem("Margarida", 'R')
    m "Lidando? Hmpf… Não estão lidando. Estão se agarrando nas cruzes e nas culpas, como sempre fizeram. Fingem que rezam, mas trancam as portas antes do pôr do sol."
    $ mostrar_personagem("Margarida", 'T')
    m "Quando a terra começa a apodrecer, os ratos são os primeiros a fugir. Mas aqui? Aqui ninguém pode fugir. Este é o purgatório deles. Eles sussurram, acusam, rezam… mas ninguém realmente escuta."
    m "Mas eu? eu escuto. E o que ouço é… medo. Medo, mais do que dor."
    m "A vila não está lidando… está esperando. Esperando que alguém sangre primeiro, para poder chamar de castigo, ou de milagre."
    $ checar_interacao()
    jump casamargaridaext

label ontem_margarida:
    $ mostrar_personagem("Margarida", 'N')
    $ alterar_interacao(-1)
    m "O que eu fiz? O mesmo que faço quando o céu fica quieto demais."
    m "Acendi o fogo, deixei a chaleira cantar e comecei a apreciar sua melodia. Alguns dormem para esquecer… eu fico acordada, para lembrar. Vigiar."
    $ mostrar_personagem("Margarida", 'F')
    m "Às vezes… o que a gente precisa ouvir só aparece no silêncio. Entre um estalo de madeira…. e o outro, entende?"
    $ checar_interacao()
    jump casamargaridaext

label historia_margarida:
    $ mostrar_personagem("Margarida", 'N')
    $ alterar_interacao(-1)
    m "Já ouviu a história da corça de três olhos? Não? Então sente e escute, ou vá embora de vez…"
    m "Dizem que, certa vez, uma mulher andava sozinha pela mata, cheia de dor e raiva do mundo. Chorava tanto que as árvores taparam os ouvidos. Foi quando encontrou um ninho, entre galhos partidos, com um choro que não era de ave nem de fera…"
    m "Lá dentro? Dois bebês, iguais… Como um espelho."
    $ adicionar_fala("Margarida", "conta uma história de uma mulher que viva na mata e encontrou dois bebês iguais como um espelho.")
    m "Mas um tinha os olhos fechados e sorria dormindo. O outro tinha os olhos abertos… e não piscava… A mulher, sozinha no mundo, mesmo sabendo que não era seu,  levou um deles nos braços."
    $ adicionar_fala("Margarida", "em sua história \"um tinha os olhos fechados e sorria o outro tinha olhos abertos e não piscava\" e a mulher \"levou um deles nos braços\".")
    m "Disse: \"é um sinal… O destino me escolheu.\"  Alimentou… deu nome… cobriu de orações. O outro bebê? … ficou. Nunca chorou. Nunca morreu. Só… ficou. Esperando."
    $ adicionar_fala("Margarida", "em sua história a mulher alimentou nomeou e orou pelo bebê que levou, enquanto o outro \"nunca chorou. Nunca morreu. Só… ficou. Esperando.\".")
    m "Um dia… a criança levada perguntou: \"Quem é meu pai?\" E ela respondeu: \"Um homem… que não tem nome… e que não pode ser acordado.\"."
    m "Desde então… dizem… a corça de três olhos ronda a aldeia… procurando seu parente perdido. E a criança… ah… ela ainda vive entre nós… Só não sabe… quem… é."
    $ adicionar_fala("Margarida", "desde sua história \"a corça de três olhos ronda a aldeia… procurando seu parente perdido. E a criança… ah… ela ainda vive entre nós… Só não sabe… quem… é.\"")
    $ checar_interacao()
    jump casamargaridaext

######################################## CENAS QUE OCORREM NA CASA DO Lázaro #######################################################
label dialogo_lazaro:
    call hide_all_screens
    $ mostrar_personagem("Padre", 'N')
    p "Buongiorno…"
    p "Não sei a notícia chegou aqui, mas eu estou encarregado de achar o culpado pelas coisas que vem acontecendo na região, pensei que, mesmo doente, você talvez tivesse alguma informação para contribuir... ou, qo menos, algo interessante a dizer."
    jump escolhas_lazaro

label escolhas_lazaro:
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Me conte sobre você" if personagens_dict["Lázaro"].conversouHoje == False and personagens_dict["Lázaro"].progresso == 0:
            $ progredir("Lázaro")
            jump meconte_lazaro
        "O que o Salvatore fez?" if personagens_dict["Lázaro"].conversouHoje == False and personagens_dict["Lázaro"].progresso == 1 and dia >= 2:
            $ progredir("Lázaro")
            jump salvatorefez_lazaro

        "Há quanto tempo está doente?" if personagens_dict["Lázaro"].pergunta1 == False:
            $ personagens_dict["Lázaro"].pergunta1 = True
            jump doenca_lazaro
        "O que você fez ontem a noite?" if personagens_dict["Lázaro"].pergunta2 == False:
            $ personagens_dict["Lázaro"].pergunta2 = True
            jump ontem_lazaro

        "Não perguntar nada":
                jump casaLazaroint

label meconte_lazaro:
    $ mostrar_personagem("Lazaro", 'N')
    $ alterar_interacao(-1)
    l "Pode chegar mais perto…"
    l "Dizem que a bruxa me amaldiçoou, eles tem medo de mim. Sussurram isso quando pensam que não ouço. Mas meus ouvidos ainda funcionam."
    l "O povo da aldeia acredita que esta carne apodrecida, estas mãos imóveis e este rosto que já não reconheço no reflexo da água... são obra de feitiçaria. São muitos boatos que circulam sobre eu ter ficado assim."
    l "Alguns dizem que cruzei o caminho da costureira e não lhe dei a devida reverência. Que tomei algo que era dela."
    l "Ou que fui tolo o bastante para recusar um favor da contadora de histórias, aquela que anda com ervas estranhas pendendo do cinto e olhos que nunca piscam."
    $ mostrar_personagem("Padre", 'T')
    menu:
        "O que você acha disso?":
            jump acredita_lazaro
        "E o que você acredita?":
            jump acredita_lazaro
label acredita_lazaro:
    $ mostrar_personagem("Lazaro", 'T')
    l "Eu sei que a verdade é outra. Fui esquecido por Deus…"
    $ mostrar_personagem("Padre", 'R')
    menu:
        "Dizer que foi esquecido por Deus é fácil quando o mundo inteiro vira o rosto. Mas será que foi Deus quem se afastou de você… ou foi você quem se escondeu afastou e se escondeu dele?":
            jump afastou_lazaro

        "Às vezes, eu também me pergunto se Ele nos ouve... ou se apenas observa. Mas me diga… quando foi a última vez que sentiu algo que não fosse dor?":
            jump dor_lazaro       
label afastou_lazaro:
    $ afastou_lazaro = True
    $ mostrar_personagem("Lazaro", 'F')
    l "Procurei, sim. Por anos. Rezei até a garganta secar. E tudo o que ouvi foi o som da minha pele caindo."
    $ mostrar_personagem("Lazaro", 'R')
    l "Se Deus está me testando... então por que ninguém mais sangra como eu?"
    l "Acho que ele me deixou, ou não se importa com um leproso como eu."
    $ mostrar_personagem("Padre", 'R')
    p "Não pode atribuir suas dores a Deus, como se tudo que mal que ocorresse no mundo fosse sua culpa."
    $ mostrar_personagem("Padre", 'F')
    p "Pode ter certeza que ele o escuta, e caso realmente acredite nele, logo estará nos céus ao seu lado. Lembre-se de Mateus 8."
    if dor_lazaro == False:
        $ mostrar_personagem("Padre", 'T')
        menu:
            "Mas me diga… quando foi a última vez que sentiu algo que não fosse dor?":
                jump dor_lazaro
    else:
        jump salvatorevinda_lazaro
label dor_lazaro:
    $ dor_lazaro = True
    $ mostrar_personagem("Lazaro", 'N')
    l "Senti algo... Uma vez. Quando o Salvatore veio aqui com olhos de choro e mãos trêmulas. Mas não era piedade, era medo."
    l "Medo de que eu soubesse o que ele fez, ou de que eu ainda lembrasse…"
    $ adicionar_pista("Salvatore", "Foi no Lázaro com olhos de choro e mãos trêmulas, parecendo ter medo de algo")
    if afastou_lazaro == False:
        $ mostrar_personagem("Padre", 'R')
        menu:
            "Dizer que foi esquecido por Deus é fácil quando o mundo inteiro vira o rosto. Mas será que foi Deus quem se afastou de você… ou foi você quem se escondeu afastou e se escondeu dele?":
                jump afastou_lazaro
    else:
        jump salvatorevinda_lazaro
label salvatorevinda_lazaro:
    $ mostrar_personagem("Padre", 'N')
    menu:
        "O que você sentiu?":
            jump sentiu_lazaro
label sentiu_lazaro:
    $ mostrar_personagem("Lazaro", 'F')
    l "Um calor estranho… Não fisico, mas emocional."
    l "Pela primeira vez em muito tempo, alguém olhou pra mim como uma pessoa que sabia de algo e não só como um doente."
    $ mostrar_personagem("Lazaro", 'T')
    l "Mas esse sentimento veio com confusão, medo e culpa. Como se eu soubesse de mais e estivesse mascarando isso com febre e dor…"
    $ checar_interacao ()
    jump casaLazaroint

label salvatorefez_lazaro:
    $ mostrar_personagem("Lazaro", 'N')
    $ alterar_interacao(-1)
    l "Aquela moça…"
    l "Aquelas crianças nascidas…"
    $ adicionar_pista("Salvatore", "Tem algo a ver com uma moça e crianças nascidas pelo que o leproso disse.")
    
    menu:
        "Crianças? Que crianças?":
            jump criancas_lazaro
label criancas_lazaro:
    $ mostrar_personagem("Lazaro", 'T')
    l "Meu corpo dói ainda mais quando lembro disso…"
    l "Por favor, me deixe em paz…"
    $ checar_interacao ()
    jump casaLazaroint

label doenca_lazaro:
    $ mostrar_personagem("Lazaro", 'N')
    $ alterar_interacao(-1)
    l "Já nem conto mais... Parei depois do segundo ano."
    l "A doença chegou devagar... Primeiro nas mãos, depois no rosto... E agora parece que está afetando por dentro da minha cabeça."
    l "Às vezes me pergunto... se ela veio de fora… Ou se sempre esteve aqui, esperando eu parar de fingir que não tinha nada..."
    $ checar_interacao ()
    jump casaLazaroint

label ontem_lazaro:
    $ mostrar_personagem("Lazaro", 'N')
    $ alterar_interacao(-1)
    l "Eu... conversei com minha pele."
    l "Ela estava saindo de novo, então eu tentei convencê-la a ficar."
    l "Ouvi passos... muitos passos... Mas não vi ninguém."
    l "Só senti aquele cheiro doce… Me lembrou do leite queimado com ervas que minha mãe fazia quando eu era criança... Só que agora... esse cheiro me causa enjoo."
    $ adicionar_fala("Lázaro", "Só senti aquele cheiro doce… Me lembrou do leite queimado com ervas")
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Você realmente não viu nada?":
            jump naoviu
        "Você não tem nenhuma pista de quem poderia estar por perto?":
            jump naoviu

label naoviu:
    $ mostrar_personagem("Lazaro", 'N')
    l "..."
    l "Quando olhei pela fresta, achei que tivesse visto algo."
    l "Era como um vulto... parecia alguém de estatura pequena...Mas... estava sem sombra."
    $ adicionar_fala("Lázaro", "Parecia alguém de estatura pequena... Mas... estava sem sombra.")
    l "Tive medo... e fechei os olhos."
    $ checar_interacao ()
    jump casaLazaroint

############################################ CENAS HOLGA ###########################################################
label dialogo_holga:
    call hide_all_screens
    show screen holgaN
    h "eu sou holga"
    jump casaholgaext

########################################### CENAS PADEIRO ###########################################################
label dialogo_bartolomeu:
    call hide_all_screens
    $ mostrar_personagem("Bartolomeu", 'N')
    b "eu sou o padeiro"
    jump padaria

########################################### CENAS BEBADO ###############################################################
label dialogo_bebado:
    call hide_all_screens
    $ mostrar_personagem("Bebado", 'N')
    if personagens_dict["Bêbado"].conversouHoje == False:
        $ alterar_interacao(-1)
        if personagens_dict["Bêbado"].progresso == 0:
            be "Ela fala coisas no sono… Não aguentei cuidar dela por muito tempo..."
            $ adicionar_fala("Bêbado", "Ela fala coisas no sono… Não aguentei cuidar dela por muito tempo...")
        if personagens_dict["Bêbado"].progresso == 1:
            be "Não pode ser culpa dela não é?"
            be "Nem minha… era só não ter nascido."
            be "Uma tarefa simples… ela ainda estaria aqui se não fosse isso"
        if personagens_dict["Bêbado"].progresso == 2:
            be "A irmã da Catarina nunca mais veio sequer nos visitar…"
        if personagens_dict["Bêbado"].progresso == 3:
            be "Porque… porque deixou tudo para trás? Tudo que te fazia especial… E eu não pude dar a vida que ela merecia…"
        if personagens_dict["Bêbado"].progresso == 4:
            be "Uma aldeia doente, morrendo. Mas minha menina está pior. Febre… todo dia"
            $ adicionar_fala("Bêbado", "Minha menina está pior. Febre… todo dia")
        if personagens_dict["Bêbado"].progresso == 5:
            be "O mais importante ele diz."
            be "Cretino."
            be "Eu sei o que ele fez… eu sei! Eu… juro… sei"
            $ adicionar_fala("Bêbado", "Eu sei o que ele fez… eu sei! Eu… juro… sei")
        if personagens_dict["Bêbado"].progresso == 6:
            be "Ela me disse que o mal que caminha nesta aldeia não tem um rosto. Como se usasse outro no lugar…"
            $ adicionar_fala("Bêbado", "Ela me disse que o mal que caminha nesta aldeia não tem um rosto. Como se usasse outro no lugar…")
        $ progredir("Bêbado")
        $ checar_interacao()
    else:
        $ mostrar_personagem("Padre", 'N')
        p "Ele parece muito bêbado para conversar agora..."
    jump casabebadoext

######################################### CENAS AGNES ###########################################################  
label dialogo_agnes:
    call hide_all_screens
    $ mostrar_personagem("Agnes", 'N')
    a "eu sou a agnes"
    jump praca2

######################################### CENAS QUE OCORREM DURANTE A NOITE #######################################################

label casapadre_noite:
    call hide_all_screens
    play music "ambiencia_int_casas.wav"
    scene bg casa padre noite
    call screen casaPadreNOITE 
    return

label noite:
    call screen pistas

######################################### PISTAS ##################################################
label pistas:
    $ pistas_list = atualizar_pistas(infoPersonagem)
    $ falas_list = atualizar_falas(infoPersonagem)
    call hide_all_screens
    call screen pistas_personagem(infoPersonagem)
    