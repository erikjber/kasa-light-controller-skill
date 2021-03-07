from mycroft import MycroftSkill, intent_file_handler


class KasaLightController(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('controller.light.kasa.intent')
    def handle_controller_light_kasa(self, message):
        self.speak_dialog('controller.light.kasa')


def create_skill():
    return KasaLightController()

