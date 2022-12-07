import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { QueryClient, QueryClientProvider } from 'react-query'
import Home from "./pages/Home";
import About from "./pages/About";
import Community from "./pages/Community";
import Navbar from "./components/Navbar";
import Result from "./pages/Result";
import Donate from "./pages/Donate";
const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        refetchOnWindowFocus: false,
        refetchOnmount: false,
        refetchOnReconnect: false,
        retry: false,
        staleTime: 6000,
      },
    },
  });

function App() {
  return (
    <QueryClientProvider client={queryClient} >
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
    </QueryClientProvider>
  );
}

export default App;
