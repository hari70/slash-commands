# Invoicing toolkit

Client tracker + branded PDF invoice. Driven by the `/invoice` command
(`../commands/invoice.md`), or run directly.

Two tracker shapes, picked by who pays the vendors:

    # you front vendor costs and pass them through (Clarity i2)
    python3 invoice.py init --client "Clarity i2" --company "Odyssey Tech LLC" \
        --mode subscriptions --out ~/OdysseyTech/Clients/ClarityI2 --logo ~/OdysseyTech/invoice-logo.png

    # the client pays their own vendors; you bill work (Cyber9 owns its GovCloud)
    python3 invoice.py init --client "Cyber9" --company "Odyssey Tech LLC" \
        --mode services --out ~/OdysseyTech/Clients/Cyber9 --logo ~/OdysseyTech/invoice-logo.png

    python3 invoice.py invoice --book <workbook.xlsx> [--month Sep-2026]

In `subscriptions` a month cell is an AMOUNT. In `services` the row carries a Rate
and a month cell is a QUANTITY (hours/units); leave Rate blank to bill a flat
amount, so retainers and hourly coexist in one sheet.
The TOTAL row applies the same rule (quantity x Rate, or the amount when Rate is
blank), so the sheet's total always equals what the invoice bills. Tests:
`python invoicing/test_invoice.py` (needs `openpyxl` and `formulas`).

**The workbook is the source of truth.** `invoice` only reads it, so regenerating
never clobbers entered figures. A blank amount is never billed and is always
reported on stdout — that warning is the guard against silently under-invoicing.

Columns are located by header TEXT, not position, so workbooks created before the
Rate column existed keep working unchanged.

Generalised from the PedalAI/Clarity i2 build (2026-08). Requires `openpyxl` and
Chrome/Chromium for headless PDF rendering.
