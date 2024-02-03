import React, { useState } from "react";

function MigrationForm() {
  const [githubUsername, setGithubUsername] = useState("");
  const [githubPassword, setGithubPassword] = useState("");
  const [bitbucketUsername, setBitbucketUsername] = useState("");
  const [bitbucketPassword, setBitbucketPassword] = useState("");

  const handleGithubUsernameChange = (e) => {
    setGithubUsername(e.target.value);
  };

  const handleGithubPasswordChange = (e) => {
    setGithubPassword(e.target.value);
  };

  const handleBitbucketUsernameChange = (e) => {
    setBitbucketUsername(e.target.value);
  };

  const handleBitbucketPasswordChange = (e) => {
    setBitbucketPassword(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Call the migration script with the provided credentials and options
    // Replace the following code with your migration script or function
    console.log("GitHub Username:", githubUsername);
    console.log("GitHub Password:", githubPassword);
    console.log("Bitbucket Username:", bitbucketUsername);
    console.log("Bitbucket Password:", bitbucketPassword);
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Migration Form</h2>
      <form onSubmit={handleSubmit} style={styles.form}>
        <br />
        <label style={styles.label}>
          GitHub Username:&nbsp;&nbsp;
          <input
            type="text"
            value={githubUsername}
            onChange={handleGithubUsernameChange}
            required
            style={styles.input}
          />
        </label>
        <br />
        <label style={styles.label}>
          GitHub Password:&nbsp;&nbsp;
          <input
            type="password"
            value={githubPassword}
            onChange={handleGithubPasswordChange}
            required
            style={styles.input}
          />
        </label>
        <br />
        <label style={styles.label}>
          Bitbucket Username:&nbsp;&nbsp;
          <input
            type="text"
            value={bitbucketUsername}
            onChange={handleBitbucketUsernameChange}
            required
            style={styles.input}
          />
        </label>
        <br />
        <label style={styles.label}>
          Bitbucket Password:&nbsp;&nbsp;
          <input
            type="password"
            value={bitbucketPassword}
            onChange={handleBitbucketPasswordChange}
            required
            style={styles.input}
          />
        </label>
        <br />
        <button type="submit" style={styles.button}>
          Start Migration
        </button>
      </form>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "400px",
    margin: "0 auto",
    padding: "20px",
    background: "rgba(248, 248, 248, 0.7)",
    //background: "#f8f8f8",
    borderRadius: "4px",
    boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
  },
  title: {
    fontSize: "24px",
    marginBottom: "20px",
  },
  form: {
    display: "flex",
    flexDirection: "column",
  },
  label: {
    fontWeight: "bold",
    marginBottom: "10px",
  },
  input: {
    padding: "8px",
    border: "1px solid #ccc",
    borderRadius: "4px",
    marginBottom: "10px",
  },
  button: {
    padding: "10px 20px",
    background: "blue",
    color: "#fff",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
  },
};

export default MigrationForm;
