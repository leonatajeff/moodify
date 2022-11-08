import axios from "axios";

export default function authorize() {
  axios({
    method: "GET",
    url: "/authorize",
  })
    .then((response) => {
      response.json();
    })
    .catch((error) => {
      if (error.response) {
        console.log(error.response);
        console.log(error.response.status);
        console.log(error.response.headers);
      }
    });
}
const jsonURL = authorize();

export const loginUrl = jsonURL["auth_endpoint"];
