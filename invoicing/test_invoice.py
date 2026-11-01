"""
Tests for invoice.py — run with a Python that has openpyxl and formulas:

    python -m pip install openpyxl formulas
    python invoicing/test_invoice.py

The TOTAL row is checked by EVALUATING the workbook's formulas (the `formulas`
package is a pure-Python Excel engine), not by reading the formula text: the
question is what the sheet shows, and that is what Michael-facing totals are
reconciled against.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import formulas
import openpyxl

HERE = Path(__file__).resolve().parent
TOOL = HERE / "invoice.py"
HEAD_ROW = 4


def init(tmp: Path, mode: str, rows: int = 3) -> Path:
    subprocess.run(
        [sys.executable, str(TOOL), "init", "--client", "Acme", "--company", "Odyssey Tech LLC",
         "--mode", mode, "--out", str(tmp), "--start", "2026-07", "--rows", str(rows)],
        check=True, capture_output=True, text=True,
    )
    return next(tmp.glob("*.xlsx"))


def fill(book: Path, lines: list[dict]) -> None:
    """Write rows starting under the header: {name, rate (or None), Jul-2026: value}."""
    wb = openpyxl.load_workbook(book)
    ws = wb.worksheets[0]
    hdr = {ws.cell(row=HEAD_ROW, column=c).value: c for c in range(1, ws.max_column + 1)}
    for i, line in enumerate(lines):
        r = HEAD_ROW + 1 + i
        ws.cell(row=r, column=1).value = line["name"]
        if "Rate" in hdr:
            ws.cell(row=r, column=hdr["Rate"]).value = line.get("rate")
        ws.cell(row=r, column=hdr["Jul-2026"]).value = line["Jul-2026"]
    wb.save(book)


def evaluated_total(book: Path, month: str = "Jul-2026") -> float:
    """What the TOTAL row actually shows for `month`, computed by a formula engine."""
    wb = openpyxl.load_workbook(book)
    ws = wb.worksheets[0]
    col = next(c for c in range(1, ws.max_column + 1) if ws.cell(row=HEAD_ROW, column=c).value == month)
    trow = next(r for r in range(HEAD_ROW + 1, ws.max_row + 1)
                if str(ws.cell(row=r, column=1).value or "").upper().startswith("TOTAL"))
    ref = f"{openpyxl.utils.get_column_letter(col)}{trow}"
    sol = formulas.ExcelModel().loads(str(book)).finish().calculate()
    key = next(k for k in sol if k.upper().endswith(f"'!{ref}") and ws.title.upper() in k.upper())
    return float(sol[key].value[0, 0])


def billed_total(book: Path, month: str = "Jul-2026") -> float:
    """What the PDF invoice would bill for `month` (invoice.py's own reader)."""
    sys.path.insert(0, str(HERE))
    import invoice  # noqa: E402
    _, _, _, total, _ = invoice.read_book(book, month)
    return total


def test_services_total_is_quantity_times_rate() -> None:
    with tempfile.TemporaryDirectory() as d:
        book = init(Path(d), "services")
        fill(book, [
            {"name": "Retainer (flat)", "rate": None, "Jul-2026": 1000},
            {"name": "Consulting (hourly)", "rate": 120, "Jul-2026": 54},
        ])
        sheet = evaluated_total(book)
        assert sheet == 1000 + 54 * 120, f"TOTAL row shows {sheet}, expected 7480"
        assert sheet == billed_total(book), "the sheet's TOTAL and the invoice disagree"


def test_subscriptions_total_still_sums_amounts() -> None:
    with tempfile.TemporaryDirectory() as d:
        book = init(Path(d), "subscriptions")
        fill(book, [
            {"name": "Apollo", "Jul-2026": 1000},
            {"name": "Azure", "Jul-2026": 250.5},
        ])
        sheet = evaluated_total(book)
        assert sheet == 1250.5, f"TOTAL row shows {sheet}, expected 1250.5"
        assert sheet == billed_total(book)


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}")
            except AssertionError as e:
                failed += 1
                print(f"FAIL {name}: {e}")
    sys.exit(1 if failed else 0)
