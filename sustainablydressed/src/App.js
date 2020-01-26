import React,{useEffect, useState} from 'react';
import Clothes from './Clothes';
import './App.css';

const App = () => {

useEffect(() => {
  console.log('Effect has been run');
})

  return (
    <div className="App">
      <form className="search-form">
        <input className="search-bar" type="text" />
        <button className="search-button" type="submit">
          search
        </button>
      </form>

      <div class = "Body">
        <Clothes/>
      </div>
    </div>
  );
}

export default App;
