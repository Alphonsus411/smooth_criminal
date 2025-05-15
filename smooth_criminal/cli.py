import argparse
import importlib.util
import inspect
from smooth_criminal.analyzer import analyze_ast
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Smooth Criminal CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Comando 'analyze'
    analyze_parser = subparsers.add_parser("analyze", help="Analiza un archivo Python en busca de optimizaciones.")
    analyze_parser.add_argument("filepath", help="Ruta del script a analizar")

    args = parser.parse_args()

    show_intro()

    if args.command == "analyze":
        analyze_file(args.filepath)
    else:
        console.print("[bold red]Annie, are you OK?[/bold red] Use '[green]smooth-criminal analyze <file.py>[/green]' to begin.")

def show_intro():
    panel = Panel.fit(
        "[bold magenta]Smooth Criminal[/bold magenta]\n[dim]By Adolfo - Powered by Python + MJ energy 🕺[/dim]",
        title="🎩 Welcome",
        border_style="magenta"
    )
    console.print(panel)

def analyze_file(filepath):
    console.print(f"\n🎤 [cyan]Analyzing [bold]{filepath}[/bold] for optimization opportunities...[/cyan]\n")

    # Carga dinámica del módulo desde archivo
    spec = importlib.util.spec_from_file_location("target_module", filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Detectar funciones definidas en ese módulo
    functions = [getattr(module, name) for name in dir(module)
                 if inspect.isfunction(getattr(module, name)) and getattr(module, name).__module__ == module.__name__]

    if not functions:
        console.print("[yellow]No se encontraron funciones para analizar.[/yellow]")
        return

    for func in functions:
        console.print(f"\n🔎 [bold blue]Analyzing function:[/bold blue] [white]{func.__name__}[/white]")
        analyze_ast(func)
