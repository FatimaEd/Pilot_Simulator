let airportId = "";


window.onload = function () {
    showDiv("home");
};

async function showDiv(destinationDivId) {
    let divId = destinationDivId;
    let response = await getData("/api/profiles/current");

    if (response.status !== 200) {
        divId = "profiles"
    }

    let divs = document.getElementsByClassName('content');
    for (let i = 0; i < divs.length; i++) {
        hideElement(divs[i]);
    }

    let selectedDiv = document.getElementById(divId);
    showElement(selectedDiv);

    switch (divId) {
        case "home":
            await loadHomeElements();
            break;
        case "makeATrip":
            let outputResult1 = document.getElementById("output_result");
            while (outputResult1.firstChild) {
                outputResult1.removeChild(outputResult1.firstChild);
            }
            await loadMakeATripElements();
            break;
        case "purchaseFuel":
            let outputResult = document.getElementById("buy_fuel_message");
            outputResult.classList.add("hidden");
            await loadPurchase();
            break;
        case "profiles":
            await loadProfileElements();
            break;
        case "statistics":
            await load_statistics();
            break;


    }
}

async function loadPurchase() {
    let response = await getData("/api/current_status");
    console.log(response.body.current_status)
    setInnerHtml("airport_info_to_purchase_value", response.body.current_status.airport_info_to);
    setInnerHtml("euro_balance_purchase_value", response.body.current_status.euro_balance);
    setInnerHtml("fuel_balance_normal_purchase_value", response.body.current_status.fuel_balance_normal);
    setInnerHtml("fuel_balance_saf_purchase_value", response.body.current_status.fuel_balance_saf);
}

async function loadProfileElements() {

    let response = await getData("/api/profiles");

    let currentProfile = -1;
    let data;

    if (response.status === 200) {
        data = response.body;
    }

    let profileSelector = document.getElementById("profileSelector")

    while (profileSelector.firstChild) {
        profileSelector.removeChild(profileSelector.firstChild);
    }

    response = await getData("/api/profiles/current");

    if (response.status === 200) {
        currentProfile = response.body.profileId;
    }

    for (let key in data) {
        if (data.hasOwnProperty(key)) {
            let value = data[key];
            let newOption = document.createElement('option');

            newOption.value = key;
            newOption.textContent = value;
            profileSelector.appendChild(newOption);
        }
    }

    if (currentProfile !== -1) {
        profileSelector.value = currentProfile;
        hideById("selectAProfileMessage");
    } else {

        showById("selectAProfileMessage");
        profileSelector.selectedIndex = -1;
    }

}

async function loadHomeElements() {
    let response = await getData("/api/current_status");

    setInnerHtml("profile_name_value", response.body.profile_info.profile_name);
    setInnerHtml("aeroplane_model_value", response.body.profile_info.aeroplane_model);
    setInnerHtml("consumption_base_value", response.body.profile_info.consumption_base + " litre/km");
    setInnerHtml("consumption_fullload_value", response.body.profile_info.consumption_fullload + " litre/km");

    setInnerHtml("airport_info_to_value", response.body.current_status.airport_info_to);
    setInnerHtml("euro_balance_value", response.body.current_status.euro_balance);
    setInnerHtml("fuel_balance_normal_value", response.body.current_status.fuel_balance_normal);
    setInnerHtml("fuel_balance_saf_value", response.body.current_status.fuel_balance_saf);

    setInnerHtml("airport_info_from_value", response.body.last_trip_info.airport_info_from);
    setInnerHtml("airport_info_to2_value", response.body.last_trip_info.airport_info_to);
    setInnerHtml("last_trip_passenger_value", response.body.last_trip_info.last_trip_passenger + " people");
    setInnerHtml("last_trip_distance_value", response.body.last_trip_info.last_trip_distance + " km");
    setInnerHtml("last_trip_consumption_normal_value", response.body.last_trip_info.last_trip_consumption_normal + " liter");
    setInnerHtml("last_trip_consumption_saf_value", response.body.last_trip_info.last_trip_consumption_saf + " liter");
    setInnerHtml("last_trip_earning_value", response.body.last_trip_info.last_trip_earning + " euro");
    setInnerHtml("last_trip_remarks_value", response.body.last_trip_info.last_trip_remarks);

}

async function saveProfile() {
    let profileSelector = document.getElementById("profileSelector")

    let data = {
        "profileId": profileSelector.value
    }

    let response = await postData("/api/profiles/current", data);


    if (response.status === 200) {
        hideById("profileSelectError");
        showById("profileSelectSuccess");
    } else {
        showById("profileSelectError");
        hideById("profileSelectSuccess");
    }
}


async function logoutButtonClick() {
    let data = await deleteData("/api/logout");
    location.reload();
}


async function buttonClick() {
    let element = document.getElementById("jsonValue");
    let jsonData = await postData("/api/test", "someToken");
    element.innerHTML = JSON.stringify(jsonData);
}

async function createNewProfile() {
    let profileName = document.getElementById("profile_name");

    let data = {
        "profile_name": profileName.value
    }

    let response = await postData("/api/profiles", data);

    if (response.status === 200) {
        hideById("profileSaveError");
        showById("profileSaveSuccess");
        await loadProfileElements()
    } else {
        showById("profileSaveError");
        hideById("profileSaveSuccess");
    }
}


async function load_statistics() {
    let table = document.createElement("table");

    table.classList.add("home-table")

    let thead = document.createElement("thead");

    let headerRow = document.createElement("tr");

    let headerCell0 = document.createElement("th");
    headerCell0.textContent = 'SL';
    headerRow.append(headerCell0);

    let headerCell1 = document.createElement("th");
    headerCell1.textContent = 'Profile Name';
    headerRow.append(headerCell1);

    let headerCell2 = document.createElement("th");
    headerCell2.textContent = 'CO2 Emission Per Kilometer (Kg)';
    headerRow.append(headerCell2);

    let headerCellEuro = document.createElement("th");
    headerCellEuro.textContent = 'Euro Balance';
    headerRow.append(headerCellEuro);

    let headerCell3 = document.createElement("th");
    headerCell3.textContent = 'SAF Fuel used (liter)';
    headerRow.append(headerCell3);

    let headerCell4 = document.createElement("th");
    headerCell4.textContent = 'Normal Fuel used (liter)';
    headerRow.append(headerCell4);


    let headerCell5 = document.createElement("th");
    headerCell5.textContent = 'Total Distance Covered (Km)';
    headerRow.append(headerCell5);

    thead.append(headerRow);
    table.append(thead);

    let response = await getData("/api/statistics");

    let statisticsTable = document.getElementById("statistics_table");

    let data = response.body;

    let count = 1;
    for (let index in data) {
        let dataRow = data[index];

        let row = document.createElement("tr");

        table.append(row)

        let labelCellSL = row.insertCell(0);
        let labelSL = document.createElement("label");
        labelSL.textContent = count;
        labelCellSL.appendChild(labelSL);

        count++;


        let labelCell0 = row.insertCell(1);
        let label0 = document.createElement("label");
        label0.textContent = dataRow.profile_name;
        labelCell0.appendChild(label0);

        let labelCell1 = row.insertCell(2);
        let label1 = document.createElement("label");
        label1.textContent = dataRow.CO2_emission_kilometer;
        labelCell1.appendChild(label1);

        let labelCellEuro = row.insertCell(3);
        let labelEuro = document.createElement("label");
        labelEuro.textContent = dataRow.total_euro_balance;
        labelCellEuro.appendChild(labelEuro);


        let labelCell2 = row.insertCell(4);
        let label2 = document.createElement("label");
        label2.textContent = dataRow.saf_fuel_used;
        labelCell2.appendChild(label2);

        let labelCell3 = row.insertCell(5);
        let label3 = document.createElement("label");
        label3.textContent = dataRow.normal_fuel_used;
        labelCell3.appendChild(label3);

        let labelCell4 = row.insertCell(6);
        let label4 = document.createElement("label");
        label4.textContent = dataRow.total_distance;
        labelCell4.appendChild(label4);
    }

    while (statisticsTable.firstChild) {
        statisticsTable.removeChild(statisticsTable.firstChild);
    }

    statisticsTable.append(table);

}

async function loadMakeATripElements() {
    airportId = ""
    let response = await getData("/api/get-random-airports");

    setInnerHtml("airport_info_to1_value", response.body.current_status.airport_info_to);
    setInnerHtml("euro_balance1_value", response.body.current_status.euro_balance);
    setInnerHtml("fuel_balance_normal1_value", response.body.current_status.fuel_balance_normal);
    setInnerHtml("fuel_balance_saf1_value", response.body.current_status.fuel_balance_saf);

    let destinationList = document.getElementById("destination_list");

    let destinationData = response.body.destination_list;

    while (destinationList.firstChild) {
        destinationList.removeChild(destinationList.firstChild);
    }

    let table = document.createElement("table");

    table.classList.add("home-table")

    let thead = document.createElement("thead");

    let headerRow = document.createElement("tr");

    let headerCell1 = document.createElement("th");
    headerCell1.textContent = ' ';
    headerRow.append(headerCell1);

    let headerCell2 = document.createElement("th");
    headerCell2.textContent = 'Airport Name';
    headerRow.append(headerCell2);

    let headerCell3 = document.createElement("th");
    headerCell3.textContent = 'Distance';
    headerRow.append(headerCell3);

    thead.append(headerRow);
    table.append(thead);

    for (let airportCode in destinationData) {

        let airport = destinationData[airportCode];

        let row = document.createElement("tr");

        let radioCell = row.insertCell(0);
        let radioInput = document.createElement("input");
        radioInput.type = "radio";
        radioInput.id = airportCode;
        radioInput.name = "airport_name";
        radioInput.value = airportCode;

        radioInput.addEventListener('change', function () {
            if (this.checked) {
                airportId = this.value;
            }
        });

        radioCell.appendChild(radioInput);
        table.append(row)

        let labelCell = row.insertCell(1);
        let label = document.createElement("label");
        label.htmlFor = airportCode;
        label.textContent = airport.name;
        labelCell.appendChild(label);

        let distanceCell = row.insertCell(2);
        let label1 = document.createElement("label");
        label1.htmlFor = airportCode;
        label1.textContent = airport.distance + " km";
        distanceCell.appendChild(label1);

    }

    destinationList.append(table);

}

//api.openweathermap.org/data/2.5/weather?lat=33.44&lon=-94.04&exclude=hourly,daily&appid=0c7e2ab7198d8fda3292aa99ec6a1209
function selectorResetErrorMessage() {
    hideById("profileSelectError");
    hideById("profileSelectSuccess");
}

async function startFly() {


    let useSAF = document.getElementById("use_saf_fuel");

    let payload = {
        "airport_IATA": airportId,
        "use_saf": useSAF.checked
    }

    let response = await postData("/api/make-a-trip", payload);


    let outputResult = document.getElementById("output_result");

    let data = response.body.output;

    while (outputResult.firstChild) {
        outputResult.removeChild(outputResult.firstChild);
    }

    for (key in data) {
        let para = document.createElement('p');
        para.append(data[key]);
        outputResult.append(para);
    }
    await loadMakeATripElements()
}

async function buyNormalFuel() {
    await buyFuel("normal_fuel", false);
}

async function buySAFFuel() {
    await buyFuel("saf_fuel", true);
}

async function buyFuel(amount_id, isSAF) {
    let amount = document.getElementById(amount_id);

    let payload = {
        "amount": parseInt(amount.value, 10),
        "use_saf": isSAF
    }

    let response = await postData("/api/purchase", payload);

    let outputResult = document.getElementById("buy_fuel_message");

    console.log(JSON.stringify(response.body))

    if ('output' in response.body) {
        let data = response.body.output;

        while (outputResult.firstChild) {
            outputResult.removeChild(outputResult.firstChild);
        }
        if (outputResult.classList.contains("red-text")) {
            outputResult.classList.remove("red-text")
        }

        showElement(outputResult)
        outputResult.classList.add("green-text")

        for (key in data) {
            let para = document.createElement('p');
            para.append(data[key]);
            outputResult.append(para);
        }

        amount.value = "";
        await loadPurchase();
    } else {
        let data = response.body.error;

        while (outputResult.firstChild) {
            outputResult.removeChild(outputResult.firstChild);
        }
        if (outputResult.classList.contains("green-text")) {
            outputResult.classList.remove("green-text")
        }

        showElement(outputResult)
        outputResult.classList.add("red-text")

        for (key in data) {
            let para = document.createElement('p');
            para.append(data[key]);
            outputResult.append(para);
        }
    }


}