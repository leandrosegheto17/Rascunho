import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from apoio import SCRIPTS

SCRIPT = SCRIPTS / "checar-tokens.py"


def rodar(pasta):
    r = subprocess.run([sys.executable, str(SCRIPT), str(pasta)], capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stdout


class TestChecarTokens(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.src = Path(self._tmp.name) / "src"
        self.src.mkdir()
        (self.src / "tokens.css").write_text(':root { --cor: #1a5fb4; --fonte: "Inter"; }', encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def escrever(self, nome, texto):
        (self.src / nome).write_text(texto, encoding="utf-8")

    def test_codigo_so_com_tokens_passa(self):
        self.escrever("app.css", ".a { color: var(--cor); font-family: var(--fonte); }\n.b { font-family: inherit; }")
        self.escrever("Tela.tsx", "const s = { color: 'var(--cor)', fontFamily: 'var(--fonte)' };")
        codigo, saida = rodar(self.src)
        self.assertEqual(codigo, 0, saida)

    def test_acusa_cores_e_fontes_soltas(self):
        self.escrever("app.css", ".a { color: #ff0000; }\n.b { background: rgba(0,0,0,.5); }\n.c { font-family: Arial; }")
        self.escrever("Tela.tsx", "const s = { color: '#abc' };\nconst f = { fontFamily: 'Roboto' };")
        codigo, saida = rodar(self.src)
        self.assertEqual(codigo, 1)
        self.assertIn("5 valor(es)", saida)
        for trecho in ("app.css:1", "app.css:2", "app.css:3", "Tela.tsx:1", "Tela.tsx:2"):
            self.assertIn(trecho, saida)

    def test_ignora_ancoras_comentarios_e_node_modules(self):
        self.escrever("Tela.tsx", "// corrige o bug #123\nconst a = <a href=\"#topo\">topo</a>;")
        (self.src / "node_modules").mkdir()
        (self.src / "node_modules" / "lib.css").write_text(".x { color: #000; }", encoding="utf-8")
        codigo, saida = rodar(self.src)
        self.assertEqual(codigo, 0, saida)

    def test_pasta_inexistente(self):
        codigo, _ = rodar(Path(self._tmp.name) / "nao-existe")
        self.assertEqual(codigo, 2)


if __name__ == "__main__":
    unittest.main()
