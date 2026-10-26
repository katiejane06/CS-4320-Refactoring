Theatrical Players Refactoring Kata - Python version
========================================================

Author: Katherine Lawler  
Date: October 25, 2026  
Language: Python

## Project overview and attribution

This project adapts the Theatrical Players example from Martin Fowler's *Refactoring: Improving the Design of Existing Code*, second edition, to Python.

- Original starter repository: https://github.com/emilybache/Theatrical-Players-Refactoring-Kata
- Fowler's first chapter: https://www.thoughtworks.com/insights/books/refactoring2
- Utilizes pytest: https://docs.pytest.org/en/latest/
- Utilizes approvaltests: https://github.com/approvals/ApprovalTests.Python

My modifications extract named calculation functions, introduce enriched performance records, and separate statement-data calculations from plain-text formatting. The HTML renderer uses the same prepared statement data. Performance calculator classes encapsulate the charge and credit rules, and a factory selects the appropriate calculator for each play type.

Added two tests for existing tragedy and comedy boundary behavior and extended the application with a HistoricalCalculator. Added three historical-play tests covering audiences of 20, 21, and 35.

## Setup and test instructions

### Tools and dependencies

- Python 3
- pip
- The dependencies listed in the Python starter project's `requirements.txt`, including pytest
- Git, if cloning the repository or recording changes in commits

Clone the starter repository if needed:

```bash
git clone https://github.com/emilybache/Theatrical-Players-Refactoring-Kata.git
cd Theatrical-Players-Refactoring-Kata
```

Open the Python starter directory. Run the following commands from the directory containing its `requirements.txt` and tests:

```bash
python3 -m pip install -r requirements.txt
python3 -m pytest
```

No separate compilation step is required for this Python implementation.

## Initial implementation review - Part 1

The original implementation had several maintainability issues:

1. The statement function handled multiple responsibilities, including play lookup, charge calculations, volume-credit calculations, and output formatting.
2. Limited explanations and unnamed numeric values made it difficult to understand the charging rules on first reading.
3. A comment described extra credit for every ten comedy attendees, while the implementation awarded credit for every five. This inconsistency made the intended behavior unclear.
4. Play-type conditionals meant that introducing another category would require editing the calculation logic.

## Test results

Run tests using `python3 -m pytest`.

### Initial results

======================================================= test session starts ========================================================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/katherinelawler/CS 4320/Refactoring/CS-4320-Refactoring/python
configfile: pytest.ini
testpaths: tests
plugins: approvaltests-0.2.4, approvaltests-17.4.3
collected 2 items                                                                                                                  

tests/test_statement.py ..                                                                                                   [100%]

======================================================== 2 passed in 0.01s =========================================================

The existing automated tests were run after each refactoring step, and the results matched the initial test run each time.

## Significant refactoring steps - Part 2

### 1. Extract the charge calculation

(a)What changed: Decomposed the statement function by moving the charge-calculation conditional into a separate function named `calculate_amount`.

(b)Why it improved the design: The function name explains the purpose of the calculation. Isolating the charging rules makes them easier to understand and change without editing the rest of the statement logic.

(c)Behavior verification: Ran the existing automated tests after this change and confirmed that the results matched the initial test run.

### 2. Extract the remaining calculations

(a)What changed: Moved the volume-credit calculation and the two total calculations into `calculate_volume_credits`, `calculate_total_amount`, and `calculate_total_volume_credits`. The total functions use Python's `sum()` to aggregate the prepared performance values.

(b)Why it improved the design: Each calculation has a meaningful name and a focused responsibility. The totals are expressed directly instead of being mixed into output construction.

(c)Behavior Verification: Ran the existing automated tests after this change and confirmed that the results matched the initial test run.

### 3. Introduce enriched performance records

(a)What changed: Added `enrich_performance`, which makes a shallow copy of each performance and adds its associated play, calculated amount, and volume credits. Stored the enriched records in the intermediate `statement_data` dictionary along with the customer and totals.

(b)Why it improved the design: The renderer receives the information it needs in one structure. Copying each performance avoids adding calculated fields to the original performance dictionary. The calculation order makes the dependencies explicit: attach the play first, then calculate its amount and credits.

(c)Behavior verification: Ran the existing automated tests after this change and confirmed that the results matched the initial test run.

### 4. Separate calculations from formatting

(a)What changed: Extracted the data-building code and its nested calculation helpers into `create_statement_data` in a separate Python file. Updated `statement` to pass that function's result to `render_plain_text`.

(b)Why it improved the design: Calculation and formatting now have separate responsibilities. The renderer reads prepared values, while the data-building function owns the charging and credit rules. The same data structure can support multiple output formats.

(c)Behavior verification: Ran the existing automated tests after this change and confirmed that the results matched the initial test run.

### 5. Encapsulate calculations and replace conditionals with polymorphism

(a)What changed: Introduced `PerformanceCalculator` to store each performance and its play, and moved amount and volume-credit calculations into properties. Added `TragedyCalculator` and `ComedyCalculator` subclasses and a `create_performance_calculator` factory to select the appropriate class. Moved each charge calculation into its subclass. Kept the standard credit calculation in the parent and overrode it in the comedy subclass to add its bonus using `super().volume_credits`. Updated `enrich_performance` to use the calculator properties and removed the original nested individual-calculation functions.

(b)Why it improved the design: Each calculator groups performance data with the rules that use it. Type-specific calculations are isolated in their subclasses, shared credit logic is reused, and the remaining play-type selection is centralized in the factory. Callers use the same interface regardless of play type, making additional categories easier to introduce without changing formatting or enrichment logic.

(c)Behavior verification: Ran the existing automated tests after the incremental changes within this step and confirmed that the results matched the initial test run.

### Git commit history

The five entries above summarize the major refactorings. The Git commit history provides the record of smaller incremental changes for part 2.

b14354c (origin/main, origin/HEAD, main) Initial commit
eada1aa calculate_amount function separation
0cb8d4a calculate_amount variable name change
95a3b33 calculate_amount parameter name change
f6da22e get_play function separation
8e00245 nested function rearrangement
fd99da1 inline variable function replacement
be1bffd calculate_amount variable to function replacement
83a6a84 calculate_amount play paramter deletion
1918f88 inline unchanged variable function replacement
8419641 calculate_volume_credits function separation
1d46722 calculate_volume_credits variable renaming
3160ebc format_as_USD function renaming
c6104b3 volume credit loop separation
9fc53ca calculate_total_volume_credits function created
82fabd4 calculate_total_amount function created
2b8c265 variable name cleanup
2072557 render_plain_text function creation and nested function rearrangement
06bb5e2 statement_data dictionary creation
6417145 statement_data data added
3d3b61a enrich_performance function creation
c7a3c77 enrich_performance expansion and rework
3f9c60d calculate_amount move and rework
f543179 calculate_volume_credits move and rework
8b203c2 total calculate functions moved
120248b function clean up
2bab13f create_statement_data function creation and move
88db3bb create_statement_data moved to separate file
5fe718d create_statement_data return value name update
adb4f01 html functions added
42ec067 format function moved
66ae771 Performance Calculator class creation
7e099ab Performance Calculator class expansion
03f8251 amount added to PerformanceCalculator
e5d999a volume_credits added to PerformanceCalculator
75b2762 creating subclasses
c6f01dd create_performance_calculator function added
7c280f9 tragedy and comedy calculators amount functions added
9ba49ab PerformanceCalculator amount deleted (subclass responsibility)
3963443 (HEAD -> refactor-process) volume_credit calculations moved to subclasses

### Python adaptation

Nested helpers are defined before the data-building code calls them. Unlike JavaScript function declarations, Python's `def` statements must execute before the functions are called. Helpers inside `create_statement_data` can access its `plays` parameter through enclosing-function scope.

JavaScript getters are represented with Python's `@property`, allowing the calculated values to be read without method-call parentheses. Subclasses inherit the constructor, and `super().volume_credits` reuses the parent's standard credit calculation. Integer floor division (`// 5`) calculates the comedy bonus.

### Additional output capability

The HTML step introduces `html_statement` and `render_html`, using the same prepared data. The `format_as_usd` formatting helper moves to module scope so both renderers can use it. Adding HTML is a new output capability; the behavior-preserving refactoring is the separation that makes this addition possible.

## Additional tests for existing behavior - Part 3

### Test 1

Test name: test_tragedy_at_30_attendees()

Purpose: Verifies that a tragedy with exactly 30 attendees receives no audience surcharge and earns zero volume credits.

Verification: Ran this test against both the original implementation and the refactored implementation using python3 -m pytest. The test passed in both versions, confirming that the existing behavior was preserved.

### Test 2

Test name: test_comedy_at_20_attendees()

Purpose: Verifies that a comedy with exactly 20 attendees receives no audience surcharge, still includes the per-attendee charge, and earns four volume credits.

Verification: Ran this test against both the original implementation and the refactored implementation using python3 -m pytest. The test passed in both versions, confirming that the existing behavior was preserved.

### Updated Test Results
======================================================= test session starts ========================================================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/katherinelawler/CS 4320/Refactoring/CS-4320-Refactoring/python
configfile: pytest.ini
testpaths: tests
plugins: approvaltests-0.2.4, approvaltests-17.4.3
collected 4 items                                                                                                                  

tests/test_statement.py ....                                                                                                 [100%]

======================================================== 4 passed in 0.01s =========================================================

## Historical-play extension - Part 4

The required rules for the `historical` play type are:

- Base charge: $500.
- Add $15 per attendee beyond 20.
- Award one volume credit for every five attendees, rounded down.

Implemented using `HistoricalCalculator` subclass and addition to `create_performance_calculator`.

### Additional Tests

Test 1 Name: test_historical_at_20_attendees()

Purpose: Confirms no surcharge at the boundary.

Test 2 Name: test_historical_at_21_attendees()

Purpose: Confirms the $15 surcharge starts immediately above 20 and credits round down.

Test 3 Name: test_historical_at_35_attendees()

Purpose: Checks the provided assignment example and catches accidentally adding the parent’s extra credits.

### Final Test Results

================================================================ test session starts =================================================================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/katherinelawler/CS 4320/Refactoring/CS-4320-Refactoring/python
configfile: pytest.ini
testpaths: tests
plugins: approvaltests-0.2.4, approvaltests-17.4.3
collected 7 items                                                                                                                                    

tests/test_statement.py .......                                                                                                                [100%]

================================================================= 7 passed in 0.01s ==================================================================

## Reflection - Part 5

The refactoring that most improved the design was replacing the play-type calculation conditionals with polymorphism. Extracting functions and separating calculations from formatting made the code easier to follow, but the calculator subclasses made it easier to extend. TragedyCalculator and ComedyCalculator each contain their own charging rules, while PerformanceCalculator provides the shared data and standard volume-credit calculation. The comedy subclass adds its bonus by reusing the parent calculation. This organization makes the differences between play types clear without requiring one calculation function to handle every category.

Refactoring changes the internal structure of software while preserving its existing externally observable behavior. Moving calculations into functions or classes should not change the charges, credits, or original statement output. Adding historical plays is different because it introduces functionality that the original implementation did not support. Keeping the structural changes separate from that extension made it easier to understand the purpose of each change. The existing automated tests provided a way to check for unintended changes, and the additional tragedy and comedy boundary tests focused on behavior at the audience surcharge thresholds.

The refactored design helped me add historical plays by giving the new rules a clear location. I added HistoricalCalculator with its own amount and volume_credits properties and added historical to the factory's selection logic. The statement renderers and the code that assembles the enriched performances did not need new play-type branches. One detail I had to account for was that amounts are stored in cents, so the $500 base charge is represented as 50000 and the $15 surcharge as 1500. Historical credits also replace the standard credit rule instead of adding to it, so the subclass returns audience divided by five using floor division without calling the parent's credit property.

Several original maintainability issues were resolved. The statement function no longer combines calculations and formatting, meaningful function and class names explain responsibilities, and each play type's charging rules are isolated. The credit calculations are also easier to inspect directly instead of relying on the original misleading comment. Numeric constants remain in the formulas, so named constants could make their meanings clearer. The new historical tests cover audiences of 20, 21, and 35 to check the surcharge boundary, rounded-down credits, and the assignment's example. Together, the design changes and focused tests make future modifications easier to understand and verify.