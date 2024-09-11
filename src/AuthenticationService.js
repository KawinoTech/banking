export default {
    login(customer_no, password_hash) {
      console.log(JSON.stringify({ customer_no, password_hash }))
      // Make a request to the backend API to authenticate the user
      return fetch('http://3.90.70.109:80/post/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ customer_no, password_hash }),
      })
      .then(response => response.json())
      .then(data => {
        // Assuming the response contains an access token
        localStorage.setItem('accessToken', data.accessToken);
        return data.accessToken;
      });
    },
    logout() {
      localStorage.removeItem('accessToken');
    },
    isAuthenticated() {
      return !!localStorage.getItem('accessToken');
    }
  };