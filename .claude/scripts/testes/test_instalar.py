import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from apoio import carregar, repo_git

inst = carregar("instalar.py")
SCRIPT = Path(__file__).resolve().parents[1] / "instalar.py"


def escrever(caminho, texto):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(texto, encoding="utf-8")


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.origem = self.dir / "rascunho" / ".claude"
        escrever(self.origem / "CLAUDE.md", "regras v1")
        escrever(self.origem / "skills" / "fluxo" / "SKILL.md", "menu v1")
        escrever(self.origem / "scripts" / "trava.py", "print('v1')")
        escrever(self.origem / ".cache" / "suite-verde.json", "{}")
        escrever(self.origem / "scripts" / "__pycache__" / "x.pyc", "lixo")
        escrever(self.origem / "settings.local.json", "{}")
        self.destino = self.dir / "projeto"

    def tearDown(self):
        self._tmp.cleanup()

    def instalar(self, **kw):
        return inst.instalar(self.origem, self.destino, **kw)


class TestInstalar(Base):
    def test_pasta_vazia_recebe_claude_git_e_gitignore(self):
        self.instalar()
        self.assertEqual((self.destino / ".claude" / "CLAUDE.md").read_text(encoding="utf-8"), "regras v1")
        self.assertTrue((self.destino / ".claude" / "skills" / "fluxo" / "SKILL.md").exists())
        self.assertTrue((self.destino / ".git").exists())
        ignorado = (self.destino / ".gitignore").read_text(encoding="utf-8")
        self.assertIn(".claude/.cache/", ignorado)
        self.assertIn("__pycache__/", ignorado)

    def test_nao_copia_cache_pycache_nem_settings_local(self):
        self.instalar()
        claude = self.destino / ".claude"
        self.assertFalse((claude / ".cache").exists())
        self.assertFalse((claude / "scripts" / "__pycache__").exists())
        self.assertFalse((claude / "settings.local.json").exists())

    def test_grava_manifesto_com_hash_de_cada_arquivo(self):
        self.instalar()
        manifesto = json.loads((self.destino / ".claude" / inst.MANIFESTO).read_text(encoding="utf-8"))
        self.assertIn("CLAUDE.md", manifesto["arquivos"])
        self.assertIn("skills/fluxo/SKILL.md", manifesto["arquivos"])
        self.assertNotIn(inst.MANIFESTO, manifesto["arquivos"])

    def test_gitignore_existente_e_preservado_sem_duplicar(self):
        escrever(self.destino / ".gitignore", "node_modules/\n__pycache__/\n")
        self.instalar()
        linhas = (self.destino / ".gitignore").read_text(encoding="utf-8").splitlines()
        self.assertIn("node_modules/", linhas)
        self.assertEqual(linhas.count("__pycache__/"), 1)
        self.assertIn(".claude/.cache/", linhas)

    def test_nao_cria_specs(self):
        self.instalar()
        self.assertFalse((self.destino / ".specs").exists())

    def test_recusa_se_ja_existe_claude(self):
        escrever(self.destino / ".claude" / "CLAUDE.md", "meu")
        with self.assertRaises(inst.Recusa):
            self.instalar()
        self.assertEqual((self.destino / ".claude" / "CLAUDE.md").read_text(encoding="utf-8"), "meu")

    def test_recusa_destino_dentro_da_origem(self):
        with self.assertRaises(inst.Recusa):
            inst.instalar(self.origem, self.origem.parent / "sub")

    def test_repositorio_git_existente_nao_e_reiniciado(self):
        self.destino.mkdir()
        repo_git(self.destino)
        escrever(self.destino / "a.txt", "x")
        subprocess.run(["git", "add", "-A"], cwd=self.destino, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "c"], cwd=self.destino, check=True)
        self.instalar()
        log = subprocess.run(["git", "log", "--oneline"], cwd=self.destino, capture_output=True, text=True).stdout
        self.assertEqual(len(log.strip().splitlines()), 1)


class TestAtualizar(Base):
    def setUp(self):
        super().setUp()
        self.instalar()

    def test_substitui_arquivo_nao_modificado(self):
        escrever(self.origem / "skills" / "fluxo" / "SKILL.md", "menu v2")
        relatorio = self.instalar(atualizar=True)
        self.assertEqual((self.destino / ".claude" / "skills" / "fluxo" / "SKILL.md").read_text(encoding="utf-8"), "menu v2")
        self.assertIn("skills/fluxo/SKILL.md", relatorio["atualizados"])

    def test_preserva_arquivo_modificado_no_projeto(self):
        escrever(self.destino / ".claude" / "CLAUDE.md", "regras v1 + ajuste do projeto")
        escrever(self.origem / "CLAUDE.md", "regras v2")
        relatorio = self.instalar(atualizar=True)
        self.assertEqual((self.destino / ".claude" / "CLAUDE.md").read_text(encoding="utf-8"), "regras v1 + ajuste do projeto")
        self.assertIn("CLAUDE.md", relatorio["conflitos"])

    def test_forcar_sobrescreve_modificado(self):
        escrever(self.destino / ".claude" / "CLAUDE.md", "ajuste local")
        escrever(self.origem / "CLAUDE.md", "regras v2")
        self.instalar(atualizar=True, forcar=True)
        self.assertEqual((self.destino / ".claude" / "CLAUDE.md").read_text(encoding="utf-8"), "regras v2")

    def test_novo_na_origem_e_adicionado(self):
        escrever(self.origem / "skills" / "bug" / "SKILL.md", "bug v1")
        relatorio = self.instalar(atualizar=True)
        self.assertTrue((self.destino / ".claude" / "skills" / "bug" / "SKILL.md").exists())
        self.assertIn("skills/bug/SKILL.md", relatorio["novos"])

    def test_removido_da_origem_sai_se_nao_modificado(self):
        (self.origem / "scripts" / "trava.py").unlink()
        relatorio = self.instalar(atualizar=True)
        self.assertFalse((self.destino / ".claude" / "scripts" / "trava.py").exists())
        self.assertIn("scripts/trava.py", relatorio["removidos"])

    def test_removido_da_origem_fica_se_modificado(self):
        escrever(self.destino / ".claude" / "scripts" / "trava.py", "print('meu')")
        (self.origem / "scripts" / "trava.py").unlink()
        relatorio = self.instalar(atualizar=True)
        self.assertTrue((self.destino / ".claude" / "scripts" / "trava.py").exists())
        self.assertIn("scripts/trava.py", relatorio["conflitos"])

    def test_arquivo_proprio_do_projeto_nao_e_tocado(self):
        escrever(self.destino / ".claude" / "skills" / "minha" / "SKILL.md", "do projeto")
        self.instalar(atualizar=True)
        self.assertEqual((self.destino / ".claude" / "skills" / "minha" / "SKILL.md").read_text(encoding="utf-8"), "do projeto")

    def test_cache_do_projeto_e_mantido(self):
        escrever(self.destino / ".claude" / ".cache" / "suite-verde.json", '{"x": 1}')
        self.instalar(atualizar=True)
        self.assertTrue((self.destino / ".claude" / ".cache" / "suite-verde.json").exists())

    def test_atualizar_sem_instalacao_recusa(self):
        with self.assertRaises(inst.Recusa):
            inst.instalar(self.origem, self.dir / "outro", atualizar=True)

    def test_simular_nao_muda_nada(self):
        escrever(self.origem / "CLAUDE.md", "regras v2")
        relatorio = self.instalar(atualizar=True, simular=True)
        self.assertEqual((self.destino / ".claude" / "CLAUDE.md").read_text(encoding="utf-8"), "regras v1")
        self.assertIn("CLAUDE.md", relatorio["atualizados"])


class TestAvisos(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.home = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_sem_superpowers_avisa(self):
        avisos = inst.avisos_de_ambiente(self.home)
        self.assertTrue(any("superpowers" in a for a in avisos))

    def test_com_superpowers_nao_avisa(self):
        escrever(self.home / ".claude" / "plugins" / "installed_plugins.json",
                 '{"plugins": {"superpowers@superpowers-marketplace": []}}')
        avisos = inst.avisos_de_ambiente(self.home)
        self.assertFalse(any("superpowers" in a for a in avisos))


class TestLinhaDeComando(Base):
    def test_cli_instala_e_sai_com_zero(self):
        r = subprocess.run([sys.executable, str(SCRIPT), str(self.destino), "--origem", str(self.origem)],
                           capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue((self.destino / ".claude" / "CLAUDE.md").exists())

    def test_cli_recusa_sai_com_dois(self):
        escrever(self.destino / ".claude" / "CLAUDE.md", "meu")
        r = subprocess.run([sys.executable, str(SCRIPT), str(self.destino), "--origem", str(self.origem)],
                           capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 2)
        self.assertIn("--atualizar", r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
