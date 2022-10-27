import axios from "axios";


function getData() {
    axios({
        method: "GET",
        url: "/login",
    })
        .then((response) => {
            // use a loading page while image generation is happening
            // finish image generation.
            // go to results page with image.
        }).catch((error) => {
            if (error.response) {
                console.log(error.response)
                console.log(error.response.status)
                console.log(error.response.headers)
            }
        })
}

module.exports = getData;