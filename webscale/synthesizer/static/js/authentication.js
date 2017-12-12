 // Client ID and API key from the Developer Console
 var CLIENT_ID = '1093638360673-48ljk7llbf3tpq57u514nh3biupe3fgc.apps.googleusercontent.com';
 var API_KEY = 'AIzaSyA7JofBjhR6yjh1uqJV4FV_MDDQfee4Uyk';

 // Array of API discovery doc URLs for APIs used by the quickstart
 var DISCOVERY_DOCS = ["https://www.googleapis.com/discovery/v1/apis/drive/v3/rest"];

 var SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly https://www.googleapis.com/auth/drive.file';

 var authorizeButton = document.getElementById('authorize-button');
 var signoutButton = document.getElementById('signout-button');

 /**
  *  On load, called to load the auth2 library and API client library.
  */
 function handleClientLoad() {
     gapi.load('client:auth2', initClient);
 }

 /**
  *  Initializes the API client library and sets up sign-in state
  *  listeners.
  */
 function initClient() {
     gapi.client.init({
         apiKey: API_KEY,
         clientId: CLIENT_ID,
         discoveryDocs: DISCOVERY_DOCS,
         scope: SCOPES
     }).then(function () {
         // Listen for sign-in state changes.
         gapi.auth2.getAuthInstance().isSignedIn.listen(updateSigninStatus);

         // Handle the initial sign-in state.
         updateSigninStatus(gapi.auth2.getAuthInstance().isSignedIn.get());
         if (authorizeButton){
             authorizeButton.onclick = handleAuthClick;
         }
         if (signoutButton) {
             signoutButton.onclick = handleSignoutClick;
         }
     });
 }

function updateSigninStatus(isSignedIn) {
    if (!signoutButton) {
        return;
    }

    if (isSignedIn) {
        document.getElementById('drive-auth').innerHTML = '&#10004;';
        document.getElementById('drive-auth').style.color = "green";
        document.getElementById('drive-auth-msg').innerText = 'Authorized for your Google Drive';
        signoutButton.style.display = 'inline-block';
    } else {
        signoutButton.style.display = 'none';
        document.getElementById('drive-auth').innerHTML = '&#10007;';
        document.getElementById('drive-auth').style.color = "red";
        document.getElementById('drive-auth-msg').innerText = 'Not authorized for your Google Drive';
    }
 }

async function handleAuthClick(event) {
    let isSignedIn = await gapi.auth2.getAuthInstance().isSignedIn.get();
    if (!isSignedIn) {
        await gapi.auth2.getAuthInstance().signIn();
        exportProgram();
    } else {
        exportProgram();
    }
}

function exportProgram() {
    const file_name = document.getElementById('snip_name').innerText.slice(23);
    const sketch = getText("snippet_editor");
    const spec = getText("spec_editor");
    const output = getText("synth_results");
    const fileData = "Sketch:\n" + sketch + "\nSpec:\n" + spec
          + "\nSynthesized Output:\n" + output;

    uploadFile(file_name, fileData);
}

 function handleSignoutClick(event) {
     gapi.auth2.getAuthInstance().signOut();
 }

function uploadFile(name,data,callback) {
    const boundary = '-------31415926535897932384';
    const delimiter = "\r\n--" + boundary + "\r\n";
    const close_delim = "\r\n--" + boundary + "--";

    const contentType = 'application/json';

    var metadata = {
        'name': name,
        'mimeType': contentType
    };

    var multipartRequestBody =
        delimiter +
        'Content-Type: application/json\r\n\r\n' +
        JSON.stringify(metadata) +
        delimiter +
        'Content-Type: ' + contentType + '\r\n\r\n' +
        data +
        close_delim;

    var request = gapi.client.request({
        'path': '/upload/drive/v3/files',
        'method': 'POST',
        'params': {'uploadType': 'multipart'},
        'headers': {
            'Content-Type': 'multipart/related; boundary="' + boundary + '"'
        },
        'body': multipartRequestBody});
    if (!callback) {
        callback = function(file) {
            console.log(file)
        };
    }
    request.execute(callback);
}
