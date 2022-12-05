export default function About() {
  return (
    <div className="about">
      <article>
        <h3>
          Moodify uses your Spotify listening history to generate AI-powered art through
          OpenAI's DALL-E.
        </h3>
        Stable Diffusion is a latent text-to-image diffusion model capable of generating photo-realistic images given any text input, cultivates autonomous freedom to produce incredible imagery, empowers billions of people to create stunning art within seconds
      </article>
      <button
        className="code-button"
        href="https://github.com/leonatajeff/moodify"
      >
        <text className="code-text"> Check out our code! </text>
      </button>
    </div>
  );
}
