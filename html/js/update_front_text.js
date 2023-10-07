// JavaScript file (script.js)
fetch('../welcome_text.txt')
.then(response => response.text())
.then(data => {
  // Split the text file content into lines
  const lines = data.split('\n');
  // Randomly select a line
  const randomIndex = Math.floor(Math.random() * (lines.length - 1));
  const selectedLine = lines[randomIndex].trim(); // trim any leading/trailing spaces
  // Display the selected line in the element with the id 'myText'
  document.getElementById('random-text').innerHTML = selectedLine;
})
.catch(error => {
  console.error('Error fetching new content:', error);
});