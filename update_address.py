#!/usr/bin/env python3
import os

REPO = "/home/claude/patientacquisition"

TARGET_FILES = [
    "pricing.html",
    "about.html",
    "london/dental-marketing-camden-town.html",
    "london/dental-marketing-hampstead.html",
    "london/dental-marketing-belsize-park.html",
    "london/dental-marketing-kentish-town.html",
    "london/dental-marketing-primrose-hill.html",
    "london/dental-marketing-chalk-farm.html",
    "london/dental-marketing-west-hampstead.html",
    "london/dental-marketing-swiss-cottage.html",
    "london/dental-marketing-kings-cross.html",
    "london/dental-patient-acquisition.html",
    "london/local-seo-dental-practices.html",
    "london/google-maps-pack-ranking.html",
    "london/gbp-optimisation-dentists.html",
    "london/hyper-local-seo-nw1.html",
    "london/hyper-local-seo-nw3.html",
    "london/cosmetic-dentistry-marketing.html",
    "london/dental-implant-marketing.html",
    "london/invisalign-marketing-dentists.html",
    "london/teeth-whitening-marketing.html",
    "london/private-dental-practice-marketing.html",
    "london/nhs-dental-practice-marketing.html",
    "london/automated-patient-review-requests.html",
    "london/post-appointment-sms-reviews.html",
    "london/negative-review-protection.html",
    "london/dental-practice-competitor-analysis.html",
    "london/missed-call-text-back.html",
    "london/lost-patient-recovery.html",
    "london/after-hours-patient-automation.html",
    "london/marketing-consultant.html",
    "london/internet-marketing-service.html",
    "london/google-reviews-service.html",
    "london/missed-call-recovery-service.html",
    "london/reputation-management-service.html",
]

# Ordered list of (description, find, replace) pairs.
# Order matters: longer/more specific multi-line patterns go first.
REPLACEMENTS = [
    (
        "Schema streetAddress field",
        '"streetAddress": "Suite G04, 1 Quality Court, Chancery Lane",',
        '"streetAddress": "5-7 Buck Street",',
    ),
    (
        "Schema postalCode field",
        '"postalCode": "WC2A 1HR",',
        '"postalCode": "NW1 8NJ",',
    ),
    (
        "Footer pin-emoji address (single line, common variant)",
        '\U0001F4CD Suite G04, 1 Quality Court<br>Chancery Lane, London WC2A 1HR',
        '\U0001F4CD 5-7 Buck Street<br>London NW1 8NJ',
    ),
    (
        "Footer address (3-line variant, google-reviews-service)",
        '            Suite G04, 1 Quality Court<br>\n            Chancery Lane<br>\n            London WC2A 1HR',
        '            5-7 Buck Street<br>\n            London NW1 8NJ',
    ),
    (
        "Footer address (single-line 3-part variant, missed-call-recovery-service)",
        '            Suite G04, 1 Quality Court<br>Chancery Lane<br>London WC2A 1HR',
        '            5-7 Buck Street<br>London NW1 8NJ',
    ),
    # --- Bonus consistency fixes for pages that already use the new address ---
    (
        "Bonus: fix stray leading <br> before Buck Street (camden-town)",
        '<br>5-7 Buck Street<br>London NW1 8NJ</div>',
        '5-7 Buck Street<br>London NW1 8NJ</div>',
    ),
    (
        "Bonus: normalise '5-7<br>Buck street' formatting (reputation-management)",
        '5-7<br>Buck street<br>London NW1 8NJ',
        '5-7 Buck Street<br>London NW1 8NJ',
    ),
]

report = []

for rel_path in TARGET_FILES:
    full_path = os.path.join(REPO, rel_path)
    if not os.path.exists(full_path):
        report.append((rel_path, ["FILE NOT FOUND"]))
        continue

    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()

    file_changes = []
    for desc, find, replace in REPLACEMENTS:
        count = content.count(find)
        if count:
            content = content.replace(find, replace)
            file_changes.append(f"{desc}: {count} replacement(s)")

    if file_changes:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        report.append((rel_path, file_changes))
    else:
        report.append((rel_path, ["no matching old-address patterns found"]))

# Print report
for rel_path, changes in report:
    print(f"\n{rel_path}")
    for c in changes:
        print(f"  - {c}")
