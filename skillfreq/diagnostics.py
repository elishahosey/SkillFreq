from __future__ import annotations

import atexit
import sys
from dataclasses import dataclass, field
from time import perf_counter

from rich.console import Console


@dataclass
class CommandDiagnostics:
    command: str
    console: Console = field(default_factory=lambda: Console(stderr=True))
    _started_at: float = field(default_factory=perf_counter)
    _finished: bool = False

    def install(self) -> None:
        """Report command lifecycle without replacing Python's traceback."""
        self.console.print(f"[dim][+0.000s] Starting '{self.command}'[/dim]")
        previous_hook = sys.excepthook

        def report_exception(exception_type, exception, traceback) -> None:
            self.fail(exception)
            previous_hook(exception_type, exception, traceback)

        sys.excepthook = report_exception
        atexit.register(self._report_interrupted_exit)

    def phase(self, message: str) -> None:
        self.console.print(f"[dim][+{self.elapsed:.3f}s] {message}[/dim]")

    def complete(self) -> None:
        if not self._finished:
            self._finished = True
            self.console.print(
                f"[green][+{self.elapsed:.3f}s] Completed '{self.command}'[/green]"
            )

    def fail(self, exception: BaseException) -> None:
        if not self._finished:
            self._finished = True
            self.console.print(
                f"[red][+{self.elapsed:.3f}s] '{self.command}' failed: {exception}[/red]"
            )

    @property
    def elapsed(self) -> float:
        return perf_counter() - self._started_at

    def _report_interrupted_exit(self) -> None:
        if not self._finished:
            self.console.print(
                f"[yellow][+{self.elapsed:.3f}s] '{self.command}' exited before completion[/yellow]"
            )
