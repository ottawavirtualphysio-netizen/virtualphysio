/**
 * Google Apps Script for booking form -> Google Sheets.
 * 1) Create a Google Sheet and copy its ID.
 * 2) In Apps Script, replace SHEET_NAME.
 * 3) Deploy as Web App with access: Anyone.
 * 4) Paste the Web App URL into data-google-sheet-url in booking.html/contact.html.
 */
const SHEET_NAME = "Appointments";

function doPost(e) {
  try {
    const payload = JSON.parse(e.postData.contents || "{}");
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
    if (!sheet) {
      return ContentService.createTextOutput(
        JSON.stringify({ ok: false, error: "Sheet not found" })
      ).setMimeType(ContentService.MimeType.JSON);
    }

    sheet.appendRow([
      new Date(),
      payload.name || "",
      payload.phone || "",
      payload.email || "",
      payload.service || "",
      payload.date || "",
      payload.time || "",
      payload.message || "",
      payload.source || ""
    ]);

    return ContentService.createTextOutput(
      JSON.stringify({ ok: true })
    ).setMimeType(ContentService.MimeType.JSON);
  } catch (error) {
    return ContentService.createTextOutput(
      JSON.stringify({ ok: false, error: String(error) })
    ).setMimeType(ContentService.MimeType.JSON);
  }
}
