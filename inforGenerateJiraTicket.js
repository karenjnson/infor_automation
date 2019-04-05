function myFunction() {

}

function onOpen() {
  var ui = SpreadsheetApp.getUi();
  // Or DocumentApp or FormApp.
  ui.createMenu('Create JIRA Ticket')
      .addItem('Generate_Jira', 'sendEmails2')
      .addSeparator()
      .addItem('PreWelcome', 'createJira2')
      .addSeparator()
      .addSubMenu(ui.createMenu('Sub-menu')
          .addItem('Second item', 'menuItem2'))
      .addToUi();
}

function menuItem1() {
  SpreadsheetApp.getUi() // Or DocumentApp or FormApp.
     .alert('You clicked the first menu item!');
}

function menuItem2() {
  SpreadsheetApp.getUi() // Or DocumentApp or FormApp.
     .alert('You clicked the second menu item!');
}

// This constant is written in column C for rows for which an email
// has been sent successfully.
var EMAIL_SENT = 'EMAIL_SENT_ADD_JIRA_TICKET';

/**
 * Sends non-duplicate emails with data from the current spreadsheet.
 */
function sendEmails2() {
  //var sheet = SpreadsheetApp.getActiveSheet();
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Web Channels");
  var startRow = 1; // First row of data to process
  var numRows = sheet.getLastRow(); // Number of rows to process
  var numColumns = 27; // Number of columns to process
  // Fetch the range of cells A2:B3
  var dataRange = sheet.getRange(startRow, 1, numRows, numColumns);
  // Fetch values for each row in the Range.
  var data = dataRange.getValues();
  var now = new Date();
  Logger.log("Sheet:  "+sheet.getName());
  Logger.log("Current Date:  "+now);
  Logger.log("Number of rows:  "+numRows);
  Logger.log("Number of columns:  "+numColumns);
  Logger.log("Data length:  "+data.length);

  for (var i = 5; i < data.length; ++i) {
    var row = data[i];
    var jiraTicket = row[2]; // Column C
    var launchDate = row[5];  // Column F
    var status = row[6]; // Column G
    if (i >= 182) {
      Logger.log("I am on row: "+i+" "+row[0]+" "+row[1])
    };
    if (jiraTicket == "" && (launchDate == "" || launchDate >= now) && status != "InActive" ) {
      Logger.log("A jira ticket for this row will be created:  "+i+" "+row[0]+" "+row[1]);
      emailContent = generateContentForEmail(row);
      Logger.log(emailContent);
      var cell = sheet.getRange(i+1,3);
      cell.setValue("JIRA CREATED by EMAIL\n"+now);
      sheet.getRange(i+1,7).setValue("Active");
      sheet.getRange(i+1,6).setValue(Utilities.formatDate(new Date(), "GMT+10:00", "''yyyy-MM-dd"));


    }
  }
}

function generateContentForEmail(rowData) {
  var column = rowData;
  var launchDate = column[5];
  var today
  var assetContent = "";
  if (column[7] == "Webmail") { assetContent = getWebmailContent(column[22])};
  if (column[7] == "MyBenefits") { assetContent = getMybenefitsContent()};
  var emailContent = ("{panel:title=INFOR OFFER REQUEST|borderStyle=solid|borderColor=white|bgColor=#8a26d0|"+
    "titleColor=white|titleAlign=center}{panel}"+"\n"+
    "{panel:borderStyle=solid|borderColor=#8a26d0|borderWidth=4|bgColor=#f2f2f2}"+"\n"+
    "*Description/History:* "+column[4]+"\n"+
    "*Channel:*  "+column[7]+"\n"+
    "*Placement:* "+column[9]+" / "+column[10]+"\n"+
    "*Business:*  "+column[11]+"\n"+
    "*Product:* "+column[12]+"\n"+
    "*Offer Type:*  "+column[13]+"\n"+
    "*Customer Strategy Group:*  "+column[14]+"\n"+
    "*Business Benefit:*  "+column[16]+"\n"+
    "*Rules:*  [List of rules for this offer]   [to view existing rules look at the Infor Offer Spreadsheet |"+
    "https://docs.google.com/spreadsheets/d/1aVwxIhBDMrqdY5_ruZyDsxGXCWTBjxDUVspcbNW5CdE/edit#gid=0]"+"\n\n\n"+
    assetContent+"\n"+
    "*NCID:*  "+column[23]+"\n"+
    "*CTA URL:*  "+column[25]+"\n"+
    "*How will you determine the Subscriptions/Successes?*  "+"\n"+
    "{panel}"
   )

  var subject = "INFOR Offer: "+column[17];
  sendEmail(subject, emailContent);

return emailContent;

}

function getWebmailContent(cdn_url) {
    return "*Assets: WEBMAIL*"+"\n"+
     "* *CDN Image Url:* "+cdn_url+"\n"+
     "** [Login/Navigate to Membership CDN on AWS HOW TO|"+
     "https://docs.google.com/document/d/1GiRoR5symAvMdfmZcHz93xgH_ybeSdY9BYbmC89TFI4/edit]"+"\n"
}


function getMybenefitsContent() {
   return  "*Assets:  MYBENEFITS*"+"\n"+
    "* *{color:#8eb021}Hero{color}:*"+"\n"+
    "** Image Size:  510x464"+"\n\n"+

    "* *{color:#8eb021}Windowleft {color}:*"+"\n"+
    "** Image Size:  TBA"+"\n"+
    "** Max Char Limit:  58"+"\n"+
    "** CTA Char Count Limit:  10"+"\n"
}

function sendEmail(subject, message) {
    var emailAddress = "infor2jira@teamaol.com";
    //var emailAddress = "karen.r.johnson@verizonmedia.com";
    MailApp.sendEmail(emailAddress, subject, message);
}
