export default {
   checkEmptyValues(obj) {
    for (let key in obj) {

        // Check if the value is empty (null, undefined, '', [], {})
        if (obj[key] === null || obj[key] === undefined || obj[key] === '' || (Array.isArray(obj[key]) && obj[key].length === 0) || (typeof obj[key] === 'object' && Object.keys(obj[key]).length === 0)) {
          return true; // Value is empty
        
      }
    }
    return false; // No empty values found
  }
}
