import '../App.css'
import axios from "axios";

// 'URLSearchParams(window.location.search)' will get url string after the '?' & .get() will get the code value from the url
const code = new URLSearchParams(window.location.search).get('code')

export default function Home() {

    const handleLogin = async () => {
        const loginUrl = await axios.get('/authorize');
        window.location.href = loginUrl.data['auth_endpoint'];
    }

    return (
        <div className="generation">
            <h1 className="moodify-header"> Moodify</h1>
            <h2 className="moodify-subheader">
                What if you can see your favorite sounds?
            </h2>
            {code ? <img style={{ width: 400, height: 400 }} src="https://www.kurin.com/wp-content/uploads/placeholder-square.jpg" alt='placeholding' /> :
                
                <button className="spotify-button" onClick={handleLogin}>
                    <text className="login-text"> LOGIN WITH SPOTIFY </text>
                </button>}
        </div>
    );
}