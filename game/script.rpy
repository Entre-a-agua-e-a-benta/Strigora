# The script of the game goes in this file.

# Define posicao de nome dos personagens
default name_side = "left"
# Define dia incial
default dia = 1
# Define quantas interações pode ter
default interacao = 1

default infoPersonagem = ""
## Variaveis do diálogo com o Vincent
default progressoVincent = 0
default progrediuVincent = False
default ontemVincent = False
default suspeitoVincent = False

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
define l = Character("Lázaro") ## Lázaro
define h = Character("Holga") ## HOLGA
define b = Character("Bartolomeu") ## PADEIRO
define be = Character("Bêbado")
define ss = Character("Salvatore")
define j = Character("Joana") ## Costureira
define a = Character("Agnes") ## Criança pedinte
define w = Character("William") ## Criança William

# The game starts here.

label start:

    show screen HUD

    init python:
        from unidecode import unidecode
        class Personagem:
            def __init__(self, nome, genero):
                self.nome = nome
                self.genero = genero
                self.conversouHoje = False
                self.progresso = 0
                self.listaPistas = []
                self.listaFalas = []
                self.vivo = True
                self.descricao = ""
                self.imagem = f"personagens/{unidecode(nome.lower())}/{unidecode(nome.lower())}.png"
                self.retrato = f"personagens/3x4/{unidecode(nome.lower())} retrato.png"
                self.pergunta0 = False
                self.pergunta1 = False
                self.pergunta2 = False
        
        ## Inicializa o dicionário de personagens
        personagens_list = [("Bartolomeu", 'M'), ("Salvatore", 'M'), ("Holga", 'F'), ("Lázaro", 'M'), ("Joana", 'F'), ("Margarida", 'F'), ("Agnes", 'F'), ("Bêbado", 'M'), ("William", 'M'), ("Vincent", 'M'), ("Seren", 'F'), ("Bruxa", 'F')]
        for personagem in personagens_list:
            # personagens_dict[personagem] = [False, 0, list(), True]
            personagens_dict[personagem[0]] = Personagem(personagem[0], personagem[1])
            # personagens_dict["nome do personagem"] = [já conversou hoje (bool), progresso (int), lista de pistas (começa vazia, vai adicionando), vivo (bool)]
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
            if valor >= 0:
                sinal = "+"
            else:
                sinal = ""
            renpy.notify(sinal + str(valor) + " interação")

        def passar_dia(matar_personagem=None):
            global dia, interacao, personagens_list, personagens_dict
            dia = dia + 1
            for personagem in personagens_list:
                personagens_dict[personagem[0]].conversouHoje = False
            interacao = 3
            renpy.notify("interações restauradas")
            renpy.notify("passou o dia")
            if matar_personagem != None:
                personagens_dict[matar_personagem].vivo = False
                renpy.notify("Matei " + matar_personagem)
            renpy.jump("casapadre")
        
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
                renpy.notify("Pista sobre ?: " + fala)
        
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
            renpy.show_screen(personagem.lower() + emocao)

        def mostrar_botao(posicao: tuple, texto: str, jumpTo: str):
            renpy.show_screen("botao_passos", posicao, texto, jumpTo)
        

#### $ adicionar_pista("Vincent", "Gosta de HOMENS") #### é assim que bota pista

########################################## AQUI COMEÇA O JOGO ##############################################################    

######################################## LOCAIS PELO MAPA ##############################################################

## Cena externa da taverna
label tavernaext:
    call hide_all_screens
    play music "ambiencia_ext_geral.mp3"
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
    play music "ambiencia_ext_geral.mp3"
    scene bg casa bebado ext
    call screen casabebado

## Cena quarto do padre dentro da taverna
label casapadre:
    call hide_all_screens
    play music "ambiencia_int_casas.wav"
    scene bg casa padre int
    call screen casapadre

## Cena Casa Margarida Ext
label casamargaridaext:
    call hide_all_screens
    play music "ambiencia_ext_geral.mp3"
    scene bg casa curandeira ext
    call screen casaMargaridaEXT

## Cena Casa Lázaro Ext
label caminhoLazaro:
    call hide_all_screens
    play music "ambiencia_ext_floresta.wav"
    scene bg casa leproso ext
    call screen casaLazaroEXT

## Cena Caminho entre bebado e margarida   
label caminhobebado_margarida:
    call hide_all_screens
    play music "ambiencia_ext_floresta.wav"
    scene bg caminho curandeira
    call screen caminhobebado_margarida

## Cena Casa Lázaro Int
label casaLazaroint:
    call hide_all_screens
    play music "ambiencia_int_casas.wav"
    scene bg leproso int
    call screen casaLazaroINT

## Cena Casa Holga
label casaholgaext:
    call hide_all_screens
    play music "ambiencia_ext_geral.mp3"
    scene bg casa holga ext
    call screen casaHolgaEXT

## Cena praca 2 que tem a escultura
label praca2:
    call hide_all_screens
    play music "ambiencia_ext_geral.mp3"
    scene bg praca2
    call screen praca2

## Cena praca 1 que tem igreja e padaria
label praca1:
    call hide_all_screens
    play music "ambiencia_ext_geral.mp3"
    scene bg praca1
    call screen praca1

label igreja:
    call hide_all_screens
    play music "ambiencia_ext_geral.mp3"
    scene bg igreja int
    call screen igrejaINT

label padaria:
    call hide_all_screens
    play music "ambiencia_ext_geral.mp3"
    scene bg padaria int
    call screen padariaINT

label casajoanaext:
    call hide_all_screens
    play music "ambiencia_ext_geral.mp3"
    scene bg costureira ext
    call screen casaJoanaEXT

label plantacao:
    call hide_all_screens
    play music "ambiencia_ext_floresta.wav"
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

transform bebado_right:
    zoom 0.5   
    ypos 0.1
    xpos 0.5

######################################## CENAS QUE OCORREM NA TAVERNA #######################################################

## Dialogo com o Vincent ao clicar no personagem
label dialogo_vincent:
    call hide_all_screens
    $ mostrar_personagem("Padre", 'N')
    p "Buongiorno… Agradeço a hospitalidade, dizem que é perigoso ficar andando de noite por aí… Então me sinto agradecido por ter onde dormir…"
    p "Agora…"
    jump escolhas_vincent
    
label escolhas_vincent:
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Me conte sobre você" if personagens_dict["Vincent"].conversouHoje == False and personagens_dict["Vincent"].progresso == 0:
            $ progredir("Vincent")
            jump meconte_vincent
        "O que aconteceu com a esposa do seu irmão?" if personagens_dict["Vincent"].conversouHoje == False and personagens_dict["Vincent"].progresso == 1 and dia >= 2:
            $ progredir("Vincent")
            jump esposa_vincent

        "Onde e o que você fez ontem a noite?" if personagens_dict["Vincent"].pergunta1 == False:
            $ personagens_dict["Vincent"].pergunta1 = True
            jump ontem_vincent

        "Algum habitante te parece estranho?" if personagens_dict["Vincent"].pergunta2 == False:
            $ personagens_dict["Vincent"].pergunta2 = True
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
    v "Passei a vassoura, contei os barris, limpei as mesas. E quando a lenha terminou, fui buscar mais atrás do depósito. Voltei antes da meia-noite."
    $ adicionar_pista("Vincent", "Gosta de HOMENS")
    v "Tranquei tudo por dentro. Ninguém entrou depois disso, nem mesmo meu irmão, que vive dizendo que a bebida chama por ele."
    $ checar_interacao()
    jump tavernaint

label suspeito_vincent:
    $ alterar_interacao(-1) 
    $ mostrar_personagem("Vincent", 'N')
    v "Estranhos? Aqui todos andam com o pescoço encolhido, como galinha no fio da faca."
    v "Mas se quer saber… Há alguém que me parece estranho, não sei o nome dele, mas ele mora quase fora da aldeia, isolado com razão. Alguém com o corpo ferido daquele jeito, com certeza boa coisa não fez e agora Deus o castiga pelos seus pecados."
    v "Não o deixo entrar aqui, mas não é pela doença. É por tudo o resto. Por esse silêncio dele que pesa, pelas coisas que diz sem dizer nada. Tem gente que traz má sorte sem precisar levantar a mão."
    $ checar_interacao()
    jump tavernaint

label default_vincent:
    $ mostrar_personagem("Vincent", 'N')
    v "Não estou num bom dia hoje..."
    jump tavernaint

label meconte_vincent:
    #diminui interação do jogador
    $ alterar_interacao(-1)
    $ mostrar_personagem("vincent", "N")
    #$ mostrar_personagem("Vincent", 'N')
    v "Bom… Eu sou o Vincent, cuido da taverna e da estalagem… Ou o que sobrou dela, parece que a aldeia resolveu que o medo é desculpa para parar de beber."
    v "Mas desde que você chegou, tenho limpado o quarto duas vezes por dia, pelo menos um pouco de trabalho para manter a mente ocupada …. "
    v "Não gosto de falar do que não vi com meus próprios olhos. E, pra ser sincero, ultimamente, prefiro ver cada vez menos. Gente demais sussurrando. Portas que antes ficavam abertas agora estão fechadas…"
    v "Mas minha porta… essa fica aberta. Sempre tem quem precise esquecer o que viu. Meu irmão aparece por aqui às vezes… Mas nunca fica muito tempo e nem fala muito."
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Quem é seu irmão?":
            jump irmao_vincent

label irmao_vincent:
    $ mostrar_personagem("Vincent", 'N')
    v "Ah, com certeza você vai vê- lo por aí… Ele está sempre pelos cantos da aldeia. Ele vem aqui, bebe sem pagar, mas não tenho coragem de cobrar."
    v "Depois que a mulher dele se foi, sobrou pouco dele também."
    #v "Eu sou mt mt gay"
    #$ adicionar_pista("Vincent", "Gosta de HOMENS")
    $ checar_interacao()
    jump tavernaint

label esposa_vincent:
    $ alterar_interacao(-1)
    $ mostrar_personagem("Vincent", 'N')
    v "Ela estava grávida…Foi um parto difícil, apenas ela e a parteira dentro do quarto…"
    v "Infelizmente ela não resistiu, mas deu a luz a uma garotinha… Isso faz 10 anos, e desde então ele vive nesse estado… Conspiracionando e dizendo que há culpados pela morte da esposa."

    $ mostrar_personagem("Padre", 'N')
    menu:
        "E a criança? Onde ela está?":
            jump crianca_vincent
label crianca_vincent:
    $ mostrar_personagem("Vincent", 'N')
    v "A menina… Bom… Ela está viva, isso é mais do que posso dizer de muita gente…"
    v "Eu cuido dela, mas de um tempo para cá, ela parece doente, às vezes fala coisa dormindo e acorda com febre alta. Eu tento ser como um pai para ela, mas mesmo assim acho que às vezes não sou o suficiente."
    $ checar_interacao()
    jump tavernaint

label dialogo_seren:
    call hide_all_screens
    $ mostrar_personagem("Padre", 'N')
    p "Buongiorno, pequena. Deus lhe abençoe, eu gostaria de conversar um pouco com você."
    menu:
        "Me conte sobre você.":
            jump meconte_seren
        "Onde e o que você fez ontem a noite?" if personagens_dict["Seren"].pergunta1 == False:
            $ personagens_dict["Vincent"].pergunta1 = True
            jump ontem_seren
        "Algum habitante te parece estranho?" if personagens_dict["Seren"].pergunta2 == False:
            $ personagens_dict["Seren"].pergunta2 = True
            jump habitante_seren
    return

label meconte_seren:
    $ alterar_interacao(-1)
    s "Olá, me chamo Seren… Tenho dez anos, mas preferia não ter nascido… Desse jeito meu pai seria feliz e minha mãe ainda estaria aqui… Foi minha culpa ela ter morrido antes da hora."
    s "Entendo o jeito que meu pai me olha, quando pensa que não estou vendo. Como se fosse difícil me enxergar… como se visse outra pessoa em mim… Acho que ele nunca me perdoou por isso, nem eu me perdoei…"
    s "Ao menos ele bebe pra esquecer, mas eu lembro por nós dois. Lembro mesmo do que nunca vi… Ainda bem que meu tio me dá pão, me dá coberta, e até me deixa ficar atrás do balcão quando chove."
    s "Ele nunca disse que me ama, mas também nunca me culpou. E isso já é mais do que o suficiente… Mas quando a noite chega… tudo muda… Não é todo sonho que dói. Só os que parecem verdade."
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Me conte mais sobre esses sonhos":
            jump sonhos_seren
        "Como são esses sonhos?":
            jump sonhos_seren
label sonhos_seren:
    s "No começo, eu só via silhuetas. Um campo, uma árvore sozinha, uma sombra me seguindo de longe. Depois vieram os sussurros. E agora, agora… Agora eu vejo tudo…"
    s "No sonho, ando pelas ruas da aldeia com passos que não são meus… As mãos... as mãos que estendo são pequenas, como as minhas. Mas elas brilham. Como brasa acesa no escuro. E quando tocam algo, tudo escurece..."
    s "E o que mais me assusta: há uma voz dentro de mim. Mas ela não fala comigo. Ela me usa… Mas o pior é quando vejo ele… o menino com voz de mulher… Ele fala, mas a boca não mexe… Ele parece viver numa tristeza que me queima..."
    s "Quando acordo, a pele está quente como se eu tivesse corrido por horas. A febre queima atrás dos olhos, e minha garganta parece de vidro."
    s "O tio diz que é só vento, ou comida estragada. Mas toda vez que eu sonho, algo na aldeia amanhece errado.Eu queria contar, gritar... Dizer o que vejo…Mas quem vai acreditar numa menina que até o próprio pai não quis segurar no colo?"
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Com o que você sonhou ontem?":
            jump sonhoontem_seren
        "Qual foi o seu sonho mais recente?":
            jump sonhoontem_seren
label sonhoontem_seren:
    s "Ontem… ontem no sonho eu estava em frente ao espelho de uma casa grande, e o menino estava dentro do espelho me olhando de volta. Só que, por um instante, os olhos dele eram os meus…"
    $ checar_interacao()
    jump tavernaint

label ontem_seren:
    $ alterar_interacao(-1)
    s "Fiquei sentada na escada da estalagem, olhando a lua por trás das nuvens. O tio me deu um pedaço de pão com mel… e eu guardei metade. Sempre guardo, caso encontre alguém com mais fome do que eu…"
    s "Depois subi pro quarto, mas não dormi logo. Fiquei ouvindo as vozes lá embaixo. Homens falando alto, rindo… e o padre perguntando coisas. Todo mundo pergunta coisas, ultimamente..."
    s "Quando o salão ficou em silêncio, fechei os olhos. Mas aí o sonho veio…Como se ele me chamasse de algum lugar longe… como se já soubesse onde eu estava."
    $ checar_interacao()
    jump tavernaint

label habitante_seren:
    $ alterar_interacao(-1)
    s "A dona Margarida me dá arrepios… Não que ela seja má, eu acho. Mas ela olha pras pessoas como se enxergasse o que tem dentro."
    s "Uma vez ela passou por mim e disse: 'Nem todo espelho mostra o que é de fora'. Eu nem entendi, mas senti um calafrio subir nas costas…"
    $ checar_interacao()
    jump tavernaint

######################################## CENAS QUE OCORREM NA CASA DA MARGARIDA #######################################################
label dialogo_margarida:
    call hide_all_screens
    $ mostrar_personagem("Padre", 'N')
    p "Buongiorno…"
    $ mostrar_personagem("Margarida", 'N')
    m "A benção, padre."
    m "Veio aqui procurar um motivo para jogar a culpa em mim?"
    $ mostrar_personagem("Padre", 'N')
    p "Não, claro que não. Estou apenas investigando… "
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
    m "Falar pra quê? Já sei o que pensa… Sei o que todos pensam… Vêem uma mulher sozinha, que mexe com coisas que não entendem, e já querem arrastar pra fogueira…"
    m "Chamam-me de contadora de histórias, como se fosse só isso que faço. Talvez seja mesmo… As palavras me obedecem mais do que as pessoas. Conto o que o povo quer ouvir, e escondo o que não estão prontos pra saber."
    m "Já vi mais gente morrer do que você viu nascer. Sei quando a terra tá doente, sei quando o vento muda de cheiro. Sei quando as mãos tremem antes mesmo de tocarem na porta"
    m "Não mexo com mortos. Não falo com sombras. Só aprendi a ouvir o que ninguém mais quer escutar."
    m "Quando o corpo deles falha… Eles veem rastejar até minha porta. Pedem chá e, pomadas. E depois… depois sussurram meu nome como se eu tivesse pacto com a minha própria sombra…"
    m "Hipócritas. Agora que a vila sangra, lembram de mim… Agora… Agora tudo fede a medo e carne podre. Quer caçar uma bruxa? Pois que caçe! Mas olhe direito, porque se me queimar, vai doer. E não só em mim."
    $ checar_interacao()
    jump casamargaridaext

label ontem_margarida:
    $ mostrar_personagem("Margarida", 'N')
    $ alterar_interacao(-1)
    m "O que eu fiz? O mesmo que faço quando o céu fica quieto demais."
    m "Acendi o fogo, deixei a chaleira cantar... e fiquei escutando… Alguns dormem pra esquecer, eu fico acordada pra lembrar e vigiar. Às vezes, o que a gente precisa ouvir só aparece no silêncio entre um estalo da madeira e outro…"
    $ checar_interacao()
    jump casamargaridaext

label historia_margarida:
    $ mostrar_personagem("Margarida", 'N')
    $ alterar_interacao(-1)
    m "Já ouviu a história da corça de três olhos? Não? Então sente e escute, ou vá embora de vez…"
    m "Dizem que, certa vez, uma mulher andava sozinha pela mata, cheia de dor e raiva do mundo. Chorava tanto que as árvores taparam os ouvidos. Foi quando encontrou um ninho, entre galhos partidos, com um choro que não era de ave nem de fera…"
    m "Lá dentro? Dois bebês, iguais… Como um espelho. Mas um tinha os olhos fechados e sorria dormindo. O outro tinha os olhos abertos… e não piscava… A mulher, sozinha no mundo, mesmo sabendo que não era seu,  levou um deles nos braços."
    m "Disse que era um sinal... Que o destino havia escolhido aquele pra ela criar, alimentou, deu nome, cobriu de orações… O outro bebe? talvez você se pergunte, o outro… ficou."
    m "Nunca chorou. Nunca morreu. Só ficou ali, esperando… Um dia, a criança levada perguntou quem era seu pai. Ela respondeu: “Um homem que não tem nome e que não pode ser acordado”."
    m "Desde então, a corça de três olhos ronda a aldeia, procurando seu parente perdido."
    m "E que a criança... bom, ela ainda vive entre nós. Só não sabe o que é."
    $ checar_interacao()
    jump casamargaridaext

######################################## CENAS QUE OCORREM NA CASA DO Lázaro #######################################################
label dialogo_lazaro:
    call hide_all_screens
    $ mostrar_personagem("Padre", 'N')
    p "Buongiorno…"
    p "Não sei a notícia chegou aqui, mas eu estou encarregado de achar o culpado pelas coisas que vem acontecendo na região, pensei que mesmo doente você talvez tivesse alguma informação para contribuir, ou algo no mínimo interessante a dizer."
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
    $ mostrar_personagem("Lázaro", 'N')
    $ alterar_interacao(-1)
    l "Pode chegar mais perto…"
    l "Dizem que a bruxa me amaldiçoou, eles tem medo de mim. Sussurram isso quando pensam que não ouço. Mas meus ouvidos ainda funcionam."
    l "O povo da aldeia acredita que esta carne apodrecida, estas mãos imóveis e este rosto que já não reconheço no reflexo da água... são obra de feitiçaria. São muitos boatos que circulam sobre eu ter ficado assim."
    l "Alguns dizem que cruzei o caminho da costureira e não lhe dei a devida reverência. Que tomei algo que era dela."
    l "Ou que fui tolo o bastante para recusar um favor da contadora de histórias, aquela que anda com ervas estranhas pendendo do cinto e olhos que nunca piscam."
    $ mostrar_personagem("Padre", 'N')
    menu:
        "O que você acha disso?":
            jump acredita_lazaro
        "E o que você acredita?":
            jump acredita_lazaro
label acredita_lazaro:
    $ mostrar_personagem("Lázaro", 'N')
    l "Eu sei que a verdade é outra. Não fui amaldiçoado por uma mulher, fui esquecido por Deus…"
    $ mostrar_personagem("Padre", 'N')
    menu:
        "Dizer que foi esquecido por Deus é fácil quando o mundo inteiro vira o rosto. Mas será que foi Deus quem se afastou de você… ou foi você quem se escondeu afastou e se escondeu dele?":
            jump afastou_lazaro

        "Às vezes, eu também me pergunto se Ele nos ouve... ou se apenas observa. Mas me diga… quando foi a última vez que sentiu algo que não fosse dor?":
            jump dor_lazaro       
label afastou_lazaro:
    $ afastou_lazaro = True
    $ mostrar_personagem("Lázaro", 'N')
    l "Procurei, sim. Por anos. Rezei até a garganta secar. E tudo o que ouvi foi o som da minha pele caindo."
    l "Se Deus está me testando... então por que ninguém mais sangra como eu?"
    if dor_lazaro == False:
        $ mostrar_personagem("Padre", 'N')
        menu:
            "Às vezes, eu também me pergunto se Ele nos ouve... ou se apenas observa. Mas me diga… quando foi a última vez que sentiu algo que não fosse dor?":
                jump dor_lazaro
    else:
        jump salvatorevinda_lazaro
label dor_lazaro:
    $ dor_lazaro = True
    $ mostrar_personagem("Lázaro", 'N')
    l "Senti algo... Uma vez. Quando o Salvatore veio aqui com olhos de choro e mãos trêmulas. Mas não era piedade, era medo."
    l "Medo de que eu soubesse o que ele fez, ou de que eu ainda lembrasse…"
    if afastou_lazaro == False:
        $ mostrar_personagem("Padre", 'N')
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
    $ mostrar_personagem("Lázaro", 'N')
    l "Um calor estranho… Não fisico, mas emocional."
    l "Pela primeira vez em muito tempo, alguém olhou pra mim como uma pessoa que sabia de algo e não só como um doente."
    l "Mas esse sentimento veio com confusão, medo e culpa. Como se eu soubesse de mais e estivesse mascarando isso com febre e dor…"
    $ checar_interacao ()
    jump casaLazaroint

label salvatorefez_lazaro:
    $ mostrar_personagem("Lázaro", 'N')
    $ alterar_interacao(-1)
    l "Aquela moça…"
    l "Aquelas crianças nascidas…"
    menu:
        "Crianças? Que crianças?":
            jump criancas_lazaro
label criancas_lazaro:
    $ mostrar_personagem("Lázaro", 'N')
    l "Não posso… Meu corpo dói ainda mais ao se lembrar disso…"
    l "Me deixe em paz"
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
    show screen bartolomeuN
    b "eu sou o padeiro"
    jump padaria

########################################### CENAS BEBADO ###############################################################
label dialogo_bebado:
    call hide_all_screens
    $ mostrar_personagem("Bebado", 'N')
    $ alterar_interacao(-1)
    be "Ela fala coisas no sono… Não aguentei cuidar dela por muito tempo..."
    $ adicionar_fala("Bêbado", "Ela fala coisas no sono… Não aguentei cuidar dela por muito tempo...")
    be "eu odeio gente"
    $ adicionar_pista("Bêbado", "Odeia gente")
    $ checar_interacao()
    jump casabebadoext
    
######################################### CENAS QUE OCORREM DURANTE A NOITE #######################################################

label casapadre_noite:
    call hide_all_screens
    play music "ambiencia_int_casas.wav"
    scene bg casa padre int
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
    