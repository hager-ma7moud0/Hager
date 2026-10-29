from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ss = getSampleStyleSheet()
body = ParagraphStyle("b", parent=ss["BodyText"], fontSize=9, leading=11.5, spaceAfter=3)
h1 = ParagraphStyle("h1", parent=ss["Title"], fontSize=15, leading=18, spaceAfter=2)
h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontSize=11, leading=13, spaceBefore=5, spaceAfter=2)
small = ParagraphStyle("s", parent=body, fontSize=8, leading=10, textColor=colors.HexColor("#444444"))
bul = ParagraphStyle("bl", parent=body, leftIndent=10, bulletIndent=0)

doc = SimpleDocTemplate("report.pdf", pagesize=A4, leftMargin=1.6*cm, rightMargin=1.6*cm,
                        topMargin=1.3*cm, bottomMargin=1.2*cm,
                        title="Sorting Benchmark Lab - Report", author="CS314 student team")
S = []
S.append(Paragraph("Sorting Benchmark Lab: Insertion, Merge, Quick and Python sorted()", h1))
S.append(Paragraph("CS314 &middot; Divide and Conquer &middot; Mini project report", ParagraphStyle("c", parent=small, alignment=1)))

S.append(Paragraph("1. Problem", h2))
S.append(Paragraph(
    "Which sorting algorithm should we use, and how does the input order change the answer? We compare "
    "<b>insertion sort</b>, <b>merge sort</b>, <b>quicksort</b> (last-element pivot, as in the lecture), "
    "<b>quicksort with a random pivot</b> (an extra) and Python's built-in <b>sorted()</b> (Timsort) on "
    "<b>sorted</b>, <b>reversed</b> and <b>random</b> data, and check whether measured running times match theory.", body))

S.append(Paragraph("2. Method", h2))
S.append(Paragraph(
    "All algorithms are in <font face='Courier'>sorts.py</font> and return a new sorted list. They pass unit tests on empty, "
    "single, duplicate, negative, sorted, reversed and random inputs, on the lecture examples (slide 94), and on stability "
    "of merge sort. Timing uses <font face='Courier'>time.perf_counter</font>, the median of 5, 3 or 2 repeats "
    "depending on n, with a fixed random seed. Sizes are n = 1,000 to 100,000. Because pure Python is slow, algorithms that "
    "are quadratic on a given input (insertion on reversed/random, last-pivot quicksort on sorted/reversed) were run only up "
    "to n = 10,000. Quicksort uses an explicit stack, so its worst case is slow but cannot overflow the recursion limit.", body))

S.append(Paragraph("3. Complexity analysis", h2))
S.append(Paragraph(
    "<b>Insertion sort</b>: best case &Theta;(n) (sorted: one comparison, no shifts per element); worst case "
    "&Theta;(n<super>2</super>) with n(n-1)/2 shifts (reversed); average &Theta;(n<super>2</super>) with about half the shifts of the worst case "
    "(each element moves about halfway). <b>Merge sort</b>: T(n) = 2T(n/2) + n, so &Theta;(n log n) for every input "
    "(Master Theorem, case 2), using O(n) extra space. <b>Quicksort (last pivot)</b>: average &Theta;(n log n), but on sorted or "
    "reversed data the pivot is always the minimum or maximum, so T(n) = T(n-1) + n = &Theta;(n<super>2</super>). A random pivot makes this "
    "bad split very unlikely. <b>Timsort</b> finds already-ordered runs, so it is O(n) on sorted or reversed input and "
    "O(n log n) otherwise.", body))

S.append(Paragraph("4. Experiments and results", h2))
S.append(Image("results/time_vs_n.png", width=17.8*cm, height=17.8*cm*4.4/15))
S.append(Paragraph("Figure 1. Median time versus n on log-log axes. Parallel lines with slope 1 are linear / n log n; slope 2 is quadratic.", small))

rows = [["Algorithm", "Sorted", "Reversed", "Random"],
        ["insertion", "1.01", "2.06", "2.04"],
        ["merge", "1.06", "1.09", "1.13"],
        ["quick (last pivot)", "2.03", "1.99", "1.11"],
        ["quick (random pivot)", "1.06", "1.07", "1.07"],
        ["python sorted()", "1.09", "1.06", "1.13"]]
t = Table(rows, colWidths=[4.2*cm, 2.4*cm, 2.4*cm, 2.4*cm])
t.setStyle(TableStyle([
    ("FONTSIZE", (0, 0), (-1, -1), 8.5), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dde6f0")),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("ALIGN", (1, 0), (-1, -1), "CENTER"),
    ("BACKGROUND", (1, 1), (1, 1), colors.HexColor("#ffe9e9")),
    ("BACKGROUND", (2, 1), (3, 1), colors.HexColor("#ffe9e9")),
    ("BACKGROUND", (1, 3), (2, 3), colors.HexColor("#ffe9e9")),
    ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]))
side = Table([[t, Image("results/random_vs_reference.png", width=7.4*cm, height=7.4*cm*4.4/6.4)]],
             colWidths=[11.6*cm, 7.0*cm])
side.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
S.append(side)
S.append(Paragraph("Table 1 (left). Estimated growth exponent: slope of log(time) vs log(n) for n &ge; 2,000; "
                   "shaded cells are the quadratic cases. Figure 2 (right). Random input with c&middot;n<super>2</super> and "
                   "c&middot;n log n reference curves.", small))

S.append(Paragraph("Main observations", h2))
for b in [
    "<b>Best case.</b> Insertion sort on sorted data has slope 1.01: doubling n from 50,000 to 100,000 multiplied the time by 2.03. "
    "It was the fastest of our own implementations there (0.006 s at n = 100,000, versus 0.096 s for merge sort).",
    "<b>Worst and average case.</b> Insertion sort has slope about 2 on both reversed and random data. At n = 10,000 the random "
    "case took 1.03 s and the reversed case 2.07 s: a ratio of 0.50, matching the theory that random input needs about half the "
    "shifts of the worst case. At n = 10,000 insertion sort on random data was 89 times slower than merge sort.",
    "<b>Last-pivot quicksort is not safe.</b> On random data it was the fastest of our own sorts (0.096 s at n = 100,000), but "
    "on sorted data it had slope 2.03 and took 2.40 s at n = 10,000, slower than insertion sort on reversed data. "
    "With a random pivot the same inputs needed only 0.10 s at n = 100,000.",
    "<b>Merge sort is predictable.</b> Slopes of 1.06 to 1.13 on all three inputs, consistent with n log n "
    "(which shows a slope slightly above 1 in this range), and almost the same time on every input order.",
    "<b>Built-in sorted()</b> was about 10 times faster than our merge sort on random data (0.015 s versus 0.150 s) and took "
    "under 1 ms on sorted and reversed data, because it is implemented in C and exploits existing runs.",
]:
    S.append(Paragraph(b, bul, bulletText="\u2022"))

S.append(Paragraph("5. Conclusion and limitations", h2))
S.append(Paragraph(
    "The measurements agree with the theory: &Theta;(n) for insertion sort on sorted data, &Theta;(n<super>2</super>) on reversed and "
    "random data, &Theta;(n log n) for merge sort on every input, and a quadratic worst case for last-pivot quicksort that "
    "random pivoting removes. In practice, use the built-in <font face='Courier'>sorted()</font>; if writing our own, "
    "prefer merge sort or randomised quicksort, and use insertion sort only for tiny or nearly sorted arrays. "
    "<b>Limitations:</b> our smallest size is n = 1,000, so we did not measure the small-n region (n &le; 20-50) where insertion "
    "sort is usually competitive, and we did not test nearly-sorted inputs; quadratic cases stop at n = 10,000; "
    "all numbers come from one machine and pure Python, so absolute times are not portable, only the growth trends.", body))

doc.build(S)
