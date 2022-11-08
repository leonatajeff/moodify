import axios from "axios";
import { useState } from "react";
import { Gallery } from "react-grid-gallery";

export default function Community() {
  // Set the image data before any rendering happens.
  const [images, setImages] = useState(() => {
    return fetchImages();
  });

  const [isLoading, setIsLoading] = useState(true);

  async function fetchImages() {
    let imageData = [];
    const images = await axios.get("/images");
    const rawImageUrls = images.data["imagePath"];
    // imageArray contains path names /image/username.png relative to https://storage.googleapis.com/cs1520moodify.appspot.com

    for (let i = 0; i < rawImageUrls.length; i++) {
      const fullUrl =
        "https://storage.googleapis.com/cs1520moodify.appspot.com" +
        rawImageUrls[i];
      imageData.push({ src: fullUrl });
    }

    setIsLoading(false);
    setImages(imageData);
  }

  return (
    <div className="community">
      <h2 className="community-header">Check out how others are feeling!</h2>
      <br />
      {isLoading ? (
        <div className="spinner-container">
          <div className="loading-spinner"></div>
        </div>
      ) : (
        <div className="gallery-grid">
          <Gallery images={images} enableImageSelection={false} />
        </div>
      )}
    </div>
    // basically, we should just create a template to hold n images that we want to retrieve from the databse,
    // then in the function call we can update up src's accordingly
    // For some reason, I'm not able to set the image src's automatically on page loading, but this method seems
    // to work perfectly fine
  );
}
