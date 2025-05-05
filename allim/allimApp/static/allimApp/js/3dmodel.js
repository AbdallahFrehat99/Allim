const modelViewer = document.querySelector("#book");
const customStopTime = 3; // Time in seconds to stop the animation
let isAnimationPaused = false;

// Mouse tracking — only active after animation pause
window.addEventListener("mousemove", e => {
  if (isAnimationPaused) {
    const x = (e.clientX / window.innerWidth - 0.5) * 2;
    const y = (e.clientY / window.innerHeight - 0.5) * -2;
    modelViewer.cameraTarget = `${x.toFixed(2)}m ${y.toFixed(2)}m 0m`;  // Template literals need backticks
  }
});

// When the model loads
modelViewer.addEventListener("load", () => {
  const model = modelViewer.model;
  if (!model || !model.materials) return;

  // Optional: Change color
  const targetColor = "#2a4d61";
  const rgba = hexToRgba(targetColor);
  model.materials.forEach(mat => {
    const pbr = mat.pbrMetallicRoughness;
    if (pbr) {
      pbr.baseColorTexture = null;
      pbr.setBaseColorFactor(rgba);
    }
  });

  // Start animation
  if (modelViewer.availableAnimations.length > 0) {
    modelViewer.animationName = modelViewer.availableAnimations[0];
    modelViewer.play();
  }

  // Check animation time using setInterval
  const interval = setInterval(() => {
    const time = modelViewer.currentTime;
    if (time >= customStopTime && !isAnimationPaused) {
      modelViewer.pause();
      isAnimationPaused = true;
      clearInterval(interval); // Stop checking
    }
  }, 100); // Check every 100ms
});

// Check animation time and pause if needed after the model is loaded
modelViewer.addEventListener("load", () => {
  if (modelViewer.currentTime >= customStopTime && !isAnimationPaused) {
    modelViewer.pause();
    isAnimationPaused = true;
    modelViewer.cameraOrbit = '45deg 70deg 1m'; // Slight zoom (from 1.5m to 1.2m)
  }
});

// Convert HEX to RGBA
function hexToRgba(hex) {
  hex = hex.replace("#", "");
  const bigint = parseInt(hex, 16);
  return [(bigint >> 16) / 255, ((bigint >> 8) & 255) / 255, (bigint & 255) / 255, 1];
}
