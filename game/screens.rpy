################################################################################
## Inicialização
################################################################################

init offset = -1

################################################################################
## Estilos
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)



################################################################################
## Telas no jogo
################################################################################


## Diga a tela #################################################################
##
## A tela say é usada para exibir o diálogo para o jogador. Ela recebe dois
## parâmetros, who e what, que são o nome do personagem que fala e o texto a ser
## exibido, respectivamente. (O parâmetro who pode ser None (Nenhum) se nenhum
## nome for fornecido).
##
## Essa tela deve criar um texto exibível com o id "what", pois o Ren'Py o
## utiliza para gerenciar a exibição de texto. Ela também pode criar exibíveis
## com id "who" e id "window" para aplicar propriedades de estilo.
##
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what):

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "namebox"

                if name_side == "left":
                    xalign 0.23
                elif name_side == "right":
                    xalign 0.73

                text who id "who"

        text what id "what"


    ## Se houver uma imagem lateral, exiba-a acima do texto. Não exiba na
    ## variante do telefone - não há espaço.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


## Disponibilize a caixa de nome para estilização por meio do objeto Character.
init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos

    adjust_spacing False

## Tela de entrada #############################################################
##
## Essa tela é usada para exibir renpy.input. O parâmetro prompt é usado para
## passar um prompt de texto.
##
## Essa tela deve criar um displayable de entrada com id "input" para aceitar os
## vários parâmetros de entrada.
##
## https://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xanchor gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Tela de escolha #############################################################
##
## Essa tela é usada para exibir as opções no jogo apresentadas pela instrução
## de menu. O único parâmetro, itens, é uma lista de objetos, cada um com campos
## de legenda e ação.
##
## https://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 405
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.text_properties("choice_button")


## Tela do menu rápido #########################################################
##
## O menu rápido é exibido no jogo para fornecer acesso fácil aos menus fora do
## jogo.

screen quick_menu():

    ## Certifique-se de que isso apareça na parte superior de outras telas.
    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 1.0

            #textbutton _("Voltar") action Rollback()
            textbutton _("Histórico") action ShowMenu('history')
            #textbutton _("Pular") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Menu") action ShowMenu('save')
            #textbutton _("Q.Salvar") action QuickSave()
            #textbutton _("Q. Carga") action QuickLoad()
            textbutton _("Config") action ShowMenu('preferences')


## Esse código garante que a tela quick_menu seja exibida no jogo, sempre que o
## jogador não tiver ocultado explicitamente a interface.
init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_button is default
style quick_button_text is button_text

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.text_properties("quick_button")


################################################################################
## Telas do menu principal e do menu do jogo
################################################################################

## Tela de navegação ###########################################################
##
## Essa tela está incluída nos menus principal e do jogo e fornece navegação
## para outros menus e para iniciar o jogo.

screen navigation:

    vbox:
        style_prefix "navigation"
        spacing gui.navigation_spacing

        if main_menu:

            xpos 150
            yalign 0.6

            textbutton _("Novo Jogo") action Start()

        else:

            xpos gui.navigation_xpos
            yalign 0.6

            textbutton _("Histórico") action ShowMenu("history")

            #textbutton _("Salvar") action ShowMenu("save")

        #textbutton _("Carregar Jogo") action ShowMenu("load")

        textbutton _("Configurações") action ShowMenu("preferences")

        if _in_replay:

            textbutton _("Fim da reprodução") action EndReplay(confirm=True)

        elif not main_menu:

            textbutton _("Menu principal") action MainMenu()

        textbutton _("Sobre") action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):

            ## A ajuda não é necessária ou relevante para dispositivos móveis.
            textbutton _("Ajuda") action ShowMenu("help")

        if renpy.variant("pc"):

            ## O botão Sair é proibido no iOS e desnecessário no Android e na
            ## Web.
            textbutton _("Sair") action Quit(confirm=not main_menu)


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.text_properties("navigation_button")


## Tela do menu principal ######################################################
##
## Usado para exibir o menu principal quando o Ren'Py é iniciado.
##
## https://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu():

    ## Isso garante que qualquer outra tela de menu seja substituída.
    tag menu

    add gui.main_menu_background

    ## Esse quadro vazio escurece o menu principal.
    frame:
        style "main_menu_frame"

    ## A instrução de uso inclui outra tela dentro desta. O conteúdo real do
    ## menu principal está na tela de navegação.
    use navigation

    if gui.show_name:

        vbox:
            style "main_menu_vbox"

            text "[config.name!t]":
                style "main_menu_title"


style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text


style main_menu_vbox:
    xalign 1.0
    xoffset -30
    xmaximum 1200
    yalign 1.0
    yoffset -30

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    properties gui.text_properties("title")

style main_menu_version:
    properties gui.text_properties("version")


## Tela do menu do jogo ########################################################
##
## Isso estabelece a estrutura básica comum de uma tela de menu de jogo. Ela
## é chamada com o título da tela e exibe o plano de fundo, o título e a
## navegação.
##
## O parâmetro de rolagem pode ser Nenhum ou um dos parâmetros "viewport"
## ou "vpgrid". Essa tela deve ser usada com um ou mais filhos, que são
## transcluídos (colocados) dentro dela.

screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):

    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background
    else:
        add gui.game_menu_background

    frame:
        style "game_menu_outer_frame"

        hbox:

            ## Reserve espaço para a seção de navegação.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            spacing spacing

                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        spacing spacing

                        transclude

                else:

                    transclude

    use navigation

    textbutton _("Voltar"):
        style "return_button"

        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 45
    top_padding 180

    background "gui/overlay/game_menu.png"

style game_menu_navigation_frame:
    xsize 420
    yfill True

style game_menu_content_frame:
    left_margin 60
    right_margin 30
    top_margin 15

style game_menu_viewport:
    xsize 1380

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 15

style game_menu_label:
    xpos 75
    ysize 180

##define o estilo do nome da aba de configurações
style game_menu_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -45


## Sobre a tela ################################################################
##
## Essa tela fornece informações de crédito e direitos autorais sobre o jogo e
## Ren'Py.
##
## Não há nada de especial nessa tela e, portanto, ela também serve como exemplo
## de como criar uma tela personalizada.

screen about():

    tag menu

    ## Essa instrução de uso inclui a tela game_menu dentro desta. O filho vbox
    ## é então incluído na janela de visualização dentro da tela game_menu.
    use game_menu(_("Sobre"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Versão [config.version!t]\n")

            ## gui.about é normalmente definido em options.rpy.
            if gui.about:
                text "[gui.about!t]\n"

            text _("Feito com {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only] .\n\n[renpy.license!t]")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Carregar e salvar telas #####################################################
##
## Essas telas são responsáveis por permitir que o jogador salve o jogo
## e o carregue novamente. Como elas têm quase tudo em comum, ambas são
## implementadas em termos de uma terceira tela, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save https://
## www.renpy.org/doc/html/screen_special.html#load

screen save():

    tag menu

    use file_slots(_("Salvar"))


screen load():

    tag menu

    use file_slots(_("Carga"))


screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Página {}"), auto=_("Salvamentos automáticos"), quick=_("Salvamentos rápidos"))

    use game_menu(title):

        fixed:

            ## Isso garante que a entrada receberá o evento enter antes de
            ## qualquer um dos botões.
            order_reverse True

            ## O nome da página, que pode ser editado clicando em um botão.
            button:
                style "page_label"

                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            ## A grade de slots de arquivo.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileAction(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("slot vazio")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            ## Botões para acessar outras páginas.
            vbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                hbox:
                    xalign 0.5

                    spacing gui.page_spacing

                    textbutton _("<") action FilePagePrevious()
                    key "save_page_prev" action FilePagePrevious()

                    if config.has_autosave:
                        textbutton _("{#auto_page}A") action FilePage("auto")

                    if config.has_quicksave:
                        textbutton _("{#quick_page}Q") action FilePage("quick")

                    ## range(1, 10) fornece os números de 1 a 9.
                    for page in range(1, 10):
                        textbutton "[page]" action FilePage(page)

                    textbutton _(">") action FilePageNext()
                    key "save_page_next" action FilePageNext()

                if config.has_sync:
                    if CurrentScreenName() == "save":
                        textbutton _("Upload Sync"):
                            action UploadSync()
                            xalign 0.5
                    else:
                        textbutton _("Baixar o Sync"):
                            action DownloadSync()
                            xalign 0.5


style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 75
    ypadding 5

style page_label_text:
    textalign 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.text_properties("slot_button")


## Tela de preferências ########################################################
##
## A tela de preferências permite que o jogador configure o jogo para se adequar
## melhor.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen preferences():

    tag menu

    use game_menu(_("Preferências"), scroll="viewport"):

        vbox:

            hbox:
                box_wrap True

                if renpy.variant("pc") or renpy.variant("web"):

                    vbox:
                        style_prefix "radio"
                        label _("Tela")
                        textbutton _("Janela") action Preference("display", "window")
                        textbutton _("Tela cheia") action Preference("display", "fullscreen")

                vbox:
                    style_prefix "check"
                    label _("Pular")
                    textbutton _("Texto invisível") action Preference("skip", "toggle")
                    textbutton _("Após as escolhas") action Preference("after choices", "toggle")
                    textbutton _("Transições") action InvertSelected(Preference("transitions", "toggle"))

                ## Vboxes adicionais do tipo "radio_pref" ou "check_pref" podem
                ## ser adicionadas aqui para acrescentar outras preferências
                ## definidas pelo criador.

            null height (4 * gui.pref_spacing)

            hbox:
                style_prefix "slider"
                box_wrap True

                vbox:

                    label _("Velocidade do texto")

                    bar value Preference("text speed")

                    label _("Tempo de encaminhamento automático")

                    bar value Preference("auto-forward time")

                vbox:

                    if config.has_music:
                        label _("Volume da música")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:

                        label _("Volume do som")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Teste") action Play("sound", config.sample_sound)


                    if config.has_voice:
                        label _("Volume da voz")

                        hbox:
                            bar value Preference("voice volume")

                            if config.sample_voice:
                                textbutton _("Teste") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("Silenciar tudo"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 3

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 338

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.text_properties("check_button")

style slider_slider:
    xsize 525

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 15

style slider_button_text:
    properties gui.text_properties("slider_button")

style slider_vbox:
    xsize 675


## Tela de histórico ###########################################################
##
## Essa é uma tela que exibe o histórico de diálogo para o jogador. Embora não
## haja nada de especial nessa tela, ela precisa acessar o histórico de diálogo
## armazenado em _history_list.
##
## https://www.renpy.org/doc/html/history.html

screen history():

    tag menu

    ## Evite prever essa tela, pois ela pode ser muito grande.
    predict False

    use game_menu(_("Histórico"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0, spacing=gui.history_spacing):

        style_prefix "history"

        for h in _history_list:

            window:

                ## Isso organiza as coisas corretamente se history_height for
                ## None.
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"
                        substitute False

                        ## Pegue a cor do texto who do caractere, se definido.
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False

        if not _history_list:
            label _("O histórico de diálogo está vazio.")


## Isso determina quais tags podem ser exibidas na tela de histórico.

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


## Tela de ajuda ###############################################################
##
## Uma tela que fornece informações sobre as combinações de teclas e mouse. Ela
## usa outras telas (keyboard_help, mouse_help e gamepad_help) para exibir a
## ajuda real.

screen help():

    tag menu

    default device = "keyboard"

    use game_menu(_("Ajuda"), scroll="viewport"):

        style_prefix "help"

        vbox:
            spacing 23

            hbox:

                textbutton _("Teclado") action SetScreenVariable("device", "keyboard")
                textbutton _("Mouse") action SetScreenVariable("device", "mouse")

                if GamepadExists():
                    textbutton _("Controle de jogo") action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help


screen keyboard_help():

    hbox:
        label _("Enter")
        text _("Avança o diálogo e escolhe a opção selecionada.")

    hbox:
        label _("Espaço")
        text _("Avança o diálogo sem selecionar opções.")

    hbox:
        label _("Teclas de seta")
        text _("Navegue pela interface.")

    hbox:
        label _("Esc")
        text _("Acessa o menu do jogo.")

    ##hbox:
    ##    label _("Ctrl")
    ##    text _("Pula o diálogo quando pressionado.")

    ##hbox:
    ##    label _("Tab")
    ##    text _("Alterna o salto de diálogo.")

    ##hbox:
    ##    label _("Página para cima")
    ##    text _("Volta ao diálogo anterior.")

    ##hbox:
    ##    label _("Página para baixo")
    ##    text _("Rola para frente o diálogo posterior.")

    hbox:
        label "H"
        text _("Oculta a interface do usuário.")

    hbox:
        label "S"
        text _("Faz uma captura de tela.")

    hbox:
        label "V"
        text _("Alterna a assistência {a=https://www.renpy.org/l/voicing}auto-voz{/a}.")

    hbox:
        label "Shift+A"
        text _("Abre o menu de acessibilidade.")


screen mouse_help():

    hbox:
        label _("Clique com o botão esquerdo do mouse")
        text _("Avança o diálogo e escolhe a opção selecionada.")

    hbox:
        label _("Clique com a rodinha do mouse")
        text _("Oculta a interface do usuário.")

    hbox:
        label _("Clique com o botão direito do mouse")
        text _("Acessa o menu do jogo.")

    ##hbox:
    ##    label _("Roda do mouse para cima\nClique em Rollback Side")
    ##    text _("Volta ao diálogo anterior.")

    ##hbox:
    ##    label _("Roda do mouse para baixo")
    ##    text _("Rola para frente o diálogo posterior.")


screen gamepad_help():

    hbox:
        label _("Gatilho direito\nBotão A/inferior")
        text _("Avança o diálogo e ativa a interface.")

    ##hbox:
    ##    label _("Gatilho esquerdo\nOmbro esquerdo")
    ##    text _("Volta ao diálogo anterior.")

    ##hbox:
    ##    label _("Ombro direito")
    ##    text _("Rola para frente o diálogo posterior.")

    hbox:
        label _("D-Pad, bastões")
        text _("Navegue pela interface.")

    hbox:
        label _("Start, Guide, B/Right Button")
        text _("Acessa o menu do jogo.")

    hbox:
        label _("Botão Y/Top")
        text _("Oculta a interface do usuário.")

    textbutton _("Calibrar") action GamepadCalibrate()


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin 12

style help_button_text:
    properties gui.text_properties("help_button")

style help_label:
    xsize 375
    right_padding 30

style help_label_text:
    size gui.text_size
    xalign 1.0
    textalign 1.0



################################################################################
## Telas adicionais
################################################################################


## Confirmar tela ##############################################################
##
## A tela de confirmação é chamada quando Ren'Py quer fazer uma pergunta de sim
## ou não ao jogador.
##
## https://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Certifique-se de que outras telas não recebam entrada enquanto essa tela
    ## estiver sendo exibida.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 45

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 150

                textbutton _("Sim") action yes_action
                textbutton _("Não") action no_action

    ## Clique com o botão direito do mouse e escape a resposta "não".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    textalign 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.text_properties("confirm_button")


## Pular a tela do indicador ###################################################
##
## A tela skip_indicator é exibida para indicar que o salto está em andamento.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 9

            text _("Pular")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## Essa transformação é usada para piscar as setas uma após a outra.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## Temos que usar uma fonte que tenha o glifo BLACK RIGHT-POINTING SMALL
    ## TRIANGLE.
    font "DejaVuSans.ttf"


## Tela de notificação #########################################################
##
## A tela de notificação é usada para mostrar uma mensagem ao jogador. (Por
## exemplo, quando o jogo é salvo rapidamente ou quando uma captura de tela é
## feita).
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 5 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")


## Tela NVL ####################################################################
##
## Essa tela é usada para o diálogo e os menus do modo NVL.
##
## https://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## Exibe o diálogo em uma vpgrid ou na vbox.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## Exibe o menu, se fornecido. O menu poderá ser exibido incorretamente
        ## se config.narrator_menu estiver definido como True.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## Isso controla o número máximo de entradas do modo NVL que podem ser exibidas
## de uma vez.
define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    textalign gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    textalign gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    textalign gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.text_properties("nvl_button")


## Tela de bolhas ##############################################################
##
## A tela de balão é usada para exibir o diálogo para o jogador ao usar balões
## de fala. A tela de bolhas recebe os mesmos parâmetros que a tela de dizer,
## deve criar um exibível com o ID de "what" e pode criar exibíveis com os IDs
## "namebox", "who" e "window".
##
## https://www.renpy.org/doc/html/bubble.html#bubble-screen

screen bubble(who, what):
    style_prefix "bubble"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "bubble_namebox"

                text who:
                    id "who"

        text what:
            id "what"

style bubble_window is empty
style bubble_namebox is empty
style bubble_who is default
style bubble_what is default

style bubble_window:
    xpadding 30
    top_padding 5
    bottom_padding 5

style bubble_namebox:
    xalign 0.5

style bubble_who:
    xalign 0.5
    textalign 0.5
    color "#000"

style bubble_what:
    align (0.5, 0.5)
    text_align 0.5
    layout "subtitle"
    color "#000"

define bubble.frame = Frame("gui/bubble.png", 55, 55, 55, 95)
define bubble.thoughtframe = Frame("gui/thoughtbubble.png", 55, 55, 55, 55)

define bubble.properties = {
    "bottom_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "bottom_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "top_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "top_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "thought" : {
        "window_background" : bubble.thoughtframe,
    }
}

define bubble.expand_area = {
    "bottom_left" : (0, 0, 0, 22),
    "bottom_right" : (0, 0, 0, 22),
    "top_left" : (0, 22, 0, 0),
    "top_right" : (0, 22, 0, 0),
    "thought" : (0, 0, 0, 0),
}



################################################################################
## Variantes do celular
################################################################################

style pref_vbox:
    variant "medium"
    xsize 675

## Como o mouse pode não estar presente, substituímos o menu rápido por uma
## versão que usa menos botões e maiores, que são mais fáceis de tocar.
screen quick_menu():
    variant "touch"

    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 1.0

            textbutton _("Voltar") action Rollback()
            textbutton _("Pular") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Automotivo") action Preference("auto-forward", "toggle")
            textbutton _("Menu") action ShowMenu()


style window:
    variant "small"
    background "gui/phone/textbox.png"

style radio_button:
    variant "small"
    foreground "gui/phone/button/radio_[prefix_]foreground.png"

style check_button:
    variant "small"
    foreground "gui/phone/button/check_[prefix_]foreground.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"

style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main_menu.png"

style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game_menu.png"

style game_menu_navigation_frame:
    variant "small"
    xsize 510

style game_menu_content_frame:
    variant "small"
    top_margin 0

style pref_vbox:
    variant "small"
    xsize 600

style bar:
    variant "small"
    ysize gui.bar_size
    left_bar Frame("gui/phone/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/phone/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    variant "small"
    xsize gui.bar_size
    top_bar Frame("gui/phone/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/phone/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    variant "small"
    ysize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    variant "small"
    xsize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    variant "small"
    ysize gui.slider_size
    base_bar Frame("gui/phone/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/horizontal_[prefix_]thumb.png"

style vslider:
    variant "small"
    xsize gui.slider_size
    base_bar Frame("gui/phone/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/vertical_[prefix_]thumb.png"

style slider_vbox:
    variant "small"
    xsize None

style slider_slider:
    variant "small"
    xsize 900


################################################################################
## Telas 
##############################################################################S##

## Tela que escreve onde o jogador vai ao passar o mouse pelo botao
screen texto_botao:
    default displayText = ""
    default x = 0
    default y = 0
    vbox:
        xpos x
        ypos y
        frame:
            text displayText

#################################### Definindo imagens ##################################################
image botao_passos = "botoes/pezinhos gulosos.png"

###################################################### Telas de lugares ###################################################
#Tela da taverna ext
screen tavernaext:
    tag passos
    use botao("botao_passos", 0.5, (750, 750), "Entrar no albergo", "tavernaint")
    use botao("botao_passos", 0.5, (150, 500), "Casa do bêbado", "casabebadoext")
    use botao("botao_passos", 0.5, (1670, 900), "Casa da Holga", "casaholgaext", False)

## Taverna interna
screen tavernaint():
    use botao("botao_passos", 0.5, (1800, 600), "Sair do albergo", "tavernaext")
    use botao("botao_passos", 0.5, (150, 500), "Entrar no quarto", "casapadre")
    if personagens_dict["Vincent"].vivo:
        use botao(personagens_dict["Vincent"].imagem, 0.10, (1250, 50), "Falar com o dono", "dialogo_vincent", False)
    if personagens_dict["Seren"].vivo and personagens_dict["Vincent"].progresso >= 2:
        use botao(personagens_dict["Seren"].imagem, 0.3, (900, 500), "Falar com a garota", "dialogo_seren")
    add "botoes/taverna balcao.png"

screen casaSalvatoreINT():
    tag passos
    use botao("botao_passos", 0.5, (150, 900), "Sair da casa", "caminhobebado_margarida")
    if personagens_dict["William"].vivo and personagens_dict["Salvatore"].progresso >= 2:
        use botao(personagens_dict["William"].imagem, 0.18, (900, 200), "Falar com o garoto", "dialogo_william")

###Tela da casa do bebado ext
screen casabebado():
    tag passos
    use botao("botao_passos", 0.5, (1700, 900), "Albergo", "tavernaext", False)
    use botao("botao_passos", 0.5, (170, 900), "Casa do senhor", "caminhobebado_margarida", False)
    if personagens_dict["Bêbado"].vivo:
        use botao(personagens_dict["Bêbado"].imagem, 0.14, (900, 350), "Falar com o bêbado", "dialogo_bebado")

## Tela da casa do padre interna
screen casapadre():
    tag passos
    if interacao > 0:
        use botao("botao_passos", 0.5, (1200, 900), "Sair do quarto", "tavernaint", False)
    use botao("mural de pistas", 0.99, (845, 254), "Ver quadro de pistas", "noite")

## Tela da casa da curandeira externa
screen casaMargaridaEXT():
    tag passos
    use botao("botao_passos", 0.5, (1300, 950), "Casa do senhor", "caminhobebado_margarida")
    use botao("botao_passos", 0.5, (90, 900), "Ponte", "caminhoLazaro")
    if personagens_dict["Margarida"].vivo:
        use botao(personagens_dict["Margarida"].imagem, 0.13, (1000, 500), "Falar com a curandeira", "dialogo_margarida")

## Tela da casa do Lázaro externa
screen casaLazaroEXT():
    tag passos
    use botao("botao_passos", 0.5, (1250, 900), "Casa da curandeira", "casamargaridaext")
    use botao("botao_passos", 0.5, (1000, 300), "Entrar na casa do leproso", "casaLazaroint")
    use botao("botao_passos", 0.5, (600, 900), "Casa da costureira", "casajoanaext")

## Tela da casa do Lázaro interna
screen casaLazaroINT():
    tag passos
    use botao("botao_passos", 0.5, (1100, 900), "Sair da casa", "caminhoLazaro", False)
    if personagens_dict["Lázaro"].vivo:
        use botao(personagens_dict["Lázaro"].imagem, 0.14, (500, 400), "Falar com o leproso", "dialogo_lazaro", False)  

## Tela da frente da casa do salvatore
screen caminhobebado_margarida():
    tag passos
    use botao("botao_passos", 0.5, (1600, 900), "Casa do bêbado", "casabebadoext")
    use botao("botao_passos", 0.5, (90, 900), "Albergo", "tavernaext")
    use botao("botao_passos", 0.5, (1000, 300), "Casa da curandeira", "casamargaridaext")
    use botao("botao_passos", 0.5, (300, 300), "Casa do senhor", "casasalvatoreint")
    if personagens_dict["Salvatore"].vivo:
        use botao(personagens_dict["Salvatore"].imagem, 0.12, (700, 320), "Falar com o senhor da vila", "dialogo_salvatore")

## Holga
screen casaHolgaEXT():
    tag passos
    use botao("botao_passos", 0.5, (100, 900), "Albergo", "tavernaext")
    use botao("botao_passos", 0.5, (1700, 900), "Monumento", "praca2")
    if personagens_dict["Holga"].vivo:
        use botao(personagens_dict["Holga"].imagem, 0.5, (700, 420), "Falar com a a irmã da Edla", "dialogo_holga", False) 

## Praca 2
screen praca2():
    tag passos
    use botao("botao_passos", 0.5, (400, 500), "Casa da irmã da Edla", "casaholgaext")
    use botao("botao_passos", 0.5, (500, 900), "Piazza", "praca1")
    if personagens_dict["Agnes"].vivo:
        use botao(personagens_dict["Agnes"].imagem, 0.55, (900, 400), "Falar com a pedinte", "dialogo_agnes", False)

screen praca1():
    tag passos
    use botao("botao_passos", 0.5, (1000, 900), "Monumento", "praca2", False)
    use botao("botao_passos", 0.5, (450, 650),   "Entrar na igreja", "igreja")
    use botao("botao_passos", 0.5, (1200, 600), "Entrar na padaria", "padaria")
    use botao("botao_passos", 0.5, (1600, 900), "Casa da costureira", "casajoanaext")

screen igrejaINT():
    tag passos
    use botao("botao_passos", 0.5, (900, 870), "Piazza", "praca1", False)

screen padariaINT():
    tag passos
    use botao("botao_passos", 0.5, (300, 900), "Piazza", "praca1", False)
    if personagens_dict["Bartolomeu"].vivo:
        use botao(personagens_dict["Bartolomeu"].imagem, 0.30, (1400, 300), "Falar com o padeiro", "dialogo_bartolomeu", False)

screen casaJoanaEXT():
    tag passos
    use botao("botao_passos", 0.5, (200, 900), "Piazza", "praca1")
    use botao("botao_passos", 0.5, (350, 400), "Campagna", "plantacao")
    use botao("botao_passos", 0.5, (1600, 900), "Ponte", "caminhoLazaro")
    if personagens_dict["Joana"].vivo:
        use botao(personagens_dict["Joana"].imagem, 0.11, (600, 470), "Falar com a costureira", "dialogo_joana")

screen plantacao():
    tag passos
    use botao("botao_passos", 0.5, (400, 910), "Casa da costureira", "casajoanaext", False)

############################################################# FUNÇÂO BOTÂO ##############################################################

screen botao(imagem, zoomBase, posicao, texto, jumpTo, textoEmBaixo=True):
    tag passos
    vbox:
        xanchor 0.5
        yanchor 0.0
        xpos posicao[0]
        ypos posicao[1]

        default displayText = ""
        if not textoEmBaixo:
            text displayText xalign 0.5 outlines [ ( 3, "#000005", 0, 0) ]
        imagebutton:
            xalign 0.5
            idle imagem
            hover imagem
            at transform:
                zoom zoomBase
                on hover:
                    linear 0.05 zoom 1.1*zoomBase  # Zooms to 110% over 0.05 seconds
                on idle:
                    linear 0.1 zoom zoomBase  # Returns to original size over 0.1 seconds
            action [SetLocalVariable("displayText", ""), Jump(jumpTo)]

            hovered SetLocalVariable("displayText", texto)
            unhovered SetLocalVariable("displayText", "")
        if textoEmBaixo:
            text displayText xalign 0.5 outlines [ ( 3, "#000005", 0, 0) ]

    
screen botao_pistas(personagem, zoomBase, posicao):
    tag passos
    python:
        retrato = personagem.retrato
        if personagem.conhecido == False:
            retrato = At(retrato, preto)
        elif personagem.vivo == False:
            retrato = At(retrato, preto_e_branco)
    
    imagebutton:
        xanchor 0.5
        yanchor 1.0
        xpos posicao[0]
        ypos posicao[1]
        idle retrato
        hover retrato
        at transform:
            zoom zoomBase
            on hover:
                linear 0.05 zoom 1.1*zoomBase  # Zooms to 110% over 0.05 seconds
            on idle:
                linear 0.1 zoom zoomBase  # Returns to original size over 0.1 seconds
        if personagem.conhecido:
            action [SetVariable("infoPersonagem", personagem.nome), Jump("pistas")]
        else:
            action Notify("Ainda não conheço este personagem...")
    if personagem.nome != "Bruxa":
        frame:
            background None
            xanchor 0.5
            yanchor 1.0
            xpos posicao[0]
            ypos posicao[1] + 60
            text personagem.nomeConhecido size 40 color "#382114" outlines [ ( 1, "#000005", 0, 0) ] font "UnifrakturMaguntia-Regular.ttf"

screen botao_quadro(imagem, zoomBase, posicaoY, passarDia):
    tag passos
    imagebutton:
        xalign 0.5
        yanchor 0.0
        ypos posicaoY
        idle imagem
        hover imagem
        at transform:
            zoom zoomBase
            on hover:
                linear 0.05 zoom 1.1*zoomBase  # Zooms to 110% over 0.05 seconds
            on idle:
                linear 0.1 zoom zoomBase  # Returns to original size over 0.1 seconds
        if passarDia:
            action [Function(passar_dia)]
        else:
            action [Jump("casapadre")]

############################################################# Hud ################################################
screen HUD():
    $ imagePath = ""
    $ zoomInteracao = 0.8
    hbox:
        xpos 25
        ypos 25
        spacing 25
        for i in range(1, interacao+1): # Interações disponíveis
            if i > 0 and i <= 3:
                $ imagem = imagePath + "interacao_normal_disponivel"
            else:
                $ imagem = imagePath + "interacao_bonus_disponivel"
            add imagem zoom zoomInteracao

        for i in range(interacaoMaxHoje, interacao, -1): # Interações indisponíveis
            if i >= 4:
                $ imagem = imagePath + "interacao_bonus_indisponivel"
            else:
                $ imagem = imagePath + "interacao_normal_indisponivel"
            add imagem zoom zoomInteracao

    frame:
        background None
        xpos 1355
        ypos -30
        add str(dia) + "_dia" zoom 0.8

######################################################### Falas de personagens ##############################################################

image lazaroN = "personagens/lazaro/lazaro neutro.png"
image lazaroF = "personagens/lazaro/lazaro felicidade.png"
image lazaroR = "personagens/lazaro/lazaro raiva.png"
image lazaroT = "personagens/lazaro/lazaro tristeza.png"

image vincentN = "personagens/vincent/vincent neutro.png"
image vincentF = "personagens/vincent/vincent felicidade.png"
image vincentR = "personagens/vincent/vincent raiva.png"
image vincentT = "personagens/vincent/vincent tristeza.png"

image margaridaN = "personagens/margarida/margarida neutra.png" 
image margaridaF = "personagens/margarida/margarida felicidade.png" 
image margaridaR = "personagens/margarida/margarida raiva.png" 
image margaridaT = "personagens/margarida/margarida tristeza.png" 

image padreN = "personagens/padre/padre neutro.png"
image padreF = "personagens/padre/padre felicidade.png"
image padreR = "personagens/padre/padre raiva.png"
image padreT = "personagens/padre/padre tristeza.png"

image holgaN = "personagens/holga/holga neutra.png"
image holgaF = "personagens/holga/holga felicidade.png"
image holgaR = "personagens/holga/holga raiva.png"
image holgaT = "personagens/holga/holga tristeza.png"

image bartolomeuN = "personagens/bartolomeu/bartolomeu neutro.png"
image bartolomeuF = "personagens/bartolomeu/bartolomeu felicidade.png"
image bartolomeuR = "personagens/bartolomeu/bartolomeu raiva.png"
image bartolomeuT = "personagens/bartolomeu/bartolomeu tristeza.png"

image bebadoN = "personagens/bebado/bebado neutro.png"
image bebadoF = "personagens/bebado/bebado felicidade.png"
image bebadoR = "personagens/bebado/bebado raiva.png"
image bebadoT = "personagens/bebado/bebado tristeza.png"

image agnesN = "personagens/agnes/agnes neutra.png"
image agnesF = "personagens/agnes/agnes felicidade.png"
image agnesR = "personagens/agnes/agnes raiva.png"
image agnesT = "personagens/agnes/agnes tristeza.png"

image joanaN = "personagens/joana/joana neutra.png"
image joanaR = "personagens/joana/joana raiva.png"
image joanaT = "personagens/joana/joana tristeza.png"

image salvatoreN = "personagens/salvatore/salvatore neutro.png"
image salvatoreF = "personagens/salvatore/salvatore felicidade.png"
image salvatoreR = "personagens/salvatore/salvatore raiva.png"
image salvatoreT = "personagens/salvatore/salvatore tristeza.png"

image serenN = "personagens/seren/seren neutra.png"
image serenF = "personagens/seren/seren felicidade.png"
image serenR = "personagens/seren/seren raiva.png"
image serenT = "personagens/seren/seren tristeza.png"

image williamN = "personagens/william/william neutro.png"
image williamF = "personagens/william/william felicidade.png"
image williamR = "personagens/william/william raiva.png"
image williamT = "personagens/william/william tristeza.png"

image bruxaN = "personagens/bruxa/bruxa neutra.png"
image bruxaR = "personagens/bruxa/bruxa raiva.png"
image bruxaC = "personagens/bruxa/bruxa capa.png"
image bruxaI = "personagens/bruxa/bruxa insana.png"

screen personagemEmocao(personagem, emocao):
    if personagem == "Padre":
        add unidecode(personagem).lower()+emocao at padre_left
    else:
        add unidecode(personagem).lower()+emocao at personagens_dict[personagem].transform 

############################################################### Esconde as telas ######################################################
label hide_all_screens:
    hide screen casabebado
    hide screen tavernaext
    hide screen tavernaint
    hide screen casapadre
    hide screen casaMargaridaEXT
    hide screen casaLazaroEXT
    hide screen casaLazaroINT
    hide screen caminhobebado_margarida
    hide screen casaHolgaEXT
    hide screen praca2
    hide screen praca1
    hide screen igrejaINT
    hide screen padariaINT
    hide screen casaJoanaEXT
    hide screen plantacao
    hide screen casaSalvatoreINT

    hide screen personagemEmocao

    hide screen pistas
    hide screen vincent_pistas

    hide screen pistas
    hide screen vincent_pistas

    hide screen botao
    return


################################# PISTAS ##############################################
image tela preta = Solid("#000")
image tela branca = Solid("#FFFFFF")

screen pistas():
    tag pistas
    add "pistas_idle.jpg"
    for personagem in personagens_list:
        $ personagem = personagens_dict[personagem[1]]
        $ zoom = 0.14 if personagem.nome != "Bruxa" else 0.3
        use botao_pistas(personagem, zoom, personagem.posicao)
    if interacao <= 0:
        use botao_quadro("botao nao matar", 0.85, 880, True)
    else:
        use botao_quadro("voltar", 0.3, 900, False)

style word_list is button:
    background None

style word_list_text is text:
    size 45
    hover_color "#2E1F34"            
    outlines [ (3, "#FFFFFF", 1, 1) ]
    color "#000000"


screen pistas_personagem(personagem):
    tag pistas
    add "fundo pistas.png"
    $ genero = "o" if personagens_dict[personagem].genero == 'M' else "a"
    frame:
        xysize(850,550)
        xpos 70
        ypos 370
        vbox:
            text "Informações encontradas:"
            text pistas_list[0]
            text pistas_list[1]
            text pistas_list[2]
            text pistas_list[3]
            text pistas_list[4]

    python:
        retrato = personagens_dict[personagem].retrato
        if personagens_dict[personagem].vivo == False:
            retrato = At(retrato, preto_e_branco)

    add retrato at zoom_retrato

    text personagens_dict[personagem].nomeConhecido:
        size 90
        xpos 310
        ypos 130
        font "UnifrakturMaguntia-Regular.ttf"
        color "#382114" 
        outlines [ ( 1, "#000005", 0, 0) ]

    frame: 
        xysize(900, 280)
        xpos 0.5
        ypos 70
        vbox:
            text "Descrição do personagem:"
            text personagens_dict[personagem].descricao

    frame:
        background None
        xpos 150
        ypos 930
        textbutton "Voltar" style "word_list":
            action Jump("noite") alt "Noite"

    if personagem != "Bruxa" and personagens_dict[personagem].vivo and pistas_list[0] != "" and interacao <= 0:
        frame:
            xpos 400
            ypos 930
            textbutton "Matar " + personagens_dict[personagem].nomeConhecido style "word_list":
                action [SetVariable("matar_personagem", personagem), Function(passar_dia)]

    frame:
        xysize(900,650)
        xpos 0.5
        ypos 370
        if personagem != "Bruxa":
            vbox:
                text "Falas de destaque:"
                text falas_list[0]
                text falas_list[1]
                text falas_list[2]
                text falas_list[3]
                text falas_list[4]
                text falas_list[5]
                text falas_list[6]

screen notificacao(mensagem):
    frame:
        xalign 0.5
        yalign 0.5
        xmaximum 960
        vbox:
            text "Pista Adquirida!" xalign 0.5 size 40 outlines [ (3, "#000000", 1, 1) ]
            text mensagem
            text ""
            button:
                xalign 0.5
                text "Fechar"
                action Return()


# screen Movie(file):
#     layer "background"
#     add "[file]" xpos 0 ypos 0