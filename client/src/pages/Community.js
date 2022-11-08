import axios from "axios"
import {useState} from "react"
import { Gallery } from "react-grid-gallery";


export default function Community() {

    // Set the image data before any rendering happens.
    const [images, setImages] = useState(() => {
        return fetchImages();
    })

    async function fetchImages(){
        let imageData = []
        const images = await axios.get('/images');
        const rawImageUrls = images.data['imagePath'];
        // imageArray contains path names /image/username.png relative to https://storage.googleapis.com/cs1520moodify.appspot.com

        for (let i = 0; i < rawImageUrls.length; i++) {
            const fullUrl = 'https://storage.googleapis.com/cs1520moodify.appspot.com' + rawImageUrls[i];
            imageData.push({src: fullUrl});
        }
        
        setImages(imageData);
    };

    return (
        <div className="about">
            <article>
                <h3>
                    Check out what others are feeling!
                </h3>
                <br />
            </article>

            <Gallery images={images} />
        </div>
        // basically, we should just create a template to hold n images that we want to retrieve from the databse, 
        // then in the function call we can update up src's accordingly
        // For some reason, I'm not able to set the image src's automatically on page loading, but this method seems 
        // to work perfectly fine
    )
}

