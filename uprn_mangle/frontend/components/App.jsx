import { useState } from "react";
import "../css/app.css";
import Header from "./Header";
import Search from "./Search";

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <Header />
      <Search />
    </>
  );
}

export default App;
