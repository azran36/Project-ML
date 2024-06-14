// Node.js script: app.js
const axios = require('axios');

const keyword = 'Lapangan Basket';  // Example keyword
const apiUrl = 'http://localhost:5000/recommend-fields?keyword=' + encodeURIComponent(keyword);

axios.get(apiUrl)
  .then(response => {
    console.log(`Rekomendasi untuk ${keyword}:`);
    console.log(response.data);
  })
  .catch(error => {
    console.error('Error fetching recommendations:', error);
  });
