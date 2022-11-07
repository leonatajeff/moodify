import axios from "axios"

export default function Community() {
    async function fetchImages(){
        // const imageDiv = document.getElementById('Images');
        const imageUrls = await axios.get('/images');
        // const testArray = ['https://cdn.discordapp.com/attachments/1024113488483864669/1033931366573805568/unknown.png', 'https://cdn.discordapp.com/attachments/1024113488483864669/1033931000260083743/unknown.png']
        const imageArray = imageUrls.data['imageUrl'];
        
        const img1 = document.getElementById('test1');
        const img2 = document.getElementById('test2');

        const testImages = [img1, img2]

        // let imagesHtml = '' + testArray.length;

        for (let i = 0; i < imageArray.length; i++) {
            const imageUrl = imageArray[i];
            // imagesHtml += '<img alt = mood' + imageUrl + ' src = ' + imageUrl +  '/> \n';
            testImages[i].src = imageUrl;
            testImages[i].style.display = "block";
        }

        const button1 = document.getElementById('button');
        button1.style.display = "none"
        

        // imageDiv.innerHTML = imagesHtml; 
        // imageDiv.innerHTML = '<p> ' + imageArray[0] + ' ' + imageArray[1] + '</p>'
    };

    return (
        <div className="about">
            <article>
                <h3>
                    Check out what others are feeling!
                </h3>
                <br />
            </article>
            <p>To be implemented... Along with some other upcoming features</p>
            <ul>
                <li> Test </li>
                <li>Spotify Integration</li>
                <li>Stable Diffusion Library</li>
                <li>Javascript Optimization</li>
                <li>Flask API Interface</li>
            </ul>

            <button id = "button" onClick = {fetchImages}>
                <text> View Images </text>
            </button> 

            <div id="Images" onLoad = {fetchImages}></div>

            <img id = "test1" alt = "test1" hidden/>
            <img id = "test2" alt = "test2" hidden/>
        </div>
        // basically, we should just create a template to hold n images that we want to retrieve from the databse, 
        // then in the function call we can update up src's accordingly
        // For some reason, I'm not able to set the image src's automatically on page loading, but this method seems 
        // to work perfectly fine
    )
}

