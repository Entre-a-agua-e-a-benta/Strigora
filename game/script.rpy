# The script of the game goes in this file.

# Define posicao de nome dos personagens
default name_side = "left"

default dia = 1 # Define dia incial
default interacao = 1 # Define quantas interações começa
default interacaoMaxHoje = 3 # Número max de interações no dia p/ HUD

default modificadorEvento = 0 # Modificador de chance para eventos aleatórios

default infoPersonagem = "" # Para o quadro de pistas
default matar_personagem = None # Personagem que será morto na noite -> deixar None
default numeroEvento = -1
default musica_atual = "ambiencia_ext_geral.mp3"
## Variaveis do diálogo com o Lázaro
default dor_lazaro = False
default afastou_lazaro = False
# Variáveis do dialogo com william
default naotinta_william = False
default sombrass_william = False

## Personagens
define personagens_list = list()
define personagens_dict = dict()
define pi = Character("Padre", what_italic=True, color="#FFFFFF") ## O PADRE QUANDO ESTÁ PENSANDO
define p =  Character("Padre", color="#522c36")
define v = Character("Dono do Albergo", color="#ddc0a4") ## DONO DA ESTALAGEM/TAVERNA
define s = Character("Filha do bêbado") ## CRIANÇA GEMEA FILHA DO BEBADO
define m = Character("Curandeira", color="#865662") ## Curandeira
define l = Character("Leproso", color="#aa3c2e") ## Leproso
define h = Character("Irmã da Edla", color="#51496d")
define b = Character("Padeiro", color="#874123") ## PADEIRO
define be = Character("Bêbado", color="#5a453b")
define ss = Character("Senhor da vila", color="#fed047") ## Senhor Salvatore
define j = Character("Costureira", color="#7f8c9b") ## Costureira
define a = Character("Pedinte") ## Criança pedinte
define w = Character("Filho do senhor") ## Criança William

define bx = Character("Bruxa")

define dev = Character("Strigora", color="#a88ab4")

define msg = Character("Mensageiro", color="#FFFFFF")
define hdc = Character("Homem da carta", color="#FFFFFF")
define no = Character(None, kind=nvl) 

define dis = {"master" : Dissolve(1.0)}

# The game starts here.

label start:
    $ _game_menu_screen = "help"
    init python:
        from unidecode import unidecode
        from random import randint

        class Personagem:
            def __init__(self, character=dev, nome = "Fulano", genero = 'M', fileira = (0, 0), ordem = 0, transform = personagem_right):
                self.character = character
                self.nomeConhecido = character.name

                self.nome = nome
                self.profissao = character.name
                self.genero = genero

                self.posicao = (fileira[0] + (175+75)*(ordem-1), fileira[1]) # 175 é a largura da imagem reduzida, 75 é o espaçamento entre elas

                self.transform = transform
                
                self.conversouHoje = False
                self.progresso = 0
                self.listaPistas = []
                self.listaFalas = []
                self.conhecido = False 
                self.conversavel = True
                self.vivo = True
                self.descricao = ""
                self.imagem = f"personagens/{unidecode(nome.lower())}/{unidecode(nome.lower())}.png"
                self.retrato = f"personagens/retrato/{unidecode(nome.lower())}_retrato.png"
                self.listaPerguntas = [False, False, False, False]

            def conhecer(self):
                self.character.name = self.nome
                self.nomeConhecido = self.nome
        
        ## Inicializa o dicionário de personagens
        primeira_fileira = (150, 450)
        segunda_fileira = (300, 815)
        personagens_list = [(b, "Bartolomeu", 'M', primeira_fileira, 3, personagem_right),
                            (ss, "Salvatore", 'M', primeira_fileira, 6, salvatore_right),
                            (h, "Holga", 'F', segunda_fileira, 1, holga_right),
                            (l, "Lázaro", 'M', primeira_fileira, 5, personagem_right),
                            (j, "Joana", 'F', segunda_fileira, 2, joana_right),
                            (m, "Margarida", 'F', primeira_fileira, 2, margarida_right),
                            (a, "Agnes", 'F', primeira_fileira, 4, crianca_right),
                            (be, "Bêbado", 'M', segunda_fileira, 5, personagem_right),
                            (w, "William", 'M', segunda_fileira, 4, crianca_right),
                            (v, "Vincent", 'M', primeira_fileira, 1, personagem_right),
                            (s, "Seren", 'F', segunda_fileira, 3, crianca_right),
                            (bx, "Bruxa", 'F', (0, 0), 1, bruxa_right)]

        eventos_list = ["Algum problema ocorreu",
                        "",
                        "Você não dormiu bem essa noite e se sente indisposto pra falar com as pessoas. (-1 interação)",
                        "Os animais da vila adoeceram... Parece ser um mal presságio. (chance maior de evento ruim na próxima noite)",
                        "Momento de paz temporária. Hoje a noite foi calma e agradável.",
                        "A Bruxa permaneceu inativa essa noite.",
                        "Você passou a noite inteira pensando no caso. Mas acordou satisfatóriamente descansado.",
                        "Houve uma missa comunitária de madrugada. Hoje será um dia promissor! (+2 interação)",
                        "Você dormiu muito bem hoje e se sente descansado para falar com as pessoas. (+1 interação)",
                        "Os aldeões se jundaram para uma janta comunitária, com certeza essa união trará mais sorte pra você. (+ chance de evento bom na próxima noite)"]
        
        def checar_interacao():
            global interacao
            if interacao <= 0:
                renpy.jump("casapadre")

        def alterar_interacao(valor: int):
            global interacao
            interacao = interacao + valor
            sinal = "+" if valor >= 0 else ""
            #renpy.notify(sinal + str(valor) + " interação")

        def passar_dia():
            global dia, interacao, interacaoMaxHoje, personagens_list, personagens_dict, matar_personagem, modificadorEvento
            dia = dia + 1
            mortos = 0
            for personagem in personagens_list:
                personagens_dict[personagem[1]].conversouHoje = False
                personagens_dict[personagem[1]].conversavel = True
                if personagens_dict[personagem[1]].vivo == False:
                    mortos = mortos + 1
            interacao = 3
            interacaoMaxHoje = 3
            if matar_personagem != None:
                personagens_dict[matar_personagem].vivo = False
                mortos = contarMortos()
                if matar_personagem == "William":
                    renpy.jump("dialogo_bruxa")
                if mortos == 1:
                    renpy.jump("morte1")
                if mortos == 2:
                    renpy.jump("morte2")
                if mortos >= 3 and dia <= 7: # Matou 3 pessoas antes do último dia
                    renpy.jump("expulso")
            if dia == 7:
                renpy.say(pi, "Hoje é o último dia... Preciso exorcizar a Bruxa.")
            elif dia >= 8:
                renpy.jump("final")
            evento_aleatorio()
            modificadorEvento = 0
            renpy.jump("casapadre")

        def evento_aleatorio():
            global modificadorEvento, numeroEvento
            # Chance para cada evento (Ruim, Neutro, Bom)
            if modificadorEvento == 1: # Dia de sorte
                chanceEventos = (10, 40, 50)
            elif modificadorEvento == 0: # Dia normal
                chanceEventos = (25, 50, 25)
            elif modificadorEvento == -1: # Dia de azar
                chanceEventos = (50, 40, 10)
            ## renpy.notify(f"chance atual de evento: {chanceEventos[0]}/{chanceEventos[1]}/{chanceEventos[2]}") # DEBUG, APAGAR!!!

            tipoEvento = randint(1, 100) # numero entre 1 e 100
            if tipoEvento <= chanceEventos[0]:  # Evento Ruim
                numeroEvento = randint(1, 3)
                renpy.call_in_new_context("eventos")
            elif tipoEvento <= chanceEventos[0] + chanceEventos[1]:  # Evento Neutro
                numeroEvento = randint(4, 6)
                renpy.call_in_new_context("eventos")
            elif tipoEvento > 100 - chanceEventos[2]:
                numeroEvento = randint(7, 9)
                renpy.call_in_new_context("eventos")
        
        # Progride o diálogo de um personagem específico, aumentando seu progresso em 1 e marcando que já conversou hoje.
        def progredir(personagem: str):
            global personagens_dict
            personagens_dict[personagem].conversouHoje = True
            personagens_dict[personagem].progresso += 1

        def contarMortos():
            global personagens_list, personagens_dict
            mortos = 0
            for personagem in personagens_list:
                if personagens_dict[personagem[1]].vivo == False:
                    mortos += 1
            return mortos

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
                personagens_dict[personagem].listaPistas.append("- " + pista)
                renpy.play("notify.mp3", relative_volume=1.67)
                renpy.call_screen("notificacao", "Pista Adquirida!", personagens_dict[personagem].nomeConhecido + " " + pista[0].lower() + pista[1:])
                # renpy.notify("Pista adquirida: " + personagens_dict[personagem].nomeConhecido + " " + pista[0].lower() + pista[1:])
 
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
                personagens_dict[personagem].listaFalas.append("- " + fala)
                renpy.play("notify.mp3", relative_volume=1.67)
                renpy.notify("Falas de " + personagens_dict[personagem].nomeConhecido + ": " + fala)
        
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
            renpy.show_screen("personagemEmocao", personagem, emocao)

        def mostrar_botao(posicao: tuple, texto: str, jumpTo: str):
            renpy.show_screen("botao_passos", posicao, texto, jumpTo)

        def tocar_musica(musica: str):
            global musica_atual
            if musica != musica_atual:
                renpy.music.play(musica)
                musica_atual = musica

        def texto_grande(texto: str, tempoDePause=10):
            renpy.show_screen("textogrande", texto)
            renpy.pause(tempoDePause)
        


#### $ adicionar_pista("Vincent", "Gosta de HOMENS") #### é assim que bota pista

########################################## AQUI COMEÇA O JOGO ##############################################################    

label primeiracena:
    python:
        for personagem in personagens_list:
            personagens_dict[personagem[1]] = Personagem(personagem[0], personagem[1], personagem[2], personagem[3], personagem[4], personagem[5])
            #personagens_dict[personagem[1]].conhecido = True # DEBUG, TIRAR

        personagens_dict["Bruxa"].conhecido = True
        personagens_dict["Bruxa"].posicao = (1720, 760)

        personagens_dict["Bartolomeu"].descricao = "O dono da padaria. Gosta de tirar proveito das situações, e se considera humilde por dar, vez ou outra, um pão amanhecido a uma criança necessitada."
        personagens_dict["Salvatore"].descricao = "O senhor da vila. Ele é pai solteiro, estava apaixonado e planejava se casar com Edla. Foi quem me chamou para vir ajudá-los."
        personagens_dict["Holga"].descricao = "É a irmã mais velha da vítima mais recente, Edla. Ela se descreve como a \"sombra\" da irmã, que era vista como a mais bela e luminosa."
        personagens_dict["Lázaro"].descricao = "Mora na parte mais vazia da aldeia, pois as pessoas têm medo de contatá-lo e acreditam que sua doença é uma praga jogada pela bruxa."
        personagens_dict["Joana"].descricao = "A costureira. Ela ganha a vida fazendo e consertando roupas, e está sempre com uma agulha presa no coque."
        personagens_dict["Margarida"].descricao = "A curandeira e contadora de histórias. É vista frequentemente colhendo plantas medicinais e fazendo rezas."
        personagens_dict["Agnes"].descricao = "É uma criança que deve ter por volta dos 12 anos, mora nas ruas."
        personagens_dict["Bêbado"].descricao = " É o irmão do dono da estalagem e pai de uma menina de 10 anos. Desde a morte da esposa, ele vive bêbado pelos cantos da aldeia, sempre bebendo algo e falando coisas confusas e sem nexo."
        personagens_dict["William"].descricao = "É uma criança de 10 anos. Ele é o filho do Senhor Salvatore e raramente é autorizado a sair de casa."
        personagens_dict["Vincent"].descricao = " É o responsável pela estalagem e taverna, que se chama \"A viúva sangrenta\"."
        personagens_dict["Seren"].descricao = "Tem cerca de 10 anos. Ela acredita ser culpada pela morte de sua mãe e se sente difícil de ser enxergada pelo pai. Seu tio, Vincent, é quem cuida dela."
        personagens_dict["Bruxa"].descricao = "A bruxa que está devastando a vila."

    jump tavernaint

    $ renpy.movie_cutscene("images/cutscene_inicial.webm")

    $ personagens_dict["Salvatore"].conhecido = True
    $ tocar_musica("tema.mp3")
    scene bg caminho curandeira
    $ mostrar_personagem("Salvatore", 'F')
    ss "Buongiorno padre."
    ss "Agradeço por ter aceitado o meu chamado."
    $ mostrar_personagem("Salvatore", 'N')
    ss "Meu nome é Salvatore."
    $ personagens_dict["Salvatore"].conhecer()
    ss "O povo da vila se refere a mim como \“Senhor”\, por respeito… ou medo. Tanto faz."
    ss "Sou o homem mais velho desta terra que ainda consegue caminhar com firmeza. Sempre tentei manter tudo sob controle, como deve ser."
    ss "Por isso lhe chamei. Se há uma bruxa entre nós… é seu dever encontrá-la."
    ss "Eu não quero rezas ou  palavras bonitas. Quero respostas. E, finalmente, silêncio."
    $ mostrar_personagem("Salvatore", 'R')
    ss "Quando o povo começa a berrar antes da hora, ninguém ouve quem realmente deveria ser escutado."
    $ mostrar_personagem("Salvatore", 'N')
    ss "Ouça padre."
    $ mostrar_personagem("Salvatore", 'T')
    ss "Edla, a vítima mais recente, era irmã de Holga, uma mulher jovem que mora nos entornos da Piazza."
    $ personagens_dict["Holga"].conhecer()
    ss "Nós éramos... bem próximos."
    ss "Na noite de sua morte, ouvi sua voz distorcida me falando que em sete dias a bruxa matará a todos nós."
    ss "Por favor, faça algo antes que seja tarde."
    show screen HUD
    jump caminhobebado_margarida


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
    $ tocar_musica("ambiencia_int_casas.wav")
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
    if interacao <= 0:
        scene tela preta 
        with dis
        pause 0.7
        scene bg casa padre int
        with dis
        python:
            if dia == 7:
                renpy.say(pi, "Chegou o fim do último dia...")
                renpy.say(pi, "Esta é minha última chance de exorcizar a Bruxa.")
            else:
                mortos = contarMortos()
                if mortos == 0:
                    renpy.say(pi, "O dia chegou ao fim...")
                    renpy.say(pi, "Vou ver o quadro na parede para revisar minhas anotações de hoje.")
                    renpy.say(pi, "Tenho que estar atento às pistas para não matar inocentes.")
                if mortos == 1:
                    renpy.say(pi, "Devo tomar mais cuidado, já matei 1 inocente. Uma hora a vila não vai mais me perdoar.")
                if mortos == 2:
                    renpy.say(pi, "Se eu matar mais alguém, tenho certeza que a vila não me perdoará.")
       
    scene bg casa padre noite
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

label casasalvatoreint:
    call hide_all_screens
    $ tocar_musica("ambiencia_int_casas.mp3")
    scene bg casa salvatore
    call screen casaSalvatoreINT

############# Arruma posição dos personagens dentro do dialogo ###############################


######################################## CENAS QUE OCORREM NA TAVERNA #######################################################

## Dialogo com o Vincent ao clicar no personagem
label dialogo_vincent:
    call hide_all_screens
    if personagens_dict["Vincent"].conversavel:
        if personagens_dict["Seren"].vivo == False:
            $ mostrar_personagem("Vincent", 'T')
            v "Ela era uma boa garota padre..."
            v "A Seren... Era como uma filha pra mim..."
            v "Não me perturbe mais."
            jump tavernaint
        elif personagens_dict["Bêbado"].vivo == False:
            $ mostrar_personagem("Vincent", 'T')
            v "Meu irmão podia viver bêbado pela cidade ou até mesmo não cuidar tão bem da filha dele."
            v "Mas ele não era assassino, padre."
            v "Ele era alguém muito melhor do que você..."
            jump tavernaint
        elif personagens_dict["Lázaro"].vivo == False:
            $ mostrar_personagem("Vincent", 'T')
            v "Eu culpava ele sem mesmo saber seu nome..."
            v "Falava que ele fazia coisas más por sua doença infeliz..."
            v "Preciso de um tempo pra refletir sobre minhas opiniões..."
            jump tavernaint
        elif personagens_dict["Vincent"].conhecido == False: # Primeiro diálogo com Vincent
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
        
        # "Passar dia":
        #     $ passar_dia()
        #     jump noite

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
    $ adicionar_pista("Lázaro", "É acusado por Vincent pois: \"O homem que mora quase fora da aldeia tem o corpo ferido, com certeza não fez coisa boa e foi castigado por Deus. O silêncio dele pesa\".")
    $ checar_interacao()
    jump tavernaint

label meconte_vincent:
    #diminui interação do jogador
    $ alterar_interacao(-1)
    $ mostrar_personagem("Vincent", "N")
    v "Bom… Eu sou o Vincent, cuido da taverna e da estalagem… Ou o que sobrou dela, parece que a aldeia resolveu que o medo é desculpa para parar de beber."
    $ personagens_dict["Vincent"].conhecer()
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
    v "Ah, com certeza você vai vê-lo por aí… Ele está sempre pelos cantos da aldeia. Ele vem aqui, bebe sem pagar, mas não tenho coragem de cobrar."
    $ mostrar_personagem("Vincent", 'T')
    v "Depois que a mulher dele se foi, sobrou pouco dele também."
    $ checar_interacao()
    jump tavernaint

label esposa_vincent:
    $ alterar_interacao(-1)
    $ mostrar_personagem("Vincent", 'T')
    v "Ela estava grávida… Foi um parto difícil, apenas ela e a parteira dentro do quarto…"
    v "Infelizmente ela não resistiu, mas deu a luz a uma garotinha… Isso faz 10 anos."
    $ adicionar_pista("Bêbado", "Teve uma esposa que morreu no parto da filha.")
    v "Desde então ele vive nesse estado… Conspirando e dizendo que há culpados pela morte da esposa."
    $ adicionar_pista("Bêbado", "Culpa alguém pela morte da esposa.")
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
    v "Mas de um tempo para cá, ela parece doente. Ás vezes, fala coisa dormindo e acorda com febre alta. Eu tento ser como um pai para ela, mas mesmo assim acho que às vezes não sou o suficiente."
    $ adicionar_pista("Seren", "Parece doente, às vezes, fala coisa dormindo e acorda com febre alta.")
    v "Pedirei para ela falar com o senhor."
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
    $ adicionar_fala("Vincent", "Acusa o antigo padre de \"sumir e quando encontraram, não era mais um homem. Era só um corpo... vazio.\"")
    $ mostrar_personagem("Padre", 'R')
    menu:
        "Ficar em silêncio":
            $ checar_interacao()
            jump tavernaint
        "Diferente ou não, não vim aqui rezar pelos mortos. Vim para entender porque  estão morrendo.":
            $ checar_interacao()
            jump tavernaint
        "Se sou diferente? Bem, ainda estou vivo, não estou?":
            $ checar_interacao()
            jump tavernaint
        "Espero que sim. Espero que minha fé seja suficiente para me manter de pé… e talvez salvar quem ainda resta.":
            $ checar_interacao()
            jump tavernaint


######################################## CENAS SEREN #######################################################
label dialogo_seren:
    call hide_all_screens
    if personagens_dict["Seren"].conversavel:
        if personagens_dict["Vincent"].vivo == False:
            $ mostrar_personagem("Seren", 'T')
            s "O tio..."
            s "O tio me deixava ficar atrás do balcão quando chovia..."
            s "Eu amava o pão com mel que ele me dava pra comer..."
            s "Por quê padre? Por quê você tirou ele de mim..."
            jump tavernaint
        elif personagens_dict["Bêbado"].vivo == False:
            $ mostrar_personagem("Seren", 'T')
            s "Meu pai nunca mais vai poder olhar triste pra mim quando pensa que eu não to vendo..."
            s "E eu também nunca vou conseguir alcançar o perdão dele..."
            jump tavernaint
        elif personagens_dict["Seren"].conhecido == False:
            $ personagens_dict["Seren"].conhecido = True
            $ mostrar_personagem("Padre", 'N')
            p "Buongiorno, pequena. Deus lhe abençoe, eu gostaria de conversar um pouco com você."
        jump escolhas_seren   
    else:
        $ mostrar_personagem("Seren", 'T')
        s "Não estou com vontade de conversar hoje..."
        jump tavernaint 

label escolhas_seren:
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Me conte sobre você." if personagens_dict["Seren"].conversouHoje == False and personagens_dict["Seren"].progresso == 0:
            $ progredir("Seren")
            jump meconte_seren
        "Vejo que algo te incomoda. O que é?"if personagens_dict["Seren"].conversouHoje == False and personagens_dict["Seren"].progresso == 1:
            $ progredir("Seren")
            jump incomoda_seren
        "Onde e o que você fez ontem a noite?" if personagens_dict["Seren"].listaPerguntas[0] == False:
            $ personagens_dict["Seren"].listaPerguntas[0] = True
            jump ontem_seren
        "Algum habitante te parece estranho?" if personagens_dict["Seren"].listaPerguntas[1] == False:
            $ personagens_dict["Seren"].listaPerguntas[1] = True
            jump habitante_seren
        "Não perguntar nada":
            jump tavernaint
    return

label meconte_seren:
    $ alterar_interacao(-1)
    $ mostrar_personagem("Seren", 'N')
    s "Eu sou a Seren. Tenho dez anos…"
    $ personagens_dict["Seren"].conhecer()
    s "Meu pai mora aqui na aldeia também… Às vezes ele passa por aqui, mas não fica muito."
    $ mostrar_personagem("Seren", 'T')
    s "Ele não gosta que eu fale com estranhos."
    $ mostrar_personagem("Seren", 'F')
    s "Mas o tio disse que você é diferente. Então eu posso responder…"
    $ checar_interacao()
    jump tavernaint

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
    $ adicionar_fala("Seren", "Ás vezes acontecem coisas estranhas a noite… Não é todo sonho que dói. Só os que parecem verdade.")
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Vcê tem tido sonhos estranhos?":
            jump sonhos_seren
        "Como são esses sonhos?":
            jump sonhos_seren
label sonhos_seren:
    $ mostrar_personagem("Seren", 'N')
    s "No começo, eu só via silhuetas. Um campo, uma árvore sozinha, uma sombra me seguindo de longe. Depois vieram os sussurros. E agora, agora… Agora eu vejo tudo…"
    $ adicionar_pista("Seren", "Sonhava vendo silhuetas ou sombras a seguindo e agora \"vê tudo\".")
    s "No sonho, ando pelas ruas da aldeia com passos que não são meus… As mãos... as mãos que estendo são pequenas, como as minhas. Mas elas brilham. Como brasa acesa no escuro. E quando tocam algo, tudo escurece..."
    $ mostrar_personagem("Seren", 'T')
    s "E o que mais me assusta: há uma voz dentro de mim. Mas ela não fala comigo. Ela me usa… "
    $ adicionar_pista("Seren", "No sonho, \"anda pelas ruas da aldeia com passos que não são seus e mãos que brilham como brasa acesa no escuro\" e há uma voz dentro dela que não fala com ela, mas a usa.")
    s "Mas o pior é quando vejo ele… o menino com voz de mulher… Ele fala, mas a boca não mexe… Ele parece viver numa tristeza que me queima..."
    $ adicionar_fala("Seren", "\"Mas o pior é quando vejo ele… o menino com voz de mulher… Ele fala, mas a boca não mexe… Ele parece viver numa tristeza que me queima...\".")
    s "Quando acordo, a pele está quente como se eu tivesse corrido por horas. A febre queima atrás dos olhos, e minha garganta parece de vidro."
    $ mostrar_personagem("Seren", 'N')
    s "O tio diz que é só vento, ou comida estragada."
    $ mostrar_personagem("Seren", 'T')
    s "Mas toda vez que eu sonho, algo na aldeia amanhece errado. Eu queria contar, gritar... Dizer o que vejo… Mas quem vai acreditar numa menina que até o próprio pai não quis segurar no colo?"
    $ adicionar_pista("Seren", "Sente que toda vez que sonha, algo na aldeia amanhece errado.")
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Com o que você sonhou ontem?":
            jump sonhoontem_seren
        "Qual foi o seu sonho mais recente?":
            jump sonhoontem_seren
label sonhoontem_seren:
    $ mostrar_personagem("Seren", 'N')
    s "Ontem… ontem no sonho eu estava em frente ao espelho de uma casa grande, e o menino estava dentro do espelho me olhando de volta. Só que, por um instante, os olhos dele eram os meus…"
    $ adicionar_fala("Seren", "\"O menino estava dentro do espelho me olhando de volta. Só que, por um instante, os olhos dele eram os meus…\".")
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Conte mais sobre esse menino do sonho":
            jump menino_seren
label menino_seren:
    $ mostrar_personagem("Seren", 'N')
    s "Ele parece triste… Sempre me olha de um jeito estranho, como se me conhecesse"
    $ adicionar_fala("Seren", "O menino do sonho \"Sempre me olha de um jeito estranho, como se me conhecesse\".")
    s "Uma vez eu vi meu rosto no lugar do dele. Mas eu sei que não era eu… Eu estava olhando pra mim, mas eu era outra pessoa. Não sei explicar…"
    $ adicionar_fala("Seren", "\"Uma vez eu vi meu rosto no lugar do \"menino do sonho\". Mas eu sei que não era eu… Eu estava olhando pra mim, mas eu era outra pessoa.\".")
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
    $ adicionar_pista("Margarida", "Olha pras pessoas como se lesse o que tem dentro.")
    $ mostrar_personagem("Seren", 'R')
    s "Um dia ela olhou pra mim, encostou a mão na minha testa e disse: \"Nem todo espelho mostra só o que é de fora\". Eu não entendi, mas me deu um arrepio."
    $ adicionar_pista("Margarida", "Disse \"Nem todo espelho mostra só o que é de fora\" para Seren.")
    $ adicionar_pista("Seren", "Escutou Margarida dizendo pra ela \"Nem todo espelho mostra só o que é de fora\".")
    $ checar_interacao()
    jump tavernaint

######################################## CENAS QUE OCORREM NA CASA DA MARGARIDA #######################################################
label dialogo_margarida:
    call hide_all_screens
    if personagens_dict["Margarida"].conversavel:
        if personagens_dict["Agnes"].vivo == False:
            $ mostrar_personagem("Margarida", 'T')
            m "Pobre garota..."
            m "Rejeitada por toda vila, vivia sem ter onde comer e dormir."
            m "Enfim encontrou o descanso eterno... Assim como seus pais."
            m "Que Deus a tenha, padre."
            m "E que Ele te perdoe por esse fim trágico que o senhor deu a ela."
            jump casamargaridaext  
        elif personagens_dict["Margarida"].conhecido == False:
            $ personagens_dict["Margarida"].conhecido = True
            $ mostrar_personagem("Padre", 'N')
            p "Buongio..."
            $ mostrar_personagem("Margarida", 'N')
            m "A benção, padre."
            m "Veio aqui procurar um motivo para jogar a culpa em mim?"
            $ mostrar_personagem("Padre", 'R')
            p "Não, claro que não. Estou apenas investigando… "
            $ mostrar_personagem("Padre", 'N')
            p "Por favor, fale comigo."
        jump escolhas_margarida
    else:
        $ mostrar_personagem("Margarida", 'T')
        s "Não estou com vontade de conversar hoje..."
        jump casamargaridaext 

label escolhas_margarida:
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Me conte sobre você" if personagens_dict["Margarida"].listaPerguntas[0] == False:
            $ personagens_dict["Margarida"].listaPerguntas[0] = True
            jump meconte_margarida
        "Onde e o que você fez ontem a noite?" if personagens_dict["Margarida"].listaPerguntas[1] == False:
            $ personagens_dict["Margarida"].listaPerguntas[1] = True
            jump ontem_margarida
        "Me conte uma história" if personagens_dict["Margarida"].listaPerguntas[2] == False:
            $ personagens_dict["Margarida"].listaPerguntas[2] = True
            jump historia_margarida
        "Viu algo de estranho ultimamente?" if personagens_dict["Margarida"].listaPerguntas[3] == False:
            $ personagens_dict["Margarida"].listaPerguntas[3] = True
            jump estranho_margarida
        "Não perguntar nada":
            jump casamargaridaext

label meconte_margarida:
    $ mostrar_personagem("Margarida", 'N')
    $ alterar_interacao(-1)
    m "Contar? o que? Porque faria isso? Já sei o que pensa. Sei o que todos pensam… "
    $ mostrar_personagem("Margarida", 'R')
    m "Uma mulher sozinha , que mexe com o que não entendem, e já afiam a corda, já juntam lenha…"
    m "Ignorantes…"
    m "Eles me chamam de contadora de histórias, como se eu fosse apenas isso."
    m "Eu tenho nome, me chamo Margarida."
    $ personagens_dict["Margarida"].conhecer()
    m "Eles não se lembram das pessoas que salvei. Já vi mais gente morrer do que você viu nascer. Sei quando a terra adoece, quando o vento muda de cheiro, quando a mão treme antes mesmo de tocar na porta."
    $ adicionar_pista("Margarida", "Fala que ela mesma \"Sabe quando a terra adoece, quando o vento muda de cheiro, quando a mão treme antes mesmo de tocar na porta.\".")
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
    $ adicionar_fala("Margarida", "Conta uma história de uma mulher que vivia na mata e encontrou dois bebês iguais como um espelho.")
    m "Mas um tinha os olhos fechados e sorria dormindo. O outro tinha os olhos abertos… e não piscava… A mulher, sozinha no mundo, mesmo sabendo que não era seu,  levou um deles nos braços."
    $ adicionar_fala("Margarida", "Em sua história \"Um tinha os olhos fechados e sorria o outro tinha olhos abertos e não piscava\" e a mulher \"levou um deles nos braços\".")
    m "Disse: \"É um sinal… O destino me escolheu.\"  Alimentou… deu nome… cobriu de orações. O outro bebê?… ficou. Nunca chorou. Nunca morreu. Só… ficou. Esperando."
    $ adicionar_fala("Margarida", "A mulher da história cuidou do bebê que levou, enquanto o outro \"Nunca chorou nem morreu. Só… ficou esperando.\".")
    m "Um dia… a criança levada perguntou: \"Quem é meu pai?\" E ela respondeu: \"Um homem… que não tem nome… e que não pode ser acordado.\"."
    m "Desde então… dizem… a corça de três olhos ronda a aldeia… procurando seu parente perdido. E a criança… ah… ela ainda vive entre nós… Só não sabe… quem… é."
    $ adicionar_fala("Margarida", "Desde sua história \"A corça de três olhos ronda a aldeia… procurando seu parente perdido. E a criança… ah… ela ainda vive entre nós… Só não sabe… quem… é.\"")
    $ checar_interacao()
    jump casamargaridaext

label estranho_margarida:
    $ mostrar_personagem("Margarida", 'R')
    $ alterar_interacao(-1)
    m "Estranho? Hmph. Estranho é o dia nascer limpo e morrer podre. Estranho é bicho fugir antes mesmo de ouvir passo."
    $ mostrar_personagem("Margarida", 'N')
    m "Mas se quer algo concreto… ontem encontrei um rastro de cheiro doce na trilha norte."
    m "Como açúcar… açúcar caro."
    m "Não era de criança brincando, posso garantir. E não é a primeira vez que esse cheiro aparece depois de um corpo cair doente."
    $ adicionar_pista("Bruxa", "Tem cheiro doce como açúcar caro")
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Doce? Como assim?":
            jump doce_margarida
label doce_margarida:
    $ mostrar_personagem("Margarida", 'N')
    m "Alguns venenos... enganam o nariz. Doces demais. "
    m "A língua acha gostoso, o corpo… não."
    m "Eu diria para ter cuidado com comida que lhe oferecerem, padre. Especialmente vindo de gente que sorri rápido demais."
    $ adicionar_fala("Margarida", "Eu diria para ter cuidado com comida que lhe oferecerem, padre. Especialmente vindo de gente que sorri rápido demais.")
    m "O doce mata mais suavemente que a lâmina"
    $ checar_interacao()
    jump casamargaridaext

######################################## CENAS QUE OCORREM NA CASA DO Lázaro #######################################################
label dialogo_lazaro:
    call hide_all_screens
    if personagens_dict["Lázaro"].conversavel:
        if personagens_dict["Lázaro"].conhecido == False:
            $ personagens_dict["Lázaro"].conhecido = True
            $ mostrar_personagem("Padre", 'N')
            p "Buongiorno…"
            p "Não sei a notícia chegou aqui, mas eu estou encarregado de achar o culpado pelas coisas que vem acontecendo na região, pensei que, mesmo doente, você talvez tivesse alguma informação para contribuir... ou, qo menos, algo interessante a dizer."
        jump escolhas_lazaro
    else:
        $ mostrar_personagem("Lázaro", 'T')
        s "Não estou com vontade de conversar hoje..."
        jump casaLazaroint 

label escolhas_lazaro:
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Me conte sobre você" if personagens_dict["Lázaro"].conversouHoje == False and personagens_dict["Lázaro"].progresso == 0:
            $ progredir("Lázaro")
            jump meconte_lazaro
        "O que o Salvatore fez?" if personagens_dict["Lázaro"].conversouHoje == False and personagens_dict["Lázaro"].progresso == 1 and dia >= 2:
            $ progredir("Lázaro")
            jump salvatorefez_lazaro

        "Há quanto tempo está doente?" if personagens_dict["Lázaro"].listaPerguntas[1] == False:
            $ personagens_dict["Lázaro"].listaPerguntas[1] = True
            jump doenca_lazaro
        "O que você fez ontem a noite?" if personagens_dict["Lázaro"].listaPerguntas[2] == False:
            $ personagens_dict["Lázaro"].listaPerguntas[2] = True
            jump ontem_lazaro

        "Não perguntar nada":
                jump casaLazaroint

label meconte_lazaro:
    $ mostrar_personagem("Lázaro", 'N')
    $ alterar_interacao(-1)
    l "Pode chegar mais perto…"
    l "O povo da vila me chama de leproso, ou só me conhecem como o cara estranho que mora quase fora da aldeia."
    l "Mas eu gostaria que você, padre, me chamasse pelo meu nome, Lázaro"
    $ personagens_dict["Lázaro"].conhecer()
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
    $ mostrar_personagem("Lázaro", 'T')
    l "Eu sei que a verdade é outra. Fui esquecido por Deus…"
    $ mostrar_personagem("Padre", 'R')
    menu:
        "Dizer que foi esquecido por Deus é fácil quando o mundo inteiro vira o rosto. Mas será que foi Deus quem se afastou de você… ou foi você quem se escondeu afastou e se escondeu dele?":
            jump afastou_lazaro

        "Às vezes, eu também me pergunto se Ele nos ouve... ou se apenas observa. Mas me diga… quando foi a última vez que sentiu algo que não fosse dor?":
            jump dor_lazaro       
label afastou_lazaro:
    $ afastou_lazaro = True
    $ mostrar_personagem("Lázaro", 'F')
    l "Procurei, sim. Por anos. Rezei até a garganta secar. E tudo o que ouvi foi o som da minha pele caindo."
    $ mostrar_personagem("Lázaro", 'R')
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
    $ mostrar_personagem("Lázaro", 'N')
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
    $ mostrar_personagem("Lázaro", 'F')
    l "Um calor estranho… Não fisico, mas emocional."
    l "Pela primeira vez em muito tempo, alguém olhou pra mim como uma pessoa que sabia de algo e não só como um doente."
    $ mostrar_personagem("Lázaro", 'T')
    l "Mas esse sentimento veio com confusão, medo e culpa. Como se eu soubesse de mais e estivesse mascarando isso com febre e dor…"
    $ checar_interacao()
    jump casaLazaroint

label salvatorefez_lazaro:
    $ mostrar_personagem("Lázaro", 'N')
    $ alterar_interacao(-1)
    l "Aquela moça…"
    l "Aquelas crianças nascidas…"
    $ adicionar_pista("Salvatore", "Tem algo a ver com uma moça e crianças nascidas pelo que o leproso disse.")
    $ mostrar_personagem("Padre", "N")
    menu:
        "Crianças? Que crianças?":
            jump criancas_lazaro
label criancas_lazaro:
    $ mostrar_personagem("Lázaro", 'T')
    l "Meu corpo dói ainda mais quando lembro disso…"
    l "Por favor, me deixe em paz…"
    $ checar_interacao()
    jump casaLazaroint

label doenca_lazaro:
    $ mostrar_personagem("Lázaro", 'N')
    $ alterar_interacao(-1)
    l "Já nem conto mais... Parei depois do segundo ano."
    l "A doença chegou devagar... Primeiro nas mãos, depois no rosto... E agora parece que está afetando por dentro da minha cabeça."
    l "Às vezes me pergunto... se ela veio de fora… Ou se sempre esteve aqui, esperando eu parar de fingir que não tinha nada..."
    $ checar_interacao()
    jump casaLazaroint

label ontem_lazaro:
    $ mostrar_personagem("Lázaro", 'N')
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
    $ mostrar_personagem("Lázaro", 'N')
    l "..."
    l "Quando olhei pela fresta, achei que tivesse visto algo."
    l "Era como um vulto... parecia alguém de estatura pequena...Mas... estava sem sombra."
    $ adicionar_fala("Lázaro", "Um vulto que parecia alguém de estatura pequena e sem sombra")
    l "Tive medo... e fechei os olhos."
    $ checar_interacao()
    jump casaLazaroint

############################################ CENAS HOLGA ###########################################################
label dialogo_holga:
    call hide_all_screens
    if personagens_dict["Holga"].conversavel:
        if personagens_dict["Salvatore"].vivo == False:
            $ mostrar_personagem("Holga", 'T')
            h "Ele sempre teve olhos pra ela..."
            h "Ele nunca conversou muito comigo. A irmã sombra de olhos fundos e mãos ásperas..."
            h "Mas foi o Salvatore que te chamou pra essa vila, padre."
            h "Por quê o senhor duvidou dele?"
            h "Ele que cuidava de todos e mantinha a ordem nessa vila, que Deus nos proteja agora. Sem ninguém pra nos acudir..."
            jump casaholgaext
        elif personagens_dict["Holga"].conhecido == False:
            $ personagens_dict["Holga"].conhecido = True
            $ mostrar_personagem("Padre", 'N')
            p "Buongiorno"
            p "Holga, lamento sua perda, que Deus a tenha. Vou fazer de tudo para pegar a pessoa culpada pela morte de sua irmã."
            p "Me ajude, qualquer pista ou evidência é essencial!"
        jump escolhas_holga
    else:
        $ mostrar_personagem("Holga", 'T')
        s "Não estou com vontade de conversar hoje..."
        jump casaholgaext

label escolhas_holga:
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Me conte sobre sua irmã" if personagens_dict["Holga"].conversouHoje == False and personagens_dict["Holga"].progresso == 0:
            $ progredir("Holga")
            jump irma_holga
        "Sua irmã e o senhor da vila tinham um caso?" if personagens_dict["Holga"].conversouHoje == False and personagens_dict["Holga"].progresso == 1:
            $ progredir("Holga")
            jump caso_holga
        "Boatos dizem que você viu essa tal bruxa, me fale mais sobre isso" if personagens_dict["Holga"].conversouHoje == False and personagens_dict["Holga"].progresso == 2:
            $ progredir("Holga")
            jump viubruxa_holga
        "O que você fez ontem a noite?" if personagens_dict["Lázaro"].listaPerguntas[0] == False:
            $ personagens_dict["Lázaro"].listaPerguntas[0] = True
            jump ontem_holga
        "Não perguntar nada":
            jump casaholgaext

label irma_holga:
    $ alterar_interacao(-1)
    $ mostrar_personagem("Holga", 'T')
    h "Edla…"
    h "Ela era bela.  A filha que todos diziam ter sido tocada pela luz de Deus."
    $ mostrar_personagem("Holga", 'R')
    h "Aquelas bochechas coradas… a voz doce…  Os homens caíam aos seus pés como trigo maduro na colheita."
    $ mostrar_personagem("Padre", 'T')
    menu:
        "Algo que te incomoda?":
            jump sombra_holga
        "Por que essa cara Holga? Algo aconteceu?":
            jump sombra_holga
label sombra_holga:
    $ mostrar_personagem("Holga", 'R')
    h "Bem… Eu  sempre fui a sombra."
    h "A irmã mais velha de mãos ásperas e olhos fundos, aquela que lavava as roupas…"
    h "Enquanto isso, ela dançava nos festivais despreocupada."
    $ adicionar_pista("Holga", 'Tinha raiva da irmã')
    h "Não é à toa que ela conquistou o coração do nosso senhor."
    $ mostrar_personagem("Padre", 'T')
    menu:
        "Ficar em silêncio e deixar Holga continuar":
            jump continuacao_holga
        "Então você tem raiva dela?":
            jump continuacao_holga
label continuacao_holga:
    $ mostrar_personagem("Holga", 'T')
    h "Mas então, ela morreu na floresta.  Sumiu. Sobraram apenas uns fiapos do vestido na beira do brejo..."
    h "E os galhos… quebrados, como se algo a tivesse arrastado para dentro da mata."
    h "Há quem diga que foi a bruxa"
    h "Tudo o que ouvi foi a sua voz chamando por ajuda… mas… em uma língua… que não era a dela."
    $ adicionar_pista("Bruxa", 'Fala e faz as vitimas falarem em uma língua estranha')
    h "Os velhos dizem que foi castigo… Os jovens, murmuram que foi inveja..."
    h "Desde então sinto sua falta todos os dias."
    $ checar_interacao()
    jump casaholgaext

label caso_holga:
    $ alterar_interacao(-1)
    $ mostrar_personagem("Holga", 'F')
    h "Acho que ele a amava…"
    h "Ela havia me contato que ele em breve pediria sua mão em casamento e que iria se mudar para morar com ele e o menino."
    $ mostrar_personagem("Holga", 'R')
    h "Edla era amada demais. Era vista demais."
    h "Quando ela sorria, ninguém via que eu também estava ali, logo atrás, carregando a cesta, limpando a sujeira, suportando o silêncio."
    h "Agora, com ela morta, eu sou a lembrança viva do que sobrou."
    h "E todos, curiosamente, querem me ouvir."
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Eu te entendo… se precisar de algo ou descobrir mais alguma coisa, não tenha medo de falar comigo.":
            $ mostrar_personagem("Holga", 'F')
            h "Tudo bem Padre (ela sorri). Pode deixar."
            $ checar_interacao()
            jump casaholgaext
        "Falando assim… parece que você não ficou triste com a morte de sua irmã.":
            $ mostrar_personagem("Holga", 'T')
            h "Talvez…"
            h "Ou talvez eu só esteja…"
            h "Cansada de carregar aquilo que nunca foi meu."
            $ checar_interacao()
            jump casaholgaext

label ontem_holga:
    $ alterar_interacao(-1)
    $ mostrar_personagem("Holga", 'T')
    h "Ontem à noite? Ah, Padre, o que uma sombra faria?"
    h "Enquanto minha irmã, Edla, estava acostumada a ser vista e amada, a noite para mim é apenas o momento de continuar o trabalho que não rende aplausos…"
    h "Eu estava aqui. Limpando a poeira que se acumula onde ninguém olha, organizando a casa que agora fede a vazio e saudade. Fico acordada, sim. Mas não para vigiar, e sim para lembrar e suportar o silêncio."
    h "A noite é longa, Padre, e nela eu sou apenas a irmã de mãos grossas e olhos fundos que lava o que sobrou da festa alheia."
    h "Passei a maior parte do tempo no escuro, ouvindo o coração bater mais alto do que deveria. "
    $ mostrar_personagem("Holga", 'F')
    h "Mas a noite tem seus próprios sons, e não estou mais sozinha, já que, curiosamente, todos querem me ouvir."
    $ mostrar_personagem("Holga", 'N')
    h "Embora eu estivesse em casa, não estava totalmente cega."
    h "Eu ouvi algo que parecia... pequeno. Um ruído discreto de algo que não queria ser descoberto, um vulto de estatura pequena que se esgueirava nas sombras."
    $ adicionar_fala("Holga", '\"Eu ouvi algo que parecia... pequeno. Um vulto de estatura pequena que se esgueirava nas sombras.\"')
    $ checar_interacao()
    jump casaholgaext

label viubruxa_holga:
    $ alterar_interacao(-1)
    $ mostrar_personagem("Holga", 'R')   
    h "Boatos, Padre?"
    h "Ah, sim. Agora que Edla se foi, eu sou a lembrança viva do que sobrou, e todos, curiosamente, querem me ouvir."
    $ mostrar_personagem("Holga", 'N')
    h "Sim, eu vi algo. Mas se o senhor espera que eu descreva uma velha corcunda com verrugas e caldeirão, está buscando a história errada."
    $ adicionar_pista("Bruxa", 'Não se parece com uma velha corcunda com verrugas e caldeirão')
    h "A bruxa de que falam... ela não tem rosto. Ela não se mostra."
    $ adicionar_pista("Bruxa", 'Não tem rosto, não se mostra')
    h "O que eu vi foi algo pequeno. Uma criatura que se movia nas sombras, mas que não era uma sombra comum. Eu a vi perto da escuridão, onde os galhos quebrados ainda marcavam o local de onde Edla foi arrastada."
    $ adicionar_pista("Bruxa", 'Algo pequeno, uma criatura que se movia nas sombras.')
    h "Quando Edla morreu na floresta, tudo o que eu consegui ouvir foi ela chamando por ajuda, com aquela voz toda distorcida."
    h "E o que eu vi, Padre, foi o reflexo dessa voz, e ela esgueirava-se como se estivesse acostumada a fugir, ou a roubar."
    $ adicionar_fala("Holga", '\" Tudo que consegui ouvir foi Edla chamando por ajuda com aquela voz distorcida e o que eu vi foi o reflexo daquela voz\"')
    h "O mal sempre ataca quem não pode se defender, mas o real monstro é a força que está por trás dessa brasa acesa."
    $ checar_interacao()
    jump casaholgaext

########################################### CENAS PADEIRO ###########################################################
label dialogo_bartolomeu:
    call hide_all_screens
    if personagens_dict["Bartolomeu"].conversavel:
        if personagens_dict["Agnes"] == False:
            $ mostrar_personagem("Bartolomeu", 'T')
            b "Senhor."
            b "Pra quem eu irei realizar ações beneficentes agora?"
            b "Como eu demonstrarei toda minha humildade sem ter à quem dar pão?"
            $ mostrar_personagem("Bartolomeu", 'R')
            b "Você me condenou padre."
            b "Preciso pensar no que vou fazer agora."
            jump padaria
        elif personagens_dict["Bartolomeu"].conhecido == False:
            $ personagens_dict["Bartolomeu"].conhecido = True
            $ mostrar_personagem("Padre", 'N')
            p "Buongiorno… pelas vestes, você deve ser o padeiro… "
            p "Imagino que saiba quem sou. As notícias por aqui correm rápido; estou encarregado de acabar com o mal que assombra este lugar."
            p "Preciso reunir informações e evidências."
            p "Agora..."
            $ mostrar_personagem("Bartolomeu", 'R')
            b "Não tenho tempo para isso!"
            b "Tenho muitos pães pra fazer! Muitos pães!"
            $ mostrar_personagem("Padre", 'N')
            p "Prometo que vai ser rápido"
        jump escolhas_bartolomeu
    else:
        $ mostrar_personagem("Bartolomeu", 'T')
        b "Não estou com vontade de conversar hoje..."
        jump padaria

label escolhas_bartolomeu:
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Me conte sobre você" if personagens_dict["Bartolomeu"].listaPerguntas[0] == False: 
            $ personagens_dict["Bartolomeu"].listaPerguntas[0] = True
            jump meconte_bartolomeu
        "Onde e o que você fez ontem a noite?" if personagens_dict["Bartolomeu"].conversouHoje == False:
            $ personagens_dict["Bartolomeu"].conversouHoje = True
            jump ontem_bartolomeu
        "Algum habitante te parece estranho?" if personagens_dict["Bartolomeu"].listaPerguntas[1] == False and personagens_dict["Bartolomeu"].progresso == 0: ## vai desbloquear pergunta pra joana
            $ personagens_dict["Bartolomeu"].listaPerguntas[1] = True
            jump habitante_bartolomeu
        "Não perguntar nada":
            jump padaria

label meconte_bartolomeu:
    $ alterar_interacao(-1)
    $ mostrar_personagem("Bartolomeu", 'N')
    b "Sou conhecido como Bartolomeu, o Padeiro."
    $ personagens_dict["Bartolomeu"].conhecer()
    $ mostrar_personagem("Bartolomeu", 'F')
    b "Mas aqui na aldeia sou muito mais que isso… deveriam me considerar a alma do lugar, pois sou eu quem aquece o estômago de muitos por aqui!"
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Então você distribui pães e alimenta eles sem nenhum custo?":
            jump paos_bartolomeu
label paos_bartolomeu:
    $ mostrar_personagem("Bartolomeu", 'R')
    b "Não, claro que não"
    $ mostrar_personagem("Bartolomeu", 'F')
    b "O que é bom precisa ser cobrado."
    b "É verdade que enquanto alguns pedintes juntam migalhas por aí, eu tenho fornadas."
    b "Enquanto o ferreiro vive cansado por moedas, eu acordo antes do sol e durmo com o tintilar de moedas no meu bolso — sem esforço, apenas vez ou outra ficando sujo de farinha… mas já me acostumei."
    $ mostrar_personagem("Padre", 'T')
    menu:
        "Isso soa meio egoísta, com certeza devem sobrar pães do dia para entregar aos mais necessitados":
            jump egoismo_bartolomeu
        "E não sobra nenhum pão no final do dia para ajudar esses pedintes?":
            jump egoismo_bartolomeu
label egoismo_bartolomeu:
    $ mostrar_personagem("Bartolomeu", 'N')
    b "  Sim, sobram. Mas eu tento deixá-los para venda o máximo de tempo possível… "
    $ mostrar_personagem("Bartolomeu", 'T')
    b "Não me orgulho… muito."
    $ mostrar_personagem("Bartolomeu", 'F')
    b "Afinal, vez ou outra dou um pão amanhecido a uma menina de rua chorosa ou a um servo de olhos fundos"
    b "É tudo que tenho a eles."
    $ checar_interacao()
    jump padaria
            
label habitante_bartolomeu:
    $ alterar_interacao(-1)
    $ mostrar_personagem("Bartolomeu", 'N')  
    b "Nesta aldeia, o pão fala… Ele revela quem tem e quem precisa.  Sei de muitas coisas e já vi muitas coisas suspeitas."
    b "Uma figura curiosa é aquela mulher que fica na praça contando histórias, Margarida. Ela fica lá durante o dia, mas vive rondando os campos ao entardecer."
    b "Certa noite, notei que ela parou diante de minha padaria fechada. Sussurrou algo em latim, ou língua que não conheço, e deixou um saquinho de sal na porta."
    $ mostrar_personagem("Bartolomeu", 'R')     
    b "No dia seguinte, minha fornada queimou inteira, mesmo com o fogo baixo."
    $ adicionar_pista("Margarida", "Falou em latim ou alguma língua estranha e deixou um saco de sal na porta da padaria, no dia seguinte a fornada inteira queimou")
    b "Só voltou a sair direito depois que esfreguei um alho nas paredes, como a velha doente me aconselhou." 
    b "Bruxaria? Não digo. Mas desde então, sempre deixo um pouco de massa crua perto da janela. Só por precaução."
    $ mostrar_personagem("Bartolomeu", 'N') 
    b "Uma outra vez, Vi dona Joana sussurrando para seus tecidos,  e também vi um corvo pousar na sua janela, e juro pelos santos que ele esperou ela terminar um bordado antes de voar."
    b "Antes que me pergunte o que ela bordava, era um manto preto, com linhas vermelhas que dançavam como labaredas."
    $ mostrar_personagem("Bartolomeu", 'T') 
    b "Vendeu ao velho padre que dias depois foi dessa para melhor."
    $ adicionar_pista("Joana", "Sussurra para os tecidos e foi vista pelo padeiro com um corvo na janela fazendo um manto que vendeu ao antigo padre que morreu dias depois")
    $ mostrar_personagem("Bartolomeu", 'N') 
    b "Ainda assim, a vida segue."
    b "Faço meu trabalho, conto minhas moedas, e ouço as histórias da vila com uma orelha atenta e um sorriso humilde."
    $ mostrar_personagem("Bartolomeu", 'F')   
    b "Dizem que a humildade é virtude dos santos, e eu sou quase um, não?"
    b "Dou pão, escuto confissões em troca de farinha, e não conto a ninguém que foi o filho do ferreiro quem roubou da feira ou que a lavadeira fala com os ratos."
    b "Todos têm pecados, mas poucos têm pão."
    $ checar_interacao()
    jump padaria

label ontem_bartolomeu:
    if dia == 1:
        $ alterar_interacao(-1)
        jump ontem1_bartolomeu

    if dia == 2:
        $ alterar_interacao(-1)
        jump ontem2_bartolomeu

    if dia == 3:
        $ alterar_interacao(-1)
        jump ontem3_bartolomeu
    if dia == 4:
        $ alterar_interacao(-1)
        jump ontem4_bartolomeu

    if dia == 5:
        $ alterar_interacao(-1)
        jump ontem5_bartolomeu

    if dia == 6:
        $ alterar_interacao(-1)
        jump ontem6_bartolomeu

    if dia == 7:
        $ alterar_interacao(-1)
        jump ontem7_bartolomeu

##################### dia 1 de o que voce fez ontem ###############################
label ontem1_bartolomeu:
    $ mostrar_personagem("Bartolomeu", 'N')
    b "Eu precisei sair, levar algumas coisas velhas para queimar."
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Que coisas eram essas?":
            jump coisas_bartolomeu
        "Coisas? Que coisas?":
            jump coisas_bartolomeu
label coisas_bartolomeu:
    $ mostrar_personagem("Bartolomeu", 'F')
    b "Farinha!"
    $ mostrar_personagem("Bartolomeu", 'N')    
    b "Era só farinha estragada, oras."
    b "Não posso deixar isso no meio da minha produção, atrai rato…"
    b "E antes que você pergunte, sim, eu fui à noite, porque trabalho de dia, como todo homem honesto…"
    $ mostrar_personagem("Bartolomeu", 'R')
    b "Agora me diga: vai prender e queimar um homem por se livrar de farinha velha?"
    $ mostrar_personagem("Padre", 'N')
    menu: 
        "Não.. Claro que não, por mais que seja estranho. Uma última coisa, você viu algo estranho durante essa sua saidinha?":
            jump estranhosaidinha_bartolomeu
label estranhosaidinha_bartolomeu:
    $ mostrar_personagem("Bartolomeu", 'N') 
    b "Hmmm, teve uma coisa estranha sim."
    b "Quando estava voltando do moinho, ao passar pela casa da costureira, Dona Joana, olhei de relance pela fresta de sua janela…"
    b "Ela estava ajoelhada no chão, cercada por bonecos de pano sem rosto, eles formavam um círculo, e no meio deles havia uma fumaça, parecia ser incenso, ou alguma mistura que queimava lentamente."
    $ adicionar_pista("Joana", "Foi vista pelo padeiro ajoelhada no chão sercada por bonecos de pano sem rosto, com alguma mistura queimando lentamente no meio deles.")
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Ela te viu?":
            jump elaviu_bartolomeu
label elaviu_bartolomeu:
    $ mostrar_personagem("Bartolomeu", 'N') 
    b "Não sei ao certo… Estava escuro, na hora que percebi que ela ia virar, eu sai correndo."
    $ mostrar_personagem("Bartolomeu", 'T') 
    b "Aquela cena gelou minha espinha, por pouco não fiquei la paralizado e fui pego por aquela esquisitona."
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Ela estava em silêncio?":
            jump silenciojoana_bartolomeu
        "Ela falou alguma coisa estranha?":
            jump silenciojoana_bartolomeu
label silenciojoana_bartolomeu:
    $ mostrar_personagem("Bartolomeu", 'N')
    b "Ela falava baixo, não deu para ouvir muito bem."
    b "Mas era como se rezasse, ou murmurava palavras antigas…"
    b "E ao lado dela havia fios de cabelo presos a alfinetes, que ela costurava na cabeça dos bonecos."
    $ adicionar_pista("Joana", "Tinha fios de cabelo presos a alfinetes do seu lado e costurava na cabeça dos bonecos.")
    $ checar_interacao()
    jump padaria
    
###################### dia 2
label ontem2_bartolomeu:
    $ mostrar_personagem("Bartolomeu", 'N')
    b "Sabe, por aqui o dia começa muito cedo. É preciso estar pronto para satisfazer o ânimo de habitantes tão famintos."
    b "Minha tarefa, de certa forma, é simples. Deixar tudo pronto para que os pães estejam frescos para a abertura da padaria."
    b "E, às vezes, para garantir que minhas ferramentas estejam em sua forma mais requintada, passo a noite as refinando."
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Que tipos de ferramentas você usa aqui?":
            jump ferramentas_bartolomeu
        "Quais ferramentas são essas?":
            jump ferramentas_bartolomeu
label ferramentas_bartolomeu:
    $ progredir("Bartolomeu")
    $ alterar_interacao(-1)
    $ mostrar_personagem("Bartolomeu", 'R')
    b "Oras... você sabe!"
    $ mostrar_personagem("Bartolomeu", 'N')
    b "Uma espátula, lâminas, um rolo de massa"
    $ mostrar_personagem("Bartolomeu", 'F')
    b "Tudo o que um bom padeiro como eu precisa para tornar suas obras ainda mais belas."
    $ checar_interacao()
    jump padaria

###################### dia 3
label ontem3_bartolomeu:
    $ mostrar_personagem("Bartolomeu", 'N')
    b "Assim como meu pão, também preciso de um tempo. Em noites mais frias, gosto de me cobrir com um pano, preaquecido. Assim posso me sentir como um de meus pães e entendê-los melhor."
    $ mostrar_personagem("Bartolomeu", 'F')
    b "Repouso o suficiente para permitir que eu me desenvolva adequadamente."
    b "Ao deixar a massa descansar, os ingredientes têm tempo de se misturar e se integrar, resultando em um produto final mais saboroso e equilibrado. Uma massa bem descansada é mais fácil de moldar e dar forma, resultando em produtos finais mais bonitos e uniformes."
    $ checar_interacao()
    jump padaria
################## dia 4
label ontem4_bartolomeu:
    $ mostrar_personagem("Bartolomeu", 'N')
    b "Fiquei enfurnado dentro da minha cozinha, tem dias que é preciso determinação para expulsar esses malditos ratos que vivem aparecendo por aqui."
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Ratos? Eles costumam aparecer bastante?":
            jump ratos_bartolomeu
label ratos_bartolomeu:
    $ mostrar_personagem("Bartolomeu", 'R')
    b "Recentemente eles têm aparecido mais."
    b "Não gosto de falar muito... mas acho que a lavadeira tem algo a ver com isso." 
    $ mostrar_personagem("Padre", 'N')
    menu:
        "De que forma?":
            jump falarratos_bartolomeu
        "O que ela fez?":
            jump falarratos_bartolomeu
label falarratos_bartolomeu:
    $ mostrar_personagem("Bartolomeu", 'N') 
    b "Certa vez, vi ela conversando com um deles, me arrepiei na hora, não fiquei para ouvir sobre o que eles estavam conversando."
    b "Mas tenho me precavido, o cheiro forte do vinagre afasta estas pragas."   
    $ checar_interacao()
    jump padaria   

################# dia 5
label ontem5_bartolomeu:
    $ mostrar_personagem("Bartolomeu", 'F')
    b "Tenho me aventurado e descobri certas coisas."
    b "Sabe, se você pegar a massa, esticá-la em um rolinho, torcer as pontas para formar um círculo e então as juntar, pressionando-as para que não se soltem, você cria algo totalmente novo?"
    b "Estou pensando em nomeá-la como rosquinha!"
    $ checar_interacao()
    jump padaria

################# dia 6
label ontem6_bartolomeu:
    $ mostrar_personagem("Bartolomeu", 'N')
    b "Amanhã é dia de recebimento de mercadorias. Estive me organizando para reabastecer o estoque."
    b "Geralmente há um planejamento semanal de produção para garantir que os produtos mais vendidos estejam sempre disponíveis."
    $ checar_interacao()
    jump padaria

################# dia 7
label ontem7_bartolomeu:
    $ mostrar_personagem("Bartolomeu", 'T')
    b "Hoje, a noite foi pesada. Tenho que garantir que os produtos que chegam serão sempre os melhores."
    $ mostrar_personagem("Bartolomeu", 'N')
    b "É fundamental verificar a data de validade de todos os produtos, as embalagens devem estar íntegras."
    b "O aspecto, a textura, cor, peso e cheiro dos produtos, tudo deve ser minuciosamente verificado."
    $ mostrar_personagem("Bartolomeu", 'F')
    b "Sabe, eu sou detalhista e prezo pelo o que eu faço."
    $ checar_interacao()
    jump padaria


########################################### CENAS BEBADO ###############################################################
label dialogo_bebado:   
    call hide_all_screens
    if personagens_dict["Bêbado"].conversavel:
        if personagens_dict["Seren"].vivo == False:
            $ mostrar_personagem("Bêbado", 'T')
            be "Agora a minha menina se foi também..."
            jump casabebadoext
        elif personagens_dict["Vincent"].vivo == False:
            $ mostrar_personagem("Bêbado", 'T')
            be "Todos... Vão embora..."
            be "Catarina... Vincent..."
            jump casabebadoext
        elif personagens_dict["Bêbado"].conhecido == False:
            $ personagens_dict["Bêbado"].conhecido = True
            $ mostrar_personagem("Padre", 'N')
            p "Buongiorno…"
            jump falas_bebado
    else:
        $ mostrar_personagem("Bêbado", 'T')
        be "Água... Estragada..."
        jump casabebadoext 

label falas_bebado:
    call hide_all_screens         
    $ mostrar_personagem("Bêbado", 'N')
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
            $ adicionar_pista("Bruxa", "\"O mal que caminha nesta aldeia não tem um rosto. Como se usasse outro no lugar…\"")
        $ progredir("Bêbado")
        $ checar_interacao()
    else:
        pi "Ele parece muito bêbado para conversar agora..."
    jump casabebadoext

######################################### CENAS AGNES ###########################################################  
label dialogo_agnes:
    call hide_all_screens
    if personagens_dict["Agnes"].conversavel:
        if personagens_dict["Bartolomeu"].vivo == False:
            $ mostrar_personagem("Agnes", 'T')
            a "Ele me dava pão, padre."
            a "Era velho e duro, mas ainda sim era pão..."
            a "O que eu vou comer agora?"
            jump praca2
        elif personagens_dict["Margarida"].vivo == False:
            $ mostrar_personagem("Agnes", 'T')
            a "A Margarida era a única na vila que era gentil comigo..."
            a "E agora não tem mais ninguém que se importa com a criança marcada..."
            jump praca2
        elif personagens_dict["Agnes"].conhecido == False:
            $ personagens_dict["Agnes"].conhecido = True
            $ mostrar_personagem("Padre", 'N')
            p "Buongiorno, pequena criança."
            p "Alguém da sua idade não deveria estar abandonada nesse estado…"
            p "Eu vou tentar achar abrigo para você, eu prometo."
            p "Mas agora, queria te fazer algumas perguntas..."
        jump escolhas_agnes
    else:
        $ mostrar_personagem("Agnes", 'T')
        a "Não estou com vontade de conversar hoje..."
        jump praca2

label escolhas_agnes:
    $ mostrar_personagem("Padre", 'N')
    menu: 
        "Me conte sobre você" if personagens_dict["Agnes"].conversouHoje == False and personagens_dict["Agnes"].progresso == 0:
            $ progredir("Agnes")
            jump meconte_agnes
        "Sabe me dizer a quanto tempo exatamente você mora na rua?"if personagens_dict["Agnes"].conversouHoje == False and personagens_dict["Agnes"].progresso == 1:
            $ progredir("Agnes")
            jump morarua_agnes

        "Onde e o que você fez ontem a noite?" if personagens_dict["Agnes"].listaPerguntas[0] == False:
            $ personagens_dict["Agnes"].listaPerguntas[0] = True
            jump ontem_agnes

        "Algum dos habitantes te parece estranho?" if personagens_dict["Agnes"].listaPerguntas[1] == False:
            $ personagens_dict["Agnes"].listaPerguntas[1] = True
            jump estranho_agnes

        "Não perguntar nada":
            jump praca2

label meconte_agnes:
    $ mostrar_personagem("Agnes", 'N')
    $ alterar_interacao(-1)
    a "Eu me chamo Agnes…"
    $ personagens_dict["Agnes"].conhecer()
    $ mostrar_personagem("Agnes", 'T')
    a "Tenho 12 anos e ninguém quis me abrigar. A maioria aqui passa por mim e finge que eu não existo."
    a "Eu durmo onde dá… Celeiro do Senhor Salvatore, às vezes o sótão da taverna, uma vez até na igreja, mas o padre antigo me expulsou."
    a "Antes, eu pegava uns grãos escondido do celeiro, mas agora… até lá mal tem o que comer."
    a "Talvez o universo esteja cobrando. Talvez ele saiba que nunca dividiram o suficiente."
    $ mostrar_personagem("Agnes", 'R')
    a "Eu não entendo por que alguns têm tanto… e outros nem um pedaço de pão."
    $ adicionar_pista("Agnes", 'Talvez odeie a vila por ninguém se importar com ela.')
    a "Bartolomeu me dá pão velho às vezes. Duro como pedra, mas é pão."
    a "Ele fala alto, diz que está \"fazendo caridade\" pra todos ouvirem."
    a "Eu finjo que acredito… porque é melhor mastigar pedra do que não mastigar nada."
    $ checar_interacao()
    jump praca2

label morarua_agnes:
    $ alterar_interacao(-1)
    $ mostrar_personagem("Agnes", 'N')
    a "Eu não sei…"
    $ mostrar_personagem("Agnes", 'T')
    a "Desde que meus pais morreram…"
    a "Já faz tanto tempo..."
    $ mostrar_personagem("Padre", 'T')
    menu:
        "E a casa que era de seus pais? Porque você não fica por lá? Pode estar vazia, mas ainda assim é um teto…":
            jump casa_agnes
label casa_agnes:
    $ mostrar_personagem("Agnes", 'T')
    a "Depois que eles morreram… queimaram a casa."
    a "Disseram que era amaldiçoada. Que ninguém devia morar onde gente “marcada” viveu."
    $ mostrar_personagem("Agnes", 'R')
    a "Não deixaram eu pegar nada. Nem uma das roupas que minha mãe costurou…"
    $ adicionar_fala("Agnes", 'Queimaram a casa onde morava com meus pais pois ninguém devia morar onde gente “marcada” viveu.')
    a "Olham pra mim como se eu também fosse marcada."
    $ adicionar_pista("Agnes", 'Talvez odeie a vila por queimar sua casa e olhar pra ela como se fosse \"marcada\".')
    $ mostrar_personagem("Agnes", 'T')
    a "Talvez eu seja mesmo. Eles podiam ter me queimado junto."
    a "Teria doído menos."
    $ checar_interacao()
    jump praca2

label ontem_agnes:
    $ mostrar_personagem("Agnes", 'N')
    $ alterar_interacao(-1)
    a "Ontem… fiquei sentada perto do moinho até escurecer."
    a "Tinha um cheiro estranho no ar… como carne e fumaça."
    a "Eu ia dormir ali mesmo, mas ouvi alguém andando no mato. Me escondi. Então eu vi uma sombra arrastando uma coisa grande…algo pesado."
    a "Depois, sumiu no meio da plantação."
    a "No fim eu acabei dormindo atrás das tábuas do curral abandonado. É frio, mas é seco."
    $ adicionar_fala("Agnes", 'Vi uma sombra perto do moinho arrastando algo pesado.')
    a "Antes de sair de lá, eu olhei para dentro da casa, bem na direção da janela do quarto do filho do Senhor. Eu fiquei ali, parada. Observando. Por um bom tempo…"
    $ mostrar_personagem("Padre", 'N')
    menu:
        "O que você viu pela janela?":
            jump janela_agnes
label janela_agnes:
    $ mostrar_personagem("Agnes", 'N')
    a "Estava escuro, mas a  escuridão não cobria tudo ali."
    a "A luz fraca do luar batia na vidraça."
    a "Eu vi o pequeno William. Ele estava deitado na cama, mas parecia acordado."
    $ checar_interacao()
    jump praca2

label estranho_agnes:
    $ mostrar_personagem("Agnes", 'N')
    $ alterar_interacao(-1)
    a "Todos são estranhos quando estão sozinhos."
    $ mostrar_personagem("Agnes", 'R')
    a "Tem gente que finge ser boa. O padeiro é um deles… mas ele ao menos me da pão as vezes."
    a "O Vincent… ele me trata como um rato, fala de mim como se eu fosse um animal."
    $ mostrar_personagem("Agnes", 'F')
    a "A Margarida ainda é gentil comigo… pelo menos…"
    $ checar_interacao()
    jump praca2

######################################## CENAS JOANA ###########################################################
label dialogo_joana:
    call hide_all_screens
    if personagens_dict["Joana"].conversavel:
        if personagens_dict["Agnes"].vivo == False:
            $ mostrar_personagem("Joana", 'T')
            j "No fim ela não era tão limpa ou marcada como eu pensava..."
            j "Pelo menos não dessa forma..."
            j "Que Deus nos perdoe, padre. Por levar a vida dessa pobre criança..."
            jump casajoanaext
        elif personagens_dict["Joana"].conhecido == False:
            $ personagens_dict["Joana"].conhecido = True
            $ mostrar_personagem("Padre", 'N')
            p "Buongiorno… Espero que esteja bem…"
            p "Está aqui por causa do mal que anda assombrando a todos, não está?"
            p "Então…"
        jump escolhas_joana
    else:
        $ mostrar_personagem("Joana", 'T')
        j "Não estou com vontade de conversar hoje..."
        jump casajoanaext

label escolhas_joana:
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Me conte sobre você" if personagens_dict["Joana"].conversouHoje == False and personagens_dict["Joana"].progresso == 0:
            $ progredir("Joana")
            jump meconte_joana
        "Onde e o que você fez ontem a noite?" if personagens_dict["Joana"].listaPerguntas[1] == False: 
            $ personagens_dict["Joana"].listaPerguntas[1] = True
            jump ontem_joana

        "Algum habitante te parece estranho?" if personagens_dict["Joana"].listaPerguntas[2] == False: 
            $ personagens_dict["Joana"].listaPerguntas[2] = True
            jump habitante_joana

        "Questionar sobre o corvo" if personagens_dict["Bartolomeu"].conversouHoje == False and personagens_dict["Bartolomeu"].progresso == 1:
            $ progredir("Bartolomeu")
            jump corvo_joana

        "Não perguntar nada":
            jump casajoanaext

label meconte_joana:
    $ mostrar_personagem("Joana", 'N')
    $ alterar_interacao(-1)
    j "Buongiorno, padre. Me chamo Joana."
    $ personagens_dict["Joana"].conhecer()
    j "Ganho a vida consertando e fazendo roupas para as pessoas desta pequena aldeia…"
    j "Sabe… costurar é coisa de silêncio. Precisa de concentração… A linha vai e volta, costurando até o que a gente não vê…"
    $ mostrar_personagem("Joana", 'T')
    j "Desde que a escuridão começou a engolir essa aldeia, ninguém mais vem buscar vestido novo. Agora só querem bainhas apertadas e panos escuros, roupa de luto e de enterrar."
    j "Costuro roupas… mas também outras coisas. Algumas que não vestem o corpo… só a saudade."
    j "Guardo pedaços de tecido de quem já partiu. Alguns me deixam à porta. Outros eu mesma recolho do chão… depois que as casas ficam vazias…"
    j "Às vezes me sinto muito sozinha… Então deixo algumas migalhas secas ou cascas de frutas na janela."
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Convive com pássaros então?":
            jump passaros_joana
label passaros_joana:
    $ mostrar_personagem("Joana", 'R')
    j "Pássaros? não."
    $ mostrar_personagem("Joana", 'N')
    j "Acabei fazendo amizade com um corvo. Ele sempre vem ao cair da tarde.  Agora, ele espera. Me observa como se soubesse quando termino um bordado…"
    $ adicionar_fala("Joana", "\"Fiz amizade com um corvo. Ele sempre vem ao cair da tarde.\"")
    $ mostrar_personagem("Joana", 'T')
    j "É como se ele reconhecesse o fim de alguma coisa…"
    $ mostrar_personagem("Joana", 'N')
    j "As pessoas acham que corvos trazem presságios… Mas eu aprendi que, às vezes, eles só vêm buscar o que resta…"
    $ checar_interacao()
    jump casajoanaext

label ontem_joana:
    $ mostrar_personagem("Joana", 'N')
    $ alterar_interacao(-1)
    j "Eu estava aqui em casa. Fazia alguns bonecos que servem como proteção para as mulheres da aldeia que ainda estão vivas… mas também representam aquelas que já partiram. Estou fazendo isso todos os dias atualmente"
    $ mostrar_personagem("Joana", 'T')
    j "Uso sobras de tecidos de pessoas que já não estão entre nós. Eu tenho esse problema… não consigo me desfazer, jogar fora uma memória de quem já se foi."
    j "Não me leve a mal por isso mas, ontem, eu fazia um tipo de ritual que eu mesma inventei: coloquei os bonecos em círculos, para que a ausência de cada um fizesse companhia ao meu próprio vazio…"
    $ adicionar_fala("Joana", "Eu fazia um tipo de ritual que inventei: coloquei os bonecos em círculos, para que a ausência de cada um fizesse companhia ao vazio…")
    j "No centro, coloquei uma mistura de erva-doce e alecrim queimado sobre carvão, para purificar o ambiente, enquanto fazia uma reza cantada que aprendi com minha avó…"
    $ adicionar_fala("Joana", "\"No centro, coloquei uma mistura de erva-doce e alecrim queimado sobre carvão, para purificar o ambiente, enquanto fazia uma reza cantada que aprendi com minha avó…\"")
    j "Não tem nenhuma má intenção por trás…"
    j "Ontem também tentei fazer algum tipo de cabelo para os bonecos… então cortei um pouco do meu próprio cabelo… Queria que eles ficassem mais bonitos…"
    $ adicionar_fala("Joana", "\"Ontem também tentei fazer algum tipo de cabelo para os bonecos… então cortei um pouco do meu próprio… Queria que eles ficassem mais bonitos…\"")
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Conte-me mais sobre esses bonecos":
            jump bonecos_joana
label bonecos_joana:
    $ mostrar_personagem("Joana", 'N')
    j "Ah, os bonecos… Pode soar muito estranho para você, ou talvez suspeito, mas já não me importo com isso."
    j "Cada um deles não só tem um fragmento de alguém, como um vestido, botão esquecido, fios de cabelo… são... memórias… vestígios de que um dia foram vivos."
    j "Os guardo com muito carinho… as vezes até mesmo… acho que eles me respondem quando converso com eles…"
    $ checar_interacao()
    jump casajoanaext

label habitante_joana:
    $ mostrar_personagem("Joana", 'R')
    $ alterar_interacao(-1)
    j "Estranho…? Estranho é viver num lugar onde a noite anda engolindo o dia sem aviso…"
    j "Os galos cantam atrasados. Os cães evitam certas encruzilhadas. Até os tecidos parecem pesar mais quando os costuro."
    $ mostrar_personagem("Joana", 'T')
    j "Mas… se quer saber o que mais me inquieta… não são os mortos… É aquela menina… Agnes…"
    $ mostrar_personagem("Joana", 'N')
    j "Foi ontem ao entardecer… Eu estava com pressa, porque está perigoso ficar fora de casa quando a noite cai… Mas, voltando do poço com um balde d'água, passei em frente à porta dos fundos da casa do senhor Salvatore…"
    j "Vi uma sombra pequena se esgueirando pelo celeiro…"
    j "Me aproximei devagar… e lá estava ela: a pequena Agnes…Parecia ter quebrado a tranca de uma caixa de mantimentos… estava com um punhado de frutas secas nas mãos… claramente roubando…"
    j "Mas não era só isso…"
    j "Antes de sair, ela olhou para dentro da casa,  bem na direção da janela do quarto do filho do senhor… "
    j "E ficou ali, parada, observando… por um bom tempo. Não sei se ela viu algo… ou se queria ser vista…"
    j "Ela não me viu, e depois… desapareceu na noite como se tivesse aprendido a andar sem fazer barulho…"
    $ mostrar_personagem("Joana", 'T')
    j "Não estou dizendo que ela é culpada de coisa alguma… "
    j "Só que, algumas crianças não vêm ao mundo limpas…"
    j "E o mundo não tem como lavá-las."
    $ adicionar_fala("Joana", "\"Algumas crianças não vêm ao mundo limpas… E o mundo não tem como lavá-las.\"")
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Você sente medo de algo ou alguém?":
            jump medo_joana
label medo_joana:
    $ mostrar_personagem("Joana", 'N')
    j "Medo? o medo mora aqui."
    $ mostrar_personagem("Joana", 'T')
    j "Em cada prego, em cada nó que eu dou."
    j "Eu só temo o dia… em que minhas mãos não tiverem mais força para costurar…"
    $ checar_interacao()
    jump casajoanaext

label corvo_joana:
    $ mostrar_personagem("Joana", 'N')
    $ alterar_interacao(-1)
    j "Ele sempre me encontra… mesmo quando mudo de lugar."
    j "Não sei se é o mesmo de anos atrás, ou se são muito… iguais."
    j "Acho que ele vem recolher as últimas histórias da aldeia, como se fossem fios soltos que só ele sabe tecer"
    $ checar_interacao()
    jump casajoanaext



######################################## CENAS Salvatore ########################################
label dialogo_salvatore:
    call hide_all_screens
    if personagens_dict["Salvatore"].conversavel:
        if personagens_dict["Holga"].vivo == False:
            $ mostrar_personagem("Salvatore", 'T')
            ss "A holga podia ser..."
            ss "Exêntrica."
            ss "Mas não era uma má pessoa."
            $ mostrar_personagem("Salvatore", 'R')
            ss "Você errou no seu julgamento padre."
            ss "Faça seu trabalho direito na próxima."
            jump caminhobebado_margarida
        elif personagens_dict["Salvatore"].conhecido == False:
            p "Buongiorno."
        jump escolhas_salvatore
    else:
        $ mostrar_personagem("Salvatore", 'T')
        ss "Não estou com vontade de conversar hoje..."
        jump caminhobebado_margarida

label escolhas_salvatore:
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Pode me contar um pouco mais sobre o que está acontecendo aqui?" if personagens_dict["Salvatore"].listaPerguntas[0] == False: 
            $ personagens_dict["Salvatore"].listaPerguntas[0] = True
            jump acontecendo_salvatore
        "Tem algo a dizer sobre o último caso?" if personagens_dict["Salvatore"].conversouHoje == False and personagens_dict["Salvatore"].progresso == 0:
            $ progredir("Salvatore")
            jump algomais_salvatore
        "Me conte mais sobre o seu filho" if personagens_dict["Salvatore"].conversouHoje == False and personagens_dict["Salvatore"].progresso == 1:
            $ progredir("Salvatore") ##Desbloqueia falar com o william
            jump filho_salvatore

        "O que você fez ontem a noite?" if personagens_dict["Salvatore"].listaPerguntas[1] == False: 
            $ personagens_dict["Salvatore"].listaPerguntas[1] = True
            jump ontem_salvatore

        "Você encontrou algo suspeito nesses últimos dias?" if personagens_dict["Salvatore"].conversouHoje == False and personagens_dict["Salvatore"].progresso == 2:
            $ progredir("Salvatore")
            jump suspeito_salvatore

        "Não perguntar nada":
            jump caminhobebado_margarida
label acontecendo_salvatore:
    $ alterar_interacao(-1)
    $ mostrar_personagem("Salvatore", 'R')
    ss "Está tudo errado... já faz mais de um mês que isso começou."
    ss "Cada manhã... uma maldição nova."
    ss "Primeiro foi o carneiro morto, com suas entranhas espalhadas na praça…"
    ss "Depois as sementes."
    ss "Elas brotavam e simplesmente apodreciam no mesmo dia."
    ss "As minhas plantações ficaram inúteis. Eu já não sabia o que fazer..."
    $ mostrar_personagem("Salvatore", 'T')
    ss "Então vieram as mortes… o ferreiro e depois o antigo padre... Ver aquela igreja vazia é…"
    ss "Doloroso"
    $ mostrar_personagem("Padre", 'N')
    menu: 
        "Como os aldeões estão lidando com isso?":
            jump lidando_salvatore
label lidando_salvatore:
    $ mostrar_personagem("Salvatore", 'N')
    ss "O povo teme o que está na noite, e o que vão encontrar ao amanhecer."
    ss "Certamente que quem não está dentro de sua casa quando chega a noite, deve ser no mínimo suspeito ou culpado pelo que anda acontecendo."
    $ adicionar_fala("Salvatore", '\"Certamente que quem não está dentro de sua casa quando chega a noite, deve ser no mínimo suspeito ou culpado.\"')
    ss "Eles rezam…"
    ss "Rezam não por salvação, mas por esquecimento."
    ss "É melhor não lembrar do que se vê por essas noites."
    $ checar_interacao()
    jump caminhobebado_margarida

label algomais_salvatore:
    $ alterar_interacao(-1)
    $ mostrar_personagem("Salvatore", 'T')
    ss "Edla…"
    ss "Ela foi a pior com certeza."
    ss "Ela estava comigo, tão radiante e cheia de alegria… E no outro dia... nada."
    ss "Só encontrei pedaços da roupa dela, manchadas de sangue e sujeira largadas na floresta. Nem um corpo para enterrar… como se o próprio mundo tivesse arrancado ela de mim."
    $ mostrar_personagem("Salvatore", 'R')
    ss "Maledizione!"
    ss "Tem uma bruxa padre! Um mal maior! Deus está nos punindo! Um mal agouro!"
    ss "Porca miséria."
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Por que ela era importante?":
            jump importante_salvatore
        "Vocês tinham alguma relação?":
            jump importante_salvatore
label importante_salvatore:
    $ mostrar_personagem("Salvatore", 'T')
    ss "Afeto…"
    ss "Eu pretendia me casar com ela no fim da colheita, ela moraria comigo e com meu filho."
    ss "Seríamos uma família de verdade..."
    $ checar_interacao()
    jump caminhobebado_margarida

label filho_salvatore:
    $ mostrar_personagem("Salvatore", 'T')
    $ alterar_interacao(-1)
    ss "Meu pobre William tem só dez anos, mas já tem olhos que perguntam demais..."
    $ personagens_dict["William"].conhecer()
    $ mostrar_personagem("Salvatore", 'F')
    ss "Dizem que se parece comigo."
    $ mostrar_personagem("Salvatore", 'T')
    ss "Pobre garoto. Não tem mãe, não como deveria."
    ss "Não comento muito sobre ele com os de fora, e nem deixo que saia muito."
    ss "Crianças precisam ser protegidas, escondidas até que saibam o peso de seu próprio nome."
    $ adicionar_fala("Salvatore", '\"Crianças precisam ser protegidas e escondidas até que saibam o peso do seu próprio nome.\"' )
    $ mostrar_personagem("Salvatore", 'F')
    ss "E não me arrependo sobre isso. Um dia, ele vai me agradecer quando for velho."
    $ mostrar_personagem("Padre", 'N')
    menu:
        "O que aconteceu com a mãe do seu filho, senhor?":
            jump nao_salvatore
label nao_salvatore:
    $ mostrar_personagem("Salvatore", 'R')
    ss "Acho que isso não é da sua conta."
    ss "E não quero falar sobre isso!"
    $ adicionar_pista("Salvatore", 'Foi agressivo quando perguntei sobre a mãe de seu filho.')
    $ mostrar_personagem("Padre", 'N')
    menu: 
        "Posso falar com o seu filho?":
            jump falarfilho_salvatore
label falarfilho_salvatore:
    $ mostrar_personagem("Salvatore", 'N')
    ss "O garoto não está acostumado a conversar com pessoas, como eu já lhe disse."
    ss "Mas fique à vontade. Ele está dentro de casa."
    $ checar_interacao()
    jump caminhobebado_margarida

label ontem_salvatore:
    $ mostrar_personagem("Salvatore", 'R')
    $ alterar_interacao(-1) 
    ss "Sei que quer a maior quantidade de informações possíveis. Mas não existe motivo para elevar esse tom suspeito comigo."
    $ mostrar_personagem("Salvatore", 'N')
    ss "Fiquei sozinho… como sempre. Rotina comum." 
    ss "Caminhei até o velho galpão dos grãos, faço isso quando o sono não me encontra."
    $ mostrar_personagem("Salvatore", 'T')
    ss "Levei vinho… o mesmo que Edla gostava. Bebi em silêncio, ouvindo o vento passando pelas tábuas pobres. Li uma carta antiga e... é isso."
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Uma carta antiga?":
            jump carta_salvatore
        "O que seria essa carta?":
            jump carta_salvatore
label carta_salvatore:
    $ mostrar_personagem("Salvatore", 'T')
    ss "A última de Edla…"
    ss "Me faz lembrar de sua voz."
    $ mostrar_personagem("Salvatore", 'T')
    ss "Agora pare de voltar neste maldito assunto."
    $ checar_interacao()
    jump caminhobebado_margarida

label suspeito_salvatore:
    $ mostrar_personagem("Salvatore", 'N')
    $ alterar_interacao(-1) 
    ss "Hmph… talvez."
    ss "Há marcas perto do celeiro. Pegadas pequenas… mas profundas."
    ss "Como se algo leve… arrastasse peso atrás de si."
    ss "Os homens dizem que é só um animal."
    ss "Animais não abrem portas, Padre."
    $ adicionar_fala("Salvatore", '\"Há pegadas pequenas e profundas perto do celeiro, homens dizem que é so um animal, mas animais não abrem portas.\"')
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Seu filho notou algo estranho?":
            jump suspeitofilho_salvatore   
label suspeitofilho_salvatore:
    $ mostrar_personagem("Salvatore", 'R')
    ss "Ele não deveria notar nada."
    $ adicionar_pista("Salvatore", 'Não gosta que falem do filho dele.')
    ss "Mas… ontem ele disse ter ouvido “batidas” na janela. Três vezes. Sempre três."
    ss "Se descobrir quem está assustando meu garoto… te juro… vai se arrepender."
    $ checar_interacao()
    jump caminhobebado_margarida


################################################### CENAS DO WILLIAM ####################################################################
label dialogo_william:
    call hide_all_screens
    if personagens_dict["William"].conversavel:
        if personagens_dict["Salvatore"].vivo == False:
            $ mostrar_personagem("Salvatore", 'T')
            w "Meu pai..."
            w "Ele era tudo que eu tinha..."
            w "O que será de mim agora? Com as pessoas ruins que ele se esforçava para me proteger lá fora..."
            jump casasalvatoreint
        elif personagens_dict["William"].conhecido == False:
            $ personagens_dict["William"].conhecido = True
            $ mostrar_personagem("Padre", 'N')
            p "Buongiorno bambino."
            p "Posso fazer algumas perguntas sobre a situação da vila?"
            $ mostrar_personagem("William", 'N')
            w "P-pode sim."
        jump escolhas_william
    else:
        $ mostrar_personagem("William", 'T')
        w "Não estou com vontade de conversar hoje..."
        jump casasalvatoreint

label escolhas_william:
    $ mostrar_personagem("Padre", 'N')
    menu: 
        "Me conte sobre você." if personagens_dict["William"].listaPerguntas[0] == False:
            $ personagens_dict["William"].listaPerguntas[0] = True
            jump meconte_william

        "Viu algo estranho nesses últimos dias?" if personagens_dict["William"].conversouHoje == False and personagens_dict["William"].progresso == 0:
            $ progredir("William") 
            jump estranho_william
        "Por favor pequeno, consegue me contar sobre seu cabelo? Isso ainda me inquieta." if personagens_dict["William"].conversouHoje == False and personagens_dict["William"].progresso == 1:
            $ progredir("William") 
            jump cabelo_william

        "O que você faz enquanto está sozinho?"if personagens_dict["William"].listaPerguntas[1] == False:
            $ personagens_dict["William"].listaPerguntas[1] = True
            jump sozinho_william

        "O que você fez ontem à noite?" if personagens_dict["William"].listaPerguntas[2] == False:
            $ personagens_dict["William"].listaPerguntas[2] = True
            jump ontem_william

        "Não perguntar nada.":
            jump casasalvatoreint

label meconte_william:
    $ mostrar_personagem("William", 'N')
    $ alterar_interacao(-1)
    w "Olá, eu sou o Wi… William."
    w "Só William."
    w "Tenho dez anos. Meu pai cuida da aldeia toda, mas ele diz que eu tenho que ficar em casa, porque ainda não entendo o que é certo."
    w "Ele nunca me deixa sair…"
    w "Papai  diz que tem gente ruim lá fora. Gente que fala demais, que inventa coisas, que olha onde não deve…"
    w "Ele diz que é melhor eu ficar quieto, que criança que escuta demais acaba ouvindo o que não devia…"
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Você tem algum amigo na vila?":
            jump amigo_william
label amigo_william:
    $ mostrar_personagem("William", 'N')
    w "Não… mas às vezes eu falo com os bichos."
    w "Tem um corvo que aparece na janela toda semana."
    w "Ele não fala nada… mas fica me olhando."
    $ adicionar_pista("William", 'Recebe a visita de um corvo toda semana que fica observando-o.')
    w "Gosto mais dele do que das pessoas…"
    $ checar_interacao()
    jump casasalvatoreint

label estranho_william:
    $ mostrar_personagem("William", 'N')
    $ alterar_interacao(-1)
    w "Estranho…?"
    w "Eu acho que sim."
    w "Outro dia, eu acordei antes do sol. Estava muito escuro, mas eu ouvi vozes lá embaixo, na sala. Fui espiar da escada, mas não consegui ver direito, só umas sombras paradas…"
    w "Parecia que cochichavam, mas quando cheguei mais perto, ficou tudo quieto, como se nunca tivessem estado ali."
    w "Eu não devia ter descido, mas eu tropecei num balde… Era aquele balde de tinta que meu pai usa pra arrumar… meu cabelo."
    w "Espalhou tudo pelo chão. Papai ficou bravo. Mandou eu subir correndo, disse que eu não podia ver quem estava ali."
    $ adicionar_pista("Salvatore", 'Disse ao William que não podia ver quem estava em sua casa quando ele viu as sombras.')
    w "No outro dia, eu vi umas pegadas pretas perto da porta. Devem ter sido minhas… mas às vezes acho que não."
    $ adicionar_fala("William", '\"No dia após as sombras, vi pegadas perto da porta que não sei se são minhas\'')
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Porque um balde de tinta?":
            jump tinta_william
        "Essas sombras... o que eram?":
            jump sombras_william
label tinta_william:
    $ naotinta_william = True
    $ mostrar_personagem("William", 'T')
    w "Papai não gosta que eu fale sobre isso… "
    $ adicionar_pista("William", 'Seu pai usa algum tipo de tinta para arrumar seu cabelo.')
    if sombrass_william == False:
        $ mostrar_personagem("Padre", 'N')
        menu:
            "Essas sombras... o que eram?":
                jump sombras_william
    else:
        jump casasalvatoreint
        $ checar_interacao()
label sombras_william:
    $ sombrass_william = True
    $ mostrar_personagem("William", 'N')
    w "Não sei… nem sei se eram pessoas."
    w "Eram como manchas no escuro…"
    w "Tinha uma maior, parecia importante… "
    $ mostrar_personagem("William", 'T')
    w "As outras menores pareciam curvadas, como se procurassem algo no chão."
    $ adicionar_fala("William", '\"Outro dia vi umas sombras paradas no primeiro andar, uma delas era maior e parecia importante, elas estavam curvadas procurando algo no chão\"')
    w "Não quero falar muito sobre…"
    if naotinta_william == False:
        $ mostrar_personagem("Padre", 'N')
        menu:
            "Porque um balde de tinta?":
                jump tinta_william   
    else:
        jump casasalvatoreint    
        $ checar_interacao()

label cabelo_william:
    $ mostrar_personagem("William", 'N')
    $ alterar_interacao(-1)
    w "Tudo bem... eu gosto de você padre."
    $ mostrar_personagem("William", 'F')
    w "Finalmente meu pai deixou eu falar com alguém."
    w "Meu cabelo não é dessa cor. É tinta."
    w "Toda vez que começa a clarear, papai chama o homem que pinta."
    $ mostrar_personagem("William", 'T')
    w "Diz que é perigoso eu parecer com… alguém. Ele nunca fala quem."
    $ adicionar_fala("William", "\"Meu pai diz que é perigoso eu parecer com alguém, por isso pinta meu cabelo sempre que ele começa a clarear.\"") 
    $ mostrar_personagem("William", 'R')
    w "Eu também não pergunto. Quando perguntei, ele ficou bravo, e me deixou de castigo por dois dias…"
    $ mostrar_personagem("William", 'T')
    w "Não conte pra ele que eu te disse isso, por favor."
    $ checar_interacao()
    jump casasalvatoreint

label sozinho_william:
    $ mostrar_personagem("William", 'N')
    $ alterar_interacao(-1)
    w "Eu desenho."
    w "Mas só escondido."
    w "Se meu pai vir, ele fala que isso deixa a cabeça fraca."
    w "Ah… e às vezes tento fazer barquinhos de madeira… mas nunca ficam bons."
    w "Ontem eu fiz um que afundou em três segundos."
    $ checar_interacao()
    jump casasalvatoreint

label ontem_william:
    $ mostrar_personagem("William", 'N')
    $ alterar_interacao(-1)  
    w "Eu tomei meu leite quente, li um pouco e fui dormir..."
    w "A mesma coisa de sempre."
    $ checar_interacao()
    jump casasalvatoreint

######################################### CENAS QUE OCORREM DURANTE A NOITE #######################################################
label noite:
    call screen pistas
    with dis

######################################### PISTAS ##################################################
label pistas:
    $ pistas_list = atualizar_pistas(infoPersonagem)
    $ falas_list = atualizar_falas(infoPersonagem)
    call hide_all_screens
    call screen pistas_personagem(infoPersonagem)
    
label dialogo_bruxa: # Matou a Bruxa
    scene tela preta
    with dis
    call hide_all_screens

    $ tocar_musica("tema.mp3")

    python:
        texto_grande("O Padre, impulsionado pela necessidade de ordem e respostas que sentia serem a chave para curar a aldeia, concentrou sua atenção no jovem William, acreditando que o menino escondia a verdadeira fonte do mal." )
        texto_grande("A cena do exorcismo, realizada no quarto silencioso de Salvatore, foi de uma tensão sufocante.")
        texto_grande("O Padre iniciou os ritos, sua voz ressoando contra a madeira da casa do Senhor Salvatore.")
        texto_grande("William, pálido e isolado, parecia mais assustado com a presença do Padre do que com qualquer mal que pudesse habitá-lo. O Padre confrontou o silêncio do garoto com orações.")
        texto_grande("Quando a voz do Padre elevou-se em comando, o corpo de William estremeceu. O padre aos poucos sentiu a presença recuar do corpo do garoto.")
        texto_grande("O Padre observou William, ele parecia exausto mas ao mesmo tempo parecia aliviado da tensão da possessão. No entanto, uma voz sibilante e seca, que não pertencia ao garoto, ressoou no quarto e logo se revelou a criatura por trás.")
    
    call hide_all_screens
    scene bg casa salvatore
    with dis
    $ mostrar_personagem("Bruxa", 'C') 
    bx "Parabéns, Padre! Você limpou o vaso, mas não arrancou a raiz."
    bx "E o que sou eu, senão um perfume, atraído para onde a terra já está podre?"
    scene bg casa salvatore
    with dis
    $ mostrar_personagem("Padre", 'R')
    p "Confesse seus crimes, mulher. A verdade pode aliviar seu espirito, mesmo que seu corpo já esteja condenado."
    scene bg casa salvatore
    with dis
    $ mostrar_personagem("Bruxa", 'I') 
    bx "Alma? Você fala como se soubesse o que é ter uma."
    scene bg casa salvatore
    with dis
    $ mostrar_personagem("Padre", 'R')
    p "Não ouse zombar do portador da voz de Deus neste estado, você mal tem forças para andar."
    scene bg casa salvatore
    with dis
    $ mostrar_personagem("Bruxa", 'N')
    bx "É verdade, minhas forças se vão…"
    bx "Mas não por causa desse sua oração patética. É o preço do que fiz."
    scene bg casa salvatore
    with dis
    $ mostrar_personagem("Padre", 'N')
    p "Finalmente admitindo o mal que causou a esse povo."
    $ mostrar_personagem("Padre", 'R')
    p "Que pacto fez? Para que demônio vendeu sua fé?"
    scene bg casa salvatore
    with dis
    $ mostrar_personagem("Bruxa", 'R')
    bx "Sempre demônios… Sempre pecados…"
    bx "Eu não entreguei a minha fé, padre. Entreguei a minha dor."
    scene bg casa salvatore
    with dis
    $ mostrar_personagem("Padre", 'R')
    p "Dor não justifica maldições, profanar corpos e acabar com vidas."
    scene bg casa salvatore
    with dis
    $ mostrar_personagem("Bruxa", 'I')
    bx "…"
    bx "Você fala como se fosse Santo…"
    bx "Mas eu vejo… Eu vejo o medo em sua voz. Você teme que ao me queimar, algo de mim fique…"
    scene bg casa salvatore
    with dis
    $ mostrar_personagem("Padre", 'R')
    p "O fogo purifica! Nada maligno sobrevive a ele."
    scene bg casa salvatore
    with dis
    $ mostrar_personagem("Bruxa", 'I')
    bx "Purifica?... Ou esconde?"
    $ mostrar_personagem("Bruxa", 'R')
    bx "O fogo é o melhor amigo de homens como você, que queimam o que não conseguem explicar…"
    scene bg casa salvatore
    with dis
    $ mostrar_personagem("Padre", 'R')
    p "Chega!"
    p "Amanhã, ao nascer do sol, você será levada à estaca."
    p "Use esta última noite para rezar…"
    p "Se ainda souber como…"
    scene bg casa salvatore
    with dis
    $ mostrar_personagem("Bruxa", 'N')
    bx "Eu não rezo, Padre…"
    bx "Eu vejo… Eu vi o que vai acontecer com essa aldeia depois que eu me for."
    scene bg casa salvatore
    with dis
    $ mostrar_personagem("Padre", 'N')
    p "Do que você está falando?"
    scene bg casa salvatore
    with dis
    $ mostrar_personagem("Bruxa", 'N')
    bx "Do menino…"
    bx "Do que habita nele quando dorme…"
    $ mostrar_personagem("Bruxa", 'I')
    bx "Ah se você soubesse…"
    scene bg casa salvatore
    with dis
    $ mostrar_personagem("Padre", 'N')
    p "Levem-a! E que Deus tenha piedade."
    scene bg casa salvatore
    with dis
    $ mostrar_personagem("Bruxa", 'C') 
    bx "Ele não terá."
    scene tela preta
    $ renpy.movie_cutscene("images/cutscene_final.webm")

    jump creditos

label morte1:
    scene bg casa padre int
    python:
        genero = personagens_dict[matar_personagem].genero
        pronome = "o" if genero == 'M' else 'a'
        renpy.say(pi, f"Ontem à noite eu matei {pronome} {personagens_dict[matar_personagem].nomeConhecido}.")
        renpy.say(pi, "Todas as técnicas de exorcizar conhecidas não funcionaram.")
        renpy.say(pi, "Imaginando que a bruxa estava tão infiltrada na pessoa que o exorcismo não funcionou, só me restou a fogueira como alternativa.")
        pronome = "ele" if genero == 'M' else "ela"
        renpy.say(pi, f"Mas quando {pronome} parou de gritar, anunciando sua morte definitiva. Tudo na vila parecia igual... E a energia maligna ainda estava no ar...")
        renpy.say(pi, "Foi ai que eu entendi que se tratava apenas de uma pessoa comum.")
        renpy.say(pi, "A vila me perdoou pela autoridade concedida por Deus à mim. Graças à minha causa nobre de livrá-los desse terrível monstro que irá matá-los.")
        pronome = "dele" if genero == 'M' else "dela"
        renpy.say(pi, f"Mas tomara que não tenha ninguém muito próximo {pronome} que não queira mais falar comigo.")
        if matar_personagem != personagens_dict[matar_personagem].nomeConhecido: # "matar_personagem" é sempre o nome real
            renpy.say(pi, "Pelo menos descobri seu nome antes que as chamas apagassem sua vida...")
            renpy.say(pi, f"{matar_personagem}.")
            personagens_dict[matar_personagem].conhecer()
        pronome = "o" if genero == 'M' else "a"
        renpy.say(pi, f"Que Deus {pronome} tenha.")
        if dia >= 8:
            renpy.jump("final")
        evento_aleatorio()
        matar_personagem = None
        renpy.jump("casapadre")
    
label morte2:
    scene bg casa padre int
    python:
        genero = personagens_dict[matar_personagem].genero
        pronome = "o" if genero == 'M' else 'a'
        renpy.say(pi, f"Dessa vez foi {pronome} {personagens_dict[matar_personagem].nomeConhecido} que morreu pelas minhas mãos.")
        renpy.say(pi, "Novamente, mais um inocente...")
        if matar_personagem != personagens_dict[matar_personagem].nomeConhecido: # "matar_personagem" é sempre o nome real
            renpy.say(pi, "Mais um nome que nunca responderá ao meu chamado novamente.")
            renpy.say(pi, f"{matar_personagem}...")
            personagens_dict[matar_personagem].conhecer()
        renpy.say(pi, "Que Deus me perdoe pelos meus pecados, realizados pela causa nobre que é salvar esse povo.")
        if dia >= 8:
            renpy.jump("final")
        evento_aleatorio()
        matar_personagem = None
        renpy.jump("casapadre")

label expulso: # Matou 3 pessoas inocentes
    scene bg casa padre int
    python:
        genero = personagens_dict[matar_personagem].genero
        pronome = "o" if genero == 'M' else 'a'
        renpy.say(pi, f"Hoje foi {pronome} {personagens_dict[matar_personagem].nomeConhecido} que foi pra fogueira.")
        if matar_personagem != personagens_dict[matar_personagem].nomeConhecido: # "matar_personagem" é sempre o nome real
            renpy.say(pi, "Ou melhor")
            renpy.say(pi, f"{matar_personagem}...")
            personagens_dict[matar_personagem].conhecer()
        renpy.say(pi, "Quando o último suspiro foi dado, percebi que a vila inteira manteve-se afastada de mim, como se tivessem nojo.")
        renpy.say(pi, f"Até mesmo aqueles que não se importavam com {pronome} {matar_personagem} se mostraram hostis comigo.")
    scene bg casa padre int
    $ mostrar_personagem("Salvatore", 'N')
    ss "Buongiorno padre."
    ss "Ontem foi uma noite..."
    $ mostrar_personagem("Salvatore", 'T')
    ss "Intensa."
    $ mostrar_personagem("Salvatore", 'R')
    ss "Receio que a vila esteja um pouco insatisfeita com a sua atuação."
    ss "Na verdade, todos estamos."
    ss "Eu lhe chamei a nossa vila pois era seu dever encontrar a bruxa. Pela ordem!"
    ss "Stronzo."
    ss "Além de não realizar seu dever, assolou nossa vila em luto. Matando nosso povo e deixando-nos à mercê da bruxa."
    ss "Eu já havia falado quando chamei o senhor, padre, que eu queria respostas, não rezas ou palavras bonitas, muito menos um massacre na aldeia que eu vi crescer."
    ss "Como o homem mais velho, que deve manter tudo sob controle, peço que se retire da vila imediatamente, e não volte a nos incomodar."
    ss "Vafanapoli."
    jump creditos

label final: # Passou do 7o dia sem matar a Bruxa e sem matar 3 pessoas inocentes
    python:
        mortos = contarMortos()
        renpy.say(pi, f"Sete dias se passaram desde que cheguei nessa vila.")
        if mortos == 0:
            renpy.say(pi, "Não incriminei nenhum inocente.")
            renpy.say(pi, "Mas também não os salvei...")
        else:
            plural = "pessoas foram" if mortos > 1 else "pessoa foi"
            renpy.say(pi,f"{mortos} {plural}  para a fogueira por conta das minhas escolhas...")
            renpy.say(pi, "Não que isso faça muita diferença agora...")
        renpy.say(pi, "A noite de ontem foi...")
        renpy.say(pi, "Difícil...")
        renpy.say(pi, "Todos os aldeões começaram a falar naquela língua estranha... e em pouco tempo não sobrou mais nada deles além daquela carcaça vazia e corrompida que a bruxa largou.")
        renpy.say(pi, "É hora de voltar e clamar à Deus por mais discernimento, para que eu possa caçá-la e não tenham mais vítmas como essa pobre vila...")
        renpy.say(pi, "Talvez até procurar ajuda... Já que claramente não fui capaz de cumprir meu papel.")
        renpy.say(pi, "Que o Senhor me guie e tenha piedade.")
    jump creditos


label eventos:
    python:
        #numeroEvento = 7 # DEBUG MANIPULAR EVENTO, TIRAR
        mensagem = eventos_list[numeroEvento]
        if numeroEvento == 1: # Personagem aleatório (exceto Bruxa) não conversável
            personagem = personagens_dict[personagens_list[randint(0, len(personagens_list)-1)][1]]
            while personagem.vivo != True or personagem.nome == "Bruxa":
                personagem = personagens_dict[personagens_list[randint(0, len(personagens_list)-1)][1]]
            personagem.conversavel = False # Faz o personagem aleatorizado não ser conversável por hoje
            if personagem.nomeConhecido == personagem.nome:
                nomeDisplay = personagem.nomeConhecido
            else:
                artigo = 'o' if personagem.genero == 'M' else 'a'
                nomeDisplay = artigo + " " + personagem.nomeConhecido
            mensagem = "O poço foi sabotado e " + nomeDisplay + " bebeu a agua. Não vou conseguir falar com " + nomeDisplay + "..."
        elif numeroEvento == 2: # Perde interação
            alterar_interacao(-1)
        elif numeroEvento == 3: # Chance maior de evento ruim na próxima noite
            modificadorEvento = -1
        elif numeroEvento == 7: # +2 interações
            interacaoMaxHoje = 5
            alterar_interacao(+2)
        elif numeroEvento == 8: # +1 interação
            interacaoMaxHoje = 4
            alterar_interacao(+1)
        elif numeroEvento == 9: # Chance maior de evento bom na próxima noite
            modificadorEvento = 1
        renpy.play("notify.mp3", relative_volume = 1.67)
        renpy.call_screen("notificacao", "EVENTO", mensagem)
        numeroEvento = 0
    return


init python:
    credito = ('Co-direção', 'Vanessa Santos da Silva & Brunna Iwamura'), ('Roteiro', 'Roteirista.........................Vanessa Santos da Silva \n Revisão de Roteiro.........................Gabriel Shiavoni \n Assistente.........................Leticia Maciel'),  ('Arte', 'Direção de Arte \n Design de personagem.........................Cauã Lopes de Oliveira Santos \n Design de cenário..........................Mel Marilac \n Design de HUD..........................Luísa f. Esquiller \n Assistentes \n João Vitor Rocha Meira & Ycaro Santos de Carvalho'), ('Programação', 'Direção de Programação..........................Brunna Iwamura \n Game Developer..........................Enzo Emidio Ferreira \n Assistente de Programação..........................Vanessa Santos da Silva \n Assistentes de Game Design \n Alexandre Martins da Silva \n Gabriel Schiavoni \n João Vítor "Jonny" de Paula Oliveira' ), ('Som', 'Direção de Som..........................Luísa F. Esquiller \n Assistente..........................Álefe Folha'), ('Produção', 'Enzo Dias')
    creditos_s = "{size=70}Créditos\n"
    c1 = ''
    for c in credito:
        if not c1==c[0]:
            creditos_s += "\n{size=60}" + c[0] + "\n"
        creditos_s += "{size=40}" + c[1] + "\n"
        c1=c[0]
    creditos_s += "\n\n{size=30} Projeto realizado para a disciplina de Hipermídia II em conjunto à Realização Audiovisual\n da Universidade Federal de São Carlos em 2025 \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n" 

#guardando as informações acima
init:
    image creditosfinais = Text(creditos_s, text_align=0.5)

#mostrando os creditos
label creditos:
    call hide_all_screens
    hide screen HUD with dissolve

    $ renpy.music.stop(fadeout=2)
    $ renpy.music.set_volume(0.5)
    play music "tema.mp3"

    scene tela preta
    $ quick_menu = False
    $ credito_velocidade = 20

    #fazendo com que apareça uma tela com o número do final jogado
    # $ renpy.show("finalnumero", at_list=[Position(xanchor=0.5, yanchor=0.5, xpos=0.5, ypos=0.5)], what=Text("{size=40}Você alcançou o final " + str(final) + " de 14 diferentes"))
    # with dissolve
    # $ renpy.pause(2.0)
    # hide finalnumero with dissolve

    #fazendo os creditos rolarem
    show creditosfinais at Move((0.5, 1.8), (0.5, -1400), credito_velocidade, repeat=False, bounce=False, xanchor="center", yanchor=900) with dissolve
    pause(credito_velocidade)
    scene tela preta
    with dissolve

    #tela agradecendo
    $ renpy.show("agradecimento",at_list=[Position(xanchor=0.5, yanchor=0.5, xpos=0.5, ypos=0.5)], what=Text("{size=70}Obrigado por jogar!"))
    with dissolve
    $ renpy.music.stop(fadeout=2)
    $ renpy.pause(2.0)

    return
