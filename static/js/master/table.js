  // JavaScript to toggle the expand/collapse icons
  
  document.querySelectorAll('.toggle-btn').forEach(button => {
    button.addEventListener('click', function() {
      const icon = this.innerHTML;
      if (icon === '+') {
        this.innerHTML = '-';
      } else {
        this.innerHTML = '+';
      }
    });
  });
