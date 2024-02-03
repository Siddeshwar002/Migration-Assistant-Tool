import React from "react";
import MigrationForm from "./MigrationForm";
import atlassian from "./images/atlassian.png";
import github from "./images/git.png";
import bitbucket from "./images/bb.png";
import bg from "./images/atb.jpeg";
import arrow from "./images/arrow.png";
const App = () => {
  const containerStyle = {
    backgroundImage: `url(${bg})`,
    backgroundSize: "1600px 750px",
    backgroundRepeat: "no-repeat",
    height: "100vh",
  };
  return (
    <div style={containerStyle}>
      <img
        src={atlassian}
        alt="Atlassian"
        style={{
          width: "300px", // Set the desired width of the image
          height: "auto", // Maintain aspect ratio by setting height to 'auto'
          boxShadow: "0 2px 4px rgba(0, 0, 0, 0.2)", // Add a box shadow
        }}
      />

      <img
        src={github}
        alt="Github"
        style={{
          width: "200px", // Set the desired width of the image
          height: "auto", // Maintain aspect ratio by setting height to 'auto'
          position: "fixed",
          bottom: 30,
          left: "35%",
          transform: "translateX(-50%)",
        }}
      />

      <img
        src={arrow}
        alt="Arrow"
        style={{
          width: "220px", // Set the desired width of the image
          height: "auto", // Maintain aspect ratio by setting height to 'auto'
          position: "fixed",
          bottom: 10,
          left: "46%",
          transform: "translateX(-50%)",
        }}
      />
      <img
        src={bitbucket}
        alt="Bitbucket"
        style={{
          width: "350px", // Set the desired width of the image
          height: "auto", // Maintain aspect ratio by setting height to 'auto'
          position: "fixed",
          bottom: 40,
          left: "65%",
          transform: "translateX(-50%)",
        }}
      />

      <MigrationForm />
    </div>
  );
};

export default App;
