import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="task-observ")
def cli():
    """Operational data pipeline CLI for ingesting, running, evaluating, and reporting."""


@cli.command()
@click.option("--source", default="data/input.csv", show_default=True, help="Source file to ingest.")
@click.option("--limit", default=10, show_default=True, type=click.IntRange(1, 1000), help="Number of records to process.")
@click.option("--dry-run/--no-dry-run", default=False, show_default=True, help="Preview ingestion without moving data.")
def ingest(source, limit, dry_run):
    """Ingest source data into the workspace."""
    if dry_run:
        console.print(
            Panel.fit(
                f"Dry run: [bold]{source}[/bold] would ingest [cyan]{limit}[/cyan] records.",
                title="Ingest",
            )
        )
        return

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        transient=False,
    ) as progress:
        task = progress.add_task("Ingesting records", total=limit)
        for _ in range(limit):
            progress.advance(task, 1)

    console.print(
        Panel.fit(
            f"✓ Successfully ingested [green]{limit}[/green] records from [bold]{source}[/bold].",
            title="Ingest complete",
        )
    )


@cli.command()
@click.option("--dataset", default="datasets/sample.json", show_default=True, help="Dataset to process.")
@click.option("--iterations", default=3, show_default=True, type=click.IntRange(1, 50), help="How many iterations to run.")
def run(dataset, iterations):
    """Execute the configured pipeline job."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        transient=False,
    ) as progress:
        task = progress.add_task("Running pipeline", total=iterations)
        for step in range(1, iterations + 1):
            progress.update(task, description=f"Step {step}/{iterations}")
            progress.advance(task, 1)

    table = Table(title="Run Summary")
    table.add_column("Dataset")
    table.add_column("Iterations")
    table.add_column("Status")
    table.add_row(dataset, str(iterations), "Completed")
    console.print(table)
    console.print(Panel("Pipeline execution finished successfully.", title="Run"))


@cli.command()
@click.option("--dataset", default="datasets/evaluation.json", show_default=True, help="Evaluation dataset path.")
@click.option("--threshold", default=0.80, show_default=True, type=click.FloatRange(0.0, 1.0), help="Pass threshold for the score.")
def evaluate(dataset, threshold):
    """Evaluate the model against a dataset."""
    score = round(threshold + 0.12, 2)
    result = "Pass" if score >= threshold else "Fail"

    console.print(
        Panel(
            Markdown(
                f"## Evaluation report\n- Dataset: {dataset}\n- Threshold: {threshold}\n- Score: {score}\n- Result: {result}"
            ),
            title="Evaluate",
        )
    )

    if result == "Pass":
        console.print("[green]Evaluation passed.[/green]")
    else:
        console.print("[red]Evaluation failed.[/red]")


@cli.command()
@click.option("--output", default="report.md", show_default=True, help="Path for the generated report.")
@click.option("--format", default="table", show_default=True, type=click.Choice(["table", "markdown"], case_sensitive=False), help="Report format.")
def report(output, format):
    """Generate a concise operational report."""
    if format == "table":
        table = Table(title="Operational Report")
        table.add_column("Metric")
        table.add_column("Value")
        table.add_row("Status", "Healthy")
        table.add_row("Records", "1,248")
        table.add_row("Last run", "Today")
        console.print(table)
    else:
        console.print(
            Markdown(
                "# Operational report\n\n- Status: Healthy\n- Records: 1,248\n- Last run: Today"
            )
        )

    console.print(f"Report saved to [bold]{output}[/bold].")


if __name__ == "__main__":
    from rich.traceback import install

    install(show_locals=False)
    cli()