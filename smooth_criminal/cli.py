import argparse
import importlib.util
import inspect
import logging
import os

from rich.logging import RichHandler

from smooth_criminal.analizer import analyze_ast
from smooth_criminal.memory import (
    suggest_boost,
    clear_execution_history,
    export_execution_history,
    score_function,
)
from smooth_criminal.dashboard import render_dashboard


log_level = os.getenv("LOG_LEVEL", "INFO").upper()
numeric_level = getattr(logging, log_level, logging.INFO)

logging.basicConfig(
    level=numeric_level,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)],
    force=True,
)

logger = logging.getLogger("SmoothCriminal")

def main():
    parser = argparse.ArgumentParser(description="Smooth Criminal CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Comando 'analyze'
    analyze_parser = subparsers.add_parser("analyze", help="Analiza un archivo Python en busca de optimizaciones.")
    analyze_parser.add_argument("filepath", help="Ruta del script a analizar")

    # Comando 'suggest'
    suggest_parser = subparsers.add_parser("suggest", help="Sugiere el mejor decorador para una función registrada.")
    suggest_parser.add_argument("func_name", help="Nombre de la función a consultar")

    # Comando 'dashboard'
    subparsers.add_parser("dashboard", help="Muestra un resumen del historial de optimizaciones.")

    # Comando 'clean'
    subparsers.add_parser("clean", help="Elimina el historial de ejecuciones registrado.")

    # Comando 'export'
    export_parser = subparsers.add_parser("export", help="Exporta el historial como archivo CSV o JSON.")
    export_parser.add_argument("filepath", help="Ruta del archivo de salida")
    export_parser.add_argument("--format", choices=["csv", "json"], default="csv", help="Formato de exportación")

    # Comando 'score'
    score_parser = subparsers.add_parser("score", help="Muestra una puntuación de optimización para una función.")
    score_parser.add_argument("func_name", help="Nombre de la función a evaluar")

    args = parser.parse_args()
    show_intro()

    if args.command == "analyze":
        analyze_file(args.filepath)
    elif args.command == "suggest":
        handle_suggestion(args.func_name)
    elif args.command == "dashboard":
        render_dashboard()
    elif args.command == "clean":
        handle_clean()
    elif args.command == "export":
        handle_export(args.filepath, args.format)
    elif args.command == "score":
        handle_score(args.func_name)

    else:
        logger.warning(
            "[bold red]Annie, are you OK?[/bold red] "
            "Use '[green]smooth-criminal analyze <file.py>[/green]', "
            "'[green]smooth-criminal suggest <func>[/green]', "
            "'[green]smooth-criminal dashboard[/green]' or "
            "'[green]smooth-criminal export <file> --format csv/json[/green]'."
        )

def show_intro():
    logger.info(
        "[bold magenta]Smooth Criminal[/bold magenta]\n"
        "[dim]By Adolfo – Powered by Python + MJ energy 🕺[/dim]"
    )

def analyze_file(filepath):
    logger.info(
        f"\n🎤 [cyan]Analyzing [bold]{filepath}[/bold] for optimization opportunities...[/cyan]\n"
    )

    spec = importlib.util.spec_from_file_location("target_module", filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    functions = [getattr(module, name) for name in dir(module)
                 if inspect.isfunction(getattr(module, name)) and getattr(module, name).__module__ == module.__name__]

    if not functions:
        logger.warning("[yellow]No se encontraron funciones para analizar.[/yellow]")
        return

    for func in functions:
        logger.info(
            f"\n🔎 [bold blue]Analyzing function:[/bold blue] [white]{func.__name__}[/white]"
        )
        analyze_ast(func)

def handle_suggestion(func_name):
    logger.info(
        f"\n🧠 [bold cyan]Consulting memory for:[/bold cyan] [white]{func_name}[/white]\n"
    )
    suggestion = suggest_boost(func_name)
    logger.info(suggestion)

def handle_clean():
    if clear_execution_history():
        logger.info("[green]Historial de ejecuciones borrado exitosamente.[/green]")
    else:
        logger.warning("[yellow]No se encontró historial para borrar.[/yellow]")

def handle_export(filepath, format):
    success = export_execution_history(filepath, format)
    if success:
        logger.info(
            f"[green]Historial exportado a [bold]{filepath}[/bold] como {format.upper()}.[/green]"
        )
    else:
        logger.warning("[yellow]No hay historial para exportar.[/yellow]")

def handle_score(func_name):
    score, summary = score_function(func_name)
    if score is None:
        logger.warning(f"[yellow]{summary}[/yellow]")
    else:
        logger.info(summary)
        color = "green" if score >= 80 else "yellow" if score >= 50 else "red"
        logger.info(f"[bold {color}]Optimization Score: {score}/100[/bold {color}]")


if __name__ == "__main__":
    main()
