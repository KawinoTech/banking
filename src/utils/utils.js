import CryptoJS from 'crypto-js';
export default {
   checkEmptyValues(obj) {
    for (let key in obj) {
        // Chekck if the value is empty (null, undefined, '', [], {})
        if (obj[key] === null || obj[key] === undefined || obj[key] === '' || (Array.isArray(obj[key]) && obj[key].length === 0)) {
          return true; // Value is empty
        
      }
    }
    return false
  }, // No empty values found
  
 generateHmacSignature(payload) {
  const secretKey = '3f9d67c4e12a4879a1b5cf0e8d3a2f9d'
  const payloadString = JSON.stringify(payload);
  const signature = CryptoJS.HmacSHA256(payloadString, secretKey).toString(CryptoJS.enc.Base64);
  const requestBody = {
    payload: payload,
    signature: signature,
  }

  return requestBody;

},

findAndReturnSubsequent(str, char) {
  const index = str.indexOf(char);
  return index !== -1 && index < str.length - 1
    ? str.substring(index + 1)
    : "";
},

checkBalance(account_no, userEnteredamount, allUseraccounts) {
  if (account_no && userEnteredamount) {
    for (const account of allUseraccounts) {
      if (
        this.findAndReturnSubsequent(account_no, ':') ===
        account.account_no
      ) {
        const newbalance = account.account_balance - userEnteredamount;
        return newbalance
      }
    }
  }
}
}