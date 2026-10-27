import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from apoio import carregar

pr = carregar("progresso.py")


def tarefa(numero, caixas, status=None):
    """Bloco de tarefa no formato do tasks.md do tlc-spec-driven; caixas = lista de True/False."""
    linhas = [f"### T{numero}: Tarefa {numero}", "", "**What**: algo", "**Where**: `src/a.py`", ""]
    if status:
        linhas += [f"**Status**: {status}", ""]
    linhas += ["**Done when**:", ""]
    linhas += [f"- [{'x' if c else ' '}] critério {i}" for i, c in enumerate(caixas)]
    linhas += ["", "**Tests**: unit", "**Gate**: quick", "", "---", ""]
    return "\n".join(linhas)


def tasks_md(*blocos, depois=""):
    return "# Tasks\n\n## Execution Plan\n\nT1 → T2\n\n## Task Breakdown\n\n" + "\n".join(blocos) + depois


def escrever(raiz, caminho, texto):
    arq = Path(raiz) / caminho
    arq.parent.mkdir(parents=True, exist_ok=True)
    arq.write_text(texto, encoding="utf-8")


class TestContarTarefas(unittest.TestCase):
    def test_tarefa_feita_quando_todas_as_caixas_marcadas(self):
        texto = tasks_md(tarefa(1, [True, True]), tarefa(2, [True, False]), tarefa(3, [False]))
        self.assertEqual(pr.contar_tarefas(texto), (3, 1))

    def test_maiuscula_x_conta_como_marcada(self):
        texto = tasks_md(tarefa(1, [True]).replace("[x]", "[X]"))
        self.assertEqual(pr.contar_tarefas(texto), (1, 1))

    def test_status_concluido_vale_quando_nao_ha_caixas(self):
        texto = tasks_md(tarefa(1, [], status="Done"), tarefa(2, [], status="Pendente"))
        self.assertEqual(pr.contar_tarefas(texto), (2, 1))

    def test_status_em_portugues_e_com_marca(self):
        texto = tasks_md(tarefa(1, [], status="Concluída"), tarefa(2, [], status="✅ Complete"))
        self.assertEqual(pr.contar_tarefas(texto), (2, 2))

    def test_caixa_aberta_vence_status_concluido(self):
        texto = tasks_md(tarefa(1, [True, False], status="Done"))
        self.assertEqual(pr.contar_tarefas(texto), (1, 0))

    def test_checklists_fora_das_tarefas_nao_contam(self):
        depois = "\n## Validação\n\n- [x] item solto\n- [x] outro\n"
        texto = tasks_md(tarefa(1, [False]), depois=depois)
        self.assertEqual(pr.contar_tarefas(texto), (1, 0))

    def test_sem_tarefas(self):
        self.assertEqual(pr.contar_tarefas("# Tasks\n\nnada aqui\n"), (0, 0))


class TestColetar(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def test_soma_todos_os_tasks_md_de_specs(self):
        escrever(self.raiz, ".specs/features/a/tasks.md", tasks_md(tarefa(1, [True]), tarefa(2, [False])))
        escrever(self.raiz, ".specs/refatoracoes/b/tasks.md", tasks_md(tarefa(1, [False])))
        itens = pr.coletar(self.raiz)
        self.assertEqual({i["item"]: (i["total"], i["feitas"]) for i in itens},
                         {".specs/features/a": (2, 1), ".specs/refatoracoes/b": (1, 0)})

    def test_ignora_pastas_de_evidencias_codigo_e_dependencias(self):
        for pasta in (".specs/spikes/x/codigo", ".specs/seguranca/d/evidencias", "node_modules/p"):
            escrever(self.raiz, f"{pasta}/tasks.md", tasks_md(tarefa(1, [True])))
        self.assertEqual(pr.coletar(self.raiz), [])

    def test_arquivo_sem_tarefas_fica_de_fora(self):
        escrever(self.raiz, ".specs/features/a/tasks.md", "# Tasks\n")
        self.assertEqual(pr.coletar(self.raiz), [])

    def test_sem_pasta_specs(self):
        self.assertEqual(pr.coletar(self.raiz), [])


class TestFrase(unittest.TestCase):
    def test_formato_pedido(self):
        self.assertEqual(pr.frase(135, 180), "Faltam 45 de 180 tarefas: 75% concluído")

    def test_singular(self):
        self.assertEqual(pr.frase(11, 12), "Falta 1 de 12 tarefas: 92% concluído")

    def test_tudo_concluido(self):
        self.assertEqual(pr.frase(12, 12), "Todas as 12 tarefas concluídas: 100% concluído")

    def test_nada_concluido(self):
        self.assertEqual(pr.frase(0, 10), "Faltam 10 de 10 tarefas: 0% concluído")

    def test_sem_tarefas(self):
        self.assertEqual(pr.frase(0, 0), "Sem tarefas ainda")

    def test_percentual_nunca_arredonda_para_cem_antes_da_hora(self):
        self.assertEqual(pr.frase(999, 1000), "Falta 1 de 1000 tarefas: 99% concluído")


STATE = """# Estado

## Decisões

AD-001: algo

## Retomada

- **Fluxo**: 3 Feature em projeto feito com IA — skill `feature`
- **Item**: `.specs/features/importar-extrato/`
- **Fase aprovada**: 4, Plano em 2026-10-20
- **Próxima fase**: 5, Rede de proteção — modelo indicado: sonnet
"""


class TestRetomada(unittest.TestCase):
    def test_le_item_fluxo_e_fases(self):
        r = pr.ler_retomada(STATE)
        self.assertEqual(r["item"], ".specs/features/importar-extrato")
        self.assertEqual(r["fluxo"], "3 Feature em projeto feito com IA")
        self.assertIn("4, Plano", r["fase_aprovada"])
        self.assertIn("5, Rede de proteção", r["proxima_fase"])

    def test_sem_secao_retomada(self):
        self.assertEqual(pr.ler_retomada("# Estado\n\n## Decisões\n"), {})


class TestRelatorio(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def test_item_atual_vem_da_retomada_e_projeto_soma_tudo(self):
        escrever(self.raiz, ".specs/STATE.md", STATE)
        escrever(self.raiz, ".specs/features/importar-extrato/tasks.md",
                 tasks_md(tarefa(1, [True]), tarefa(2, [False]), tarefa(3, [False]), tarefa(4, [False])))
        escrever(self.raiz, ".specs/features/outra/tasks.md", tasks_md(tarefa(1, [True]), tarefa(2, [True])))
        rel = pr.relatorio(self.raiz)
        self.assertEqual(rel["item"], {"nome": ".specs/features/importar-extrato", "total": 4, "feitas": 1})
        self.assertEqual(rel["projeto"], {"total": 6, "feitas": 3})
        texto = pr.formatar(rel)
        self.assertIn("Item atual (.specs/features/importar-extrato): Faltam 3 de 4 tarefas: 25% concluído", texto)
        self.assertIn("Projeto: Faltam 3 de 6 tarefas: 50% concluído", texto)

    def test_argumento_item_vence_a_retomada(self):
        escrever(self.raiz, ".specs/STATE.md", STATE)
        escrever(self.raiz, ".specs/features/importar-extrato/tasks.md", tasks_md(tarefa(1, [False])))
        escrever(self.raiz, ".specs/features/outra/tasks.md", tasks_md(tarefa(1, [True])))
        rel = pr.relatorio(self.raiz, item=".specs/features/outra/")
        self.assertEqual(rel["item"]["nome"], ".specs/features/outra")
        self.assertEqual(rel["item"]["feitas"], 1)

    def test_sem_retomada_usa_o_unico_item_em_aberto(self):
        escrever(self.raiz, ".specs/features/pronta/tasks.md", tasks_md(tarefa(1, [True])))
        escrever(self.raiz, ".specs/features/aberta/tasks.md", tasks_md(tarefa(1, [True]), tarefa(2, [False])))
        rel = pr.relatorio(self.raiz)
        self.assertEqual(rel["item"]["nome"], ".specs/features/aberta")

    def test_varios_itens_em_aberto_sem_retomada_mostra_so_o_projeto(self):
        escrever(self.raiz, ".specs/features/a/tasks.md", tasks_md(tarefa(1, [False])))
        escrever(self.raiz, ".specs/features/b/tasks.md", tasks_md(tarefa(1, [False])))
        rel = pr.relatorio(self.raiz)
        self.assertIsNone(rel["item"])
        self.assertNotIn("Item atual", pr.formatar(rel))

    def test_item_sem_tasks_md_e_declarado_sem_tarefas(self):
        escrever(self.raiz, ".specs/STATE.md", STATE)
        rel = pr.relatorio(self.raiz)
        self.assertEqual(rel["item"], {"nome": ".specs/features/importar-extrato", "total": 0, "feitas": 0})

    def test_sem_tarefas_mostra_a_fase_do_fluxo(self):
        escrever(self.raiz, ".specs/STATE.md", STATE)
        texto = pr.formatar(pr.relatorio(self.raiz))
        self.assertIn("Sem tarefas ainda", texto)
        self.assertIn("Fluxo: 3 Feature em projeto feito com IA", texto)
        self.assertIn("Fase aprovada: 4, Plano em 2026-10-20", texto)
        self.assertIn("Próxima fase: 5, Rede de proteção", texto)
        self.assertNotIn("%", texto)

    def test_sem_tarefas_e_sem_retomada(self):
        texto = pr.formatar(pr.relatorio(self.raiz))
        self.assertIn("Sem tarefas ainda", texto)
        self.assertIn("nenhum tasks.md", texto)

    def test_nao_escreve_nada(self):
        escrever(self.raiz, ".specs/features/a/tasks.md", tasks_md(tarefa(1, [False])))
        antes = sorted(p.relative_to(self.raiz).as_posix() for p in self.raiz.rglob("*"))
        pr.formatar(pr.relatorio(self.raiz))
        depois = sorted(p.relative_to(self.raiz).as_posix() for p in self.raiz.rglob("*"))
        self.assertEqual(antes, depois)


class TestMain(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        escrever(self.raiz, ".specs/features/a/tasks.md", tasks_md(tarefa(1, [True]), tarefa(2, [False])))

    def rodar(self, *args):
        saida = io.StringIO()
        with contextlib.redirect_stdout(saida):
            codigo = pr.main(["--raiz", str(self.raiz), *args])
        return codigo, saida.getvalue()

    def test_saida_em_texto(self):
        codigo, saida = self.rodar()
        self.assertEqual(codigo, 0)
        self.assertIn("Projeto: Falta 1 de 2 tarefas: 50% concluído", saida)

    def test_saida_json(self):
        codigo, saida = self.rodar("--json")
        self.assertEqual(codigo, 0)
        dados = json.loads(saida)
        self.assertEqual(dados["projeto"], {"total": 2, "feitas": 1})

    def test_raiz_inexistente_recusa(self):
        saida = io.StringIO()
        with contextlib.redirect_stdout(saida), contextlib.redirect_stderr(saida):
            codigo = pr.main(["--raiz", str(self.raiz / "nao-existe")])
        self.assertEqual(codigo, 2)


if __name__ == "__main__":
    unittest.main()
