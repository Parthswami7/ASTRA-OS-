// hologram_ui/app.js

// 1. Initialize the 3D Scene
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

// Use alpha: true for a transparent background (floating hologram effect)
const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('hud-container').appendChild(renderer.domElement);

// 2. Build the ASTRA AI Core (Rotating Icosahedron)
const coreGeometry = new THREE.IcosahedronGeometry(1.2, 1);
const coreMaterial = new THREE.MeshBasicMaterial({ 
    color: 0x00d2ff, 
    wireframe: true,
    transparent: true,
    opacity: 0.8
});
const astraCore = new THREE.Mesh(coreGeometry, coreMaterial);
scene.add(astraCore);

// 3. Add an outer data ring
const ringGeometry = new THREE.TorusGeometry(2, 0.05, 16, 100);
const ringMaterial = new THREE.MeshBasicMaterial({ color: 0x00a8cc, wireframe: true });
const dataRing = new THREE.Mesh(ringGeometry, ringMaterial);
scene.add(dataRing);

camera.position.z = 6;

// --- PRO-TIP: Speed Multiplier for smooth animation ---
let currentSpeed = 1.0; 

// 4. The Animation Loop (Runs 60 times per second)
function animate() {
    requestAnimationFrame(animate);
    
    // Rotate the inner core smoothly using the speed multiplier
    astraCore.rotation.x += 0.005 * currentSpeed;
    astraCore.rotation.y += 0.01 * currentSpeed;
    
    // Rotate the outer ring in the opposite direction
    dataRing.rotation.y -= 0.008 * currentSpeed;
    dataRing.rotation.z += 0.002 * currentSpeed;
    
    renderer.render(scene, camera);
}

// Handle window resizing seamlessly
window.addEventListener('resize', () => {
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
});

// Boot the animation
animate();

// --- THE WEBSOCKET BRIDGE ---
// Connect to the Python AI backend
const socket = new WebSocket('ws://localhost:8765');

socket.onopen = function() {
    console.log("Connected to ASTRA Brain.");
    document.querySelector('.status-standby').innerText = "ACTIVE";
    document.querySelector('.status-standby').style.color = "#00ffcc";
};

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    const indicator = document.getElementById('voice-indicator');

    // React to Gestures in Real-Time
    if (data.gesture !== "IDLE") {
        indicator.innerText = "GESTURE: " + data.gesture;
        indicator.classList.add('listening');
        
        // Ramp up the speed multiplier for smooth, fast spinning
        currentSpeed = 15.0; 
        dataRing.scale.set(1.1, 1.1, 1.1); // Pulse the outer ring
    } else {
        indicator.classList.remove('listening');
        
        // Return to normal speed smoothly
        currentSpeed = 1.0; 
        dataRing.scale.set(1.0, 1.0, 1.0); // Return to normal size
    }
};

socket.onerror = function(error) {
    console.log("WebSocket Error: " + error);
};