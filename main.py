from lembretes import Lembretes
from winotify import Notification, audio
from pathlib import Path
import os

class AntiForg:

    lembretes = Lembretes()

    #Criando o arquivo para que o APP inicie com o windows
    startup_path = fr"{Path.home()}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
    start_bat = fr'{startup_path}\\open.bat'
    file_path = os.path.dirname(os.path.realpath(__file__))
    with open(startup_path + '\\' + 'open.bat', 'w+') as bat_file:
        bat_file.write(fr'python {file_path}\\main.py')

    todos_lembretes = list(lembretes.ler_lembrete(todos=True)).sort(reverse=True)

    def __init__(self) -> None:
        pass

    def notificar_windows(self, titulo, desc):
        notif = Notification(
            app_id='AntiForg',
            title=titulo,
            msg=desc,
            duration="short"
        )
        notif.show()

if __name__ == '__main__':
    antiforg = AntiForg()