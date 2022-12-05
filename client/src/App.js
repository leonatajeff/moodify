import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import About from "./pages/About";
import Community from "./pages/Community";
import Navbar from "./components/Navbar";
import Result from "./pages/Result";
import Donate from "./pages/Donate";

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route exact path="/" element={<Home />} />
        <Route path="/About" element={<About />} />
        <Route path="/Community" element={<Community />} />
        <Route path="/Result" element={<Result />} />
        <Route path="/Donate" element={<Donate />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
