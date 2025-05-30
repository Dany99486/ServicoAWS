import axios from 'axios';

function DataFetchPost(url, data) {
  url = 'http://127.0.0.1:8000/' + url;

  let token = localStorage.getItem("token");

  if (token != null) {
    return new Promise((resolve, reject) => {
      axios.post(url, data, {
        headers: {
          Authorization: token
        }
      })
      .then(response => { resolve({ success: "yes", data: response.data }) })
      .catch(error => { reject({ success: "no", error: error }) });
    });
  } else {
    return new Promise((resolve, reject) => {
      axios.post(url, data)
        .then(response => { resolve({ success: "yes", data: response.data }) })
        .catch(error => { reject({ success: "no", error: error }) });
    });
  }
}

export default DataFetchPost;