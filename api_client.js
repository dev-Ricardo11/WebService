const fetch = require('node-fetch'); // Requires: npm install node-fetch
// Or run in browser console without require

async function validateCreditLimit() {
    const xmlData = `<?xml version="1.0" encoding="UTF-8"?>
<CreditLimitRQ>
  <CodeClientBackOffice>6252</CodeClientBackOffice>
  <CodeClientOBT>627</CodeClientOBT>
  <Name>Test User</Name>
  <locValidacion>LOC1</locValidacion>
  <value>1000</value>
  <Currency>COP</Currency>
  <product>AIR</product>
  <description>Test transaction</description>
  <paymentType>CASH</paymentType>
  <mailUser>test@example.com</mailUser>
</CreditLimitRQ>`;

    try {
        const response = await fetch('http://localhost:8000/validateCreditLimit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/xml',
            },
            body: xmlData
        });

        const text = await response.text();
        console.log('Response from Server:');
        console.log(text);
    } catch (error) {
        console.error('Error connecting to API:', error);
    }
}

validateCreditLimit();
