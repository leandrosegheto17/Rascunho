import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from apoio import carregar, git, repo_git

fl = carregar("fechar-lote.py")

TASKS = """# Tarefas

### Phase 1: Base

### T1: Primeira

**What**: algo
**Estimativa**: 1h

**Status**: rascunhada

- [ ] primeiro critério

### T2: Segunda

**What**: algo
**Estimativa**: 1h

- [ ] segundo critério
- [ ] terceiro critério

### Phase 2: Depois

### T3: Terceira

**What**: algo
**Estimativa**: 5h

- [ ] quarto critério
"""


class TestMarcarLote(unittest.TestCase):
    def test_marca_caixas_e_status_so_das_tarefas_do_lote_e_poe_o_gate_ao_fim(self):
        saida = fl.marcar_lote(TASKS, ["T1", "T2"], "Gate: x @ abc = verde")
        self.assertIn("**Status**: concluída", saida)
        self.assertEqual(saida.count("- [x]"), 3)
        self.assertEqual(saida.count("- [ ]"), 1)  # a T3 segue aberta
        self.assertLess(saida.index("Gate: x @ abc = verde"), saida.index("### Phase 2"))
        self.assertGreater(saida.index("Gate: x @ abc = verde"), saida.index("terceiro critério"))


class TestFecharLote(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self._tmp.name)
        repo_git(self.raiz)
        pasta = self.raiz / ".specs" / "features" / "x"
        pasta.mkdir(parents=True)
        (pasta / "tasks.md").write_text(TASKS, encoding="utf-8")
        self.config({"comando": f'"{sys.executable}" -c "pass"'})
        git(self.raiz, "add", "-A")
        git(self.raiz, "commit", "-q", "-m", "chore: base")

    def tearDown(self):
        self._tmp.cleanup()

    def config(self, conteudo):
        pasta = self.raiz / ".specs" / "projeto"
        pasta.mkdir(parents=True, exist_ok=True)
        (pasta / "testes.json").write_text(json.dumps(conteudo), encoding="utf-8")

    def fechar(self, *extra):
        with contextlib.redirect_stdout(io.StringIO()) as saida:
            codigo = fl.main(["--raiz", str(self.raiz), "--item", ".specs/features/x", *extra])
        return codigo, saida.getvalue()

    def texto(self):
        return (self.raiz / ".specs" / "features" / "x" / "tasks.md").read_text(encoding="utf-8")

    def test_gate_verde_fecha_o_lote_com_um_commit_e_tres_linhas(self):
        codigo, saida = self.fechar("--rodape", "Co-Authored-By: Teste <t@x>")
        self.assertEqual(codigo, 0, saida)
        linhas = saida.strip().splitlines()
        self.assertEqual(len(linhas), 3, saida)
        self.assertTrue(linhas[0].startswith("Gate: ") and linhas[0].endswith("= verde"))
        self.assertIn("Lote 1", linhas[1])
        self.assertIn(linhas[0], self.texto())
        mensagem = subprocess.run(["git", "log", "-1", "--format=%B"], cwd=self.raiz, capture_output=True, text=True).stdout
        self.assertTrue(mensagem.startswith("chore(tasks): fecha o lote 1"))
        self.assertIn("Co-Authored-By: Teste", mensagem)
        self.assertEqual(self.texto().count("- [x]"), 4)  # lote final de 1 tarefa se junta ao anterior

    def test_gate_que_falha_nao_escreve_nem_commita(self):
        self.config({"comando": f'"{sys.executable}" -c "import sys; print(\'quebrou aqui\'); sys.exit(3)"'})
        antes = self.texto()
        codigo, saida = self.fechar()
        self.assertEqual(codigo, 1)
        self.assertIn("quebrou aqui", saida)
        self.assertEqual(self.texto(), antes)
        log = subprocess.run(["git", "log", "--oneline"], cwd=self.raiz, capture_output=True, text=True).stdout
        self.assertEqual(len(log.strip().splitlines()), 1)

    def test_sem_comando_de_gate_recusa(self):
        (self.raiz / ".specs" / "projeto" / "testes.json").unlink()
        self.assertEqual(self.fechar()[0], 2)

    def test_parametro_gate_vale_mais_que_o_arquivo(self):
        self.config({"comando": f'"{sys.executable}" -c "import sys; sys.exit(1)"'})
        self.assertEqual(self.fechar("--gate", f'"{sys.executable}" -c "pass"')[0], 0)


BLOQUEADAS = """# Tarefas

### Phase 1: Base

### T1: Primeira

**What**: algo
**Estimativa**: 3h

- [ ] primeiro critério

### T2: Segunda

**What**: algo
**Estimativa**: 3h
**Bloqueio**: qual o limite?

- [ ] segundo critério

### Phase 2: Depois

### T3: Terceira

**What**: algo
**Estimativa**: 6h
**Depends on**: T2

- [ ] terceiro critério

### Phase 3: Fim

### T4: Quarta

**What**: algo
**Estimativa**: 6h

- [ ] quarto critério
"""


class TestFecharComBloqueio(TestFecharLote):
    """Passo 42: o fechamento não conclui o que está bloqueado e segue para o próximo lote executável."""

    def setUp(self):
        super().setUp()
        (self.raiz / ".specs" / "features" / "x" / "tasks.md").write_text(BLOQUEADAS, encoding="utf-8")
        git(self.raiz, "commit", "-q", "-am", "chore: bloqueadas")

    def log(self):
        return subprocess.run(["git", "log", "-1", "--format=%s"], cwd=self.raiz, capture_output=True,
                              text=True, encoding="utf-8").stdout

    def test_fecha_so_as_tarefas_executaveis(self):
        codigo, saida = self.fechar()
        self.assertEqual(codigo, 0, saida)
        self.assertEqual(self.texto().count("- [x]"), 1)
        self.assertIn("- [x] primeiro", self.texto())
        self.assertIn("T1", self.log())
        self.assertNotIn("T2", self.log())

    def test_pula_o_lote_so_com_travadas(self):
        self.fechar()
        codigo, saida = self.fechar()
        self.assertEqual(codigo, 0, saida)
        self.assertIn("- [x] quarto", self.texto())
        self.assertIn("- [ ] terceiro", self.texto())

    def test_so_restam_travadas_recusa_e_diz_quais(self):
        self.fechar()
        self.fechar()
        with contextlib.redirect_stderr(io.StringIO()) as erro:
            codigo, _ = self.fechar()
        self.assertEqual(codigo, 2)
        self.assertIn("T2", erro.getvalue())
        self.assertIn("qual o limite?", erro.getvalue())

    # os testes herdados usam o tasks.md original
    test_gate_verde_fecha_o_lote_com_um_commit_e_tres_linhas = None
    test_gate_que_falha_nao_escreve_nem_commita = None
    test_sem_comando_de_gate_recusa = None
    test_parametro_gate_vale_mais_que_o_arquivo = None


if __name__ == "__main__":
    unittest.main()
