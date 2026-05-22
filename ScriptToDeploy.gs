function doPost(e) {
  try {
    // 1. Parse the incoming JSON body
    const { url, fileName } = JSON.parse(e.postData.contents);

    // 2. Validate inputs
    if (!url) throw new Error("Missing 'url' parameter");
    if (!fileName) throw new Error("Missing 'fileName' parameter");

    // 3. Set your target Google Drive folder ID
    const folderId = 'YOUR_DRIVE_FOLDER_ID';  // <-- Replace with your real folder ID
    const folder = DriveApp.getFolderById(folderId);

    // 4. Fetch the remote file as a Blob
    const response = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
    const blob = response.getBlob();

    // 5. Create the file in your Drive folder
    const file = folder.createFile(blob);

    // 6. Rename the file (optional, but recommended)
    file.setName(fileName);

    // 7. Return success response with file URL
    return ContentService
      .createTextOutput(JSON.stringify({ 
        success: true, 
        fileUrl: file.getUrl(),
        fileName: file.getName()
      }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    // Error handling
    return ContentService
      .createTextOutput(JSON.stringify({ success: false, error: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}