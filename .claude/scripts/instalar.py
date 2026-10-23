#!/usr/bin/env python3
"""Instala ou atualiza os fluxos (esta pasta .claude) num projeto.

    python .claude/scripts/instalar.py <pasta do projeto>                 instala numa pasta vazia ou num repositório
    python .claude/scripts/instalar.py <pasta do projeto> --atualizar     traz a versão atual dos fluxos
        [--simular] [--forcar] [--origem <outra .claude>]

Instalar: cria a pasta se faltar, faz git init se não for repositório, copia a .claude
(sem .cache, __pycache__ e settings.local.json), acrescenta o que falta no .gitignore e grava
.claude/.instalacao.json com o hash de cada arquivo copiado. Não cria .specs: ela é do projeto.

Atualizar: arquivo que o projeto não mudou é substituído; arquivo mudado no projeto fica como
está e é listado como conflito (--forcar sobrescreve); arquivo que saiu dos fluxos é apagado
só se não foi mudado; arquivo criado pelo projeto dentro da .claude nunca é tocado.

Sai com 0 quando conclui, 1 se houver conflito na atualização e 2 quando recusa.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

MANIFESTO = ".instalacao.json"
PASTAS_FORA = {".cache", "__pycache__"}
ARQUIVOS_FORA = {"settings.local.json", MANIFESTO}
GITIGNORE = [".claude/.cache/", "__pycache__/"]
ORIGEM_PADRAO = Path(__file__).resolve().parents[1]


class Recusa(Exception):
    pass


def hash_de(caminho: Path) -> str:
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def arquivos_da_origem(origem: Path) -> dict[str, str]:
    """Caminho relativo (com /) -> hash, sem o que é gerado ou pessoal."""
    resultado = {}
    for caminho in sorted(origem.rglob("*")):
        rel = caminho.relative_to(origem)
        if not caminho.is_file() or PASTAS_FORA & set(rel.parts[:-1]) or rel.name in ARQUIVOS_FORA:
            continue
        resultado[rel.as_posix()] = hash_de(caminho)
    return resultado


def commit_da_origem(origem: Path) -> str:
    r = subprocess.run(["git", "-C", str(origem), "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else "desconhecido"


def completar_gitignore(destino: Path) -> None:
    arquivo = destino / ".gitignore"
    atual = arquivo.read_text(encoding="utf-8") if arquivo.exists() else ""
    faltam = [linha for linha in GITIGNORE if linha not in atual.splitlines()]
    if faltam:
        separador = "" if not atual or atual.endswith("\n") else "\n"
        arquivo.write_text(atual + separador + "\n".join(faltam) + "\n", encoding="utf-8")


def instalar(origem: Path, destino: Path, atualizar: bool = False, forcar: bool = False, simular: bool = False) -> dict:
    origem, destino = Path(origem).resolve(), Path(destino).resolve()
    raiz_origem = origem.parent
    if destino == raiz_origem or raiz_origem in destino.parents:
        raise Recusa(f"O destino {destino} fica dentro do repositório dos fluxos ({raiz_origem}).")
    claude = destino / ".claude"
    manifesto_atual = claude / MANIFESTO

    if atualizar and not manifesto_atual.exists():
        raise Recusa(f"{claude} não foi instalada por este script (falta {MANIFESTO}); instale sem --atualizar.")
    if not atualizar and claude.exists():
        raise Recusa(f"{claude} já existe. Para trazer a versão nova dos fluxos, use --atualizar.")

    novos_hashes = arquivos_da_origem(origem)
    antigos = json.loads(manifesto_atual.read_text(encoding="utf-8"))["arquivos"] if atualizar else {}
    relatorio = {"novos": [], "atualizados": [], "removidos": [], "conflitos": []}
    copiar, apagar, registro = [], [], {}

    for rel, novo in novos_hashes.items():
        alvo = claude / rel
        if not alvo.exists():
            relatorio["novos"].append(rel)
            copiar.append(rel)
            registro[rel] = novo
            continue
        atual = hash_de(alvo)
        if atual == novo:
            registro[rel] = novo
        elif forcar or atual == antigos.get(rel):
            relatorio["atualizados"].append(rel)
            copiar.append(rel)
            registro[rel] = novo
        else:
            relatorio["conflitos"].append(rel)
            registro[rel] = antigos.get(rel, novo)

    for rel, antigo in antigos.items():
        alvo = claude / rel
        if rel in novos_hashes or not alvo.exists():
            continue
        if forcar or hash_de(alvo) == antigo:
            relatorio["removidos"].append(rel)
            apagar.append(rel)
        else:
            relatorio["conflitos"].append(rel)

    if simular:
        return relatorio

    destino.mkdir(parents=True, exist_ok=True)
    if not (destino / ".git").exists():
        subprocess.run(["git", "init", "-q"], cwd=destino, check=True)
    for rel in copiar:
        (claude / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origem / rel, claude / rel)
    for rel in apagar:
        (claude / rel).unlink()
        pasta = (claude / rel).parent
        while pasta != claude and pasta.exists() and not any(pasta.iterdir()):
            pasta.rmdir()
            pasta = pasta.parent
    manifesto = {"origem": str(origem), "commit": commit_da_origem(origem), "data": date.today().isoformat(),
                 "arquivos": registro}
    manifesto_atual.write_text(json.dumps(manifesto, ensure_ascii=False, indent=2), encoding="utf-8")
    completar_gitignore(destino)
    return relatorio


def avisos_de_ambiente(home: Path | None = None) -> list[str]:
    avisos = []
    for programa, uso in (("git", "versionamento e trava de testes"), ("node", "comparação visual do redesign")):
        if shutil.which(programa) is None:
            avisos.append(f"`{programa}` não está no PATH ({uso}).")
    plugins = (home or Path.home()) / ".claude" / "plugins" / "installed_plugins.json"
    if not plugins.exists() or "superpowers@" not in plugins.read_text(encoding="utf-8"):
        avisos.append("plugin superpowers não instalado nesta conta (os fluxos usam systematic-debugging, "
                      "test-driven-development, worktrees, verificação e fim de branch). No Claude Code: "
                      "/plugin marketplace add obra/superpowers-marketplace e /plugin install superpowers@superpowers-marketplace.")
    return avisos


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Instala ou atualiza os fluxos num projeto.")
    parser.add_argument("destino", help="pasta do projeto")
    parser.add_argument("--atualizar", action="store_true", help="traz a versão atual dos fluxos para um projeto já instalado")
    parser.add_argument("--forcar", action="store_true", help="na atualização, sobrescreve também o que o projeto mudou")
    parser.add_argument("--simular", action="store_true", help="mostra o que mudaria, sem mexer em nada")
    parser.add_argument("--origem", default=str(ORIGEM_PADRAO), help="pasta .claude de origem (padrão: esta)")
    args = parser.parse_args()

    try:
        relatorio = instalar(Path(args.origem), Path(args.destino), args.atualizar, args.forcar, args.simular)
    except Recusa as erro:
        print(f"Recusado: {erro}")
        return 2

    acao = "Simulação" if args.simular else ("Atualização" if args.atualizar else "Instalação")
    print(f"{acao} em {Path(args.destino).resolve()}:")
    for chave, rotulo in (("novos", "novos"), ("atualizados", "atualizados"), ("removidos", "removidos"),
                          ("conflitos", "conflitos (mudados no projeto, mantidos)")):
        itens = relatorio[chave]
        print(f"- {rotulo}: {len(itens)}")
        if chave != "novos" or args.atualizar:
            for rel in itens:
                print(f"    {rel}")
    for aviso in avisos_de_ambiente():
        print(f"Aviso: {aviso}")
    if not args.atualizar and not args.simular:
        print("Próximo passo: abra o Claude Code nessa pasta e digite /fluxo.")
    return 1 if relatorio["conflitos"] else 0


if __name__ == "__main__":
    sys.exit(main())
