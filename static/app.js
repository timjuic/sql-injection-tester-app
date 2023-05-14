const form = document.querySelector('form');
const inputElement = document.querySelector("#username")
const table = document.querySelector(".results")
const submitButton = document.querySelector('.submit')
const automaticTest = document.querySelector('.automatic-test')
const vulnerabilityCounter = document.querySelector('.vulnerabilities')
const payloadsHTML = document.querySelector('.payloads')
const queryPathElement = document.querySelector("#query-path")
let recordedVulnerabilities = 0
let payloadsCounter = 0;


import payloads from "./injection-payloads.js";
console.log(payloads);

let isExpectedResult = (data) => {
   return data.length === 0 || data.length === 1;
}
let injectionDetected = (data) => {
   return data == "sql injection detected"
}

console.log(injectionDetected("sql injection detected"));

form.addEventListener('submit', (event) => {
   event.preventDefault(); // prevent the form from submitting normally
   let username = inputElement.value;
   
   let selectedIndex = queryPathElement.selectedIndex;
   let selectedOption = queryPathElement.options[selectedIndex];
   let queryPath = selectedOption.value;
   console.log(`Sending GET request at /${queryPath}?username=${username}`);

   payloadsCounter++;
   payloadsHTML.innerHTML = `Payloads Attempted: ${payloadsCounter}`
   let url = `/${queryPath}?username=${username}`;
   fetch(url)
     .then(response => response.json())
     .then(data => {
      removeOldResults()
         console.log(data);
         console.log();
         if (!isExpectedResult(data) && !injectionDetected(data)) {
            console.log("found vulnerability");
            recordedVulnerabilities++;
            vulnerabilityCounter.innerHTML = `Recorded Vulnerabilities: ${recordedVulnerabilities}`
            console.log(recordedVulnerabilities);
            
            if ((data instanceof String)) return
         } else if (injectionDetected(data)) return

         data.forEach((user, i) => {
            let rowElement = document.createElement('tr');
            let usernameCell = document.createElement('td')
            let firstNameCell = document.createElement('td')
            let lastNameCell = document.createElement('td')
            let emailCell = document.createElement('td')
            let ageCell = document.createElement('td')
            
            usernameCell.innerHTML = user.username;
            firstNameCell.innerHTML = user.firstname;
            lastNameCell.innerHTML = user.lastname;
            emailCell.innerHTML = user.email;
            ageCell.innerHTML = user.age;

            rowElement.appendChild(usernameCell)
            rowElement.appendChild(firstNameCell)
            rowElement.appendChild(lastNameCell)
            rowElement.appendChild(emailCell)
            rowElement.appendChild(ageCell)

            if (i % 2 === 0) {
               rowElement.classList.add('alternate-row');
            }
            table.appendChild(rowElement)
         })
     }).catch(err => {
      console.log(err);
      recordedVulnerabilities++
      vulnerabilityCounter.innerHTML = `Recorded Vulnerabilities: ${recordedVulnerabilities}`
   })


 });


 function removeOldResults() {
   const rowsToRemove = document.querySelectorAll('.results tr:not(.header-row)');
   rowsToRemove.forEach(row => row.remove());
 }


 function insertRows(str) {
   const rows = str.split('\n');
   let index = 0;

   const intervalId = setInterval(() => {
     if (index >= rows.length) {
       clearInterval(intervalId);
       return;
     }
     inputElement.value = rows[index++];
     submitButton.click()
   }, 100);
 }

// console.log(Object.values(payloads));
 

automaticTest.addEventListener("click", function(e) {
   e.preventDefault();
   Object.values(payloads).forEach(payload => {
      insertRows(payload)
   })
})





// insertRows(sqlInjectionPayload)