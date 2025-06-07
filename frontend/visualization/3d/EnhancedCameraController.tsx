// Enhanced Camera Controller with WASD and Focal Point
import React, { useRef, useEffect, useState } from 'react';
import { useThree, useFrame } from '@react-three/fiber';
import { OrbitControls as OrbitControlsImpl } from 'three-stdlib';
import * as THREE from 'three';

interface EnhancedCameraControllerProps {
  showFocalPoint?: boolean;
  movementSpeed?: number;
  onFocalPointChange?: (position: THREE.Vector3) => void;
  onCameraPositionChange?: (position: THREE.Vector3) => void;
}

const EnhancedCameraController: React.FC<EnhancedCameraControllerProps> = ({
  showFocalPoint = true,
  movementSpeed = 30,
  onFocalPointChange,
  onCameraPositionChange
}) => {
  const { camera, gl, scene } = useThree();
  const controlsRef = useRef<OrbitControlsImpl>();
  const focalPointRef = useRef<THREE.Mesh>();
  const [target, setTarget] = useState(new THREE.Vector3(0, 0, 0));
  
  // Keyboard state
  const keysPressed = useRef<Set<string>>(new Set());
  const velocity = useRef(new THREE.Vector3());

  // Create focal point indicator
  useEffect(() => {
    if (!showFocalPoint) return;

    // Create focal point geometry
    const geometry = new THREE.SphereGeometry(0.5, 16, 16);
    const material = new THREE.MeshBasicMaterial({
      color: 0xffff00,
      transparent: true,
      opacity: 0.8,
      wireframe: true
    });
    
    const focalPoint = new THREE.Mesh(geometry, material);
    focalPoint.position.copy(target);
    scene.add(focalPoint);
    focalPointRef.current = focalPoint;

    return () => {
      if (focalPointRef.current) {
        scene.remove(focalPointRef.current);
        geometry.dispose();
        material.dispose();
      }
    };
  }, [scene, showFocalPoint, target]);

  // Mouse interaction state
  const mouseState = useRef({
    isLeftDown: false,
    isRightDown: false,
    lastX: 0,
    lastY: 0,
    sensitivity: 0.01
  });

  // Initialize OrbitControls - ZOOM ONLY + Custom Mouse Handlers
  useEffect(() => {
    const controls = new OrbitControlsImpl(camera, gl.domElement);

    // ZOOM ONLY - We'll handle rotation and panning manually
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.enableZoom = true;
    controls.enablePan = false;      // Disable - we'll handle manually
    controls.enableRotate = false;   // Disable - we'll handle manually
    controls.zoomSpeed = 2;
    controls.minDistance = 3;
    controls.maxDistance = 2000;

    // Set target
    controls.target.copy(target);

    controlsRef.current = controls;

    return () => {
      controls.dispose();
    };
  }, [camera, gl, target]);

  // Custom mouse handlers for camera position changes
  useEffect(() => {
    const canvas = gl.domElement;

    const handleMouseDown = (event: MouseEvent) => {
      if (event.button === 0) { // Left mouse button
        mouseState.current.isLeftDown = true;
      } else if (event.button === 2) { // Right mouse button
        mouseState.current.isRightDown = true;
      }
      mouseState.current.lastX = event.clientX;
      mouseState.current.lastY = event.clientY;
    };

    const handleMouseUp = (event: MouseEvent) => {
      if (event.button === 0) {
        mouseState.current.isLeftDown = false;
      } else if (event.button === 2) {
        mouseState.current.isRightDown = false;
      }
    };

    const handleMouseMove = (event: MouseEvent) => {
      if (!mouseState.current.isLeftDown && !mouseState.current.isRightDown) return;

      const deltaX = event.clientX - mouseState.current.lastX;
      const deltaY = event.clientY - mouseState.current.lastY;

      if (mouseState.current.isLeftDown) {
        // Left drag: Rotate camera around focal point
        rotateCameraAroundTarget(deltaX, deltaY);
      } else if (mouseState.current.isRightDown) {
        // Right drag: Pan camera and focal point together
        panCameraAndTarget(deltaX, deltaY);
      }

      mouseState.current.lastX = event.clientX;
      mouseState.current.lastY = event.clientY;
    };

    const handleContextMenu = (event: MouseEvent) => {
      event.preventDefault(); // Prevent right-click context menu
    };

    // Add event listeners
    canvas.addEventListener('mousedown', handleMouseDown);
    canvas.addEventListener('mouseup', handleMouseUp);
    canvas.addEventListener('mousemove', handleMouseMove);
    canvas.addEventListener('contextmenu', handleContextMenu);

    return () => {
      canvas.removeEventListener('mousedown', handleMouseDown);
      canvas.removeEventListener('mouseup', handleMouseUp);
      canvas.removeEventListener('mousemove', handleMouseMove);
      canvas.removeEventListener('contextmenu', handleContextMenu);
    };
  }, [gl.domElement]);

  // Rotate camera around target (left mouse drag)
  const rotateCameraAroundTarget = (deltaX: number, deltaY: number) => {
    if (!controlsRef.current) return;

    const controls = controlsRef.current;
    const sensitivity = mouseState.current.sensitivity;

    // Get current camera position relative to target
    const offset = new THREE.Vector3().subVectors(camera.position, controls.target);

    // Convert to spherical coordinates
    const spherical = new THREE.Spherical().setFromVector3(offset);

    // Apply rotation
    spherical.theta -= deltaX * sensitivity;
    spherical.phi += deltaY * sensitivity;

    // Clamp phi to prevent flipping
    spherical.phi = Math.max(0.1, Math.min(Math.PI - 0.1, spherical.phi));

    // Convert back to cartesian and update camera position
    offset.setFromSpherical(spherical);
    camera.position.copy(controls.target).add(offset);

    // Update camera position state
    if (onCameraPositionChange) {
      onCameraPositionChange(camera.position.clone());
    }
  };

  // Pan camera and target together (right mouse drag)
  const panCameraAndTarget = (deltaX: number, deltaY: number) => {
    if (!controlsRef.current) return;

    const controls = controlsRef.current;
    const sensitivity = mouseState.current.sensitivity * 5; // More sensitive for panning

    // Get camera's right and up vectors
    const right = new THREE.Vector3(1, 0, 0).applyQuaternion(camera.quaternion);
    const up = new THREE.Vector3(0, 1, 0).applyQuaternion(camera.quaternion);

    // Calculate movement
    const movement = new THREE.Vector3();
    movement.add(right.multiplyScalar(-deltaX * sensitivity));
    movement.add(up.multiplyScalar(deltaY * sensitivity));

    // Move both camera and target
    camera.position.add(movement);
    controls.target.add(movement);

    // Update focal point
    if (focalPointRef.current) {
      focalPointRef.current.position.copy(controls.target);
    }

    // Update states
    setTarget(controls.target.clone());
    if (onFocalPointChange) {
      onFocalPointChange(controls.target.clone());
    }
    if (onCameraPositionChange) {
      onCameraPositionChange(camera.position.clone());
    }
  };

  // Keyboard event handlers
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      // Prevent default for movement keys
      if (['KeyW', 'KeyA', 'KeyS', 'KeyD', 'KeyQ', 'KeyE'].includes(event.code)) {
        event.preventDefault();
      }

      keysPressed.current.add(event.code);
      
      // Reset camera with 'R' key
      if (event.code === 'KeyR') {
        resetCamera();
        event.preventDefault();
      }
      
      // Focus on Earth with 'Home' key
      if (event.code === 'Home') {
        focusOnTarget(new THREE.Vector3(0, 0, 0));
        event.preventDefault();
      }
    };

    const handleKeyUp = (event: KeyboardEvent) => {
      keysPressed.current.delete(event.code);
    };

    // Add event listeners
    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, []);

  // Focus on target with smooth transition
  const focusOnTarget = (newTarget: THREE.Vector3) => {
    if (!controlsRef.current) return;
    
    const controls = controlsRef.current;
    const startTarget = controls.target.clone();
    const startPosition = camera.position.clone();
    
    // Calculate optimal camera position
    const direction = new THREE.Vector3().subVectors(camera.position, startTarget).normalize();
    const distance = Math.max(20, Math.min(200, camera.position.distanceTo(startTarget)));
    const newPosition = new THREE.Vector3().addVectors(newTarget, direction.multiplyScalar(distance));
    
    // Animate transition
    const duration = 1000;
    const startTime = Date.now();
    
    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const easeProgress = 1 - Math.pow(1 - progress, 3);
      
      // Interpolate target and camera position
      controls.target.lerpVectors(startTarget, newTarget, easeProgress);
      camera.position.lerpVectors(startPosition, newPosition, easeProgress);
      
      // Update focal point
      if (focalPointRef.current) {
        focalPointRef.current.position.copy(controls.target);
      }
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        setTarget(newTarget);
        if (onFocalPointChange) {
          onFocalPointChange(newTarget);
        }
      }
    };
    
    animate();
  };

  // Reset camera to default position
  const resetCamera = () => {
    camera.position.set(0, 50, 120);
    focusOnTarget(new THREE.Vector3(0, 0, 0));
  };

  // Frame update for WASD movement
  useFrame((state, delta) => {
    if (!controlsRef.current) return;

    const controls = controlsRef.current;
    const moveSpeed = movementSpeed * delta;

    // Get camera's local coordinate system for precise movement
    const forward = new THREE.Vector3(0, 0, -1).applyQuaternion(camera.quaternion);
    const right = new THREE.Vector3(1, 0, 0).applyQuaternion(camera.quaternion);
    const up = new THREE.Vector3(0, 1, 0); // World up

    // Precise WASD movement - only one direction per key
    let keyboardMoved = false;

    // W - Forward only
    if (keysPressed.current.has('KeyW')) {
      const movement = forward.clone().multiplyScalar(moveSpeed);
      camera.position.add(movement);
      controls.target.add(movement);
      keyboardMoved = true;
    }

    // S - Backward only
    if (keysPressed.current.has('KeyS')) {
      const movement = forward.clone().multiplyScalar(-moveSpeed);
      camera.position.add(movement);
      controls.target.add(movement);
      keyboardMoved = true;
    }

    // A - Left only
    if (keysPressed.current.has('KeyA')) {
      const movement = right.clone().multiplyScalar(-moveSpeed);
      camera.position.add(movement);
      controls.target.add(movement);
      keyboardMoved = true;
    }

    // D - Right only
    if (keysPressed.current.has('KeyD')) {
      const movement = right.clone().multiplyScalar(moveSpeed);
      camera.position.add(movement);
      controls.target.add(movement);
      keyboardMoved = true;
    }

    // Q - Up only
    if (keysPressed.current.has('KeyQ')) {
      const movement = up.clone().multiplyScalar(moveSpeed);
      camera.position.add(movement);
      controls.target.add(movement);
      keyboardMoved = true;
    }

    // E - Down only
    if (keysPressed.current.has('KeyE')) {
      const movement = up.clone().multiplyScalar(-moveSpeed);
      camera.position.add(movement);
      controls.target.add(movement);
      keyboardMoved = true;
    }

    // Update focal point and states if keyboard moved
    if (keyboardMoved) {
      if (focalPointRef.current) {
        focalPointRef.current.position.copy(controls.target);
      }

      // Update states
      setTarget(controls.target.clone());
      if (onFocalPointChange) {
        onFocalPointChange(controls.target.clone());
      }

      if (onCameraPositionChange) {
        onCameraPositionChange(camera.position.clone());
      }
    }

    // Update controls (for zoom only)
    controls.update();
  });

  // Expose control functions globally
  useEffect(() => {
    if (typeof window !== 'undefined') {
      (window as any).enhancedCameraControls = {
        focusOnTarget,
        resetCamera,
        focusOnEarth: () => focusOnTarget(new THREE.Vector3(0, 0, 0)),
        focusOnSun: () => focusOnTarget(new THREE.Vector3(10, 0, 0)),
        getCurrentTarget: () => target.clone(),
        getCameraPosition: () => camera.position.clone()
      };
    }
  }, [target, camera.position]);

  return null;
};

export default EnhancedCameraController;
