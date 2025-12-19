## Esse arquivo contém opções que podem ser alteradas para personalizar o jogo.
##
## As linhas que começam com duas marcas '#' são comentários e você não deve
## descomentá-las. As linhas que começam com uma única marca '#' são códigos
## comentados, e você pode querer descomentá-las quando apropriado.


## Noções básicas ##############################################################

## Um nome do jogo legível por humanos. Ele é usado para definir o título padrão
## da janela e aparece na interface e nos relatórios de erros.
##
## O _() ao redor da string a marca como elegível para tradução.

define config.name = _("Strigora")


## Determina se o título fornecido acima será mostrado na tela do menu
## principal. Defina como False para ocultar o título.

define gui.show_name = False


## A versão do jogo.

define config.version = "1.0"


## Texto que é colocado na tela "Sobre" do jogo. Coloque o texto entre aspas
## triplas e deixe uma linha em branco entre os parágrafos.

define gui.about = _p("""
O nome Strigora refere-se a um festival anual que ocorre em Triora, uma vila na Ligúria, Itália. É uma celebração dedicada à história e lendas sobre bruxaria, e é especialmente relevante porque Triora é conhecida como a "cidade das bruxas" devido ao grande número de mulheres que foram acusadas e perseguidas por bruxaria durante a Idade Média e o Renascimento. 

Este jogo se passa durante a Inquisição, quando um padre caçador de bruxas é enviado à vila isolada de Triora, na Itália, para investigar relatos de bruxaria. Em meio ao medo e à desconfiança, o jogador deve explorar o vilarejo, interagir com os moradores, realizar missões paralelas, reunir pistas e decidir quem acusar a cada noite.

A equipe Strigora recomenda jogar esse jogo de forma contínua, para que a experiência e a imersão não sejam afetadas, por isso, o jogo não possui um sistema de salvamentos. Tenha certeza de possuir, em média, 20 minutos para iniciar a gameplay.
""")

define gui.creditomenu = _p("""{size=+15}{b}Co-Direção{/size}{/b}\n
 Vanessa Santos da Silva & Brunna Iwamura\n
 {size=+15}{b} Roteiro {/size}{/b} \n
 {b}Roteirista:{/b}   Vanessa Santos da Silva \n 
 {b}Revisão de Roteiro:{/b}   Gabriel Shiavoni \n 
 {b}Assistente:{/b}   Leticia Maciel \n
{size=+15} {b}Arte {/size}{/b} \n
{b}Direção de Arte{/b} \n 
{b}Design de personagem:{/b}   Cauã Lopes de Oliveira Santos \n 
{b}Design de cenário:{/b}   Mel Marilac \n 
{b}Design de HUD:{/b}   Luísa f. Esquiller \n 
{b}Assistentes {/b}\n
João Vitor Rocha Meira \n
Ycaro Santos de Carvalho \n
{size=+15} {b}Programação {/size}{/b} \n
{b}Direção de Programação:{/b}   Brunna Iwamura \n 
{b}Game Developer:{/b}   Enzo Emidio Ferreira \n 
{b}Assistente de Programação:{/b}   Vanessa Santos da Silva \n
{b}Assistentes de Game Design{/b} \n
Alexandre Martins da Silva \n
Gabriel Schiavoni \n
João Vítor "Jonny" de Paula Oliveira \n 
{size=+15}{b}Som {/size}{/b}\n
{b}Direção de Som:{/b}   Luísa F. Esquiller \n 
{b}Assistente:{/b}   Álefe Folha \n
{size=+15}{b}Produção{/size}{/b} \n
Enzo Dias
 
 """)

## Um nome curto para o jogo usado para executáveis e diretórios na distribuição
## construída. Ele deve ser somente ASCII e não deve conter espaços, dois pontos
## ou ponto e vírgula.

define build.name = "Strigora"


## Sons e música ###############################################################

## Essas três variáveis controlam, entre outras coisas, quais mixers são
## mostrados ao jogador por padrão. Definir uma delas como False ocultará o
## mixer apropriado.

define config.has_sound = True
define config.has_music = True
define config.has_voice = True

default preferences.volume.sfx = 0.33


## Para permitir que o usuário reproduza um som de teste no canal de som ou
## voz, descomente a linha abaixo e use-a para definir um som de amostra a ser
## reproduzido.

# define config.sample_sound = "sample-sound.ogg"
# define config.sample_voice = "sample-voice.ogg"


## Descomente a linha a seguir para definir um arquivo de áudio que será
## reproduzido enquanto o jogador estiver no menu principal. Esse arquivo
## continuará sendo reproduzido no jogo até que seja interrompido ou outro
## arquivo seja reproduzido.

define config.main_menu_music = "audio/tema.mp3"


## Transições ##################################################################
##
## Essas variáveis definem as transições que são usadas quando determinados
## eventos ocorrem. Cada variável deve ser definida como uma transição ou None
## para indicar que nenhuma transição deve ser usada.

## Entrar ou sair do menu do jogo.

define config.enter_transition = dissolve
define config.exit_transition = dissolve


## Entre as telas do menu do jogo.

define config.intra_transition = dissolve


## Uma transição que é usada depois que um jogo é carregado.

define config.after_load_transition = None


## Usado ao entrar no menu principal após o término do jogo.

define config.end_game_transition = None


## Não existe uma variável para definir a transição usada quando o jogo começa.
## Em vez disso, use uma instrução with depois de mostrar a cena inicial.


## Gerenciamento de janelas ####################################################
##
## Isso controla quando a janela de diálogo é exibida. Se for "show", ela será
## sempre exibida. Se for "hide" (ocultar), ela só será exibida quando o diálogo
## estiver presente. Se for "auto", a janela será ocultada antes das declarações
## de cena e mostrada novamente quando o diálogo for exibido.
##
## Após o início do jogo, isso pode ser alterado com as instruções "window
## show", "window hide" e "window auto".

define config.window = "auto"


## Transições usadas para mostrar e ocultar a janela de diálogo

define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)


## Padrões de preferência ######################################################

## Controla a velocidade padrão do texto. O padrão, 0, é infinito, enquanto
## qualquer outro número é o número de caracteres por segundo a serem digitados.

default preferences.text_cps = 30


## O atraso padrão do encaminhamento automático. Números maiores levam a esperas
## mais longas, sendo 0 a 30 o intervalo válido.

default preferences.afm_time = 15


## Salvar diretório ############################################################
##
## Controla o local específico da plataforma onde o Ren'Py colocará os arquivos
## salvos para este jogo. Os arquivos de salvamento serão colocados em:
##
## Windows: %APPDATA\RenPy\<config.save_directory>
##
## Macintosh: $HOME/Library/RenPy/<config.save_directory>
##
## Linux: $HOME/.renpy/<config.save_directory>
##
## Isso geralmente não deve ser alterado e, se for, deve ser sempre uma string
## literal, não uma expressão.

define config.save_directory = "Strigora-1759369428"


## Ícone #######################################################################
##
## O ícone exibido na barra de tarefas ou no dock.

define config.window_icon = "gui/window_icon.png"


## Configuração de compilação ##################################################
##
## Esta seção controla como o Ren'Py transforma o seu projeto em arquivos de
## distribuição.

init python:

    ## As funções a seguir aceitam padrões de arquivos. Os padrões de arquivos
    ## não diferenciam maiúsculas de minúsculas e são comparados com o
    ## caminho relativo ao diretório base, com e sem um /. Se vários padrões
    ## corresponderem, o primeiro será usado.
    ##
    ## Em um padrão:
    ##
    ## / é o separador de diretórios.
    ##
    ## * corresponde a todos os caracteres, exceto o separador de diretório.
    ##
    ## ** corresponde a todos os caracteres, inclusive o separador de diretório.
    ##
    ## Por exemplo, "*.txt" corresponde a arquivos txt no diretório base, "game/
    ## **.ogg" corresponde a arquivos ogg no diretório do jogo ou em qualquer um
    ## de seus subdiretórios e "**.psd" corresponde a arquivos psd em qualquer
    ## lugar do projeto.

    ## Classifique os arquivos como None (Nenhum) para excluí-los das
    ## distribuições criadas.

    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)

    ## Para arquivar arquivos, classifique-os como "arquivo".

    # build.classify('game/**.png', 'archive')
    # build.classify('game/**.jpg', 'archive')

    ## Os arquivos que correspondem aos padrões de documentação são duplicados
    ## em uma compilação de aplicativo para Mac, de modo que aparecem tanto no
    ## aplicativo quanto no arquivo zip.

    build.documentation('*.html')
    build.documentation('*.txt')


## É necessária uma chave de licença do Google Play para realizar compras no
## aplicativo. Ela pode ser encontrada no console do desenvolvedor do Google
## Play, em "Monetizar" > "Configuração de monetização" > "Licenciamento".

# define build.google_play_key = "..."


## O nome de usuário e o nome do projeto associados a um projeto itch.io,
## separados por uma barra.

# define build.itch_project = "renpytom/test-project"
