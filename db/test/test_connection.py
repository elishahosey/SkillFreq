import importlib.util
import os
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch


CONNECTION_PATH = Path(__file__).resolve().parents[1] / "connection.py"


class ConnectionTest(unittest.TestCase):
    def test_connection_uses_environment_values(self):
        connect = Mock(return_value="connection")
        load_dotenv = Mock()

        fake_modules = {
            "psycopg2": SimpleNamespace(connect=connect),
            "dotenv": SimpleNamespace(load_dotenv=load_dotenv),
        }
        env = {
            "DB_NAME": "skillfreq_test",
            "DB_USER": "skillfreq_user",
            "DB_PASSWORD": "skillfreq_password",
            "DB_HOST": "localhost",
        }

        with (
            patch.dict(sys.modules, fake_modules),
            patch.dict(os.environ, env, clear=True),
        ):
            spec = importlib.util.spec_from_file_location(
                "connection_under_test",
                CONNECTION_PATH,
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

        load_dotenv.assert_called_once_with()
        connect.assert_called_once_with(
            dbname="skillfreq_test",
            user="skillfreq_user",
            password="skillfreq_password",
            host="localhost",
        )
        self.assertEqual(module.conn, "connection")


if __name__ == "__main__":
    unittest.main()
