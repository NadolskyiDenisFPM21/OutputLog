import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label



import db

# Установка белого фона приложения
Window.clearcolor = (1, 1, 1, 1)

KV = '''
ScreenManager:
    InitialScreen:
    MainScreen:
    ReturnScreen:

<InitialScreen>:
    name: 'initial'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)

        Widget:
            size_hint_y: 0.3

        MyButton:
            text: 'Записаться на выход'
            size_hint_y: None
            height: dp(60)
            font_size: '20sp'
            on_release: 
                app.root.current = 'main'

        MyButton:
            text: 'Возврат'
            size_hint_y: None
            height: dp(60)
            font_size: '20sp'
            on_release: 
                app.root.current = 'return'

        Widget:
            size_hint_y: 0.3

<MainScreen>:
    name: 'main'
    ExitScreen:

<ReturnScreen>:
    name: 'return'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)

        BoxLayout:
            size_hint_y: None
            height: dp(54)
            TextInput:
                id: return_name_input
                user_id: None
                hint_text: 'Введите ваше имя'
                multiline: False
                size_hint_y: None
                height: dp(44)
                font_size: '16sp'
                foreground_color: (0, 0, 0, 1)
                background_color: (0.95, 0.95, 0.95, 1)
                cursor_color: (0, 0, 0, 1)
                padding: dp(10)
                on_text: root.update_return_name_list(self.text)

        RecycleView:
            id: return_name_list
            size_hint_y: None
            height: min(self.layout_manager.minimum_height, dp(150))
            viewclass: 'MyButton'
            RecycleBoxLayout:
                default_size: None, dp(44)
                default_size_hint: 1, None
                size_hint_y: None
                orientation: 'vertical'
                height: self.minimum_height

        Widget:
            size_hint_y: .3

        MyButton:
            text: 'Запись'
            size_hint_y: None
            height: dp(50)
            font_size: '16sp'
            background_color: (0.2, 0.6, 0.86, 1)
            color: (1, 1, 1, 1)
            on_release: 
                root.record_return()
                app.root.current = 'initial'

        MyButton:
            text: 'Назад'
            size_hint_y: None
            height: dp(50)
            font_size: '16sp'
            background_color: (0.8, 0.8, 0.8, 1)
            color: (0, 0, 0, 1)
            on_release: app.root.current = 'initial'
        
        Widget:
            size_hint_y: .3

<CustomSpinner@Spinner>:
    background_normal: ''
    background_color: 0.95, 0.95, 0.95, 1
    color: 0, 0, 0, 1
    option_cls: 'CustomSpinnerOption'
    canvas.before:
        Color:
            rgba: 0.8, 0.8, 0.8, 1
        Line:
            width: 1
            rectangle: self.x, self.y, self.width, self.height
    canvas.after:
        Color:
            rgba: 0, 0, 0, 1
        Triangle:
            points: [self.right - dp(15), self.center_y - dp(5), self.right - dp(5), self.center_y - dp(5), self.right - dp(10), self.center_y + dp(5)]

<CustomSpinnerOption@SpinnerOption>:
    background_normal: ''
    background_color: 0.95, 0.95, 0.95, 1
    color: 0, 0, 0, 1
    height: dp(44)

<MCQCheckBox@CheckBox>:
    color: 0, 0, 0, 1
    size_hint: 0.15, 1

<MCQLabel@ButtonBehavior+Label>:
    text_size: self.size
    valign: 'center'
    font_size: '20sp'
    color: 0, 0, 0, 1

<MCQLabelCheckBox@BoxLayout>:
    text: ''
    size_hint_y: None
    height: dp(44)
    MCQCheckBox:
        id: cb
        on_active: root.set_inactive()
    MCQLabel:
        on_press: cb._do_press()
        text: root.text

<MyButton@Button>:
    background_normal: ''
    background_color: (0.95, 0.95, 0.95, 1)
    color: (0.15, 0.15, 0.15, 1)
    font_size: '16sp'
    size_hint_y: None
    height: dp(44)
    canvas.before:
        Color:
            rgba: self.background_color

<ExitScreen>:
    orientation: 'vertical'
    padding: dp(10)
    spacing: dp(10)

    BoxLayout:
        size_hint_y: None
        height: dp(54)
        TextInput:
            id: name_input
            user_id: None
            hint_text: 'Введите ваше имя'
            multiline: False
            size_hint_y: None
            height: dp(44)
            font_size: '16sp'
            foreground_color: (0, 0, 0, 1)
            background_color: (0.95, 0.95, 0.95, 1)
            cursor_color: (0, 0, 0, 1)
            padding: dp(10)
            on_text: root.update_name_list(self.text)

    ScrollView:
        do_scroll_x: False
        do_scroll_y: True
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            spacing: dp(10)

            RecycleView:
                id: name_list
                size_hint_y: None
                height: min(self.layout_manager.minimum_height, dp(150))
                viewclass: 'MyButton'
                RecycleBoxLayout:
                    default_size: None, dp(44)
                    default_size_hint: 1, None
                    size_hint_y: None
                    orientation: 'vertical'
                    height: self.minimum_height

            CustomSpinner:
                id: reason_spinner
                text: 'Выберите причину'
                values: ['По работе', 'По личным вопросам']
                size_hint_y: None
                height: dp(44)
                font_size: '16sp'

            TextInput:
                id: comment_input
                hint_text: 'Комментарий'
                size_hint_y: None
                height: dp(100)
                font_size: '16sp'
                foreground_color: (0, 0, 0, 1)
                background_color: (0.95, 0.95, 0.95, 1)
                cursor_color: (0, 0, 0, 1)
                padding: dp(10)

            
            MCQLabelCheckBox:
                id: start_of_day_checkbox
                text: 'С начала рабочего дня по сейчас'
                    
        
            
            MCQLabelCheckBox:
                id: end_of_day_checkbox
                text: 'До конца рабочего дня'
                    
        
            MyButton:
                text: 'Записать'
                size_hint_y: None
                height: dp(50)
                font_size: '16sp'
                background_color: (0.2, 0.6, 0.86, 1)
                color: (1, 1, 1, 1)
                on_release: 
                    root.record_data()
                    app.root.current = 'initial'
        
            MyButton:
                text: 'Назад'
                size_hint_y: None
                height: dp(50)
                font_size: '16sp'
                background_color: (0.8, 0.8, 0.8, 1)
                color: (0, 0, 0, 1)
                on_release: app.root.current = 'initial'
'''


class MyButton(Button):
    pass


class InitialScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class ReturnScreen(Screen):
    users = db.get_users()

    def find_users(self, text, users):
        return [(user['id'], user['fullname']) for user in users if (text.lower() in user['fullname'].lower())]

    def update_return_name_list(self, text):
        if text:
            matches = self.find_users(text, self.users)
            self.ids.return_name_list.data = [{'text': name, 'size_hint_y': None, 'height': dp(44),
                                               'on_release': lambda name=name, user_id=id: self.select_return_name(name, user_id)} for id, name in matches]
        else:
            self.ids.return_name_list.data = []

    def select_return_name(self, name, id):
        self.ids.return_name_input.text = name
        self.ids.return_name_input.user_id = id
        self.ids.return_name_list.data = []

    def record_return(self):
        name = self.ids.return_name_input.text
        user_id = self.ids.return_name_input.user_id

        # Popup notification with wrapped text and increased width
        popup_content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        popup_label = Label(
            text=f"Запись возврата для пользователя:\nИмя: {name}\nВремя: {datetime.datetime.now()}",
            text_size=(dp(350), None),  # Set a width limit for text wrapping
            halign="left",
            valign="top"
        )
        popup_label.bind(size=popup_label.setter('text_size'))  # Adjust text size based on label size
        popup_content.add_widget(popup_label)

        ok_button = MyButton(text='OK', size_hint_y=None, height=dp(50))
        popup_content.add_widget(ok_button)

        popup = Popup(
            title="Запись создана",
            content=popup_content,
            size_hint=(None, None),
            size=(400, 200)  # Increased width and height
        )
        ok_button.bind(on_release=popup.dismiss)
        popup.open()

        # Clear input fields
        self.ids.return_name_input.text = ''


class MCQLabelCheckBox(BoxLayout):
    def set_inactive(self, *args):
        # Находим все BoxLayout, которые содержат чекбоксы
        if self.ids.cb.active:
            parent = self.parent  # Получаем доступ к основному BoxLayout
            checkboxes = [child for child in parent.children if isinstance(child, MCQLabelCheckBox) and child != self]
            for checkbox in checkboxes:
                checkbox.ids.cb.active = False



class ExitScreen(BoxLayout):
    users = db.get_users()


    def find_users(self, text, users):
        return [(user['id'], user['fullname']) for user in users if text.lower() in user['fullname'].lower() and user['in_office']]

    def update_name_list(self, text):
        if text:
            matches = self.find_users(text, self.users)
            self.ids.name_list.data = [{'text': name, 'size_hint_y': None, 'height': dp(44),
                                        'on_release': lambda name=name, user_id=id: self.select_name(name, user_id)} for id, name in matches]
        else:
            self.ids.name_list.data = []

    def select_name(self, name, id):
        self.ids.name_input.text = name
        self.ids.name_input.user_id = id
        self.ids.name_list.data = []

    def record_data(self):
        name = self.ids.name_input.text
        user_id = self.ids.name_input.user_id
        reason = self.ids.reason_spinner.text
        comment = self.ids.comment_input.text
        end_of_day = self.ids.end_of_day_checkbox.ids.cb.active
        start_of_day = self.ids.start_of_day_checkbox.ids.cb.active

        # Popup notification with wrapped text and increased width
        popup_content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        popup_label = Label(
            text=f"Имя: {name}\nПричина: {reason}\nКомментарий: {comment}\nС начала рабочего дня по сейчас: {'Да' if start_of_day else 'Нет'}\nДо конца рабочего дня: {'Да' if end_of_day else 'Нет'}\nВремя: {datetime.datetime.now()}",
            text_size=(dp(350), None),  # Set a width limit for text wrapping
            halign="left",
            valign="top"
        )
        popup_label.bind(size=popup_label.setter('text_size'))  # Adjust text size based on label size
        popup_content.add_widget(popup_label)

        ok_button = MyButton(text='OK', size_hint_y=None, height=dp(50))
        popup_content.add_widget(ok_button)

        popup = Popup(
            title="Запись создана",
            content=popup_content,
            size_hint=(None, None),
            size=(400, 300)  # Increased width and height
        )
        ok_button.bind(on_release=popup.dismiss)
        popup.open()

        # Clear input fields
        self.ids.name_input.text = ''
        self.ids.name_input.user_id = ''
        self.ids.reason_spinner.text = 'Выберите причину'
        self.ids.comment_input.text = ''
        self.ids.end_of_day_checkbox.ids.cb.active = False

class MyApp(App):
    def build(self):
        Window.size = (600, 800)
        return Builder.load_string(KV)

if __name__ == '__main__':
    MyApp().run()
