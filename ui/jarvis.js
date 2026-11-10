setInterval(() => {
    fetch('/get_speech_status')
        .then(response => response.json())
        .then(data => {
            const visualizer = document.getElementById('visualizer');
            if (data.is_speaking) {
                // ASTRA is talking! Turn on the glow.
                visualizer.classList.remove('idle');
                visualizer.classList.add('active');
            } else {
                // ASTRA is quiet. Return to standby.
                visualizer.classList.remove('active');
                visualizer.classList.add('idle');
            }
        })
        .catch(error => console.error("UI Neural Link Error:", error));
}, 250); 

function updateClock() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', { hour12: false });
    const dateString = now.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }).toUpperCase();
    document.getElementById('clock-time').innerText = timeString;
    document.getElementById('clock-date').innerText = dateString;
}
setInterval(updateClock, 1000);
updateClock();

// --- 2. SYSTEM HARDWARE SCANNERS ---
function updateDiagnostics() {
    fetch('/status')
        .then(response => response.json())
        .then(data => {
            if (data.status === "ONLINE") {
                const cpu = data.cpu;
                const ram = data.ram;
                document.getElementById('cpu-text').innerText = cpu;
                document.getElementById('ram-text').innerText = ram;
                document.getElementById('cpu-gauge').style.setProperty('--progress', cpu + '%');
                document.getElementById('ram-gauge').style.setProperty('--progress', ram + '%');
                
                const cpuColor = cpu > 85 ? '#ff5500' : '#00f3ff';
                const ramColor = ram > 85 ? '#ff5500' : '#00f3ff';
                document.getElementById('cpu-gauge').style.background = `conic-gradient(${cpuColor} ${cpu}%, rgba(0, 243, 255, 0.1) 0deg)`;
                document.getElementById('ram-gauge').style.background = `conic-gradient(${ramColor} ${ram}%, rgba(0, 243, 255, 0.1) 0deg)`;
            }
        }).catch(err => console.log("[DIAGNOSTICS] Open http://127.0.0.1:5000 in your browser, not the local file!"));
}
setInterval(updateDiagnostics, 2000);
updateDiagnostics();

// --- 3. ENVIRONMENTAL WEATHER UPLINK ---
function updateWeather() {
    fetch('/weather')
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                document.getElementById('temp-text').innerText = data.temp;
            }
        }).catch(err => console.log("[WEATHER] Uplink offline."));
}
setInterval(updateWeather, 600000);
updateWeather();


// --- 4. ADVANCED 3D GRAPHICS ENGINE ---
let scene, camera, renderer;
let outerRing, innerRing, globe, particleSystem, tacticalGrid;
let audioContext, analyser, dataArray;
let isAudioInitialized = false;

function initHologram() {
    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x000000, 0.015);

    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    
    renderer.domElement.style.position = 'absolute';
    renderer.domElement.style.top = '0';
    renderer.domElement.style.left = '0';
    renderer.domElement.style.zIndex = '-1';
    document.body.appendChild(renderer.domElement);

    // [ELEMENT 1] Giant Tactical World Grid (From ASTRA.jpg background)
    const gridHelper = new THREE.GridHelper(60, 30, 0x00f3ff, 0x004455);
    gridHelper.position.y = -10;
    gridHelper.rotation.x = Math.PI / 6; // Angled matrix shift
    scene.add(gridHelper);

    // [ELEMENT 2] The Global Radar Sphere
    const globeGeo = new THREE.SphereGeometry(22, 24, 24);
    const globeMat = new THREE.MeshBasicMaterial({ color: 0x00a8cc, wireframe: true, transparent: true, opacity: 0.04 });
    globe = new THREE.Mesh(globeGeo, globeMat);
    scene.add(globe);

    // [ELEMENT 3] Main Core Arc Reactor Rings
    const geometry1 = new THREE.TorusGeometry(7, 0.08, 16, 80);
    const material1 = new THREE.MeshBasicMaterial({ color: 0x00f3ff, wireframe: true, transparent: true, opacity: 0.7 });
    outerRing = new THREE.Mesh(geometry1, material1);
    outerRing.position.set(0, -2, 0);
    scene.add(outerRing);

// Changed segments back to 16, 100 for a perfectly round Arc Reactor Core
    const geometry2 = new THREE.TorusGeometry(5, 0.3, 16, 100); 
    const material2 = new THREE.MeshBasicMaterial({ color: 0x00f3ff, wireframe: true, transparent: true, opacity: 0.25 });
    innerRing = new THREE.Mesh(geometry2, material2);
    innerRing.position.set(0, -2, 0);
    scene.add(innerRing);

    // [ELEMENT 4] Tactical Target Crosshairs (Framing the Left/Right Panels)
    const crosshairGeo = new THREE.RingGeometry(11, 11.2, 4, 1, 0, Math.PI / 2);
    const crosshairMat = new THREE.MeshBasicMaterial({ color: 0x00f3ff, side: THREE.DoubleSide, transparent: true, opacity: 0.4 });
    
    const leftCrosshair = new THREE.Mesh(crosshairGeo, crosshairMat);
    leftCrosshair.position.set(-15, 2, -5);
    scene.add(leftCrosshair);

    const rightCrosshair = leftCrosshair.clone();
    rightCrosshair.position.set(15, 2, -5);
    rightCrosshair.rotation.z = Math.PI;
    scene.add(rightCrosshair);

    // [ELEMENT 5] Floating Data Particles
    const particlesGeo = new THREE.BufferGeometry();
    const particlesCount = 1000;
    const posArray = new Float32Array(particlesCount * 3);
    for(let i = 0; i < particlesCount * 3; i++) {
        posArray[i] = (Math.random() - 0.5) * 80;
    }
    particlesGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    const particlesMat = new THREE.PointsMaterial({ size: 0.08, color: 0x00f3ff, transparent: true, opacity: 0.4 });
    particleSystem = new THREE.Points(particlesGeo, particlesMat);
    scene.add(particleSystem);

    camera.position.z = 22;
    document.addEventListener('mousemove', onDocumentMouseMove);
    animate();
}

let mouseX = 0, mouseY = 0;
function onDocumentMouseMove(event) {
    mouseX = (event.clientX - window.innerWidth / 2);
    mouseY = (event.clientY - window.innerHeight / 2);
}

function animate() {
    requestAnimationFrame(animate);

    // Interactive Parallax Camera Control
    camera.position.x += (mouseX * 0.003 - camera.position.x) * 0.05;
    camera.position.y += (-mouseY * 0.003 - camera.position.y) * 0.05;
    camera.lookAt(scene.position);

    // Rotational Matrices
    globe.rotation.y += 0.0008;
    particleSystem.rotation.y -= 0.0003;
    outerRing.rotation.z += 0.005;
    innerRing.rotation.z -= 0.008;

    // Real-Time Audio Reactivity Engine
    if (isAudioInitialized && analyser && dataArray) {
        analyser.getByteFrequencyData(dataArray);
        let sum = 0;
        for(let i = 0; i < dataArray.length; i++) { sum += dataArray[i]; }
        let average = sum / dataArray.length;
        
        let dynamicScale = 1 + (average / 256) * 0.4; 
        outerRing.scale.set(dynamicScale, dynamicScale, dynamicScale);
        innerRing.scale.set(dynamicScale * 1.05, dynamicScale * 1.05, dynamicScale * 1.05);
    }

    renderer.render(scene, camera);
}

function initializeSystem() {
    const btn = document.getElementById('init-btn');
    const status = document.getElementById('status-text');
    const audioElement = document.getElementById('astra-voice');

    btn.style.display = 'none';
    status.innerText = "[ SYSTEMS SECURE - MARK III HUD ACTIVE ]";

    if (!isAudioInitialized) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioContext.createAnalyser();
        const source = audioContext.createMediaElementSource(audioElement);
        source.connect(analyser);
        analyser.connect(audioContext.destination);
        analyser.fftSize = 256;
        dataArray = new Uint8Array(analyser.frequencyBinCount);
        isAudioInitialized = true;
    }
    playASTRASpeech("boot.mp3"); 
}

function playASTRASpeech(audioFileUrl) {
    const audioElement = document.getElementById('astra-voice');
    audioElement.src = audioFileUrl;
    audioElement.play();
}

window.addEventListener('resize', () => {
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
});

window.onload = initHologram;