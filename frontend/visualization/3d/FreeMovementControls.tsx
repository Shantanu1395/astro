// Free Movement Camera Controls
import React, { useRef, useEffect, useState } from 'react';
import { useThree, useFrame } from '@react-three/fiber';
import { OrbitControls as OrbitControlsImpl } from 'three-stdlib';
import * as THREE from 'three';

interface FreeMovementControlsProps {
  enableFreeMovement?: boolean;
  movementSpeed?: number;
  rotationSpeed?: number;
  zoomSpeed?: number;
  dampingFactor?: number;
  onModeChange?: (isFreeMode: boolean) => void;
}

const FreeMovementControls: React.FC<FreeMovementControlsProps> = ({
  enableFreeMovement = false,
  movementSpeed = 50,
  rotationSpeed = 1,
  zoomSpeed = 1.2,
  dampingFactor = 0.1,
  onModeChange
}) => {
  const { camera, gl, scene } = useThree();
  const controlsRef = useRef<OrbitControlsImpl>();
  const [isFreeMode, setIsFreeMode] = useState(enableFreeMovement);
  const [target, setTarget] = useState(new THREE.Vector3(0, 0, 0));
  
  // Movement state
  const keysPressed = useRef<Set<string>>(new Set());
  const velocity = useRef(new THREE.Vector3());
  const direction = useRef(new THREE.Vector3());

  // Initialize controls
  useEffect(() => {
    const controls = new OrbitControlsImpl(camera, gl.domElement);
    
    // Configure controls
    controls.enableDamping = true;
    controls.dampingFactor = dampingFactor;
    controls.enableZoom = true;
    controls.enablePan = true;
    controls.enableRotate = true;
    
    // Distance and speed settings
    controls.minDistance = 5;
    controls.maxDistance = 1500;
    controls.panSpeed = 2;
    controls.rotateSpeed = rotationSpeed;
    controls.zoomSpeed = zoomSpeed;
    
    // Allow full rotation
    controls.maxPolarAngle = Math.PI;
    controls.minPolarAngle = 0;
    controls.maxAzimuthAngle = Infinity;
    controls.minAzimuthAngle = -Infinity;
    
    // Screen space panning for intuitive movement
    controls.screenSpacePanning = true;
    
    // Set initial target
    controls.target.copy(target);
    
    controlsRef.current = controls;
    
    return () => {
      controls.dispose();
    };
  }, [camera, gl, dampingFactor, rotationSpeed, zoomSpeed, target]);

  // Keyboard event handlers
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      keysPressed.current.add(event.code);
      
      // Toggle free movement with 'F' key
      if (event.code === 'KeyF') {
        const newFreeMode = !isFreeMode;
        setIsFreeMode(newFreeMode);
        if (onModeChange) onModeChange(newFreeMode);
        event.preventDefault();
      }
      
      // Reset camera with 'R' key
      if (event.code === 'KeyR') {
        resetCamera();
        event.preventDefault();
      }
      
      // Focus on Earth with 'E' key
      if (event.code === 'KeyE') {
        focusOnTarget(new THREE.Vector3(0, 0, 0));
        event.preventDefault();
      }
    };

    const handleKeyUp = (event: KeyboardEvent) => {
      keysPressed.current.delete(event.code);
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, [isFreeMode]);

  // Focus on target with smooth transition
  const focusOnTarget = (newTarget: THREE.Vector3) => {
    if (!controlsRef.current) return;
    
    const controls = controlsRef.current;
    setTarget(newTarget);
    
    // Smooth transition to new target
    const startTarget = controls.target.clone();
    const duration = 1000;
    const startTime = Date.now();
    
    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const easeProgress = 1 - Math.pow(1 - progress, 3);
      
      controls.target.lerpVectors(startTarget, newTarget, easeProgress);
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };
    
    animate();
  };

  // Reset camera to default position
  const resetCamera = () => {
    camera.position.set(0, 50, 120);
    focusOnTarget(new THREE.Vector3(0, 0, 0));
    setIsFreeMode(false);
    if (onModeChange) onModeChange(false);
  };

  // Frame update for movement
  useFrame((state, delta) => {
    if (!controlsRef.current) return;
    
    const controls = controlsRef.current;
    
    // Handle free movement mode
    if (isFreeMode) {
      const moveSpeed = movementSpeed * delta;
      direction.current.set(0, 0, 0);
      
      // Get camera's local coordinate system
      const forward = new THREE.Vector3(0, 0, -1).applyQuaternion(camera.quaternion);
      const right = new THREE.Vector3(1, 0, 0).applyQuaternion(camera.quaternion);
      const up = new THREE.Vector3(0, 1, 0);
      
      // WASD movement
      if (keysPressed.current.has('KeyW')) {
        direction.current.add(forward);
      }
      if (keysPressed.current.has('KeyS')) {
        direction.current.sub(forward);
      }
      if (keysPressed.current.has('KeyA')) {
        direction.current.sub(right);
      }
      if (keysPressed.current.has('KeyD')) {
        direction.current.add(right);
      }
      
      // QE for up/down movement
      if (keysPressed.current.has('KeyQ')) {
        direction.current.add(up);
      }
      if (keysPressed.current.has('KeyE')) {
        direction.current.sub(up);
      }
      
      // Apply movement with smooth acceleration
      if (direction.current.length() > 0) {
        direction.current.normalize();
        velocity.current.lerp(direction.current.multiplyScalar(moveSpeed), 0.1);
      } else {
        velocity.current.multiplyScalar(0.9); // Deceleration
      }
      
      // Apply velocity to camera and target
      if (velocity.current.length() > 0.01) {
        camera.position.add(velocity.current);
        controls.target.add(velocity.current);
      }
    }
    
    // Update controls
    controls.update();
  });

  // Expose control functions
  useEffect(() => {
    if (typeof window !== 'undefined') {
      (window as any).cameraControls = {
        focusOnTarget,
        resetCamera,
        toggleFreeMode: () => {
          const newMode = !isFreeMode;
          setIsFreeMode(newMode);
          if (onModeChange) onModeChange(newMode);
        },
        isFreeMode,
        focusOnEarth: () => focusOnTarget(new THREE.Vector3(0, 0, 0)),
        focusOnSun: () => focusOnTarget(new THREE.Vector3(10, 0, 0)),
        focusOnJupiter: () => focusOnTarget(new THREE.Vector3(-44, 0, 0))
      };
    }
  }, [isFreeMode]);

  return null;
};

export default FreeMovementControls;
