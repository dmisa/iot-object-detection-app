  // Function to generate a random color for labels not in the mapping
function getRandomColor() {
return `#${Math.floor(Math.random() * 16777215).toString(16)}`;
}

export { getRandomColor };