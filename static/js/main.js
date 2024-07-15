
// const HOME_URL = 'http://127.0.0.1:8000/api'
// const HOME_URL = 'https://clownfish-app-8om3z.ondigitalocean.app/api:8000'
const HOME_URL = 'https://clownfish-app-8om3z.ondigitalocean.app/dob-soda2/api'
// const HOME_URL = 'https://couponsdomain.com:8000';

const DATA_INDICATOR = "data";
const LOGIN_INDICATOR = "login";

var stateArr = [];
var loggedIn = false;
var currUserEmail = null;
var accessToken = null;
// enum: login, data
var currScreenIndicator = LOGIN_INDICATOR;

// TOKENS!
// Authorization
//

// -top
// -Listeners
function tempCaptcha() {
    const body = document.getElementById('the-body');
    body.remove();
    // pass cookies
    return fetch(HOME_URL + '/trying', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: "trying"
  }).then()
}

// LOAD TRACKING - add listener
function reload() {
    // entity
    const tracking = document.getElementById('tracking');
    tracking.addEventListener("click", () =>
        clickEntityButton(), false
    );
    // home
    const home = document.getElementById('homee');
    home.addEventListener("click",  () =>
        clickHome(), false
    );
    // build
     const buildings = document.getElementById('building');
    buildings.addEventListener("click",  () =>
        clickBuildingButton(), false
    );
    hideEntityInputField();
    hideBuildingInputField();

}
reload();
console.log("RELOAD");

// -building


function hideBuildingInputField() {
    const ent = document.getElementById('building-tracking');
    ent.style.display = 'none';
    try {
        let bfr = document.getElementById('building-form-response');
        bfr.display.textContent = "--";
        bfr.className = "neutral-message";
    }  catch (e) {console.log(e) }

}

function showBuildingInputField() {
     const ent = document.getElementById('building-tracking');
    ent.style.display = 'block';

}

function hideEntityInputField() {
    const ent = document.getElementById('input-tracking');
    ent.style.display = 'none';
    // let tfr = document.getElementById(`${type_lit}-form-response`);
    try {
        let tfr = document.getElementById('input-form-response');
        tfr.display.textContent = "--";
        tfr.className = "neutral-message";
    } catch (e) {console.log(e) }
}

function showEntityInputField() {
     const ent = document.getElementById('input-tracking');
    ent.style.display = 'block';

}


// -Data Container -big table

class DataContainer {
  constructor() {
    // curr user
    this.userEmail = null;
    // Job Apps Data - raw html string
    this.basicDataTable = null;
    // Tracked:
    this.filings = null;
    this.entities = null;
    this.buildings = null;
  }
}


let data_container = DataContainer;



// -Data Table Actions

function printDataTable() {
    data_container.basicDataTable.then(v => console.log(v));
}

function hideDataTable() {
    // hide the basic data table
    console.log("hide data table");
    let loginForm = document.getElementById('basic-data-table');
    loginForm.style.display = 'none';

}

function showDataTable() {
    console.log("show data table");
    let loginForm = document.getElementById('basic-data-table');
    loginForm.style.display = 'block';
}

 async function insertOrShowDataTable() {
    console.log("insert DT");
    if (document.getElementById('basic-data-table') == null) {
        data_container.basicDataTable.then( result => {
        let anchor = document.getElementById('anchor');
        var tempDiv = document.createElement('div');
        tempDiv.id = "basic-data-table";
        tempDiv.innerHTML =  result;
        // var tableElement = tempDiv.firstElementChild;
        anchor.appendChild(tempDiv);
    });
    } else {
        showDataTable();
    }

}


 function getUserData() {
    let anchor = document.getElementById('anchor');
    console.log(currScreenIndicator)
    const requestBody = {
    email: data_container.userEmail,
    };

  return fetch(HOME_URL + '/get_user_data', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestBody)
  })
  .then(response => {
    // Handle the response from the server
    if (response.ok) {
        const msg= 'Got data';

        // userDataTable = response.body;
        let r = response.text();
        r.then(() => {
            data_container.basicDataTable = r;
            console.log(msg, r);
        });
        // data_container.basicDataTable = r;
      return r;
      // You can redirect the user or perform additional actions here
    } else {
      const errMsg = 'Fetch failed';
      console.error(errMsg);
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

 function showLoginForm() {
    // if not logged in, show form
    let loginForm = document.getElementById('loginForm');
     if (data_container.userEmail !== null)    {
         if (loginForm.style.display === 'block') {
            loginForm.style.display = 'none';
        } else {
            loginForm.style.display = 'block';
        }
     }
}

 function hideLoginForm() {
    let loginForm = document.getElementById('login-formm');
    loginForm.style.display = 'none';
}


 function displayFailedLogin(message) {
        const errorContainer = document.getElementById('error-container');
        errorContainer.innerHTML = ''; // Clear any previous messages

        if (message) {
            const errorMessage = document.createElement('div');
            errorMessage.className = 'error-message';
            errorMessage.textContent = message;
            errorContainer.appendChild(errorMessage);
        }
}


async function homePageAndDataFetch() {
    // Fetch datatable if not present
    // Revert to home page

     console.log("Try data table fetch ");
     // If table not yet fetched, fetch
     let userDataTable = data_container.basicDataTable;
     if (userDataTable == null) {
         userDataTable = await getUserData();
     }
     await insertOrShowDataTable(userDataTable);
}

function hideDataButton() {
    try {
        let dataButton = document.getElementById('dataLoaderButton');
    dataButton.style.display = 'none';
    }
    catch (e) {
        console.log(e);
    }

}

// async function showDataButton() {
//     let dataButton = document.getElementById('dataLoaderButton');
//     dataButton.style.display = 'block';
// }

 function displaySuccessfulLogin(message, email) {
    const successContainer = document.getElementById('success-container');
    successContainer.innerHTML = ''; // Clear any previous messages
    if (message) {
        const msg = document.createElement('div');
        msg.className = 'success-message';
        msg.textContent = `Logged in as ${email}` ;
        successContainer.appendChild(msg);
        hideLoginForm();
        homePageAndDataFetch();
        // currScreenIndicator = DATA_INDICATOR;
        // const btn = document.createElement('button');
        // btn.textContent = "Load data";
        // btn.id = "dataLoaderButton";
        // btn.className = "btn";
        // btn.addEventListener('click', homePageAndDataFetch);
        // successContainer.appendChild(btn);
    }
}


// -Login
function loginUser(event) {
    // after login, fetch data!

  event.preventDefault(); // Prevent the form from submitting and reloading the page
  const url = HOME_URL;
  // Get the form values
  const email = document.getElementById('user_email').value;
  const password = document.getElementById('user_password').value;
  console.log("SIGNING IN...")
  // Create the request body with the form data
  const requestBody = {
    email: email,
    password: password
  };
  let r = fetch(url + '/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestBody)
  })
  .then(response => {
    // Handle the response from the server
    if (response.ok) {
      const msg= 'Login successful';
      console.log(msg);
      displaySuccessfulLogin(msg, email);
      // UPDATE EMAIL
      // currUserEmail = email;
      data_container.userEmail = email;


    } else {
      const errMsg = 'Login failed';
      console.error(errMsg);
      displayFailedLogin(errMsg);
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
}


// -Anchor
function hideAnchor() {
    let anchor = document.getElementById('anchor');
    anchor.style.display = 'none';
    hideLoginForm();
    console.log("HIDE ANCHOR");
}

function showAnchor() {
    let anchor = document.getElementById('anchor');
    anchor.style.display = 'block';
    showLoginForm();
    console.log("SHOW ANCHOR")
}

// -Entities
async function getTrackedEntities(event) {
  const url = HOME_URL;
  // Get the form values
  // const email = document.getElementById('user_email').value;
    const email = data_container.userEmail;
  // Create the request body with the form data
  const requestBody = {
    email: email,
  };

  return fetch(url + '/get_user_tracked_entities', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestBody)
  })
  .then(response => {
    // Handle the response from the server
    if (response.ok) {
      const msg= 'entities fetched';
      console.log(msg);
      // displaySuccessfulLogin(msg, email);
      // UPDATE EMAIL
      // currUserEmail = email;
      let r = response.text();
      // r.then(data_container.userEmail = r);
      r.then(() => {data_container.entities = r});
      return r;

    } else {
      const errMsg = 'entities failed';
      console.error(errMsg);
      displayFailedLogin(errMsg);
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });

}


async function showEntitiesTable() {
    console.log("show entities ")
    let elt = document.getElementById('entities-data-table');
    if (elt == null)
      {
        let anchor = document.getElementById('anchor');
        var tempDiv = document.createElement('div');
        tempDiv.textContent = "Currently Tracked:"
        tempDiv.id = "entities-data-table";
        let htmlString = data_container.entities;
        tempDiv.innerHTML = htmlString;
        console.log(htmlString);
        // var tableElement = tempDiv.firstElementChild;
        anchor.appendChild(tempDiv);
    } else if (elt.style.display === 'none') {
        elt.style.display = 'block';
    }
}

function hideEntitiesTable() {
     // hide the basic data table
    console.log("hide entities table");
    try {
        let loginForm = document.getElementById('entities-data-table');
        loginForm.style.display = 'none';
    } catch (e) {
        console.log(e)
    }
}

async function fetchSodaUpdate() {
    // fetch yesterdays data soda dob

}

async function clickHome() {
    // issue ?
    console.log("CLICK HOME");
    if (data_container.userEmail == null) {
        console.log("undeff")
        showLoginForm();
        // show fetch button


    } else {
        // issue ?
        hideEntitiesTable();
        hideBuildingsTable();  // 7/9
        await homePageAndDataFetch();
        //
    }
    hideEntityInputField();
    hideBuildingInputField();
}


async function clickEntityButton() {
    //entity
    console.log("Click tracking")
    hideLoginForm();
    hideDataTable();
    hideBuildingsTable(); //
    hideBuildingInputField(); //
    showEntityInputField();
    let entitiesData = "";
    // if cached in data_container
    if (data_container.entities == null) {
        entitiesData = getTrackedEntities();
        entitiesData.then(v => {
            console.log(v)
            data_container.entities = v;
            showEntitiesTable();
            // switch screens !!
        }
    );
    } else {
        showEntitiesTable();
    }
}

async function showEntitySubmitResult(msg, was_success, type_lit) {
    let tfr = document.getElementById(`${type_lit}-form-response`);
     if (was_success === true) {
         tfr.className = 'success-message';
     } else { tfr.className = 'error-message'; }
     tfr.textContent = msg;
}


// -entity

async function submitEntity(event) {
    // given form input,
    // try-submit new entity to backend
    event.preventDefault();
  const url = HOME_URL;
  // Get the form values
    const email = data_container.userEmail;
    const et = document.getElementById('entity_type').value;
    const fn = document.getElementById('first_name_et').value;
    const ln = document.getElementById('last_name_et').value;
    const biz = document.getElementById('biz_name_o_et').value;
    const lic = document.getElementById('license').value;
  // Create the request body with the form data
    const requestBody = {
    email: email,
    entity_type: et,
    applicant_first_name: fn,
    applicant_last_name: ln,
    owner_s_business_name: biz,
    applicant_license: lic,
  };

  return fetch(url + '/submit_new_entity', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestBody)
  })
  .then(response => {
    // Handle the response from the server
    if (response.ok) {
      const msg= 'Entity submitted';
      console.log(msg);
      showEntitySubmitResult(msg,true, 'entity');
      // let r = response.text();
      // // r.then(data_container.userEmail = r);
      // r.then(() => {data_container.entities = r});
      // return r;

    } else {
        // never called... issue
      const errMsg = 'Submit Failed';
      console.error(errMsg);
      showEntitySubmitResult(errMsg, false, 'entity');
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
}


// -building

function clickDeleteEntity() {
    // Needs to be expanded upon -
    const col = document.getElementById('del_col_name').value;
    const cell_data = document.getElementById('del_content').value;
    // const item_id = document.getElementById('del-entity').value;
    // const fn = document.getElementById('del_first_name_et').value;
    // const ln = document.getElementById('del_last_name_et').value;
    // const biz = document.getElementById('del_biz_name_o_et').value;
    // const lic = document.getElementById('del_license').value;
    const arr = [fn, ln, biz, lic]

    let p = deleteItem('entity', col, cell_data);  // entity
    let r = p.then( () => {
            clickEntityButton();
        }
    )

}

function clickDeleteBuilding() {
    // only option for building is bin
    const item_id = document.getElementById('del_bin_no').value;
    let p = deleteItem('building',  'bin', item_id);  // building
    let r = p.then( () => {
            clickBuildingButton();
        }
    )

}

async function deleteItem(item_type, lookup_col, item_id) {
    // make request
    const url = HOME_URL;
    // Get the form values
    const email = data_container.userEmail;
    // Create the request body with the form data
    const requestBody = {
    email: email,
    item_type: item_type,
    identifier: item_id,
    col: lookup_col,
  };
  return fetch(url + '/delete_item', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestBody)
  })
  .then(response => {
    // Handle the response from the server
    if (response.ok) {
      const msg= 'Deletion successful';
      console.log(msg);
      showEntitySubmitResult(msg,true, 'item_type');

    } else {
        // never called... issue
      const errMsg = 'Deletion Failed';
      console.error(errMsg);
      showEntitySubmitResult(errMsg, false, 'item_type');
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
}


async function showBuildingsTable() {
    console.log("show bt ")
    let elt = document.getElementById('buildings-data-table');
    if (elt == null)
      {
        let anchor = document.getElementById('anchor');
        var tempDiv = document.createElement('div');
        tempDiv.textContent = "Buildings Currently Tracked:"
        tempDiv.id = "buildings-data-table";
        let htmlString = data_container.buildings;
        tempDiv.innerHTML = htmlString;
        console.log(htmlString);
        // var tableElement = tempDiv.firstElementChild;
        anchor.appendChild(tempDiv);
    } else if (elt.style.display === 'none') {
        elt.style.display = 'block';
    }
}

function hideBuildingsTable() {
     // hide the basic data table
    console.log("hide b table");
    try {
        let t = document.getElementById('buildings-data-table');
        t.style.display = 'none';
    } catch (e) {
        console.log("no buildings table")
    }


}
async function clickBuildingButton() {
    //entity
    console.log("Click building")
    hideLoginForm();
    hideDataTable();
    hideEntitiesTable();
    hideEntityInputField(); //
    showBuildingInputField();
    let buildingsData = "";
    // if cached in data_container
    if (data_container.buildings == null) {
        buildingsData = getTrackedBuildings();
        buildingsData.then(v => {
            console.log(v)
            data_container.buildings = v;
            showBuildingsTable();
            // switch screens !!
        }
    );
    } else {
        showBuildingsTable();
    }
}
async function submitBuilding(event) {
    // given form input,
    // try-submit new entity to backend
    event.preventDefault();
  const url = HOME_URL;
  // Get the form values
    const email = data_container.userEmail;
    const bin = document.getElementById('bin_no').value;
  // Create the request body with the form data
    const requestBody = {
    email: email,
    bin: bin,
  };
  return fetch(url + '/submit_new_building', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestBody)
  })
  .then(response => {
    // Handle the response from the server
    if (response.ok) {
      const msg= 'building submitted';
      console.log(msg);
      showEntitySubmitResult(msg,true, 'building');

    } else {
        // never called... issue
      const errMsg = 'Submit Failed';
      console.error(errMsg);
      showEntitySubmitResult(errMsg, false, 'building');
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });

}


async function getTrackedBuildings(event) {
  const url = HOME_URL;
  // Get the form values
  // const email = document.getElementById('user_email').value;
    const email = data_container.userEmail;
  // Create the request body with the form data
  const requestBody = {
    email: email,
  };

  return fetch(url + '/get_user_tracked_buildings', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestBody)
  })
  .then(response => {
    // Handle the response from the server
    if (response.ok) {
      const msg= 'buildings fetched';
      console.log(msg);

      let r = response.text();
      // r.then(data_container.userEmail = r);
      r.then(() => {data_container.buildings = r});
      return r;

    } else {
      const errMsg = 'buildings failed';
      console.error(errMsg);
      displayFailedLogin(errMsg);
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });

}

// document.addEventListener('DOMContentLoaded', function() {
//     const tracking = document.getElementById('tracking');
//     const navbarMenu = document.getElementById('nb-main');
//
//     tracking.addEventListener('click', function() {
//         navbarMenu.classList.toggle('active');
//     });
//
//     // Identify the special link
//     const specialLink = document.getElementById('special-link');
//
//     // Define the function to be called
//     function specialFunction(event) {
//         event.preventDefault(); // Prevent the default link behavior
//         alert('Special link clicked!');
//         // Add your custom functionality here
//     }
//
//     // Add an event listener to the special link
//     specialLink.addEventListener('click', specialFunction);
// });

