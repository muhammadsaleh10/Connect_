import React, { Component } from "react";
import { useEffect } from 'react';
import UserPage from "./UserPage";
import {
	BrowserRouter as Router,
	Routes,
	Route,
  } from "react-router-dom";
import BasicPage from "./BasicPage";

function HomePage (props){
  
	console.log("called homepage render");
	  return (
		<Router>
		  <Routes>
			<Route exact path="/" element={<BasicPage/>} />
			  
			<Route path="/user/:devicePlatform/:userName" element={<UserPage />} />
		  </Routes>
		</Router>
	  );
}


export default HomePage;






