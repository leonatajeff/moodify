import './App.css';
import {BrowserRouter, Route, Routes} from "react-router-dom";
import Generate from "./pages/Generate";
import About from "./pages/About";
import Community from "./pages/Community";
import Navbar from "./components/Navbar";


function App() {
  return (
    <BrowserRouter>
    <Navbar />
      <Routes>
          <Route exact path='/' element={<Generate />}/>
          <Route path='/About' element={<About />}/>
          <Route path='/Community' element={<Community />}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
