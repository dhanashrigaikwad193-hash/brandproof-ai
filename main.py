from flask import Flask, request
from datetime import datetime
import re

app = Flask(__name__)


HTML = """
<!DOCTYPE html>
<html>

<head>

<title>BrandProof AI</title>

<meta name="viewport" content="width=device-width, initial-scale=1">

<style>

body {
    font-family: Arial, sans-serif;
    background: #f3f6fa;
    margin: 0;
    padding: 20px;
}

.container {
    max-width: 750px;
    margin: auto;
}

.header {
    background: #172b4d;
    color: white;
    padding: 28px;
    border-radius: 14px;
    margin-bottom: 20px;
}

.header h1 {
    margin: 0 0 8px 0;
    font-size: 30px;
}

.header p {
    margin: 0;
    color: #dbe5f5;
}

.intro {
    background: white;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
}

.card {
    background: white;
    padding: 22px;
    border-radius: 12px;
    margin-bottom: 20px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
}

label {
    display: block;
    font-weight: bold;
    margin-top: 15px;
    margin-bottom: 8px;
    color: #172b4d;
}

textarea,
input[type="text"] {
    width: 100%;
    box-sizing: border-box;
    padding: 13px;
    border: 1px solid #ccd5e0;
    border-radius: 8px;
    font-size: 15px;
    font-family: Arial, sans-serif;
}

textarea {
    min-height: 140px;
    resize: vertical;
}

input[type="text"] {
    height: 45px;
}

button {
    margin-top: 20px;
    width: 100%;
    background: #172b4d;
    color: white;
    border: none;
    padding: 14px;
    border-radius: 8px;
    font-size: 16px;
    font-weight: bold;
}

.result {
    background: white;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    border-left: 5px solid #172b4d;
}

.claim-label {
    font-size: 13px;
    color: #6b778c;
    font-weight: bold;
    text-transform: uppercase;
}

.claim {
    font-size: 17px;
    font-weight: bold;
    color: #172b4d;
}

.supported {
    color: #15803d;
    font-weight: bold;
    font-size: 16px;
}

.conflict {
    color: #dc2626;
    font-weight: bold;
    font-size: 16px;
}

.verify {
    color: #d97706;
    font-weight: bold;
    font-size: 16px;
}

.reason {
    color: #374151;
    line-height: 1.5;
}

.evidence {
    background: #f6f8fb;
    padding: 12px;
    border-radius: 8px;
    color: #374151;
    line-height: 1.5;
}

.suggestion {
    background: #fff7ed;
    border-left: 4px solid #f97316;
    padding: 12px;
    border-radius: 6px;
    color: #7c2d12;
}

.fresh {
    border-left-color: #16a34a;
}

.old {
    border-left-color: #f97316;
}

.footer {
    text-align: center;
    color: #6b7280;
    font-size: 13px;
    margin-top: 25px;
}

.small {
    font-size: 13px;
    color: #6b7280;
    margin-top: 6px;
}

</style>

</head>


<body>

<div class="container">

<div class="header">

<h1>BrandProof AI</h1>

<p>
Claim Passport — Marketing Claim Verification
</p>

</div>


<div class="intro">

<h2>Protect your brand claims</h2>

<p>
Check marketing statements against approved evidence before publishing.
</p>

<p>
BrandProof AI helps identify supported claims,
conflicting information, and claims that need
further verification.
</p>

</div>


<div class="card">

<form method="POST">

<label>
Marketing Draft
</label>

<textarea
name="draft"
placeholder="Enter your marketing content here..."
required
>{{ draft }}</textarea>


<label>
Approved Evidence
</label>

<textarea
name="evidence"
placeholder="Enter approved product facts or evidence here..."
required
>{{ evidence }}</textarea>


<label>
Evidence Review Date
</label>

<input
type="text"
name="review_date"
value="{{ review_date }}"
placeholder="DD/MM/YYYY"
>

<div class="small">
Enter the date when the approved evidence should be reviewed again.
</div>


<button type="submit">
Check Claims →
</button>

</form>

</div>


<h2 style="color:#172b4d;">
Claim Passport Results
</h2>

{{ results }}


<div class="footer">

BrandProof AI • Claim-level traceability for safer marketing

</div>

</div>

</body>

</html>
"""


def check_claims(draft, evidence):

    results = ""

    evidence_sentences = [
        s.strip()
        for s in re.split(r'[.!?]+', evidence)
        if s.strip()
    ]

    claims = [
        s.strip()
        for s in re.split(r'[.!?]+', draft)
        if s.strip()
    ]

    stop_words = {
        "our", "the", "is", "are", "was", "were",
        "this", "that", "with", "from", "for",
        "and", "can", "will", "it", "its", "to",
        "of", "in", "on", "a", "an", "as",
        "approximately", "expected", "customers",
        "product"
    }

    synonym_map = {
        "lasts": "life",
        "lasting": "life",
        "lifetime": "life",
        "duration": "life",
        "years": "year",

        "save": "saving",
        "saves": "saving",
        "saved": "saving",
        "savings": "saving",
        "discount": "saving",
        "discounts": "saving",
        "off": "saving",

        "recyclable": "recycle",
        "recycled": "recycle",
        "recyclability": "recycle",
        "materials": "material"
    }

    def get_words(text):

        words = re.findall(
            r'\b[a-zA-Z]+\b',
            text.lower()
        )

        cleaned = set()

        for word in words:

            if word in stop_words:
                continue

            word = synonym_map.get(
                word,
                word
            )

            if len(word) > 2:
                cleaned.add(word)

        return cleaned

    def get_numbers(text):

        return re.findall(
            r'\d+(?:\.\d+)?',
            text
        )

    for claim in claims:

        claim_words = get_words(claim)
        claim_numbers = get_numbers(claim)

        best_evidence = ""
        best_score = 0
        best_common = set()

        for evidence_sentence in evidence_sentences:

            evidence_words = get_words(
                evidence_sentence
            )

            common_words = claim_words.intersection(
                evidence_words
            )

            score = len(common_words)

            if claim_numbers:

                evidence_numbers = get_numbers(
                    evidence_sentence
                )

                if evidence_numbers:
                    score += 2

            if score > best_score:

                best_score = score
                best_evidence = evidence_sentence
                best_common = common_words

        suggestion = ""

        if best_score == 0:

            status = "⚠ Needs Verification"
            status_class = "verify"

            reason = (
                "No sufficient supporting evidence "
                "was found for this claim."
            )

            evidence_used = (
                "No matching approved evidence was found."
            )

        else:

            evidence_numbers = get_numbers(
                best_evidence
            )

            if claim_numbers:

                if len(best_common) == 0:

                    status = "⚠ Needs Verification"
                    status_class = "verify"

                    reason = (
                        "A numeric value was found in "
                        "the evidence, but it does not "
                        "relate to this claim."
                    )

                    evidence_used = (
                        "No relevant numeric evidence "
                        "was found."
                    )

                elif not evidence_numbers:

                    status = "⚠ Needs Verification"
                    status_class = "verify"

                    reason = (
                        "The claim contains a numeric "
                        "value, but the matching evidence "
                        "does not provide a supporting "
                        "numeric value."
                    )

                    evidence_used = best_evidence

                else:

                    claim_number = claim_numbers[0]

                    if claim_number in evidence_numbers:

                        status = "✓ Supported"
                        status_class = "supported"

                        reason = (
                            "The claim's numeric information "
                            "matches the approved evidence."
                        )

                        evidence_used = best_evidence

                    else:

                        status = "✗ Conflict"
                        status_class = "conflict"

                        correct_number = evidence_numbers[0]

                        reason = (
                            "The claim contains a numeric "
                            "value that conflicts with the "
                            "approved evidence."
                        )

                        corrected_claim = claim.replace(
                            claim_number,
                            correct_number
                        )

                        suggestion = f"""
<p class="suggestion">

<b>Suggested Correction:</b><br>

{corrected_claim}

</p>
"""

                        evidence_used = best_evidence

            else:

                if len(best_common) >= 1:

                    status = "✓ Supported"
                    status_class = "supported"

                    reason = (
                        "The approved evidence contains "
                        "matching information that supports "
                        "this claim."
                    )

                    evidence_used = best_evidence

                else:

                    status = "⚠ Needs Verification"
                    status_class = "verify"

                    reason = (
                        "The claim could not be fully "
                        "verified using the approved evidence."
                    )

                    evidence_used = best_evidence

        results += f"""
<div class="result">

<div class="claim-label">
Claim
</div>

<p class="claim">
{claim}
</p>

<p class="{status_class}">
{status}
</p>

<p class="reason">
<b>Explanation:</b><br>
{reason}
</p>

<p class="evidence">
<b>Evidence Used:</b><br>
{evidence_used}
</p>

{suggestion}

</div>
"""

    return results


@app.route("/", methods=["GET", "POST"])
def home():

    draft = ""
    evidence = ""
    review_date = ""
    results = ""

    if request.method == "POST":

        draft = request.form.get(
            "draft",
            ""
        ).strip()

        evidence = request.form.get(
            "evidence",
            ""
        ).strip()

        review_date = request.form.get(
            "review_date",
            ""
        ).strip()

        results = check_claims(
            draft,
            evidence
        )

        # Evidence Freshness

        if review_date:

            try:

                review_day = datetime.strptime(
                    review_date,
                    "%d/%m/%Y"
                ).date()

                today = datetime.now().date()

                if review_day < today:

                    results += f"""
<div class="result old">

<div class="claim-label">
Evidence Freshness
</div>

<p class="verify">
🟠 Evidence Review Recommended
</p>

<p class="reason">
The evidence review date was
<b>{review_date}</b>.
It is due for review.
</p>

<p class="evidence">
Review the approved evidence before
relying on it for new marketing claims.
</p>

</div>
"""

                else:

                    results += f"""
<div class="result fresh">

<div class="claim-label">
Evidence Freshness
</div>

<p class="supported">
🟢 Evidence Fresh
</p>

<p class="reason">
The evidence review date is
<b>{review_date}</b>.
</p>

<p class="evidence">
No review is currently due based
on the selected date.
</p>

</div>
"""

            except ValueError:

                results += """
<div class="result old">

<div class="claim-label">
Evidence Freshness
</div>

<p class="verify">
⚠ Invalid Review Date
</p>

<p class="reason">
Please enter the date in DD/MM/YYYY format.
</p>

</div>
"""

    return HTML.replace(
        "{{ draft }}",
        draft
    ).replace(
        "{{ evidence }}",
        evidence
    ).replace(
        "{{ review_date }}",
        review_date
    ).replace(
        "{{ results }}",
        results
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
              )
