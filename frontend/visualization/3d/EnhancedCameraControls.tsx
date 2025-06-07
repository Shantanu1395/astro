// Enhanced Camera Controls for Free Movement and Dynamic Targeting
import React, { useRef, useEffect, useState } from 'react';
import { useThree, useFrame } from '@react-three/fiber';
import { OrbitControls as OrbitControlsImpl } from 'three-stdlib';
import * as THREE from 'three';

interface EnhancedCameraControlsProps {
  enableFreeMovement?: boolean;
  enableKeyboardControls?: boolean;
  movementSpeed?: number;
  zoomSpeed?: number;
  rotationSpeed?: number;
  dampingFactor?: number;
  minDistance?: number;
  maxDistance?: number;
  target?: THREE.Vector3;
  onTargetChange?: (target: THREE.Vector3) => void;
}

const EnhancedCameraControls: React.FC<EnhancedCameraControlsProps> = ({
  enableFreeMovement = true,
  enableKeyboardControls = true,
  movementSpeed = 10,
  zoomSpeed = 1.2,
  rotationSpeed = 1,
  dampingFactor = 0.05,
  minDistance = 5,
  maxDistance = 1000,
  target,
  onTargetChange
}) => {
  const { camera, gl, scene } = useThree();
  const controlsRef = useRef<OrbitControlsImpl>();
  const [currentTarget, setCurrentTarget] = useState(new THREE.Vector3(0, 0, 0));
  const [isFreeMoveMode, setIsFreeMoveMode] = useState(false);
  
  // Keyboard state
  const keysPressed = useRef<Set<string>>(new Set());
  const mousePosition = useRef(new THREE.Vector2());
  const raycaster = useRef(new THREE.Raycaster());

  // Initialize controls
  useEffect(() => {
    const controls = new OrbitControlsImpl(camera, gl.domElement);
    
    // Enhanced control settings
    controls.enableDamping = true;
    controls.dampingFactor = dampingFactor;
    controls.enableZoom = true;
    controls.enablePan = true;
    controls.enableRotate = true;
    
    // Distance limits
    controls.minDistance = minDistance;
    controls.maxDistance = maxDistance;
    
    // Speed settings
    controls.panSpeed = 2;
    controls.rotateSpeed = rotationSpeed;
    controls.zoomSpeed = zoomSpeed;
    controls.keyPanSpeed = movementSpeed;
    
    // Mouse button mappings
    controls.mouseButtons = {
      LEFT: THREE.MOUSE.ROTATE,
      MIDDLE: THREE.MOUSE.DOLLY,
      RIGHT: THREE.MOUSE.PAN
    };
    
    // Touch settings
    controls.touches = {
      ONE: THREE.TOUCH.ROTATE,
      TWO: THREE.TOUCH.DOLLY_PAN
    };
    
    // Set initial target
    if (target) {
      controls.target.copy(target);
      setCurrentTarget(target.clone());
    }
    
    controlsRef.current = controls;
    
    return () => {
      controls.dispose();
    };
  }, [camera, gl, dampingFactor, minDistance, maxDistance, rotationSpeed, zoomSpeed, movementSpeed, target]);

  // Keyboard event handlers
  useEffect(() => {
    if (!enableKeyboardControls) return;

    const handleKeyDown = (event: KeyboardEvent) => {
      keysPressed.current.add(event.code);
      
      // Toggle free movement mode with 'F' key
      if (event.code === 'KeyF') {
        setIsFreeMoveMode(!isFreeMoveMode);
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

    const handleMouseMove = (event: MouseEvent) => {
      mousePosition.current.x = (event.clientX / window.innerWidth) * 2 - 1;
      mousePosition.current.y = -(event.clientY / window.innerHeight) * 2 + 1;
    };

    const handleDoubleClick = (event: MouseEvent) => {
      if (!enableFreeMovement) return;
      
      // Cast ray to find intersection point
      raycaster.current.setFromCamera(mousePosition.current, camera);
      const intersects = raycaster.current.intersectObjects(scene.children, true);
      
      if (intersects.length > 0) {
        const point = intersects[0].point;
        focusOnTarget(point);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);
    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('dblclick', handleDoubleClick);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('dblclick', handleDoubleClick);
    };
  }, [enableKeyboardControls, enableFreeMovement, isFreeMoveMode, camera, scene]);

  // Focus on target with smooth transition
  const focusOnTarget = (newTarget: THREE.Vector3) => {
    if (!controlsRef.current) return;
    
    const controls = controlsRef.current;
    const startTarget = controls.target.clone();
    const startPosition = camera.position.clone();
    
    // Calculate optimal camera position
    const direction = new THREE.Vector3().subVectors(camera.position, startTarget).normalize();
    const distance = Math.max(minDistance * 2, Math.min(maxDistance * 0.5, 50));
    const newPosition = new THREE.Vector3().addVectors(newTarget, direction.multiplyScalar(distance));
    
    // Animate transition
    const duration = 1000; // 1 second
    const startTime = Date.now();
    
    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const easeProgress = 1 - Math.pow(1 - progress, 3); // Ease out cubic
      
      // Interpolate target
      controls.target.lerpVectors(startTarget, newTarget, easeProgress);
      
      // Interpolate camera position
      camera.position.lerpVectors(startPosition, newPosition, easeProgress);
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        setCurrentTarget(newTarget.clone());
        if (onTargetChange) {
          onTargetChange(newTarget);
        }
      }
    };
    
    animate();
  };

  // Reset camera to default position
  const resetCamera = () => {
    focusOnTarget(new THREE.Vector3(0, 0, 0));
    camera.position.set(0, 50, 100);
  };

  // Frame update for keyboard movement
  useFrame((state, delta) => {
    if (!controlsRef.current) return;
    
    const controls = controlsRef.current;
    
    // Update controls
    controls.update();
    
    // Handle keyboard movement in free move mode
    if (enableKeyboardControls && isFreeMoveMode) {
      const moveSpeed = movementSpeed * delta;
      const direction = new THREE.Vector3();
      
      // Get camera's local coordinate system
      const forward = new THREE.Vector3(0, 0, -1).applyQuaternion(camera.quaternion);
      const right = new THREE.Vector3(1, 0, 0).applyQuaternion(camera.quaternion);
      const up = new THREE.Vector3(0, 1, 0);
      
      // WASD movement
      if (keysPressed.current.has('KeyW')) {
        direction.add(forward);
      }
      if (keysPressed.current.has('KeyS')) {
        direction.sub(forward);
      }
      if (keysPressed.current.has('KeyA')) {
        direction.sub(right);
      }
      if (keysPressed.current.has('KeyD')) {
        direction.add(right);
      }
      
      // QE for up/down movement
      if (keysPressed.current.has('KeyQ')) {
        direction.add(up);
      }
      if (keysPressed.current.has('KeyE')) {
        direction.sub(up);
      }
      
      // Apply movement
      if (direction.length() > 0) {
        direction.normalize().multiplyScalar(moveSpeed);
        camera.position.add(direction);
        controls.target.add(direction);
      }
    }
  });

  return null;
};

export default EnhancedCameraControls;
