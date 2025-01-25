import CryptoJS from 'crypto-js';

export default {
  /**
   * Checks if any values in the given object are empty.
   * Empty values include: `null`, `undefined`, an empty string `''`, an empty array `[]`, or an empty object `{}`.
   *
   * @param {Object} obj - The object to check.
   * @returns {boolean} - Returns `true` if any value is empty, otherwise `false`.
   */
  checkEmptyValues(obj) {
    for (let key in obj) {
      // Check if the value is null, undefined, an empty string, an empty array, or an empty object
      if (
        obj[key] === null ||
        obj[key] === undefined ||
        obj[key] === '' ||
        (Array.isArray(obj[key]) && obj[key].length === 0)
      ) {
        return true; // An empty value is found
      }
    }
    return false; // No empty values found
  },

  /**
   * Generates an HMAC signature for a given payload using a secret key.
   *
   * @param {Object} payload - The data to be signed.
   * @returns {Object} - An object containing the original payload and its HMAC signature.
   */
  generateHmacSignature(payload) {
    const secretKey = '3f9d67c4e12a4879a1b5cf0e8d3a2f9d'; // Secret key for HMAC generation
    const payloadString = JSON.stringify(payload); // Convert the payload to a JSON string
    const signature = CryptoJS.HmacSHA256(payloadString, secretKey).toString(CryptoJS.enc.Base64); // Generate the HMAC signature
    return {
      payload: payload, // Original payload
      signature: signature, // Generated signature
    };
  },

  /**
   * Finds a character in a string and returns the substring after the character.
   *
   * @param {string} str - The input string to search.
   * @param {string} char - The character to find in the string.
   * @returns {string} - The substring after the character, or an empty string if the character is not found or is the last character.
   */
  findAndReturnSubsequent(str, char) {
    const index = str.indexOf(char); // Find the index of the character
    return index !== -1 && index < str.length - 1
      ? str.substring(index + 1) // Return substring after the character
      : ''; // Return an empty string if not found or at the end
  },

  /**
   * Checks the balance of a specific account after deducting a user-entered amount.
   *
   * @param {string} account_no - The account number with a prefix (e.g., "account:12345").
   * @param {number} userEnteredamount - The amount to be deducted from the account balance.
   * @param {Array} allUseraccounts - An array of all user accounts, each containing `account_no` and `account_balance`.
   * @returns {number|undefined} - Returns the new balance if the account is found, otherwise `undefined`.
   */
  checkBalance(account_no, userEnteredamount, allUseraccounts) {
    if (account_no && userEnteredamount) {
      for (const account of allUseraccounts) {
        // Extract the account number suffix using findAndReturnSubsequent
        if (this.findAndReturnSubsequent(account_no, ':') === account.account_no) {
          const newbalance = account.account_balance - userEnteredamount; // Calculate the new balance
          return newbalance;
        }
      }
    }
  },
  isTokenExpired() {
    const expiresAt = localStorage.getItem("expiresAt");
    return !expiresAt || Date.now() > parseInt(expiresAt, 10);
  }
};
