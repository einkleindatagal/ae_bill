# Aesthetics & Electrology Bill Batch Extraction

This simplifies submitting health insurance claims for treatment with Aesthetics & Electrology in Seattle.

It will extract a google takeout zip mailbox (.mbox), go through each email to generate a list of dates of treatments, confirm a PDF was received for that date, and organize them into a simple to upload folder for your treatments.

## How To Use

### Gmail Users

1. Label all emails from Aesthetics & Electrology using a search like `electrology` as `electrology export <date>`
   1. It is recommended to do this manually to simplify recognizing the next batch of emails that need processing for the next time you do this.
2. Go to <https://takeout.google.com>
3. Select only the Mail product
4. Select only the new label you created like `electrology export 10/15/25`
5. Wait a couple minutes, and then refresh the page to download the Takeout zip.
6. Wait for the author to invent the rest of the process
