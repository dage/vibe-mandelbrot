// Vibe Coding Test App - Main JavaScript
// This file has intentional issues for AI to fix

// Counter functionality
let counter = 0;
const counterElement = document.getElementById('counter');
const incrementBtn = document.getElementById('increment');
const decrementBtn = document.getElementById('decrement');
const resetBtn = document.getElementById('reset');

incrementBtn.addEventListener('click', () => {
  counter++; // Missing semicolon
  counterElement.textContent = counter;
});

decrementBtn.addEventListener('click', () => {
  counter--; // Missing semicolon
  counterElement.textContent = counter;
});

resetBtn.addEventListener('click', () => {
  counter = 0;
  counterElement.textContent = counter;
});

// Todo list functionality
const todoInput = document.getElementById('todoInput');
const addTodoBtn = document.getElementById('addTodo');
const todoList = document.getElementById('todoList');

addTodoBtn.addEventListener('click', () => {
  const todoText = todoInput.value.trim();
  if (todoText) {
    const li = document.createElement('li');
    li.textContent = todoText; // No delete functionality
    todoList.appendChild(li);
    todoInput.value = '';
  }
});

// Color changer functionality
const changeColorBtn = document.getElementById('changeColor');
const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57'];

changeColorBtn.addEventListener('click', () => {
  const randomColor = colors[Math.floor(Math.random() * colors.length)];
  document.body.style.backgroundColor = randomColor;
});

// Missing error handling and accessibility features
// No keyboard navigation
// No ARIA labels
// No loading states
// No error messages

console.log('App loaded with intentional issues for AI to fix!'); 