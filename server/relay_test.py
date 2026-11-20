from relay import Server
import builtins
from unittest.mock import Mock


def test_listner_print():
    serv = Server("127.0.0.1", 5000)

    def stop_after_print(message):
        serv.is_work = False

    builtins.print = Mock(side_effect=stop_after_print)

    serv.listner()
    serv.close()
    builtins.print.assert_called_with("жду подключения на: ('127.0.0.1', 5000)")
