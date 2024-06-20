document.addEventListener('DOMContentLoaded', function() {
    let mouseX = 0; // Current mouse X position
    let mouseY = 0; // Current mouse Y position
    let targetX = 0; // Target X position for the gradient
    let targetY = 0; // Target Y position for the gradient
    const delayFactor = 0.05; // Adjust the delay factor to control the speed of the catch-up
  
    document.addEventListener('mousemove', (e) => {
      targetX = e.clientX; // Update the target position based on the mouse movement
      targetY = e.clientY;
    });
  
    function updateGradientPosition() {
      // Gradually adjust the current position towards the target position
      mouseX += (targetX - mouseX) * delayFactor;
      mouseY += (targetY - mouseY) * delayFactor;
  
      const radius = Math.min(window.innerWidth, window.innerHeight) ; // Adjust radius as needed
  
      // Apply the gradient style with the updated position
      document.body.style.background = `
        radial-gradient(circle at ${mouseX}px ${mouseY}px, #c11e38, #220b34 ${radius}px)
      `;
  
      requestAnimationFrame(updateGradientPosition); // Continue updating the position
    }
  
    updateGradientPosition(); // Start the animation
  });